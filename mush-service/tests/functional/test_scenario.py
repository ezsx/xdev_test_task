import pytest
from settings import logger

# Explicit specification of test files
TEST_FILES = [
    "/opt/tests/functional/src/test_mush.py",
    "/opt/tests/functional/src/test_basket.py",
    # Add any additional files you want to run here
]


def run_tests():
    """
    Executes the test suite using pytest with specified test files and options.

    The function configures pytest arguments to stop at the first failure,
    suppress warnings, and provide verbose output.
    """
    logger.info("Starting the test run with specified test files...")

    # Pytest arguments for the test run configuration
    pytest_args = [
        "--maxfail=10",  # Stop on the first failure
        "--disable-warnings",  # Suppress warnings for cleaner output
        "-v",  # Verbose output
    ] + TEST_FILES  # Append specified test files to the argument list

    # Run pytest with the configured arguments
    result = pytest.main(pytest_args)

    # Check test result status and log accordingly
    if result == 0:
        logger.info("All tests passed successfully.")
    else:
        logger.error("Some tests failed. Check the logs for details.")
        # exit(1)


if __name__ == "__main__":
    run_tests()
