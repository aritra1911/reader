from .article import Article


class ConfigParser:
    def __init__(self, file=None):
        if file is not None:
            self.parse_config(file)


    def parse_config(self, file):
        with open(file) as config_file:
            self.configs = list()

            for line in config_file.readlines():
                line = line.strip()

                if line.startswith('#') or not line:
                    # Comments begin with `#` and
                    # Ignore blank lines obviously.
                    continue

                # TODO: What happens in case of a failed parse
                #       due to a syntax error?
                cat, path, ext = line.split(':')
                self.configs.append({
                    "category": cat,
                    "path": path,
                    "extension": ext,
                })


    def get_instances(self):
        article_instances = list()

        for config in self.configs:
            article_instances.append(Article(
                category=config["category"],
                path=config["path"],
                extension=config["extension"],
            ))

        return article_instances
