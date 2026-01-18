"""Demo generation workflow for creating animated demos."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from workflows.base import Workflow, WorkflowResult


OutputFormat = Literal["gif", "mp4", "webm"]


class DemoGenerationWorkflow(Workflow):
    """Generate animated demo from a recorded workflow or script.

    This workflow automates:
    1. Executing demo script
    2. Recording screen
    3. Converting to output format
    4. Optimizing file size

    Example:
        workflow = DemoGenerationWorkflow(
            demo_script="scripts/notepad_demo.py",
            output_format="gif",
            duration_seconds=15,
            fps=10
        )

        result = workflow.execute()
        print(f"Demo saved to: {result.artifacts[0]}")
    """

    def __init__(
        self,
        demo_script: str | Path,
        output_format: OutputFormat = "gif",
        duration_seconds: int = 15,
        fps: int = 10,
        output_path: str | Path | None = None,
    ):
        self.demo_script = Path(demo_script)
        self.output_format = output_format
        self.duration_seconds = duration_seconds
        self.fps = fps
        self.output_path = (
            Path(output_path) if output_path else Path(f"demo.{output_format}")
        )

    def execute(self) -> WorkflowResult:
        """Execute demo generation workflow.

        Stub implementation. Full implementation would:
        1. Start screen recording
        2. Execute demo script
        3. Stop recording after duration_seconds
        4. Convert to output_format
        5. Optimize (reduce file size)

        For now, just validates inputs.
        """
        logs = []

        try:
            # Validate demo script exists
            if not self.demo_script.exists():
                return WorkflowResult(
                    success=False,
                    workflow_name="demo_generation",
                    error=f"Demo script not found: {self.demo_script}",
                )

            logs.append(f"Demo script: {self.demo_script}")
            logs.append(f"Output format: {self.output_format}")
            logs.append(f"Duration: {self.duration_seconds}s @ {self.fps} fps")

            # TODO: Implement actual demo generation
            # 1. Start screen recording with openadapt-capture
            # 2. Execute demo_script
            # 3. Stop recording after duration_seconds
            # 4. Convert video to output_format
            # 5. Optimize (compress, reduce colors for GIF, etc.)

            logs.append("Demo generation not yet implemented (stub)")

            return WorkflowResult(
                success=True,
                workflow_name="demo_generation",
                artifacts=[],  # Would be [self.output_path]
                logs=logs,
            )

        except Exception as e:
            return WorkflowResult(
                success=False,
                workflow_name="demo_generation",
                logs=logs,
                error=str(e),
            )
