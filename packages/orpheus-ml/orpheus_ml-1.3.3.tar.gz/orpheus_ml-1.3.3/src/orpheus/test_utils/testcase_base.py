import sys
import unittest


class CustomStream:
    def __init__(self, file):
        self.file = file

    def write(self, data):
        self.file.write(data)
        self.file.flush()

    def writeln(self, data=""):
        self.write(data + "\n")

    def flush(self):
        self.file.flush()


class TestCaseBase(unittest.TestCase):
    log_file_path = None  # Default is None, which means output to console

    @classmethod
    def set_log_file(cls, path: str):
        cls.log_file_path = path

    @classmethod
    def run_tests(cls) -> unittest.TestResult:
        """run all tests in class and return the result"""
        test = unittest.defaultTestLoader.loadTestsFromTestCase(cls)

        runner = None
        if cls.log_file_path:
            with open(cls.log_file_path, "a+", encoding="utf-8") as f:  # Append to the log file
                custom_stream = CustomStream(f)
                runner = unittest.TextTestRunner(stream=custom_stream, verbosity=2)
                test_result = runner.run(test)
        else:
            runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)  # Default is console
            test_result = runner.run(test)

        return test_result

    def setUp(self):
        """Initialize objects for testing"""
        raise NotImplementedError

    def tearDown(self):
        """Clean up the objects after running the test"""
        raise NotImplementedError
