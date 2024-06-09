import unittest

from itakello_logging import ItakelloLogging

logger = ItakelloLogging().get_logger(__name__)


class TestLogging(unittest.TestCase):
    def test_func_with_args(self) -> None:
        logger.debug("Test debug message from test.py")
        logger.info("Test info message from test.py")
        logger.confirmation("Test confirmation message from test.py")
        logger.warning("Test warning message from test.py")
        logger.error("Test error message from test.py")
        logger.critical("Test critical message from test.py")

    def test_func_with_exception(self) -> None:
        try:
            raise ValueError("This is a test error")
        except ValueError as e:
            logger.error(f"Test error message from test_func_with_exception: {str(e)}")

    def test_func_with_critical_exception(self) -> None:
        try:
            raise Exception("This is a test critical error")
        except Exception as e:
            logger.critical(
                f"Test critical message from test_func_with_critical_exception: {str(e)}"
            )


if __name__ == "__main__":
    unittest.main()
