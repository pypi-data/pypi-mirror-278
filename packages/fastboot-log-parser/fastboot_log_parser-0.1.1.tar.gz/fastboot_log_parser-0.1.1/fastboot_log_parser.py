import io
import json
import logging
import re

class FlashLogParser:
    def __init__(self):
        self.event = {}  # The latest event status
        self.event_history = []  # Keep history

    def capture_log_content(self, logger):
        # Create a StringIO object to capture the logger's output
        log_capture_string = io.StringIO()
        # Create a stream handler that writes log output to the StringIO object
        stream_handler = logging.StreamHandler(log_capture_string)
        stream_handler.setLevel(logging.INFO)

        # Use a context manager to ensure the handler is added and removed atomically
        with self._temporary_log_handler(logger, stream_handler):
            # Get the log content from the StringIO object
            log_content = log_capture_string.getvalue()

        log_capture_string.close()
        return log_content

    from contextlib import contextmanager

    @contextmanager
    def _temporary_log_handler(self, logger, handler):
        logger.addHandler(handler)
        try:
            yield
        finally:
            logger.removeHandler(handler)

    def parse_log(self, log):
        # Check if log is a Logger object
        if isinstance(log, logging.Logger):
            # Retrieve the log content as a string
            log_content = self.capture_log_content(log)
        else:
            log_content = log
        
        lines = log_content.split('\n')
        for line in lines:
            if any(keyword in line for keyword in ['Erasing', 'Sending', 'Writing', 'Rebooting']):
                self.parse_event_line(line)
            if any(status in line for status in ['OKAY', 'FAIL']):
                self.update_last_event_status(line)
            if 'Finished' in line:
                self.update_total_duration(line)
            self.event_history.append(self.event.copy())  # Add to event history

    def calculate_progress_ratio(self, ratio_str):
        actual_progress = eval(ratio_str)
        percentage_progress = actual_progress * 100
        return f"{percentage_progress:.2f}%"

    def parse_event_line(self, line):
        self.event.clear()
        if 'Erasing' in line:
            self.event['action'] = 'erasing'
            self.event['partition'] = line.split(' ')[1].strip("'")
        elif 'Sending' in line:
            self.event['action'] = 'sending'
            parts = line.split(' ')
            if parts[1] == "sparse":
                self.event['type'] = parts[1]
                self.event['partition'] = parts[2].strip("'")
                self.event['progress'] = self.calculate_progress_ratio(parts[3])
                self.event['size'] = parts[4].strip("()")
                self.event['unit'] = parts[5].strip("()")
            else:
                self.event['partition'] = parts[1].strip("'")
                self.event['size'] = parts[2].strip("()")
                self.event['unit'] = parts[3].strip("()")
        elif 'Writing' in line:
            self.event['action'] = 'writing'
            self.event['partition'] = line.split(' ')[1].strip("'")
            self.event['status'] = line.split(' ')[2]
            self.event['duration'] = f"{line.split(' ')[3]}s"
        elif 'Rebooting' in line:
            self.event['action'] = 'rebooting'

    def update_last_event_status(self, line):
        status_match = re.search(r'([A-Z]+) \[\s*(\d+\.\d+)s\]', line)
        if status_match:
            self.event['status'] = status_match.group(1)
            self.event['duration'] = f"{float(status_match.group(2))}s"

    def update_total_duration(self, line):
        duration_match = re.search(r'Total time: \s*(\d+\.\d+)s', line)
        if duration_match:
            self.event['total_duration'] = f"{float(duration_match.group(1))}s"

    def get_event_as_json(self):
        return json.dumps(self.event, indent=4)

    def get_event_history_as_json(self):
        return json.dumps(self.event_history, indent=4)