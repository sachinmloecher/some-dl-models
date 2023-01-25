## Developers

- "Alejandro Armas <armas@ucdavis.edu>", 
- "Lia Hepler-Mackey <lmheplermackey@ucdavis.edu>", 
- "Sachin Loecher <smloecher@ucdavis.edu>"
- "Matthew Schulz <mkschulz@ucdavis.edu>"

## Getting Started

We are using `poetry` as our package manager solution. To get started, run `poetry shell`, to create a nested shell with a virtual environment. Verify your environment with `poetry env info`. Then, run `poetry install` to capture all the dependencies. 


To use Comet, make sure to use the environment variable found [here](https://www.comet.com/account-settings/apiKeys)
```
export COMET_API_KEY=<paste_your_key_here>
```

You should now be able to run a particular script with the following command:
```
poetry run python -m script.stage_1_script.script_mlp
```

## Testing and Static Analysis

type checking library like MyPy and use annotations to ask for hard guarantees that all of the objects processed by your code — both container and contents — implement the runtime behaviors that your code requires

To unit test your code use `poetry run python -m unittest`. If you are interested in testing a particular file use:
```
poetry run python -m unittest code.tests.test_example
```

Pylint enforces a coding standard and is also a general linter.
To use linter on a particular file:
```python
pylint code/lib/evaluate_notifier.py
```


MyPy is a static type checker for Python.

To use static type checking on a particular file, use for example:
```python
mypy code/lib/comet_listeners.py
```

## Workflow

### Before Getting Started

- Discuss what you'll be working on in team meetings / with team leads
- Make sure there is a GitHub issue in the repo that is tracking the item you're working on

### Get Started on a Work Item

- On GitHub
  - Assign yourself to the issue you'll work on (if not already)

- In your local Git repo
  - Switch to `main` branch (unless otherwise specified)
  - Sync latest changes on `main` branch (IMPORTANT!!!)
  - Create and checkout a new branch from `main`
    - Branch name may start with the issue ID followed by feature, like `10-code-review-doc`
  - Start coding

### Work on an Item

- Commit and push changes frequently
  - Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages
  - Check out the reason behind [Adopting Conventional Commits](/blog/memo-2021-07-21#adopting-conventional-commits)

- Create a pull request on GitHub as early as you make the first commit
  - Title should start with `Draft:` and followed by the feature, like `Draft: Code Review Doc`
  - Description should start with a line like `Closes #10` to let GitHub link the issue with the pull request automatically

- Write unit tests while developing new features (if applicable)

- Try to resolve merge conflicts (if any) with the target branch as you notice

### Finish up

- Clean up code
- Run and pass all related unit tests (if applicable)
- Remove `Draft:` from title of the pull request
- Request a code review
- Wait for review
- Implement feedbacks (if any) by continue adding commits and request another review
- Wait for approval and merge

