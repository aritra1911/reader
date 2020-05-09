FILE_PATH = '/home/ray/codes/python/flask/reader/test_file.md'

def get_file_content():
    with open(FILE_PATH, "r") as file:
        return file.read()

if __name__ == '__main__':
    print(get_file_content())
