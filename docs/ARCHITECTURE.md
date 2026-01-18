# OpenAdapt Bootstrap Architecture

## Vision

**OpenAdapt building OpenAdapt** - A self-hosting infrastructure where development workflows are recorded as OpenAdapt demonstrations and replayed autonomously via Claude Code integration.

## Core Concept

Traditional software development requires constant human attention. OpenAdapt Bootstrap flips this model:

1. **Record** a development task once (manually demonstrate it)
2. **Replay** the task autonomously when needed (via Claude Code)
3. **Iterate** by recording improvements to the workflow

This enables:
- **Mobile-first development**: User directs from mobile, desktop executes
- **Reproducible workflows**: Exact same steps every time
- **Self-documenting**: Workflow is the documentation
- **Recursive improvement**: Can record the recording process itself

## Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   WORKFLOW LAYER                        │
│  (High-level development tasks)                         │
│                                                          │
│  - ScreenshotWorkflow                                   │
│  - DemoGenerationWorkflow                               │
│  - TestExecutionWorkflow                                │
│  - PRCreationWorkflow                                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 EXECUTION LAYER                         │
│  (Replay and orchestration)                             │
│                                                          │
│  - WorkflowExecutor (playback engine)                   │
│  - ClaudeCodeIntegration (decision-making)              │
│  - GitHubIntegration (trigger/result posting)           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 RECORDING LAYER                         │
│  (OpenAdapt capture infrastructure)                     │
│                                                          │
│  - openadapt-capture (event recording)                  │
│  - Workflow metadata (name, description, artifacts)     │
│  - Storage (SQLite + media files)                       │
└─────────────────────────────────────────────────────────┘
```

## Components

### 1. WorkflowRecorder

**Purpose**: Capture development tasks with rich metadata

**Design**:
```python
class WorkflowRecorder:
    """Records a development workflow with metadata."""

    def __init__(
        self,
        name: str,
        description: str,
        output_artifacts: list[str] | None = None,
        required_inputs: dict[str, str] | None = None,
    ):
        self.name = name
        self.description = description
        self.output_artifacts = output_artifacts or []
        self.required_inputs = required_inputs or {}

    def __enter__(self):
        # Start openadapt-capture Recorder
        # Add workflow metadata to recording
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Stop recording
        # Save workflow metadata
        # Generate workflow manifest
        pass
```

**Metadata Schema**:
```json
{
  "workflow_name": "generate_pr_screenshots",
  "description": "Generate screenshots for benchmark viewer PR",
  "version": "1.0.0",
  "recorded_at": "2026-01-18T12:00:00Z",
  "recorded_by": "abrichr",
  "input_parameters": {
    "html_path": "string (file path)",
    "output_dir": "string (directory path)",
    "viewports": "list[string] (desktop, tablet, mobile)"
  },
  "output_artifacts": [
    "screenshots/desktop_overview.png",
    "screenshots/tablet_overview.png",
    "screenshots/mobile_overview.png"
  ],
  "dependencies": [
    "openadapt-evals",
    "playwright"
  ],
  "recording_path": "recordings/demo_generation/pr_screenshots.db"
}
```

### 2. WorkflowExecutor

**Purpose**: Replay workflows with parameterization and error handling

**Design**:
```python
class WorkflowExecutor:
    """Executes a recorded workflow with parameter substitution."""

    def __init__(
        self,
        workflow_name: str,
        parameters: dict[str, Any] | None = None,
        claude_code_enabled: bool = False,
    ):
        self.workflow_name = workflow_name
        self.parameters = parameters or {}
        self.claude_code = ClaudeCodeIntegration() if claude_code_enabled else None

    def execute(self) -> WorkflowResult:
        """
        Execute the workflow:
        1. Load recording
        2. Substitute parameters
        3. Replay actions
        4. Handle prompts/decisions via Claude Code
        5. Collect output artifacts
        6. Return result
        """
        pass
```

**Execution Flow**:
```
1. Load Workflow Manifest
   ├─ Validate parameters
   ├─ Check dependencies
   └─ Load recording

2. Setup Environment
   ├─ Create output directories
   ├─ Launch required applications
   └─ Initialize Claude Code session

3. Replay Actions
   ├─ For each action in recording:
   │  ├─ Substitute parameters (e.g., file paths)
   │  ├─ Execute action (click, type, etc.)
   │  ├─ Wait for UI state
   │  └─ Handle errors via Claude Code

4. Collect Artifacts
   ├─ Screenshot files
   ├─ Generated demos
   ├─ Test results
   └─ Log files

5. Return Result
   ├─ Success/failure status
   ├─ Artifact paths
   ├─ Execution logs
   └─ Error messages (if any)
```

### 3. ClaudeCodeIntegration

**Purpose**: Enable autonomous decision-making during replay

**Design**:
```python
class ClaudeCodeIntegration:
    """Handles prompts and decisions during workflow execution."""

    def handle_prompt(
        self,
        prompt: str,
        context: dict[str, Any],
        screenshot: Image.Image | None = None,
    ) -> str:
        """
        When workflow encounters a prompt:
        1. Capture current screen state
        2. Send to Claude Code API
        3. Get decision
        4. Continue execution
        """
        pass

    def handle_error(
        self,
        error: Exception,
        context: dict[str, Any],
    ) -> Action:
        """
        When workflow encounters error:
        1. Analyze error
        2. Propose fix (retry, skip, abort)
        3. Execute fix
        4. Continue or fail gracefully
        """
        pass
```

**Example Usage**:
```python
# During replay, workflow encounters dialog box
prompt = "Save file as?"
screenshot = capture_current_screen()

# Claude Code decides what to do
response = claude_code.handle_prompt(
    prompt=prompt,
    context={
        "workflow": "generate_screenshots",
        "current_step": "saving_screenshot",
        "parameters": {"output_dir": "screenshots/"}
    },
    screenshot=screenshot
)

# Response: "Type 'desktop_overview.png' and click Save"
# Executor translates to actions: TYPE(...), CLICK(...)
```

### 4. Workflow Library

**Pre-built workflows for common development tasks**

#### ScreenshotWorkflow
```python
class ScreenshotWorkflow(Workflow):
    """Generate screenshots across multiple viewports."""

    def __init__(
        self,
        html_path: str,
        output_dir: str,
        viewports: list[str] = ["desktop", "tablet", "mobile"],
        states: list[str] = ["overview", "detail"],
    ):
        pass

    def execute(self) -> list[Path]:
        """
        1. Launch browser with html_path
        2. For each viewport:
           - Resize browser window
           - For each state:
             - Navigate to state
             - Capture screenshot
             - Save to output_dir
        3. Return screenshot paths
        """
        pass
```

#### DemoGenerationWorkflow
```python
class DemoGenerationWorkflow(Workflow):
    """Generate animated demo GIF/video."""

    def __init__(
        self,
        demo_script: str,
        output_format: str = "gif",
        duration_seconds: int = 15,
    ):
        pass

    def execute(self) -> Path:
        """
        1. Execute demo script
        2. Record screen during execution
        3. Convert to output_format
        4. Return demo path
        """
        pass
```

#### PRCreationWorkflow
```python
class PRCreationWorkflow(Workflow):
    """End-to-end PR creation with artifacts."""

    def __init__(
        self,
        branch: str,
        generate_screenshots: bool = True,
        run_tests: bool = True,
        create_demo: bool = False,
    ):
        pass

    def execute(self) -> str:
        """
        1. Create branch (if not exists)
        2. Generate screenshots (if enabled)
        3. Run tests (if enabled)
        4. Create demo (if enabled)
        5. Commit artifacts
        6. Push branch
        7. Create PR with artifacts
        8. Return PR URL
        """
        pass
```

## GitHub Integration

### Trigger Workflows from Mobile

**Option 1: GitHub Issue Comments**

User posts comment on issue:
```
/bootstrap run screenshot_workflow --html-path viewer.html --output-dir screenshots/
```

GitHub Actions workflow:
```yaml
name: Bootstrap Workflow
on:
  issue_comment:
    types: [created]

jobs:
  execute-workflow:
    if: startsWith(github.event.comment.body, '/bootstrap run')
    runs-on: self-hosted  # Runs on user's desktop via Tailscale
    steps:
      - name: Parse command
        id: parse
        run: |
          COMMAND="${{ github.event.comment.body }}"
          # Parse workflow name and parameters

      - name: Execute workflow
        run: |
          cd ~/oa/src/openadapt-bootstrap
          uv run python -m workflows.execute ${{ steps.parse.outputs.workflow }}

      - name: Post result
        run: |
          # Post result back to GitHub issue
          gh issue comment ${{ github.event.issue.number }} \
            --body "Workflow complete. See artifacts: ..."
```

**Option 2: GitHub Actions Manual Dispatch**

```yaml
name: Generate Screenshots
on:
  workflow_dispatch:
    inputs:
      html_path:
        description: 'Path to HTML file'
        required: true
      output_dir:
        description: 'Output directory'
        required: true

jobs:
  generate:
    runs-on: self-hosted
    steps:
      - name: Execute workflow
        run: |
          cd ~/oa/src/openadapt-bootstrap
          uv run python -m workflows.screenshot_workflow \
            --html-path ${{ github.event.inputs.html_path }} \
            --output-dir ${{ github.event.inputs.output_dir }}
```

**Option 3: SSH via Tailscale**

Direct command from mobile:
```bash
# User on mobile executes
ssh desktop "cd ~/oa/src/openadapt-bootstrap && \
  uv run python -m workflows.screenshot_workflow --html-path viewer.html"
```

## Proof of Concept: Screenshot Automation

### Goal
Automate the manual process of generating screenshots for the benchmark viewer PR.

### Current Manual Process
1. Open benchmark viewer HTML in browser
2. Resize to desktop viewport (1920x1080)
3. Scroll to overview section
4. Take screenshot
5. Repeat for tablet (768x1024)
6. Repeat for mobile (375x667)
7. Repeat for different states (task detail, log expanded, etc.)
8. Save all screenshots to `screenshots/` directory
9. Commit and push

**Time**: ~15-20 minutes

### Automated Process

**Record once**:
```python
from openadapt_bootstrap import WorkflowRecorder

with WorkflowRecorder(
    name="benchmark_screenshots",
    description="Generate viewer screenshots across viewports",
    output_artifacts=["screenshots/*.png"],
    required_inputs={
        "html_path": "string",
        "output_dir": "string"
    }
) as recorder:
    # Manually perform the task once
    # OpenAdapt records every action
    pass
```

**Replay forever**:
```python
from openadapt_bootstrap import WorkflowExecutor

executor = WorkflowExecutor(
    workflow_name="benchmark_screenshots",
    parameters={
        "html_path": "benchmark_results/my_eval_run/viewer.html",
        "output_dir": "screenshots/"
    },
    claude_code_enabled=True
)

result = executor.execute()
# Screenshots generated automatically!
```

**Time**: ~2-3 minutes (automated)

### Implementation

See `examples/generate_benchmark_screenshots.py`:

```python
#!/usr/bin/env python3
"""
Proof of concept: Automated screenshot generation for benchmark viewer.

This demonstrates the full bootstrap workflow:
1. Load recorded workflow
2. Substitute parameters
3. Execute via OpenAdapt playback
4. Collect artifacts
5. Commit to PR branch

Usage:
    uv run python examples/generate_benchmark_screenshots.py \
        --html-path benchmark_results/viewer.html \
        --output-dir screenshots/ \
        --commit-to-pr
"""

from openadapt_bootstrap import WorkflowExecutor
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--html-path", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--commit-to-pr", action="store_true")
    args = parser.parse_args()

    # Execute workflow
    executor = WorkflowExecutor(
        workflow_name="benchmark_screenshots",
        parameters={
            "html_path": args.html_path,
            "output_dir": args.output_dir
        },
        claude_code_enabled=True
    )

    result = executor.execute()

    if result.success:
        print(f"Generated {len(result.artifacts)} screenshots")

        if args.commit_to_pr:
            # Commit and push
            result.commit_and_push(
                branch="pr-screenshots",
                message="Add benchmark viewer screenshots"
            )
            print(f"Committed to branch: pr-screenshots")
    else:
        print(f"Failed: {result.error}")

if __name__ == "__main__":
    main()
```

## Recursive Self-Improvement

The ultimate goal: OpenAdapt can improve itself by recording its own development process.

### Level 1: Record Development Tasks
- Record "generate screenshots" workflow
- Record "run tests" workflow
- Record "create PR" workflow

### Level 2: Record Workflow Creation
- Record the process of creating a new workflow
- Replay to create new workflows autonomously

### Level 3: Record Recording
- Record the process of recording a workflow
- System can now record arbitrary tasks on command

### Level 4: Full Bootstrap
- System can improve any part of itself
- User provides high-level goal
- System records, optimizes, and executes

## Technical Challenges

### 1. Parameterization
**Challenge**: Recordings are literal (exact coordinates, file paths)
**Solution**:
- Extract parameters from actions
- Use vision models to identify UI elements
- Relative positioning instead of absolute coordinates

### 2. State Management
**Challenge**: Workflows depend on specific UI state
**Solution**:
- Record preconditions (expected state before workflow)
- Validate state before each action
- Claude Code can adapt if state differs

### 3. Error Handling
**Challenge**: Replayed workflows will encounter errors
**Solution**:
- Checkpoint system (save state periodically)
- Retry logic with backoff
- Claude Code can propose fixes
- Graceful degradation (skip non-critical steps)

### 4. Version Compatibility
**Challenge**: UI changes break recorded workflows
**Solution**:
- Version workflows with dependencies
- Record multiple paths (if/else branches)
- Regenerate workflows when UI changes significantly

## Comparison with Existing Systems

### vs. GitHub Actions
| Feature | GitHub Actions | OpenAdapt Bootstrap |
|---------|---------------|---------------------|
| **Trigger** | Git events, schedule, API | Git events + visual workflows |
| **Execution** | YAML scripts | Recorded demonstrations |
| **Flexibility** | High (code-based) | Very high (visual + code) |
| **Learning curve** | Medium (YAML + bash) | Low (just demonstrate) |
| **Desktop tasks** | Limited (headless) | Full (GUI automation) |
| **Self-documenting** | No | Yes (recording is documentation) |

### vs. Selenium/Playwright
| Feature | Selenium/Playwright | OpenAdapt Bootstrap |
|---------|---------------------|---------------------|
| **Creation** | Write code | Demonstrate once |
| **Maintenance** | Update code | Re-record |
| **Scope** | Web only | Desktop + web |
| **AI assistance** | External | Built-in (Claude Code) |
| **Replay** | Brittle (exact selectors) | Flexible (vision-based) |

### vs. RPA (Robotic Process Automation)
| Feature | Traditional RPA | OpenAdapt Bootstrap |
|---------|-----------------|---------------------|
| **Target** | Business processes | Development tasks |
| **Integration** | Proprietary | Open source |
| **Intelligence** | Limited | High (LMM-based) |
| **Version control** | External | Git-based |
| **Cost** | High (licensing) | Free |

## Next Steps

### Phase 1: Foundation (Current)
1. Create repository structure
2. Implement WorkflowRecorder (wraps openadapt-capture)
3. Implement basic WorkflowExecutor (playback without AI)
4. Build proof-of-concept screenshot workflow

### Phase 2: Claude Code Integration
1. Implement ClaudeCodeIntegration class
2. Add prompt handling during replay
3. Add error recovery
4. Test with screenshot workflow

### Phase 3: GitHub Integration
1. Create GitHub Actions workflow for triggers
2. Implement result posting to issues
3. Add artifact upload to PRs
4. Test mobile-triggered workflow

### Phase 4: Workflow Library
1. Implement ScreenshotWorkflow
2. Implement DemoGenerationWorkflow
3. Implement TestExecutionWorkflow
4. Implement PRCreationWorkflow

### Phase 5: Self-Improvement
1. Record "create workflow" workflow
2. Record "record workflow" workflow
3. Achieve full recursive bootstrap
4. Document the experience

## Success Metrics

1. **Time savings**: Reduce manual task time by 80%+
2. **Reproducibility**: 95%+ success rate on replays
3. **Adoption**: 5+ workflows in active use
4. **Self-improvement**: Successfully record workflow creation
5. **Mobile enablement**: Complete development tasks from mobile

## References

- [OpenAdapt Architecture](https://github.com/OpenAdaptAI/OpenAdapt/blob/main/docs/architecture-evolution.md)
- [Demo-Conditioned Prompting](https://github.com/OpenAdaptAI/OpenAdapt#core-approach-demo-conditioned-prompting)
- [openadapt-capture](https://github.com/OpenAdaptAI/openadapt-capture)
- [openadapt-evals](https://github.com/OpenAdaptAI/openadapt-evals)
