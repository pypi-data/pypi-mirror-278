import sys

class CustomWriter:
    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = self

    def write(self, text):
        if "pygame" not in text:
            self.stdout.write(text)

    def flush(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.stdout


with CustomWriter():
    print("pygame govno")
    
    print("Ahhh")