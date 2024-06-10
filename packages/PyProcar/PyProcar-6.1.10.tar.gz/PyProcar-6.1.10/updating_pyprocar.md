# Process to update pyprocar in pypi

1. Update version number in pyprocar/version.py
2. Update version number in setup.json
3.  Update version number in README.md

4.  Recompile docs to update version.

    Only deletes the autosummarys directories
    ```bash
    make clean-autosummary && make html

    make deploy
    ```

    deletes the autosummarys, removes build directory directories
    ```bash
    make clean-except-examples && make html

    make deploy
    ```

    Complete clean, redos all the examples, remove builddir Takes the longest
    ```bash
    make clean && make html

    make deploy
    ```