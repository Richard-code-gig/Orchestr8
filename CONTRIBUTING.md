# Contributing to Orchestr8

Thank you for your interest in contributing to Orchestr8! We welcome contributions from the community and are grateful for your support.

## How to Contribute

### Reporting Issues

If you encounter any bugs or have a feature request, please report them using the [GitHub Issues](https://github.com/richard-code-gig/Orchestr8/issues) tracker. When reporting an issue, please include:

- A clear and descriptive title
- A detailed description of the problem or suggestion
- Steps to reproduce the issue (if applicable)
- Any relevant logs, screenshots, or code snippets

### Setting Up Your Development Environment

To set up your development environment:

1. Fork the repository to your GitHub account.
2. Clone your fork to your local machine:
    ```sh
    git clone https://github.com/richard-code-gig/Orchestr8.git
    ```
3. Navigate to the project directory:
    ```sh
    cd Orchestr8
    ```
4. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
5. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On MacOS and Linux:
        ```sh
        source venv/bin/activate
        ```
6. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Making Changes

1. Create a new branch for your changes:
    ```sh
    git checkout -b your-feature-branch
    ```
2. Make your changes in the code.
3. Write or update tests to cover your changes.
4. Run tests to ensure everything works correctly:
    ```sh
    pytest
    ```
5. Commit your changes with a meaningful commit message:
    ```sh
    git commit -m "Description of your changes"
    ```
6. Push your branch to your fork:
    ```sh
    git push origin your-feature-branch
    ```

### Submitting a Pull Request

1. Go to the repository on GitHub and click the "New pull request" button.
2. Select the branch with your changes and the base branch you want to merge into.
3. Provide a clear and descriptive title for your pull request.
4. In the pull request description, include the following:
    - A brief summary of your changes
    - Any relevant issues that are addressed by your changes (e.g., Closes #123)
    - Any additional notes or context
5. Submit the pull request and wait for feedback from the maintainers.

### Code Style and Guidelines

- Follow the [PEP 8](https://pep8.org/) coding style guide.
- Write clear and concise commit messages.
- Ensure your code is well-documented with docstrings and comments where necessary.

### Running Tests

To run the tests locally, use:
```sh
cd Orchestr8 && \
export PYTHONPATH=. && \
pytest tests
```

Documentation

If your changes affect the public API or usage of Orchestr8, please update the documentation accordingly. The documentation files are located in the `docs` directory.

Code of Conduct

Please note that we have a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

Contact

If you have any questions or need further assistance, feel free to reach out to the maintainers.

Thank you for your contributions!