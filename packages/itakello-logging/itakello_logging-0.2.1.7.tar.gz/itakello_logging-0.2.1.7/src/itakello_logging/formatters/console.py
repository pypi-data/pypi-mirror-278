import logging

INSTRUCTION_LEVEL = 24
CONFIRMATION_LEVEL = 25


class ConsoleFormatter(logging.Formatter):
    """Custom formatter to add colors to logging levels."""

    color_codes = {
        logging.DEBUG: "\033[94m",  # Blue
        CONFIRMATION_LEVEL: "\033[92m",  # Green
        INSTRUCTION_LEVEL: "\033[36m",  # Orange
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[95m",  # Magenta
    }

    def format(self, record):
        level_color = self.color_codes.get(
            record.levelno, "\033[0m"
        )  # Default to no color
        if record.levelno == INSTRUCTION_LEVEL:
            level_color += f"\n\033[1mInstructions\033[0m{level_color}:\n"
        elif record.levelno == logging.WARNING:
            level_color += f"\n\033[1mWarning\033[0m{level_color}:\n"
        message = super().format(record)
        final_message = f"{level_color}{message}\033[0m"
        return final_message
