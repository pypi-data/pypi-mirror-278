import argparse
import platform
from .windows import WindowsCleaner
from .macos import MacOSCleaner
from .linux import LinuxCleaner
from .chromeos import ChromeOSCleaner

def get_cleaner():
    os_name = platform.system()
    if os_name == 'Windows':
        return WindowsCleaner()
    elif os_name == 'Darwin':
        return MacOSCleaner()
    elif os_name == 'Linux':
        return LinuxCleaner()
    elif os_name == 'Chrome OS':
        return ChromeOSCleaner()
    else:
        raise NotImplementedError(f"OS {os_name} is not supported")

def main():
    parser = argparse.ArgumentParser(description="DiskScan - A cross-platform disk cleaner")
    parser.add_argument('command', choices=['scan', 'fullscan', 'scango'])

    args = parser.parse_args()
    cleaner = get_cleaner()

    if args.command == 'scan':
        cleaner.clean_temp_files()
    elif args.command == 'fullscan':
        cleaner.full_clean()
    elif args.command == 'scango':
        cleaner.clean_temp_files()
        cleaner.clean_cache()
        cleaner.clean_log_files()

if __name__ == '__main__':
    main()
