from .cleaner import Cleaner
import os
import shutil

class WindowsCleaner(Cleaner):
    def clean_temp_files(self):
        temp_dirs = [
            os.getenv('TEMP'),
            os.getenv('TMP'),
            os.path.expanduser('~\\AppData\\Local\\Temp'),
            os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\INetCache'),
            os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\Caches'),
            os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\Explorer'),
        ]
        for temp_dir in temp_dirs:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)

    def clean_cache(self):
        cache_dirs = [
            os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache'),
            os.path.expanduser('~\\AppData\\Local\\Mozilla\\Firefox\\Profiles'),
        ]
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir, ignore_errors=True)

    def clean_log_files(self):
        log_dirs = [
            os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\Logs'),
            'C:\\Windows\\Temp',
            'C:\\Windows\\Logs'
        ]
        for log_dir in log_dirs:
            if os.path.exists(log_dir):
                shutil.rmtree(log_dir, ignore_errors=True)
