#!/usr/bin/env python3
"""Proof of concept: Automated screenshot generation for benchmark viewer.

This demonstrates the full bootstrap workflow:
1. Load workflow configuration
2. Execute via screenshot workflow
3. Collect artifacts
4. Optionally commit to PR branch

Usage:
    python examples/generate_benchmark_screenshots.py \
        --html-path benchmark_results/viewer.html \
        --output-dir screenshots/

    # With git commit
    python examples/generate_benchmark_screenshots.py \
        --html-path benchmark_results/viewer.html \
        --output-dir screenshots/ \
        --commit-to-pr
"""

import argparse
import subprocess
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from workflows.screenshot_workflow import ScreenshotWorkflow, PlaywrightScreenshotWorkflow


def commit_and_push(artifacts: list[Path], branch: str = "pr-screenshots") -> None:
    """Commit artifacts and push to branch."""
    try:
        # Create branch if not exists
        subprocess.run(["git", "checkout", "-b", branch], capture_output=True)

        # Add screenshots
        for artifact in artifacts:
            subprocess.run(["git", "add", str(artifact)], check=True)

        # Commit
        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                f"Add benchmark viewer screenshots\n\nGenerated {len(artifacts)} screenshots across viewports.",
            ],
            check=True,
        )

        # Push
        subprocess.run(["git", "push", "-u", "origin", branch], check=True)

        print(f"\nCommitted and pushed to branch: {branch}")

    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate screenshots for benchmark viewer"
    )
    parser.add_argument(
        "--html-path",
        required=True,
        help="Path to benchmark viewer HTML file",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Output directory for screenshots",
    )
    parser.add_argument(
        "--viewports",
        nargs="+",
        default=["desktop", "tablet", "mobile"],
        choices=["desktop", "tablet", "mobile"],
        help="Viewports to capture",
    )
    parser.add_argument(
        "--states",
        nargs="+",
        default=["overview", "task_detail", "log_expanded", "log_collapsed"],
        choices=["overview", "task_detail", "log_expanded", "log_collapsed"],
        help="UI states to capture",
    )
    parser.add_argument(
        "--commit-to-pr",
        action="store_true",
        help="Commit screenshots and push to PR branch",
    )
    parser.add_argument(
        "--use-playwright",
        action="store_true",
        help="Use Playwright for real browser automation (requires: playwright install)",
    )

    args = parser.parse_args()

    # Choose workflow implementation
    WorkflowClass = PlaywrightScreenshotWorkflow if args.use_playwright else ScreenshotWorkflow

    # Create workflow
    workflow = WorkflowClass(
        html_path=args.html_path,
        output_dir=args.output_dir,
        viewports=args.viewports,
        states=args.states,
    )

    print("=" * 60)
    print("OpenAdapt Bootstrap: Screenshot Workflow")
    print("=" * 60)
    print(f"HTML: {args.html_path}")
    print(f"Output: {args.output_dir}")
    print(f"Viewports: {', '.join(args.viewports)}")
    print(f"States: {', '.join(args.states)}")
    print(f"Implementation: {'Playwright' if args.use_playwright else 'Stub'}")
    print()

    # Execute workflow
    print("Executing workflow...")
    result = workflow.execute()

    # Display results
    print("\nWorkflow completed!")
    print(f"Success: {result.success}")

    if result.success:
        print(f"\nGenerated {len(result.artifacts)} screenshots:")
        for artifact in result.artifacts:
            print(f"  - {artifact}")

        # Commit if requested
        if args.commit_to_pr and result.artifacts:
            print("\nCommitting to PR branch...")
            commit_and_push(result.artifacts)

    else:
        print(f"\nError: {result.error}")

    # Show logs
    if result.logs:
        print("\nExecution logs:")
        for log in result.logs:
            print(f"  {log}")

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
