import re
from re import compile, sub
from typing import Union, List
from pathlib import Path

TEST_FILE_PATH = Path(__file__).parent / "test_file.oc"
VARIABLE_ASSIGNMENT_REGEX = compile(r"^(\w+)\s*<-\s*(\w+)$")  # bedzie trzeba zmienic na alpha itd
GOTO_REGEX = compile(r"^goto\s*(\d+)$")
CONDITION_GOTO_REGEX = compile(r"^if\((\w+)\s*!?[<>=]\s*(\w+)\)\s*goto\s*(\d+)$")
# bedzie trzeba podmieniac wartosci zmiennych na wartosci i potem do eval
CONDITION_ACTION_REGEX = compile(r"^if\((\w+)\s*!?[<>=]\s*(\w+)\)\s*(\w+)\s*[+*/-]\s*(\w+)$")


class Compiler:
    def __init__(self, path: Union[str, Path], **kwargs):
        # kwargs to wejscie
        # wyjscie bedize sie wybieralo ze zmiennych
        self.variables = kwargs
        self.steps = []
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
        # self.update_variables()

    def update_variables(self):
        """update values of variables(change type and so on)"""
        # step 1 check if all variables contain only values(opposed to names of other variables)
        for variable, value in self.variables.items():
            if type(value) is str and value.isalpha():
                # substitute name of variable with value
                self.variables[variable] = self.variables[value]
            else:
                self.variables[variable] = int(value)

    # these two methods can be processed as one(to do)
    def variable_operation_number(self, name, operation):
        value = self.variables[name]
        operation = operation.replace(name, str(value))
        self.variables[name] = eval(operation)

    def variable_operation_variables(self, name, operation):
        names = re.sub(r"\s*[-+*/]\s*", ",", re.sub(r"\s*<-\s*", ",", operation)).split(",")  # can be done better
        value1, value2 = self.variables[names[0]], self.variables[names[1]]
        operation_sign = re.sub(r"[^-+*/]*", "", operation)
        self.variables[name] = eval(f"{value1} {operation_sign} {value2}")

    def load_steps(self):
        ...

    def event_loop(self):
        """the very place of OnderCode execution"""
        ...


if __name__ == "__main__":
    c = Compiler(TEST_FILE_PATH, x=6, y=2)
    c.assign_variables()
    c.variable_operation_number('x', 'x + 2')
    c.variable_operation_variables('x', 'x + y')
    c.update_variables()
    print(c.variables)
