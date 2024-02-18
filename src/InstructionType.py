from enum import Enum


class InstructionType(Enum):
    VARIABLE_ASSIGNMENT = 1
    VARIABLE_ASSIGNMENT_CHANGE = 2
    GOTO = 3
    CONDITIONAL_GOTO = 4
    CONDITIONAL_ACTION = 5
    END = 6
