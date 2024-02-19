from re import sub
from typing import Union
from pathlib import Path
from time import sleep

from src.regex_patterns import VARIABLE_ASSIGNMENT_REGEX, VARIABLE_ASSIGNMENT_CHANGE_REGEX, GOTO_REGEX, CONDITION_REGEX, \
    CONDITION_GOTO_REGEX, CONDITION_ASSESSMENT_REGEX
from src.InstructionType import InstructionType


def sqrt(x: int) -> int:
    """only in case of need to use sqrt function in pseudo code
    It has to return an integer
    :param x: number to be squared
    :type x: int
    :return: square root of x
    :rtype: int"""
    return int(x ** 0.5)


class Interpreter:
    """Intepreter for onderCode"""

    def __init__(self, path: Union[str, Path], debug: bool = False, **kwargs):
        """initialize interpreter
        keyword arguments represent variables accesible at the beginning of the program
        :param path: path to the file with onderCode
        :type path: Union[str, Path]
        :param debug: flag to enable debug mode
        :type debug: bool
        :param kwargs: variables to be used in the program
        """
        self.variables = {}
        # NOTE!!! for array elements each element is stored as variable_name_1, variable_name_2, etc.
        # however the length of the array is stored as variable_name
        for x, y in kwargs.items():
            if type(y) is list:
                for i in range(len(y)):
                    self.variables[f"{x}_{i + 1}"] = y[i]
                self.variables[x] = len(y)
            else:
                self.variables[x] = y
        self.debug = debug
        self.steps = []
        self.lines = []
        self.path = Path(path)
        self.read_lines()
        # self.assign_variables()

    def read_lines(self) -> None:
        """read lines from the file and store them in list of lines"""
        if not self.path.exists():
            raise FileNotFoundError(f"File {self.path} not found")

        # for ind, line in enumerate(path.read_text().splitlines(), 0):
        for line in self.path.read_text().splitlines():
            line = sub(r"\s*\d+\.\s*", "", line)
            self.lines.append(line)

    # there is a possibility that this method will be removed
    def assign_variables(self) -> None:
        """assign names and values to variables"""
        filtered = [i for i in self.lines if VARIABLE_ASSIGNMENT_REGEX.match(i)]  # do poprawy
        for i in filtered:
            name, value = VARIABLE_ASSIGNMENT_REGEX.match(i).groups()
            self.variables[name] = value
        self.update_variables()

    # same as above
    def update_variables(self):
        """update values of variables(change type and so on)"""
        # step 1 check if all variables contain only values(opposed to names of other variables)
        for variable, value in self.variables.items():
            if type(value) is str and value.isidentifier():
                # substitute name of variable with value
                self.variables[variable] = self.variables[value]
            else:
                self.variables[variable] = int(value)

    def check_is_array(self, variable: str) -> bool:
        """check if variable is an array
        :param variable: variable to be checked
        :type variable: str
        :return: result of the check
        :rtype: bool
        """
        return "_" in variable and variable.split("_")[0] in self.variables.keys()

    def variable_operation(self, operation: str) -> None:
        """calculate result of variable operation
        :param operation: operation to be performed
        :type operation: str
        """
        result, val1, sign, val2 = VARIABLE_ASSIGNMENT_CHANGE_REGEX.match(operation).groups()
        if len(result.split("_")) > 1 and self.check_is_array(result):
            name, var = result.split("_")
            result = f"{name}_{self.variables[var]}" if not var.isnumeric() else f"{name}_{var}"

        if self.check_is_array(val1):
            name, var = val1.split("_")
            name = f"{name}_{self.variables[var]}" if not var.isnumeric() else f"{name}_{var}"
            val1 = self.variables[name]
        elif val1.isidentifier():
            val1 = self.variables[val1]
        else:
            val1 = int(val1)

        if self.check_is_array(val2):
            name, var = val2.split("_")
            name = f"{name}_{self.variables[var]}" if not var.isnumeric() else f"{name}_{var}"
            val2 = self.variables[name]
        elif val2.isidentifier():  # trzeba uwzglednic sytuacje dla np nazwy temp_1, czyli liczba i underscore
            val2 = self.variables[val2]
        else:
            val2 = int(val2)
        if sign == "/":
            sign = '//'
        self.variables[result] = eval(f"{val1} {sign} {val2}")

    def variable_assign(self, assignment: str) -> None:
        """assign value to variable
        :param assignment: assignment to be performed
        :type assignment: str
        """
        name, val = VARIABLE_ASSIGNMENT_REGEX.match(assignment).groups()
        # the place where the first exception will be thrown!
        if len(name.split("_")) > 1 and self.check_is_array(name):
            name, var = name.split("_")
            name = f"{name}_{self.variables[var]}" if not var.isnumeric() else f"{name}_{var}"

        if self.check_is_array(val):
            _, val_end = val.split("_")
            if not val_end.isnumeric():
                val_end = self.variables[val_end]
            self.variables[name] = self.variables[f"c_{val_end}"]
        elif val.isidentifier():
            self.variables[name] = self.variables[val]
        else:
            self.variables[name] = int(val)

    @staticmethod
    def get_goto_line(line) -> int:
        """return line specified in goto instruction
        :param line: line with goto instruction
        :type line: str
        :return: line to which the program should go
        :rtype: int
        """
        return int(GOTO_REGEX.match(line).groups(0)[0])

    def check_condition(self, condition: str) -> bool:
        """check condition in if clause
        :param condition: condition to be checked
        :type condition: str
        :return: result of the condition
        :rtype: bool
        """
        val1, sign, val2 = CONDITION_REGEX.match(condition).groups()
        if self.check_is_array(val1):
            name, var = val1.split("_")
            name = f"{name}_{self.variables[var]}" if not var.isnumeric() else f"{name}_{var}"
            val1 = self.variables[name]
        elif val1.isidentifier():
            val1 = self.variables[val1]
        else:
            val1 = int(val1)

        if self.check_is_array(val2):
            name, var = val2.split("_")
            name = f"{name}_{self.variables[var]}" if not var.isnumeric() else f"{name}_{var}"  # moze niedzialac
            val2 = self.variables[name]
        elif val2.isidentifier():
            val2 = self.variables[val2]
        else:
            val2 = int(val2)
        if sign == "=":
            sign = "=="
        return eval(f"{val1} {sign} {val2}")

    def process_condition(self, condition: str) -> str:
        """processes condition and calls its action
        :param condition: condition to be processed
        :type condition: str
        :return: action to be performed
        :rtype: str
        """
        if self.check_condition(condition):
            if CONDITION_GOTO_REGEX.match(condition):
                return f"goto {CONDITION_GOTO_REGEX.match(condition).groups()[2]}"
            else:
                _, _, res, val1, sign, val2 = CONDITION_ASSESSMENT_REGEX.match(condition).groups()
                return f"{res} <- {val1} {sign} {val2}"
        else:
            return ""  # zeby nie bylo bledu

    @staticmethod
    def determine_instruction_type(instruction: str) -> InstructionType:
        """determine type of instruction
        :param instruction: instruction to be checked
        :type instruction: str
        :return: type of instruction
        :rtype: InstructionType
        """
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

    def load_steps(self) -> None:
        """load full list of steps during execution"""
        finished = False
        start_index = 0
        while not finished:
            for line in self.lines[start_index:]:
                instruction_type = self.determine_instruction_type(line)
                if self.debug:
                    print(line, self.variables, instruction_type)
                    sleep(0.5)
                if instruction_type == InstructionType.VARIABLE_ASSIGNMENT:
                    self.steps.append(line)
                    self.variable_assign(line)
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
                    self.steps.append(line)
                else:
                    self.steps.append(line)
                    finished = True
                    break

    def __call__(self, *args, **kwargs):
        """execute the program"""
        self.load_steps()
