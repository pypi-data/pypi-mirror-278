python-package-boilerplate
==========================
**Current version: 0.1.1**

Boilerplate for a Python Package

## Package

Basic structure of package is

```
├── README.md
├── package
│   ├── __init__.py
│   ├── package.py
│   └── version.py
├── pytest.ini
├── requirements.txt
├── setup.py
└── tests
    ├── __init__.py
    ├── helpers
    │   ├── __init__.py
    │   └── my_helper.py
    ├── tests_helper.py
    └── unit
        ├── __init__.py
        ├── test_example.py
        └── test_version.py
```

## Requirements

Package requirements are handled using pip. To install them do

```
pip install -r requirements.txt
```

## Setup

To set up your package, ensure you have the necessary files and directories as shown in the package structure above. Specifically, you'll need:

- `README.md`: This file.
- `package/`: Directory containing your package's main code.
- `tests/`: Directory containing your tests.

### Setup Commands

1. **Install the package:**
   ```
   pip install .
   ```

2. **Install the package in editable mode (for development):**
   ```
   pip install -e .
   ```

3. **Upload to PyPI:**
   ```
   python setup.py sdist
   twine upload dist/*
   ```

## Tests

Testing is set up using [pytest](http://pytest.org) and coverage is handled with the pytest-cov plugin.

### Running Tests

Run your tests with:

```
pytest
```

in the root directory.

### Coverage

Coverage is run by default and is set in the `pytest.ini` file. To see an HTML output of coverage, open `htmlcov/index.html` after running the tests.

## Continuous Integration

### GitHub Actions (Optional)

If you prefer GitHub Actions for CI, you can set it up with a `.github/workflows/ci.yml` file. Here’s a basic example:

```yaml
name: Deploy Python Package

on:
  push:
    branches: [ "master" ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8

    - name: Install dependencies
      run: |
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        pip install bump2version twine wheel

    - name: Bump version
      id: bumpversion
      run: |
        source venv/bin/activate
        git config --global user.email "dev@runners.im"
        git config --global user.name "Runners"
        bump2version patch --allow-dirty
        git push --follow-tags

    - name: Build package
      run: |
        source venv/bin/activate
        python setup.py sdist bdist_wheel

    - name: Deploy package
      run: |
        source venv/bin/activate
        twine upload --verbose dist/*
      env:
        TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
```

This will set up CI for multiple Python versions and upload the coverage report to Codecov.

## License

Specify your package's license. For example:

```
MIT License
```

## Contribution Guidelines

If you want others to contribute to your package, add contribution guidelines. For example:

- Fork the repository.
- Create a new branch (`git checkout -b feature-foo`).
- Commit your changes (`git commit -am 'Add feature foo'`).
- Push to the branch (`git push origin feature-foo`).
- Create a new Pull Request.

Feel free to customize this boilerplate according to your specific needs.
