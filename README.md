# OpenAdapt Bootstrap

**Self-hosting infrastructure for OpenAdapt recursive development**

## Concept

OpenAdapt Bootstrap enables OpenAdapt to build OpenAdapt - a recursive self-improvement system where recorded development workflows can be replayed autonomously via Claude Code integration.

This creates infrastructure for:
- Automated demo generation
- Self-documenting workflows
- Reproducible development tasks
- Mobile-first development (user directs from mobile, desktop executes autonomously)

## Architecture

```
openadapt-bootstrap/
├── recordings/           # OpenAdapt recordings of dev workflows
│   ├── demo_generation/
│   ├── screenshot_capture/
│   ├── test_execution/
│   └── pr_creation/
├── workflows/            # High-level workflow definitions
│   ├── __init__.py
│   ├── base.py          # WorkflowRecorder, WorkflowExecutor base classes
│   ├── demo_generation.py
│   ├── screenshot_workflow.py
│   └── test_workflow.py
├── playback/            # Replay automation scripts
│   ├── __init__.py
│   └── executor.py      # Claude Code integration
├── examples/            # Example workflow usage
│   └── generate_benchmark_screenshots.py
├── docs/
│   └── ARCHITECTURE.md
└── README.md
```

## Key Components

### 1. Workflow Recorder
Captures development tasks as OpenAdapt recordings:

```python
from openadapt_bootstrap import WorkflowRecorder

# Record a workflow once (manual demonstration)
with WorkflowRecorder(
    name="generate_pr_screenshots",
    description="Generate screenshots for benchmark viewer PR"
) as recorder:
    # Perform the task manually...
    # - Open browser to benchmark viewer
    # - Navigate to different states
    # - Capture screenshots
    # - Save to screenshots/ directory
    pass

print(f"Recorded workflow: {recorder.recording_path}")
```

### 2. Workflow Executor
Replays workflows autonomously via Claude Code:

```python
from openadapt_bootstrap import WorkflowExecutor

# Replay workflow without user intervention
executor = WorkflowExecutor(
    recording_path="recordings/demo_generation/pr_screenshots.db",
    claude_code_enabled=True
)

result = executor.execute()
print(f"Screenshots saved to: {result.output_dir}")
```

### 3. Claude Code Integration
Execute workflows in the background while user is on mobile:

```python
from openadapt_bootstrap import ClaudeCodeWorkflow

# Trigger from GitHub issue comment (user on mobile)
workflow = ClaudeCodeWorkflow.from_github_issue(
    repo="OpenAdaptAI/openadapt-evals",
    issue_number=42
)

# Execute autonomously
result = workflow.execute()

# Post results back to GitHub
workflow.post_result_to_issue(result)
```

## Use Cases

### 1. Auto-Generate PR Screenshots

**Problem**: Creating screenshots for PRs is manual and time-consuming

**Solution**: Record the screenshot workflow once, replay for each PR

```python
from openadapt_bootstrap.workflows import ScreenshotWorkflow

workflow = ScreenshotWorkflow(
    target_url="http://localhost:8080/viewer.html",
    viewports=["desktop", "tablet", "mobile"],
    states=["overview", "task_detail", "log_expanded"]
)

screenshots = workflow.execute()
workflow.commit_and_push(screenshots, branch="pr-screenshots")
```

### 2. Automated Demo Generation

**Problem**: Demos need to be regenerated when UI changes

**Solution**: Record demo workflow, replay on demand

```python
from openadapt_bootstrap.workflows import DemoGenerationWorkflow

workflow = DemoGenerationWorkflow(
    demo_script="scripts/notepad_demo.py",
    output_format="gif",
    duration_seconds=15
)

demo_path = workflow.execute()
```

### 3. Test Suite Execution with Visual Verification

**Problem**: Tests pass but UI might be broken

**Solution**: Record test execution with visual checkpoints

```python
from openadapt_bootstrap.workflows import TestWorkflow

workflow = TestWorkflow(
    test_command="pytest tests/",
    capture_screenshots=True,
    visual_regression_check=True
)

result = workflow.execute()
```

### 4. PR Creation with Artifacts

**Problem**: Creating PRs with screenshots/demos requires multiple manual steps

**Solution**: Single workflow from code change to PR with all artifacts

```python
from openadapt_bootstrap.workflows import PRCreationWorkflow

workflow = PRCreationWorkflow(
    branch="feature/new-viewer",
    generate_screenshots=True,
    run_tests=True,
    create_demo=True
)

pr_url = workflow.execute()
print(f"PR created: {pr_url}")
```

## Mobile-First Development

User on mobile can trigger workflows via:

1. **GitHub Issues**: Comment with workflow trigger
   ```
   /bootstrap run screenshot_workflow
   ```

2. **GitHub Actions**: Manually triggered workflows
   ```yaml
   name: Generate Screenshots
   on: workflow_dispatch
   ```

3. **Tailscale SSH**: Direct command execution
   ```bash
   ssh desktop "cd ~/oa/src/openadapt-bootstrap && python -m workflows.screenshot_workflow"
   ```

Results posted back to GitHub for mobile review.

## Integration with OpenAdapt Ecosystem

### With openadapt-capture
```python
from openadapt_capture import Recorder
from openadapt_bootstrap import WorkflowRecorder

# WorkflowRecorder wraps openadapt-capture Recorder
# with development-specific metadata and structure
```

### With openadapt-evals
```python
# Generate benchmark screenshots automatically
from openadapt_bootstrap.workflows import BenchmarkScreenshotWorkflow

workflow = BenchmarkScreenshotWorkflow(
    benchmark_dir="benchmark_results/my_eval_run",
    output_dir="screenshots/"
)
```

### With openadapt-viewer
```python
# Auto-generate viewer artifacts
from openadapt_bootstrap.workflows import ViewerWorkflow

workflow = ViewerWorkflow(
    capture_path="my_capture/",
    generate_html=True,
    generate_gif=True
)
```

## Installation

```bash
cd /Users/abrichr/oa/src/openadapt-bootstrap
uv sync
```

## Quick Start

### Record a workflow

```bash
# Start recording
uv run python -m workflows.record --name my_workflow

# Perform task manually...

# Stop recording (Ctrl+C)
```

### Replay a workflow

```bash
# Replay autonomously
uv run python -m workflows.replay --name my_workflow

# With Claude Code for decision-making
uv run python -m workflows.replay --name my_workflow --claude-code
```

### List workflows

```bash
uv run python -m workflows.list
```

## Proof of Concept: Screenshot Automation

See `examples/generate_benchmark_screenshots.py` for a working example that:

1. Launches benchmark viewer HTML
2. Uses OpenAdapt to navigate and capture screenshots
3. Saves to screenshots/ directory
4. Commits and pushes to PR branch
5. All without user intervention

```bash
uv run python examples/generate_benchmark_screenshots.py \
    --html-path benchmark_results/viewer.html \
    --output-dir screenshots/ \
    --commit-to-pr
```

## Roadmap

### Phase 1: Foundation (Current)
- [x] Repository structure
- [x] Architecture documentation
- [ ] Basic WorkflowRecorder implementation
- [ ] Basic WorkflowExecutor implementation
- [ ] Proof-of-concept screenshot workflow

### Phase 2: Claude Code Integration
- [ ] ClaudeCodeWorkflow base class
- [ ] GitHub issue trigger system
- [ ] Result posting to GitHub
- [ ] Error handling and retry logic

### Phase 3: Workflow Library
- [ ] Screenshot workflow (PR automation)
- [ ] Demo generation workflow
- [ ] Test execution workflow
- [ ] PR creation workflow
- [ ] Documentation update workflow

### Phase 4: Self-Improvement
- [ ] Record workflow for "record workflow"
- [ ] Record workflow for "execute workflow"
- [ ] Fully recursive self-improvement loop
- [ ] Workflow optimization via evaluation

## Related Projects

- [openadapt-capture](https://github.com/OpenAdaptAI/openadapt-capture) - Recording infrastructure
- [openadapt-evals](https://github.com/OpenAdaptAI/openadapt-evals) - Benchmark evaluation
- [openadapt-viewer](https://github.com/OpenAdaptAI/openadapt-viewer) - Visualization

## License

MIT

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
