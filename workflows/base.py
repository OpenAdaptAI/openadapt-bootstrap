"""Base classes for OpenAdapt Bootstrap workflows."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
import json


@dataclass
class WorkflowManifest:
    """Metadata for a recorded workflow."""

    workflow_name: str
    description: str
    version: str = "1.0.0"
    recorded_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    recorded_by: str = ""
    input_parameters: dict[str, str] = field(default_factory=dict)
    output_artifacts: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    recording_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "workflow_name": self.workflow_name,
            "description": self.description,
            "version": self.version,
            "recorded_at": self.recorded_at,
            "recorded_by": self.recorded_by,
            "input_parameters": self.input_parameters,
            "output_artifacts": self.output_artifacts,
            "dependencies": self.dependencies,
            "recording_path": self.recording_path,
        }

    def to_json(self, path: Path) -> None:
        """Save manifest to JSON file."""
        path.write_text(json.dumps(self.to_dict(), indent=2))

    @classmethod
    def from_json(cls, path: Path) -> WorkflowManifest:
        """Load manifest from JSON file."""
        data = json.loads(path.read_text())
        return cls(**data)


@dataclass
class WorkflowResult:
    """Result of workflow execution."""

    success: bool
    workflow_name: str
    artifacts: list[Path] = field(default_factory=list)
    logs: list[str] = field(default_factory=list)
    error: str | None = None
    execution_time_seconds: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "workflow_name": self.workflow_name,
            "artifacts": [str(p) for p in self.artifacts],
            "logs": self.logs,
            "error": self.error,
            "execution_time_seconds": self.execution_time_seconds,
        }


class Workflow(ABC):
    """Base class for all workflows."""

    @abstractmethod
    def execute(self) -> WorkflowResult:
        """Execute the workflow and return result."""
        pass


class WorkflowRecorder:
    """Records a development workflow with metadata.

    Usage:
        with WorkflowRecorder(
            name="my_workflow",
            description="Description of what this workflow does"
        ) as recorder:
            # Perform task manually
            # OpenAdapt records every action
            pass

        print(f"Recording saved to: {recorder.recording_path}")
    """

    def __init__(
        self,
        name: str,
        description: str,
        output_artifacts: list[str] | None = None,
        required_inputs: dict[str, str] | None = None,
        recordings_dir: Path | None = None,
    ):
        self.name = name
        self.description = description
        self.output_artifacts = output_artifacts or []
        self.required_inputs = required_inputs or {}
        self.recordings_dir = recordings_dir or Path("recordings")
        self.recording_path: Path | None = None
        self.manifest: WorkflowManifest | None = None

    def __enter__(self):
        """Start recording workflow."""
        # Create recordings directory
        workflow_dir = self.recordings_dir / self.name
        workflow_dir.mkdir(parents=True, exist_ok=True)

        # Create manifest
        self.manifest = WorkflowManifest(
            workflow_name=self.name,
            description=self.description,
            input_parameters=self.required_inputs,
            output_artifacts=self.output_artifacts,
            recording_path=str(workflow_dir / "recording.db"),
        )

        # TODO: Start openadapt-capture Recorder
        # For now, just prepare the directory
        self.recording_path = workflow_dir

        print(f"Recording workflow: {self.name}")
        print(f"Output directory: {self.recording_path}")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop recording and save manifest."""
        if self.manifest and self.recording_path:
            # Save manifest
            manifest_path = self.recording_path / "manifest.json"
            self.manifest.to_json(manifest_path)

            print(f"Workflow recorded successfully")
            print(f"Manifest: {manifest_path}")

        # TODO: Stop openadapt-capture Recorder


class WorkflowExecutor:
    """Executes a recorded workflow with parameter substitution.

    Usage:
        executor = WorkflowExecutor(
            workflow_name="my_workflow",
            parameters={"html_path": "viewer.html"},
            claude_code_enabled=True
        )

        result = executor.execute()
        print(f"Success: {result.success}")
        print(f"Artifacts: {result.artifacts}")
    """

    def __init__(
        self,
        workflow_name: str,
        parameters: dict[str, Any] | None = None,
        claude_code_enabled: bool = False,
        recordings_dir: Path | None = None,
    ):
        self.workflow_name = workflow_name
        self.parameters = parameters or {}
        self.claude_code_enabled = claude_code_enabled
        self.recordings_dir = recordings_dir or Path("recordings")

    def execute(self) -> WorkflowResult:
        """Execute the workflow.

        Steps:
        1. Load workflow manifest
        2. Validate parameters
        3. Load recording
        4. Replay actions with parameter substitution
        5. Collect output artifacts
        6. Return result
        """
        import time

        start_time = time.time()
        logs = []

        try:
            # Load manifest
            workflow_dir = self.recordings_dir / self.workflow_name
            manifest_path = workflow_dir / "manifest.json"

            if not manifest_path.exists():
                return WorkflowResult(
                    success=False,
                    workflow_name=self.workflow_name,
                    error=f"Workflow not found: {self.workflow_name}",
                )

            manifest = WorkflowManifest.from_json(manifest_path)
            logs.append(f"Loaded workflow: {manifest.workflow_name}")

            # Validate parameters
            missing = set(manifest.input_parameters.keys()) - set(self.parameters.keys())
            if missing:
                return WorkflowResult(
                    success=False,
                    workflow_name=self.workflow_name,
                    error=f"Missing required parameters: {missing}",
                )

            logs.append(f"Parameters validated: {self.parameters}")

            # TODO: Load and replay recording
            # For now, simulate execution
            logs.append("Executing workflow...")

            # Simulate some work
            time.sleep(1)

            # Collect artifacts
            artifacts = []
            for artifact_pattern in manifest.output_artifacts:
                # TODO: Actually collect artifacts from execution
                # For now, just log
                logs.append(f"Would collect artifact: {artifact_pattern}")

            execution_time = time.time() - start_time

            return WorkflowResult(
                success=True,
                workflow_name=self.workflow_name,
                artifacts=artifacts,
                logs=logs,
                execution_time_seconds=execution_time,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return WorkflowResult(
                success=False,
                workflow_name=self.workflow_name,
                logs=logs,
                error=str(e),
                execution_time_seconds=execution_time,
            )
