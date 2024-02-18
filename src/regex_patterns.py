from re import compile

VARIABLE_ASSIGNMENT_REGEX = compile(r"^(\w+)\s*<-\s*(\w+)$")  # bedzie trzeba zmienic na alpha itd
VARIABLE_ASSIGNMENT_CHANGE_REGEX = compile(r"^(\w+)\s*<-\s*(\w+)\s*([-+*/])\s*(\w+)$")
GOTO_REGEX = compile(r"^goto\s*(\d+)$")
CONDITION_REGEX = compile(r"^if\((\w+)\s*(!?[<>=])\s*(\w+)\)")
CONDITION_GOTO_REGEX = compile(r"^if\((\w+)\s*!?[<>=]\s*(\w+)\)\s*goto\s*(\d+)$")
# bedzie trzeba podmieniac wartosci zmiennych na wartosci i potem do eval
# trzeba poprawic!!!
CONDITION_ASSESSMENT_REGEX = compile(r"^if\((\w+)\s*!?[<>=]\s*(\w+)\)\s*(\w+)\s*<-\s*(\w+)\s*([-+*/])\s*(\w+)$")
