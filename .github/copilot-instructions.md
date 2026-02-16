# Copilot Instructions

This document explains how GitHub Copilot-like automated agents should interact with
the FlatDict repository.

## Project Overview

The FlatDict project is a Python library designed to help users work with nested
dictionaries by flattening and inflating them. It provides a simple and consistent
API for manipulating complex dictionary structures.

**Key Components:**
- **FlatDict Class**: The class that handles nested dictionaries only.
- **FlatterDict Class**: The class that handles both nested dictionaries and sequences.

The FlatDict distribution library (i.e. source code) maintains Python 3.6 compatibility
although development infrastructure requires Python 3.8+.

## Development Setup

### Prerequisites

- Python 3.10+
- [Optional] asdf cli version manager for managing multiple runtimes

### Development Installation

```bash
# Set up for development
bash ./scripts/dev_setup.sh
```

### Making Changes

Minimal PR checklist:

- [ ] Ensure all tests pass locally and that the local quality gate is passed.

  ```bash
  # Run Lint/Formatting checks
  ruff check --output-format=full --exit-non-zero-on-fix
  ruff format --check

  # Run type checks
  mypy .

  # Run tests with coverage and fail if coverage is below 95%
  pytest -vv --cov=cj365.flatdict --cov-context=test --cov-report=term-missing --cov-fail-under=95
  ```

- [ ] If you added dependencies: update `pyproject.toml` and mention them in the PR.
- [ ] Review the helpful tips at the bottom of this document to ensure best practices.
- [ ] Verify that commit messages follow the Commit Message Conventions section below.

## Commit Message Conventions

This project uses **Conventional Commits** specification and is versioned by
[`python-semantic-release`](https://python-semantic-release.readthedocs.io/en/stable).
Review `src/docs/source/misc/changelog.rst` for reference of how the conventional
commits and specific rules this project uses are used in practice to communicate
changes to users.

It is highly important to separate the code changes into their respective commit types
and scopes to ensure that the changelog is generated correctly and that users can
understand the changes in each release. The commit message format is strictly enforced
and should be followed for all commits.

When submitting a pull request, it is recommended to commit any end-2-end test cases
first as a `test` type commit, then the implementation changes as `feat`, `fix`, etc.
This order allows reviewers to run the test which demonstrates the failure case before
validating the implementation changes by doing a `git merge origin/<branch>` to run the
test again and see it pass. Unit test cases will need to be committed after the source
code implementation changes as they will not run without the implementation code.
Documentation changes should be committed last and the commit scope should be a short
reference to the page its modifying (e.g. `docs(github-actions): <description>` or
`docs(configuration): <description>`). Commit types should be chosen based on reference
to the default branch as opposed to its previous commits on the branch. For example, if
you are fixing a bug in a feature that was added in the same branch, the commit type
should be `refactor` instead of `fix` since the bug was introduced in the same branch
and is not present in the default branch.

### Format

```
<type>(<scope>): <summary>

<body - short code level description focusing on what and why, not how>

[optional footer(s)]
```

Scopes by the specification are optional but for this project, they are required and
only by exception can they be omitted.

Footers include:

- `BREAKING CHANGE: <description>` for breaking changes

- `NOTICE: <description>` for additional release information that should be included
  in the changelog to give users more context about the release

- `Resolves: #<issue_num>` for linking to bug fixes. Use `Implements: #<issue_num>`
   for new features.

You should not have a breaking change and a notice in the same commit. If you have a
breaking change, the breaking change description should include all relevant information
about the change and how to update.

### Types

- `feat`: New feature (minor version bump)
- `fix`: Bug fix (patch version bump)
- `perf`: Performance improvement (patch version bump)
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without feature changes or bug fixes
- `test`: Adding or updating tests
- `build`: Changes to build system or dependencies
- `ci`: Changes to CI configuration
- `chore`: Other changes that don't modify src or test files

### Breaking Changes

- Add `!` after the scope: `feat(scope)!: breaking change` and add
  `BREAKING CHANGE:` in footer with detailed description of what was changed,
  why, and how to update.

### Notices

- Add `NOTICE: <description>` in footer to include important information about the
  release that should be included in the changelog. This is for things that require
  more explanation than a simple commit message and are not breaking changes.

### Scopes

Use scopes as categories to indicate the area of change. They are most important for the
types of changes that are included in the changelog (bug fixes, features, performance
improvements, documentation, build dependencies) to tell the user what area was changed.

## Important Files

- `.github/release-templates/`: Project-specific Jinja2 templates for changelog and release notes

## Documentation

- Source in `docs/source` directory
- Uses Sphinx with Furo theme
- Build locally: `bash ./scripts/build_docs.sh`
- Hot Reload in browser (port 9000): `bash ./scripts/watch_docs.sh`

## Helpful Tips

- Never add real secrets, tokens, or credentials to source, commits, fixtures, or logs.

- All proposed changes must include tests (unit and/or e2e as appropriate) and pass the
  local quality gate before creating a PR.

- When creating a Pull Request, create a PR description that fills out the
  PR template found in `.github/PULL_REQUEST_TEMPLATE.md`. This will help
  reviewers understand the changes and the impact of the PR.

- If creating an issue, fill out one of the issue templates found in
  `.github/ISSUE_TEMPLATE/` related to the type of issue (bug, feature request, etc.).
  This will help maintainers understand the issue and its impact.

- When adding new features, consider how they will affect the changelog and
  versioning. Make as few breaking changes as possible by adding backwards compatibility
  and if you do make a breaking change, be sure to include a detailed description in the
  `BREAKING CHANGE` footer of the commit message.
