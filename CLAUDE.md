# Claude Code Guidelines for openadapt-bootstrap

## Project Status & Priorities

**IMPORTANT**: Before starting work, always check the project-wide status document:
- **Location**: `/Users/abrichr/oa/src/STATUS.md`
- **Purpose**: Tracks P0 priorities, active background tasks, blockers, and strategic decisions
- **Action**: Read this file at the start of every session to understand current priorities

This ensures continuity between Claude Code sessions and context compactions.

---

## Repository Overview

OpenAdapt Bootstrap is the self-hosting infrastructure for OpenAdapt recursive development. It enables OpenAdapt to build OpenAdapt through recorded and replayed development workflows.

**Key concept**: Record development tasks once (manual), replay autonomously (via Claude Code).

## Repository Structure

```
openadapt-bootstrap/
├── workflows/              # Workflow implementations
│   ├── base.py            # Base classes (Workflow, WorkflowRecorder, WorkflowExecutor)
│   ├── screenshot_workflow.py
│   ├── demo_generation.py
│   └── __init__.py
├── playback/              # Replay automation (future)
├── recordings/            # Recorded workflows
├── examples/              # Example usage
│   └── generate_benchmark_screenshots.py
├── docs/
│   └── ARCHITECTURE.md    # Full architecture documentation
├── README.md              # User-facing documentation
└── pyproject.toml         # Package configuration
```

## Important Rules

### Git Workflow
- Safe to push directly to `main` (no branch protection yet)
- Use conventional commits: `feat:`, `fix:`, `docs:`, etc.
- Keep commits atomic and descriptive

### Development Setup
```bash
uv sync --dev
uv run pytest tests/ -v
```

### Testing
Always test workflows before committing:
```bash
# Test screenshot workflow
uv run python examples/generate_benchmark_screenshots.py \
    --html-path test.html \
    --output-dir test_screenshots/
```

## Key Classes

### WorkflowRecorder
Records development tasks with metadata. Wraps openadapt-capture.

```python
with WorkflowRecorder(
    name="my_workflow",
    description="What this workflow does"
) as recorder:
    # Perform task manually
    pass
```

### WorkflowExecutor
Replays recorded workflows with parameter substitution.

```python
executor = WorkflowExecutor(
    workflow_name="my_workflow",
    parameters={"param": "value"}
)
result = executor.execute()
```

### Workflow
Base class for all workflows. Implement `execute()` method.

```python
class MyWorkflow(Workflow):
    def execute(self) -> WorkflowResult:
        # Implementation
        pass
```

## Current State

### Implemented
- [x] Repository structure
- [x] Base classes (WorkflowRecorder, WorkflowExecutor, Workflow)
- [x] Screenshot workflow (stub + Playwright implementation)
- [x] Demo generation workflow (stub)
- [x] Proof-of-concept example script
- [x] Architecture documentation

### Not Yet Implemented
- [ ] Integration with openadapt-capture for actual recording
- [ ] Claude Code integration for autonomous decision-making
- [ ] GitHub Actions triggers
- [ ] Workflow replay from recordings
- [ ] Full test suite

## Next Steps

### Phase 1: Foundation
1. Integrate openadapt-capture for real recording
2. Implement replay from recordings
3. Add comprehensive tests

### Phase 2: Claude Code Integration
1. Implement ClaudeCodeIntegration class
2. Add prompt handling during replay
3. Add error recovery

### Phase 3: GitHub Integration
1. Create GitHub Actions workflows
2. Implement result posting to issues
3. Add artifact upload to PRs

## Related Projects

- [openadapt-capture](https://github.com/OpenAdaptAI/openadapt-capture) - Recording infrastructure
- [openadapt-evals](https://github.com/OpenAdaptAI/openadapt-evals) - Benchmark evaluation
- [openadapt-viewer](https://github.com/OpenAdaptAI/openadapt-viewer) - Visualization

## Mobile-First Development

User on mobile can trigger workflows via:
1. GitHub Issues: `/bootstrap run workflow_name`
2. GitHub Actions: Manual dispatch
3. Tailscale SSH: Direct command execution

Results posted back to GitHub for mobile review.

## Vision

**OpenAdapt building OpenAdapt** - Recursive self-improvement where the system can record and replay its own development process.

Level 1: Record development tasks
Level 2: Record workflow creation
Level 3: Record recording process
Level 4: Full bootstrap - system improves itself

See `docs/ARCHITECTURE.md` for complete vision and technical details.
