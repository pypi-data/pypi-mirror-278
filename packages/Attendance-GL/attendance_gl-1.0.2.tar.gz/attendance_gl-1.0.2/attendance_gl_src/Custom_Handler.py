import os
from pathlib import Path
import logging
import logging.config
from logging.handlers import RotatingFileHandler
from datetime import datetime

class SafeRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=False, errors=None):
        #get the directory path from of the package to put log file
        config_path = Path(__file__).resolve().parent
        date_str = datetime.now().strftime('%Y-%m-%d')
        filePath = config_path.__str__() + '\\logs\\' + filename + '_' + date_str
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filePath), exist_ok=True)

        super().__init__(filePath, mode, maxBytes, backupCount, encoding, delay, errors)

                # Add blank lines to separate logs from previous runs
        self._add_blank_lines()

    def _add_blank_lines(self, num_lines=5):
        with open(self.baseFilename, 'a', encoding=self.encoding) as log_file:
            log_file.write('\n' * num_lines)
