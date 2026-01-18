"""Tests for workflow base classes."""

import pytest
from pathlib import Path
import tempfile
import shutil

from workflows.base import (
    WorkflowManifest,
    WorkflowRecorder,
    WorkflowExecutor,
    WorkflowResult,
)
from workflows.screenshot_workflow import ScreenshotWorkflow


class TestWorkflowManifest:
    """Test WorkflowManifest class."""

    def test_create_manifest(self):
        """Test creating a manifest."""
        manifest = WorkflowManifest(
            workflow_name="test_workflow",
            description="Test description",
            input_parameters={"param1": "string"},
            output_artifacts=["output.txt"],
        )

        assert manifest.workflow_name == "test_workflow"
        assert manifest.description == "Test description"
        assert manifest.input_parameters == {"param1": "string"}
        assert manifest.output_artifacts == ["output.txt"]

    def test_manifest_to_dict(self):
        """Test converting manifest to dict."""
        manifest = WorkflowManifest(
            workflow_name="test_workflow",
            description="Test description",
        )

        data = manifest.to_dict()
        assert data["workflow_name"] == "test_workflow"
        assert data["description"] == "Test description"

    def test_manifest_save_load(self, tmp_path):
        """Test saving and loading manifest."""
        manifest = WorkflowManifest(
            workflow_name="test_workflow",
            description="Test description",
        )

        # Save
        manifest_path = tmp_path / "manifest.json"
        manifest.to_json(manifest_path)
        assert manifest_path.exists()

        # Load
        loaded = WorkflowManifest.from_json(manifest_path)
        assert loaded.workflow_name == manifest.workflow_name
        assert loaded.description == manifest.description


class TestWorkflowRecorder:
    """Test WorkflowRecorder class."""

    def test_recorder_context_manager(self, tmp_path):
        """Test recorder as context manager."""
        with WorkflowRecorder(
            name="test_workflow",
            description="Test description",
            recordings_dir=tmp_path,
        ) as recorder:
            assert recorder.name == "test_workflow"
            assert recorder.recording_path is not None

        # Check manifest was created
        manifest_path = tmp_path / "test_workflow" / "manifest.json"
        assert manifest_path.exists()

        # Load and verify
        manifest = WorkflowManifest.from_json(manifest_path)
        assert manifest.workflow_name == "test_workflow"


class TestWorkflowExecutor:
    """Test WorkflowExecutor class."""

    def test_executor_missing_workflow(self, tmp_path):
        """Test executor with missing workflow."""
        executor = WorkflowExecutor(
            workflow_name="nonexistent",
            recordings_dir=tmp_path,
        )

        result = executor.execute()
        assert result.success is False
        assert "not found" in result.error.lower()

    def test_executor_missing_parameters(self, tmp_path):
        """Test executor with missing parameters."""
        # Create workflow with required parameters
        manifest = WorkflowManifest(
            workflow_name="test_workflow",
            description="Test",
            input_parameters={"param1": "string", "param2": "string"},
        )

        workflow_dir = tmp_path / "test_workflow"
        workflow_dir.mkdir()
        manifest.to_json(workflow_dir / "manifest.json")

        # Execute without required parameters
        executor = WorkflowExecutor(
            workflow_name="test_workflow",
            parameters={"param1": "value1"},  # Missing param2
            recordings_dir=tmp_path,
        )

        result = executor.execute()
        assert result.success is False
        assert "missing" in result.error.lower()

    def test_executor_with_valid_parameters(self, tmp_path):
        """Test executor with all required parameters."""
        # Create workflow
        manifest = WorkflowManifest(
            workflow_name="test_workflow",
            description="Test",
            input_parameters={"param1": "string"},
        )

        workflow_dir = tmp_path / "test_workflow"
        workflow_dir.mkdir()
        manifest.to_json(workflow_dir / "manifest.json")

        # Execute with parameters
        executor = WorkflowExecutor(
            workflow_name="test_workflow",
            parameters={"param1": "value1"},
            recordings_dir=tmp_path,
        )

        result = executor.execute()
        assert result.success is True
        assert result.workflow_name == "test_workflow"


class TestScreenshotWorkflow:
    """Test ScreenshotWorkflow class."""

    def test_workflow_missing_html(self, tmp_path):
        """Test workflow with missing HTML file."""
        workflow = ScreenshotWorkflow(
            html_path=tmp_path / "nonexistent.html",
            output_dir=tmp_path / "screenshots",
        )

        result = workflow.execute()
        assert result.success is False
        assert "not found" in result.error.lower()

    def test_workflow_creates_output_dir(self, tmp_path):
        """Test workflow creates output directory."""
        # Create dummy HTML
        html_path = tmp_path / "test.html"
        html_path.write_text("<html><body>Test</body></html>")

        output_dir = tmp_path / "screenshots"

        workflow = ScreenshotWorkflow(
            html_path=html_path,
            output_dir=output_dir,
        )

        result = workflow.execute()
        assert result.success is True
        assert output_dir.exists()
        assert output_dir.is_dir()

    def test_workflow_generates_screenshots(self, tmp_path):
        """Test workflow generates screenshot files."""
        # Create dummy HTML
        html_path = tmp_path / "test.html"
        html_path.write_text("<html><body>Test</body></html>")

        output_dir = tmp_path / "screenshots"

        workflow = ScreenshotWorkflow(
            html_path=html_path,
            output_dir=output_dir,
            viewports=["desktop", "mobile"],
            states=["overview"],
        )

        result = workflow.execute()
        assert result.success is True

        # Should generate 2 screenshots (desktop + mobile)
        assert len(result.artifacts) == 2

        # Check files were created (stub implementation just touches files)
        for artifact in result.artifacts:
            assert artifact.exists()
