import io
import logging
import os
from unittest.mock import patch

from orpheus.test_utils.testcase_base import TestCaseBase
from orpheus.utils.logger import ColoredLogger


class TestsColoredLogger(TestCaseBase):
    def setUp(self):
        self.test_file = "test.log"
        self.logger = ColoredLogger()

    def tearDown(self):
        del self.logger
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_Info_WhenVerbose3_PrintedSuccessfullyToConsole(self):
        """If verbose is set to 3, the logger should print to the console."""

        # Arrange
        message = "Test INFO logging"
        self.logger.set_verbose(3)

        # Act & Assert
        assert self.logger.disabled == False
        self.assertEqual(len(self.logger.handlers), 1)
        assert self.logger.get_verbose() == 3, f"expected verbose of 3, but verbose is {self.logger.get_verbose()}"
        assert self.logger.level == 20
        assert self.logger.getEffectiveLevel() == 20
        assert self.logger.isEnabledFor(20)

        with self.assertLogs(self.logger, level="INFO") as log_manager:
            self.logger.info(message)
            self.assertIn(message, log_manager.output[0])

    def test_Notice_WhenVerbose2_PrintedsuccessfullyToConsole(self):
        """If verbose is set to 2, the logger should print to the console."""

        # Arrange
        message = "Test NOTICE logging"
        self.logger.set_verbose(2)

        # Act & Assert
        assert not self.logger.disabled
        self.assertEqual(len(self.logger.handlers), 1)
        assert self.logger.get_verbose() == 2, f"expected verbose of 2, but verbose is {self.logger.get_verbose()}"
        assert self.logger.level == 25, f"expected level of 25, but level is {self.logger.level}"
        assert (
            self.logger.getEffectiveLevel() == 25
        ), f"expected level of 25, but level is {self.logger.getEffectiveLevel()}"
        assert self.logger.isEnabledFor(25), f"expected level enabled of 25, level is {self.logger.getEffectiveLevel()}"

        with self.assertLogs(self.logger, level="NOTICE") as log_manager:
            self.logger.notice(message)
            self.assertIn(message, log_manager.output[0])

    def test_Warning_WhenVerbose1_PrintedSuccesfullyToConsole(self):
        """If verbose is set to 1, the logger should print to the console."""

        # Arrange
        message = "Test WARNING logging"
        self.logger.set_verbose(1)

        # Act & Assert
        assert not self.logger.disabled
        self.assertEqual(len(self.logger.handlers), 1)
        assert self.logger.get_verbose() == 1, f"expected verbose of 1, but verbose is {self.logger.get_verbose()}"
        assert self.logger.level == 30, f"expected level of 30, but level is {self.logger.level}"
        assert (
            self.logger.getEffectiveLevel() == 30
        ), f"expected level of 30, but level is {self.logger.getEffectiveLevel()}"
        assert self.logger.isEnabledFor(
            30
        ), f"expected level enabled of 30, level is now {self.logger.getEffectiveLevel()}"

        with self.assertLogs(self.logger, level="WARNING") as log_manager:
            self.logger.warning(message)
            self.assertIn(message, log_manager.output[0])

    def test_Error_WhenVerbose0_DidNotPrintToConsole(self):
        """If verbose is set to 0, the logger should not print to the console."""
        # Arrange
        message = "Test no logging"
        self.logger.set_verbose(0)

        # Act & Assert
        assert self.logger.disabled
        assert self.logger.get_verbose() == 0
        self.assertEqual(len(self.logger.handlers), 0)
        assert self.logger.level == 0
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            try:
                self.logger.error(message)
            except Exception as e:
                self.fail(f"test_Error_WhenVerbose0_DidNotPrintToConsole failed: {str(e)}")
            assert (
                message not in fake_out.getvalue()
            ), f"Expected message not found in stdout, is now '{fake_out.getvalue()}' and not '{message}'"

    def test_SetVerbose_WhenNegative_ThrowsValueError(self):
        """If verbose is set to a negative value, a ValueError should be raised."""
        # Arrange, Act & Assert
        with self.assertRaises(ValueError):
            self.logger.set_verbose(-1)

    def test_GetVerbose_WhenCalled_ReturnsCurrentVerbose(self):
        """If verbose is set, get_verbose() should return the current verbose level."""
        # Arrange
        self.logger.set_verbose(2)

        # Act & Assert
        self.assertEqual(self.logger.get_verbose(), 2)

    def test_AddCustomLevel_WhenNewLevel_AddedSuccessfully(self):
        """If a new custom level is added, it should be added succesfully to the logger."""

        # Arrange
        self.logger.add_custom_level("CUSTOM", 50)

        # Act & Assert
        self.assertIn("CUSTOM", logging._levelToName.values())

    def test_SetLogFile_WhenCalled_SetsLogFile(self):
        """If logfile is given, the logger will set the logfile correctly."""
        # Act/Arrange
        self.logger.set_log_file(self.test_file, mode="a+")

        # Assert
        self.assertEqual(self.logger.filename, self.test_file)
        self.assertEqual(self.logger.mode, "a+")

    def test_SetLogFile_WhenCalledWithNone_ShouldNotUndertakeAction(self):
        """If logfile is None, the logger will only write to the console."""
        # Act/Arrange
        self.logger.set_log_file(None)
        self.logger.set_verbose(3)
        message = "test"

        # Assert
        with self.assertLogs(self.logger, level="INFO") as log_manager:
            self.logger.info(message)
            self.assertIn(message, log_manager.output[0])
        self.assertEqual(self.logger.filename, None)
        self.assertEqual(self.logger.mode, "a+")
