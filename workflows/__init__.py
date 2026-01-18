"""OpenAdapt Bootstrap Workflows.

High-level development workflow automation using OpenAdapt recordings.
"""

from workflows.base import (
    Workflow,
    WorkflowRecorder,
    WorkflowExecutor,
    WorkflowResult,
    WorkflowManifest,
)
from workflows.screenshot_workflow import ScreenshotWorkflow
from workflows.demo_generation import DemoGenerationWorkflow

__all__ = [
    "Workflow",
    "WorkflowRecorder",
    "WorkflowExecutor",
    "WorkflowResult",
    "WorkflowManifest",
    "ScreenshotWorkflow",
    "DemoGenerationWorkflow",
]
