from .cleaner import Cleaner
import os
import shutil

class ChromeOSCleaner(Cleaner):
    def clean_temp_files(self):
        temp_dirs = [
            '/tmp',
            '/home/chronos/user/.config/google-chrome/Default/Cache',
            '/home/chronos/user/.cache',
            '/home/chronos/user/.config/chrome/pnacl',
        ]
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)

    def clean_cache(self):
        cache_dirs = [
            os.path.expanduser('~/.cache'),
            '/var/cache'
        ]
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir, ignore_errors=True)

    def clean_log_files(self):
        log_dirs = [
            '/var/log',
            os.path.expanduser('~/.config/google-chrome/Default/Application Cache/Cache')
        ]
        for log_dir in log_dirs:
            if os.path.exists(log_dir):
                shutil.rmtree(log_dir, ignore_errors=True)
