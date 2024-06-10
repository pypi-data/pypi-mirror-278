
### Commands for Using the Module

1. **Installing the module:**

    ```sh
    pip install pyoura
    ```

2. **Using the spinner in a Python script:**

    ```python
    from pyoura.spinner import Spinner

    spinner = Spinner('Loading', 'dots')  # You can replace 'dots' with other spinner types
    spinner.start()

    try:
        # Simulate a long-running process
        import time
        time.sleep(5)
    finally:
        spinner.stop()
    ```

3. **Running the spinner from the command line:**

    ```sh
    pyoura <spinner-type> <message>
    ```

    Example:

    ```sh
    pyoura dots "Loading, please wait..."
    ```

4. **Creating distribution files:**

    ```sh
    python setup.py sdist bdist_wheel
    ```

5. **Uploading to TestPyPI:**

    ```sh
    twine upload --repository testpypi dist/*
    ```

6. **Uploading to PyPI:**

    ```sh
    twine upload --repository pypi dist/*
    ```

This `README.md` should help users understand how to install, use, and contribute to the Pyoura module.
