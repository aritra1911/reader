import re


class FileParsingError(Exception):
    pass


class JournalEntry:
    def __init__(self, filename=None):
        if filename is not None:
            self.set_filename(filename)
            self.read_file()
            self.parse()

    def set_filename(self, filename):
        self.filename = filename

    def get_title(self):
        return self.title

    def get_paragraphs(self):
        return self.paragraphs

    def read_file(self):
        with open(self.filename, "r") as file:
            self.file_content = file.read()

    def parse(self):
        lines = self.file_content.splitlines()
        lines.append('')  # this is for later

        if not len(lines):
            raise FileParsingError("Empty file supplied")

        title = lines.pop(0)
        # loop until a line with text is found
        # the first line is supposed to contain the title
        while len(title) == 0:
            try:
               title = lines.pop(0)
            except IndexError:
                raise FileParsingError("Empty file supplied")

        title_regex = re.compile(r'"(.*)"|# (.*)')

        if title_regex.match(title) is None:
            raise FileParsingError(
                "Titles must be put in double quotation marks or begin with " +
                "a single hash(#) character followed by a space character."
            )

        # `title_regex.findall(title)` outputs a list of tuple(s). In this case
        # we're interested in the first tuple only. This tuple is the the form:
        # `('Title', '')` for the first match according to `title_regex` and
        # `('', 'Title')` for the second match pattern according to
        # `title_regex`. `p_titles` is an abbreviation for `possible_titles`
        p_titles = title_regex.findall(title)[0]
        self.title = p_titles[0] if p_titles[0] != '' else p_titles[1]

        # `self.paragraphs` is a list of list(s) of line(s)
        # You'll notice the blank line at the end of `lines`. Encountering this
        # will cause the last accumulated paragragraph to be appended. This is
        # a supposed hack in order to save me a block of code repetition. You
        # can see this blank line as the null terminating character of a string
        # in C.
        self.paragraphs = list()
        paragraph = list()
        for line in lines:
            if not len(line):
                if len(paragraph):
                    self.paragraphs.append(paragraph)
                    paragraph = list()
            else:
                paragraph.append(line)


if __name__ == '__main__':
    entry = JournalEntry('sample.md')
    print(entry.get_title(), end='\n\n')
    print('[')
    for paragraph in entry.get_paragraphs():
        print('  [')
        for line in paragraph:
            print(f'    "{line}",')
        print('  ],')
    print(']')
