from .cleaner import Cleaner
import os
import shutil

class MacOSCleaner(Cleaner):
    def clean_temp_files(self):
        temp_dirs = [
            '/tmp',
            '/private/tmp',
            os.path.expanduser('~/Library/Caches/com.apple.Safari/WebKitCache'),
            os.path.expanduser('~/Library/Caches/com.apple.Safari/fsCachedData'),
        ]
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)

    def clean_cache(self):
        cache_dirs = [
            os.path.expanduser('~/Library/Caches'),
            os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/Application Cache'),
            '/Library/Caches'
        ]
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir, ignore_errors=True)

    def clean_log_files(self):
        log_dirs = [
            os.path.expanduser('~/Library/Logs'),
            '/Library/Logs',
            '/var/log'
        ]
        for log_dir in log_dirs:
            if os.path.exists(log_dir):
                shutil.rmtree(log_dir, ignore_errors=True)
