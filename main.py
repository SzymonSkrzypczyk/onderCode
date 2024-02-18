import re
from re import compile, sub
from typing import Union, List
from pathlib import Path

TEST_FILE_PATH = Path(__file__).parent / "test_file.oc"
VARIABLE_ASSIGNMENT_REGEX = compile(r"^(\w+)\s*<-\s*(\w+)$")  # bedzie trzeba zmienic na alpha itd
GOTO_REGEX = compile(r"^goto\s*(\d+)$")
CONDITION_GOTO_REGEX = compile(r"^if\((\w+)\s*!?[<>=]\s*(\w+)\)\s*goto\s*(\d+)$")
# bedzie trzeba podmieniac wartosci zmiennych na wartosci i potem do exec
CONDITION_ACTION_REGEX = compile(r"^if\((\w+)\s*!?[<>=]\s*(\w+)\)\s*(\w+)\s*[+*/-]\s*(\w+)$")


class Compiler:
    def __init__(self, path: Union[str, Path], **kwargs):
        # kwargs to wejscie
        # wyjscie bedize sie wybieralo ze zmiennych
        self.variables = kwargs
        print(self.variables)
        self.lines = []
        self.path = Path(path)
        self.read_lines()

    def read_lines(self):
        """read lines from the file"""
        if not self.path.exists():
            raise FileNotFoundError(f"File {self.path} not found")

        # for ind, line in enumerate(path.read_text().splitlines(), 0):
        for line in self.path.read_text().splitlines():
            line = sub(r"\s*\d+\.\s*", "", line)
            self.lines.append(line)

    def assign_variables(self):
        """assign names and values to variables"""
        filtered = [i for i in self.lines if VARIABLE_ASSIGNMENT_REGEX.match(i)]  # do poprawy
        for i in filtered:
            name, value = VARIABLE_ASSIGNMENT_REGEX.match(i).groups()
            self.variables[name] = value

    def update_variables(self):
        """update values of variables(change type and so on)"""
        ...

    def event_loop(self):
        """the very place of OnderCode execution"""
        ...


if __name__ == "__main__":
    c = Compiler(TEST_FILE_PATH, x=6, y=2)
    c.assign_variables()
    print(c.variables)
