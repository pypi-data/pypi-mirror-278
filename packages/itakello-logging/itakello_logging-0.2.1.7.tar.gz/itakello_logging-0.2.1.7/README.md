<h1 align="center">Itakello Logging</h1>

## 🪵 What is Itakello Logging

Itakello Logging is a custom logging library built on top of Python's standard `logging` module, designed to offer a more straightforward and flexible logging setup for your applications. It provides a convenient way to control log output and format, enhancing the debugging process and monitoring of Python applications.

## 🚀 Getting Started

### 🛠️ Installation

To install Itakello Logging, run the following command in your terminal:

```shell
pip install itakello_logging
```

### 🤔 Usage

Using Itakello Logging is simple. Here's a quick example to get you started:

```python
import logging
from itakello_logging import ItakelloLogging

# Initialize the logging system with optional filtering by filename
ItakelloLogging(debug=False, excluded_modules=["test.py", "another_module.py"])

logging.debug("This is a debug message")
logging.info("This is an info message")
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")
```

This setup initializes the logging system, and based on the `debug` parameter, it adjusts the log level. Additionally, by specifying the `excluded_modules` parameter, messages originating from the listed filenames (e.g., "test.py" and "another_module.py") will be excluded from the logs. This feature makes it easier to focus on the relevant information by filtering out noise from specific modules or scripts.