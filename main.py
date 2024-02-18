from time import sleep
import re
from enum import Enum
from re import compile, sub
from typing import Union, List
from pathlib import Path

TEST_FILE_PATH = Path(__file__).parent / "test_file.oc"
TEST_SIMPLE_PATH = Path(__file__).parent / "test_2.oc"
VARIABLE_ASSIGNMENT_REGEX = compile(r"^(\w+)\s*<-\s*(\w+)$")  # bedzie trzeba zmienic na alpha itd
VARIABLE_ASSIGNMENT_CHANGE_REGEX = compile(r"^(\w+)\s*<-\s*(\w+)\s*([-+*/])\s*(\w+)$")
GOTO_REGEX = compile(r"^goto\s*(\d+)$")
CONDITION_REGEX = compile(r"^if\((\w+)\s*(!?[<>=])\s*(\w+)\)")
CONDITION_GOTO_REGEX = compile(r"^if\((\w+)\s*!?[<>=]\s*(\w+)\)\s*goto\s*(\d+)$")
# bedzie trzeba podmieniac wartosci zmiennych na wartosci i potem do eval
# trzeba poprawic!!!
CONDITION_ASSESSMENT_REGEX = compile(r"^if\((\w+)\s*!?[<>=]\s*(\w+)\)\s*(\w+)\s*<-\s*(\w+)\s*([-+*/])\s*(\w+)$")


class InstructionType(Enum):
    VARIABLE_ASSIGNMENT = 1
    VARIABLE_ASSIGNMENT_CHANGE = 2
    GOTO = 3
    CONDITIONAL_GOTO = 4
    CONDITIONAL_ACTION = 5
    END = 6


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

    def variable_operation(self, operation):
        """calculate result of variable operation"""
        name, val1, sign, val2 = VARIABLE_ASSIGNMENT_CHANGE_REGEX.match(operation).groups()
        if val1.isalpha():
            val1 = self.variables[val1]
        else:
            val1 = int(val1)

        if val2.isalpha():
            val2 = self.variables[val2]
        else:
            val2 = int(val2)
        if sign == "/":
            sign = '//'
        self.variables[name] = eval(f"{val1} {sign} {val2}")

    @staticmethod
    def get_goto_line(line):
        """return line specified in goto instruction"""
        return int(GOTO_REGEX.match(line).groups(0)[0])

    def check_condition(self, condition):
        """check condition in if clause"""
        val1, sign, val2 = CONDITION_REGEX.match(condition).groups()
        if val1.isalpha():
            val1 = self.variables[val1]
        else:
            val1 = int(val1)

        if val2.isalpha():
            val2 = self.variables[val2]
        else:
            val2 = int(val2)
        if sign == "=":
            sign = "=="
        return eval(f"{val1} {sign} {val2}")

    def process_condition(self, condition):
        """processes condition and calls its action"""
        # moze trzeba zmienic nazwe na cos w stylu extract_action_condition
        # mozliwe ze bedize trzeba zmieniac co sie dzieje w ramach akcji
        if self.check_condition(condition):
            if CONDITION_GOTO_REGEX.match(condition):
                return f"goto {CONDITION_GOTO_REGEX.match(condition).groups()[2]}"
            else:
                _, _, res, val1, sign, val2 = CONDITION_ASSESSMENT_REGEX.match(condition).groups()
                return f"{res} <- {val1} {sign} {val2}"
        else:
            return "" # zeby nie bylo bledu

    @staticmethod
    def determine_instruction_type(instruction):
        """determine type of instruction"""
        if VARIABLE_ASSIGNMENT_REGEX.match(instruction):
            return InstructionType.VARIABLE_ASSIGNMENT
        elif VARIABLE_ASSIGNMENT_CHANGE_REGEX.match(instruction):
            return InstructionType.VARIABLE_ASSIGNMENT_CHANGE
        elif GOTO_REGEX.match(instruction):
            return InstructionType.GOTO
        elif CONDITION_GOTO_REGEX.match(instruction):
            return InstructionType.CONDITIONAL_GOTO
        elif CONDITION_ASSESSMENT_REGEX.match(instruction):
            return InstructionType.CONDITIONAL_ACTION
        elif instruction == "end":
            return InstructionType.END

    def load_steps(self):
        """load full list of steps during execution"""
        finished = False
        start_index = 0
        while not finished:
            for line in self.lines[start_index:]:
                instruction_type = self.determine_instruction_type(line)
                if instruction_type == InstructionType.VARIABLE_ASSIGNMENT:
                    self.steps.append(line)
                    continue
                elif instruction_type in (InstructionType.CONDITIONAL_GOTO, InstructionType.CONDITIONAL_ACTION):
                    value = self.process_condition(line)
                    self.steps.append(line)
                    if "goto" in value:
                        start_index = self.get_goto_line(value) - 1
                        break
                    elif "<-" in value:
                        self.variable_operation(value)
                elif instruction_type == InstructionType.GOTO:
                    start_index = self.get_goto_line(line) - 1
                    self.steps.append(line)
                    break
                elif instruction_type == InstructionType.VARIABLE_ASSIGNMENT_CHANGE:
                    self.variable_operation(line)
                else:
                    self.steps.append(line)
                    finished = True
                    break
                """
                if instruction_type == InstructionType.GOTO:
                    start_index = self.get_goto_line(line) - 1
                    print("Goto ", line)
                    break
                elif instruction_type == InstructionType.END:
                    print("END ", line)
                    finished = True
                    break
                else:
                    print("OTHER ", line)
                    if instruction_type in (InstructionType.CONDITIONAL_ACTION, InstructionType.CONDITIONAL_GOTO):
                        line = self.process_condition(line)
                    if GOTO_REGEX.match(line):
                        start_index = self.get_goto_line(line) - 1
                        break
                    elif instruction_type == InstructionType.VARIABLE_ASSIGNMENT_CHANGE:
                        print(line)
                        self.variable_operation(line)
                sleep(1)
                """

    def event_loop(self):
        """the very place of onderCode execution"""
        ...


if __name__ == "__main__":
    c = Compiler(TEST_SIMPLE_PATH, x=6, y=2)
    print(c.variables)
    c.assign_variables()
    c.update_variables()
    c.load_steps()
    print(c.variables)
