"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their 
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.

Your task is to complete the is_unlocked function which helps students determine 
if their course can be taken or not. 

We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the 
code by eye.

NOTE: This challenge is EXTREMELY hard and we are not expecting anyone to pass all
our tests. In fact, we are not expecting many people to even attempt this.
For complete transparency, this is worth more than the easy challenge. 
A good solution is favourable but does not guarantee a spot in Projects because
we will also consider many other criteria.
"""
import json

import re

UNIT = 6

# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()

def tokenize(text: str):
    tokens = list(filter(
        lambda s: s not in ('',' ', 'COURSES'),
        re.split(r"(\W)", text.upper())
    ))

    return clean_tokens(tokens)

def clean_tokens(tokens: list)->list:
    # ignore stuffs before ':'
    if ':' in tokens:
        tokens = tokens[tokens.index(':') + 1 :]

    # ignore 'completion of'
    while 'COMPLETION' in tokens:
        index = tokens.index('COMPLETION')
        tokens = skip(tokens, index, 2)

    # ignore two words after units for easier parsing
    while 'CREDIT' in tokens:
        index = tokens.index('CREDIT')
        tokens = skip(tokens, index - 1, 2)

    return tokens

def skip(tokens:list, start: int, n: int):
    return tokens[:start] + tokens[start + n:]


class CourseNode:
    def __init__(self, code) -> None:
        self.code = code

    def evaluate(self, courses_list)->bool:
        return self.code in courses_list

    def __str__(self) -> str:
        return f"CourseNode {{course: {self.code}}}"

class AndNode:
    def __init__(self, node_list) -> None:
        self.list = node_list

    def evaluate(self, courses_list)->bool:
        return all(node.evaluate(courses_list) for node in self.list)
    
    def __str__(self) -> str:
        return f"AndNode {{ nodes: [{','.join(str(item) for item in self.list)}]}}"

class OrNode:
    def __init__(self, node_list) -> None:
        self.list = node_list
    
    def evaluate(self, courses_list)->bool:
        return any(node.evaluate(courses_list) for node in self.list)
    
    def __str__(self) -> str:
        return f"OrNode {{nodes: [{','.join(str(item) for item in self.list)}]}}"

class TotalUOCNode:
    def __init__(self, units) -> None:
        self.units = units
    
    def evaluate(self, courses_list)->bool:
        return len(courses_list) * UNIT >= self.units
    
    def __str__(self) -> str:
        return f"TotalUOCNode {{ units: {self.units}}}"

class PrefixNode:
    def __init__(self, units, prefix) -> None:
        self.units = units
        self.prefix = prefix

    def evaluate(self, courses_list)->bool:
        return (len(
            [course for course in courses_list if course.startswith(self.prefix)]
        ) * UNIT) >= self.units
    
    def __str__(self) -> str:
        return f"PrefixNode {{units: {self.units}, prefix: {self.prefix} }}"

class SetNode:
    def __init__(self, units, courses_set) -> None:
        self.units = units
        self.set:set = courses_set

    def evaluate(self, courses_list)->bool:
        return ((len(
            [course for course in courses_list if course in self.set]
        ) * UNIT) >= self.units)

    def __str__(self) -> str:
        return f"SetNode {{units: {self.units}, set: {{ {', '.join(str(item) for item in self.set)} }} }}"

class NoneNode:
    def evaluate(self, courses_list)->bool:
        return True
    def __str__(self) -> str:
        return "NoneNode {}"

def parse_text(text: str):
    tokens = tokenize(text)
    if len(tokens) == 0:
        return NoneNode()
    return expr(tokens, 0)[0]

def expr(tokens, index):
    first_node, index = term(tokens, index)

    end = len(tokens)
    if index >= end:
        return first_node, index
    elif tokens[index] in ('AND', 'OR'):
        # create AndNode/OrNode
        node_list = [first_node]
        if tokens[index] == 'AND':
            node_list, index = create_node_list(node_list, tokens, index, 'AND')
            return AndNode(node_list), index
        else:
            node_list, index = create_node_list(node_list, tokens, index, 'OR')
            return OrNode(node_list), index
    else:
        return first_node, index

def create_node_list(node_list, tokens, index, keyword):
    while index < len(tokens) and tokens[index] == keyword:
        next_node, index = term(tokens, index + 1)
        node_list.append(next_node)
    return node_list, index

def term(tokens, index):
    if tokens[index] == '(':
        # ([expr])
        node, index = expr(tokens, index + 1)
        assert tokens[index] == ')'
        return node, index + 1
    elif is_course_code(tokens[index]):
        # [course_code]
        return CourseNode(tokens[index]), index + 1
    elif tokens[index].isdigit():
        # [digits] ...
        units = int(tokens[index])
        if (index + 1 < len(tokens)) and tokens[index + 1] == 'UNITS':
            if index + 2 < len(tokens) and tokens[index + 2] == 'IN':

                if tokens[index + 3] == 'LEVEL':
                    # [digits] units in level [digit] [course_prefix]
                    return PrefixNode(units, tokens[index + 5] + tokens[index + 4]), index + 6
                if tokens[index + 3] == '(':
                    # [digits] units in ([course_codes])
                    courses_set, index = get_courses_set(tokens, index + 4)
                    return SetNode(units, courses_set), index
                if is_course_prefix(tokens[index + 3]):
                    # [digits] units in [course_prefix]
                    return PrefixNode(units, tokens[index + 3]), index + 4
                raise Exception(f"unexpected tokens {tokens} {index}")
            else:
                # [digits] units
                return TotalUOCNode(units), index + 2
        else:
            # [four-digits]
            if len(tokens[index]) == 4:
                return CourseNode('COMP' + tokens[index]), index + 1
            raise Exception(f"unexpected tokens {tokens} {index}")

def get_courses_set(tokens, index):
    courses_set = set()
    courses_set.add(course_code(tokens[index]))

    while tokens[index + 1] != ')':
        assert tokens[index + 1] == ','
        courses_set.add(course_code(tokens[index + 2]))
        index += 2
    
    return courses_set, index + 2


def course_code(token: str) ->str:
    if (is_course_code(token)):
        return token
    if is_four_digits(token):
        return 'COMP' + token
    raise Exception("Unexpected token {token} {index}")

def is_course_code(token: str) -> bool:
    return (len(token) == 8) and token[:4].isalpha() and token[4:].isdigit()
    # return re.match(r'^[A-Z]{4}\d{4}$', token)

def is_course_prefix(token: str) -> bool:
    return (token.isalpha()) and (len(token) == 4)

def is_four_digits(token: str) -> bool:
    return (token.isdigit()) and (len(token) == 4)

def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """

    evaluator = parse_text(CONDITIONS[target_course])
    return evaluator.evaluate(set(courses_list))

# better formatting
def format(text: str) -> str:
    depth = 0
    ret: str = ""
    nextLine = False
    for c in text:
        if nextLine:
            if c == ' ':
                continue
            ret += '\n' + '\t' * depth
            nextLine = False
    
        if c in (")", "]", "}"):
            if depth > 0:
                depth -= 1
                ret += '\n' + '\t' * depth + c
        else:
            if c == ',':
                nextLine = True
            elif c in ("(", "[", "{"):
                depth += 1
                nextLine = True
            ret += c
    return ret

if __name__ == "__main__":
    for course in CONDITIONS:
        print(course + ': ' + format(str(parse_text(CONDITIONS[course]))))
