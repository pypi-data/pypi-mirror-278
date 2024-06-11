from .cleaner import Cleaner
import os
import shutil

class LinuxCleaner(Cleaner):
    def clean_temp_files(self):
        temp_dirs = [
            '/tmp',
            '/var/tmp',
            os.path.expanduser('~/.cache/thumbnails'),
        ]
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)

    def clean_cache(self):
        cache_dirs = [
            os.path.expanduser('~/.cache'),
            '/var/cache',
            os.path.expanduser('~/.mozilla/firefox/*.default-release/cache2'),
            os.path.expanduser('~/.config/google-chrome/Default/Application Cache'),
        ]
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir, ignore_errors=True)

    def clean_log_files(self):
        log_dirs = [
            '/var/log',
            os.path.expanduser('~/.cache/upstart')
        ]
        for log_dir in log_dirs:
            if os.path.exists(log_dir):
                shutil.rmtree(log_dir, ignore_errors=True)
