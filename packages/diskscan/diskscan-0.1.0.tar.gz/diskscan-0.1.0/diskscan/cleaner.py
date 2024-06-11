import os
import shutil

class Cleaner:
    def clean_temp_files(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def clean_cache(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def full_clean(self):
        self.clean_temp_files()
        self.clean_cache()
