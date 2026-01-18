# Contributing to OpenAdapt Bootstrap

Thank you for your interest in contributing to OpenAdapt Bootstrap!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/openadapt-bootstrap.git`
3. Install dependencies: `uv sync --dev`
4. Create a branch: `git checkout -b feature/your-feature-name`

## Development Workflow

### Running Tests

```bash
uv run pytest tests/ -v
```

### Code Style

We use Ruff for linting and formatting:

```bash
uv run ruff check .
uv run ruff format .
```

### Creating a New Workflow

1. Create a new file in `workflows/` (e.g., `workflows/my_workflow.py`)
2. Subclass `Workflow` from `workflows.base`
3. Implement the `execute()` method
4. Add to `workflows/__init__.py`
5. Add example usage to `examples/`
6. Add tests to `tests/`

Example:

```python
from workflows.base import Workflow, WorkflowResult

class MyWorkflow(Workflow):
    def __init__(self, param1: str):
        self.param1 = param1

    def execute(self) -> WorkflowResult:
        # Implementation here
        return WorkflowResult(
            success=True,
            workflow_name="my_workflow",
            artifacts=[],
            logs=["Executed successfully"]
        )
```

## Commit Messages

Follow conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks

Example: `feat: add demo generation workflow`

## Pull Requests

1. Ensure tests pass: `uv run pytest`
2. Format code: `uv run ruff format .`
3. Update documentation if needed
4. Create PR with descriptive title and description
5. Link related issues

## Code of Conduct

Be respectful, collaborative, and constructive.

## Questions?

Join us on [Discord](https://discord.gg/yF527cQbDG) or open an issue.
