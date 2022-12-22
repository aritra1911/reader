from .article import Article
from typing import List, Optional
from os import walk
from os.path import expanduser
import fnmatch

class ConfigParser:
    def __init__(self, file: Optional[str]=None):
        if file is not None:
            self.parse_config(file)

    def parse_config(self, file: str):
        with open(file) as config_file:
            self.config = dict()

            for line in config_file.readlines():
                line = line.strip()

                if line.startswith('#') or not line:
                    # Comments begin with `#` and
                    # Ignore blank lines obviously.
                    continue

                # TODO: What happens in case of a failed parse
                #       due to a syntax error?
                cat, path, pats = line.split(':')
                cat = cat.strip()
                path = path.strip()
                if path.startswith('~'): path = expanduser(path)
                patterns = list(map(str.strip, pats.split(',')))
                self.config[cat] = {
                    "path": path,
                    "patterns": patterns,
                }

    def get_categories(self) -> List[str]:
        return list(self.config.keys())

    def get_path(self, cat: str) -> str:
        return self.config[cat]['path']

    def get_patterns(self, cat: str) -> str:
        return self.config[cat]['patterns']

    def get_files(self, cat: str) -> List[str]:
        files = list()

        try:
            files = next(walk(self.config[cat]['path']))[2]
        except StopIteration:
            return []

        return list(filter(lambda file: any([
            fnmatch.fnmatchcase(file, pattern)
            for pattern in self.config[cat]['patterns']
        ]), files))

    def get_category_from_filename(self, filename: str) -> Optional[str]:
        for cat in self.config.keys():
            if any([ fnmatch.fnmatchcase(filename, pattern)
                     for pattern in self.config[cat]['patterns'] ]):
                return cat
        return None
