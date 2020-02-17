

class Reader:
    def __init__(self, file):
        self.lines = open(file).readlines()

    def __enter__(self):
        print("enter")
        return self

    def __iter__(self):
        for i in self.lines:
            yield i

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit")

if __name__ == "__main__":

    with Reader("file.txt") as reader:
        for i in reader:
            print(i)


