# Fastboot Log Parser

Fastboot Log Parser is a Python module designed to parse logs from stdout during Fastboot flash image process. It converts the status into events and outputs the current status in JSON format.

## Usage

To use the Fastboot Log Parser module in your Python project, follow these steps:

1. Install the module using pip:
   ```bash
   $ pip install fastboot-log-parser

2. Import the parser module and initialize in your Python code:
   ```python
   from fastboot_log_parser import FlashLogParser

   # Initialize the parser
   parser = FlashLogParser

3. Parse the log and get result as json
   # Parse log
   parser.parse_log(self.logger)

   # Output the parsed log as json event
   print(self.parser.get_event_as_json())

   # Output the parsed history as json list
   print(self.parser.get_event_history_as_json())

   