import unittest
from diskscan.windows import WindowsCleaner
from diskscan.macos import MacOSCleaner
from diskscan.linux import LinuxCleaner
from diskscan.chromeos import ChromeOSCleaner

class TestDiskScan(unittest.TestCase):
    def test_windows_cleaner(self):
        cleaner = WindowsCleaner()
        cleaner.clean_temp_files()
        cleaner.clean_cache()
        cleaner.clean_log_files()

    def test_macos_cleaner(self):
        cleaner = MacOSCleaner()
        cleaner.clean_temp_files()
        cleaner.clean_cache()
        cleaner.clean_log_files()

    def test_linux_cleaner(self):
        cleaner = LinuxCleaner()
        cleaner.clean_temp_files()
        cleaner.clean_cache()
        cleaner.clean_log_files()

    def test_chromeos_cleaner(self):
        cleaner = ChromeOSCleaner()
        cleaner.clean_temp_files()
        cleaner.clean_cache()
        cleaner.clean_log_files()

if __name__ == '__main__':
    unittest.main()
