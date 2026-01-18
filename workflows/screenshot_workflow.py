"""Screenshot workflow for generating viewer screenshots across viewports."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal
import time

from workflows.base import Workflow, WorkflowResult


ViewportType = Literal["desktop", "tablet", "mobile"]
StateType = Literal["overview", "task_detail", "log_expanded", "log_collapsed"]


@dataclass
class ViewportConfig:
    """Viewport configuration."""

    name: ViewportType
    width: int
    height: int


VIEWPORTS: dict[ViewportType, ViewportConfig] = {
    "desktop": ViewportConfig("desktop", 1920, 1080),
    "tablet": ViewportConfig("tablet", 768, 1024),
    "mobile": ViewportConfig("mobile", 375, 667),
}


class ScreenshotWorkflow(Workflow):
    """Generate screenshots of HTML page across multiple viewports and states.

    This workflow automates the process of:
    1. Opening HTML file in browser
    2. Resizing to each viewport
    3. Navigating to each state
    4. Capturing screenshot
    5. Saving to output directory

    Example:
        workflow = ScreenshotWorkflow(
            html_path="benchmark_results/viewer.html",
            output_dir="screenshots/",
            viewports=["desktop", "tablet", "mobile"],
            states=["overview", "task_detail"]
        )

        result = workflow.execute()
        print(f"Generated {len(result.artifacts)} screenshots")
    """

    def __init__(
        self,
        html_path: str | Path,
        output_dir: str | Path,
        viewports: list[ViewportType] | None = None,
        states: list[StateType] | None = None,
        browser: str = "chromium",
    ):
        self.html_path = Path(html_path)
        self.output_dir = Path(output_dir)
        self.viewports = viewports or ["desktop", "tablet", "mobile"]
        self.states = states or ["overview", "task_detail"]
        self.browser = browser

    def execute(self) -> WorkflowResult:
        """Execute screenshot workflow.

        This is a stub implementation that demonstrates the workflow structure.
        In the full implementation, this would:
        1. Use Playwright or Selenium to control browser
        2. Load the HTML file
        3. For each viewport:
           - Resize browser window
           - For each state:
             - Navigate to state (click elements, scroll, etc.)
             - Wait for rendering
             - Capture screenshot
             - Save to output directory with naming: {viewport}_{state}.png

        For now, this just simulates the workflow.
        """
        logs = []
        artifacts = []

        try:
            # Validate inputs
            if not self.html_path.exists():
                return WorkflowResult(
                    success=False,
                    workflow_name="screenshot_workflow",
                    error=f"HTML file not found: {self.html_path}",
                )

            # Create output directory
            self.output_dir.mkdir(parents=True, exist_ok=True)
            logs.append(f"Created output directory: {self.output_dir}")

            # Simulate screenshot generation
            for viewport_name in self.viewports:
                viewport = VIEWPORTS[viewport_name]
                logs.append(f"Setting viewport: {viewport.name} ({viewport.width}x{viewport.height})")

                for state in self.states:
                    screenshot_name = f"{viewport_name}_{state}.png"
                    screenshot_path = self.output_dir / screenshot_name

                    # TODO: Actually generate screenshot
                    # For now, just simulate
                    logs.append(f"Capturing: {screenshot_name}")
                    time.sleep(0.1)  # Simulate work

                    # Create dummy file to demonstrate
                    screenshot_path.touch()
                    artifacts.append(screenshot_path)

            return WorkflowResult(
                success=True,
                workflow_name="screenshot_workflow",
                artifacts=artifacts,
                logs=logs,
            )

        except Exception as e:
            return WorkflowResult(
                success=False,
                workflow_name="screenshot_workflow",
                logs=logs,
                error=str(e),
            )


class PlaywrightScreenshotWorkflow(ScreenshotWorkflow):
    """Screenshot workflow using Playwright for real browser automation.

    This is the full implementation that actually generates screenshots.
    Requires: pip install playwright && playwright install chromium

    Example:
        workflow = PlaywrightScreenshotWorkflow(
            html_path="viewer.html",
            output_dir="screenshots/",
            viewports=["desktop", "tablet", "mobile"],
            states=["overview", "task_detail"]
        )

        result = workflow.execute()
    """

    def execute(self) -> WorkflowResult:
        """Execute using Playwright."""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            return WorkflowResult(
                success=False,
                workflow_name="playwright_screenshot_workflow",
                error="Playwright not installed. Run: pip install playwright && playwright install",
            )

        logs = []
        artifacts = []

        try:
            # Validate HTML exists
            if not self.html_path.exists():
                return WorkflowResult(
                    success=False,
                    workflow_name="playwright_screenshot_workflow",
                    error=f"HTML file not found: {self.html_path}",
                )

            # Create output directory
            self.output_dir.mkdir(parents=True, exist_ok=True)
            logs.append(f"Created output directory: {self.output_dir}")

            # Launch Playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                logs.append("Launched browser")

                # Convert to file:// URL
                html_url = f"file://{self.html_path.absolute()}"

                for viewport_name in self.viewports:
                    viewport = VIEWPORTS[viewport_name]
                    logs.append(
                        f"Setting viewport: {viewport.name} ({viewport.width}x{viewport.height})"
                    )

                    # Create page with viewport
                    page = browser.new_page(
                        viewport={"width": viewport.width, "height": viewport.height}
                    )

                    # Navigate to HTML
                    page.goto(html_url)
                    page.wait_for_load_state("networkidle")
                    logs.append(f"Loaded page: {html_url}")

                    for state in self.states:
                        # Navigate to state
                        # This is simplified - in reality you'd click elements, scroll, etc.
                        if state == "task_detail":
                            # Example: Click first task
                            try:
                                page.click(".task-item:first-child")
                                page.wait_for_timeout(500)
                            except:
                                logs.append(f"Could not navigate to state: {state}")

                        elif state == "log_expanded":
                            try:
                                page.click("#log-toggle")
                                page.wait_for_timeout(500)
                            except:
                                logs.append(f"Could not navigate to state: {state}")

                        # Capture screenshot
                        screenshot_name = f"{viewport_name}_{state}.png"
                        screenshot_path = self.output_dir / screenshot_name

                        page.screenshot(path=str(screenshot_path), full_page=False)
                        logs.append(f"Captured: {screenshot_name}")
                        artifacts.append(screenshot_path)

                    page.close()

                browser.close()
                logs.append("Browser closed")

            return WorkflowResult(
                success=True,
                workflow_name="playwright_screenshot_workflow",
                artifacts=artifacts,
                logs=logs,
            )

        except Exception as e:
            return WorkflowResult(
                success=False,
                workflow_name="playwright_screenshot_workflow",
                logs=logs,
                error=str(e),
            )
