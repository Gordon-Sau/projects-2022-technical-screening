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
        lambda s: s not in ('',' '), 
        re.split(r"(\W)", text.upper())
    ))

    # ignore stuffs before ':'
    if ':' in tokens:
        tokens = tokens[tokens.index(':') + 1 :]

    # ignore 'completion of'
    while 'COMPLETION' in tokens:
        index = tokens.index('COMPLETION')
        tokens = tokens[:index].extend(tokens[index + 2:])

    # ignore two words after units for easier parsing
    while 'UNITS' in tokens:
        index = tokens.index('UNITS')
        tokens = tokens[:index + 1].extend(tokens[index + 3:])

    # "4951" -> "COMP4951"
    if (len(tokens) == 1) and tokens[0].isdigit() and len(tokens[0]) == 4:
        tokens[0] = 'COMP' + tokens[0]

    return tokens

class CourseNode:
    def __init__(self, code) -> None:
        self.code = code

    def evaluate(self, courses_list)->bool:
        return self.code in courses_list

class AndNode:
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def evaluate(self, courses_list)->bool:
        return self.left.evaluate(courses_list) and self.right.evaluate(courses_list)

class OrNode:
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right
    
    def evaluate(self, courses_list)->bool:
        return self.left.evaluate(courses_list) or self.right.evaluate(courses_list)

class TotalUOCNode:
    def __init__(self, units) -> None:
        self.units = units
    
    def evaluate(self, courses_list)->bool:
        return len(courses_list) * UNIT >= self.units

class COMPUOCNode:
    def __init__(self, units) -> None:
        self.units = units
    
    def evaluate(self, courses_list)->bool:
        return (len(filter(lambda course: course.startswith("COMP"), courses_list))
            * UNIT) >= self.units

class LevelNode:
    def __init__(self, units, level) -> None:
        self.units = units
        self.level = level

    def evaluate(self, courses_list)->bool:
        return (len(filter(
                lambda course: course.startswith("COMP" + str(self.level)),
                courses_list))* UNIT) >= self.units

class SetNode:
    def __init__(self, units, courses_set) -> None:
        self.units = units
        self.set:set = courses_set

    def evaluate(self, courses_list)->bool:
        return ((len(course in self.units for course in courses_list) * UNIT)
            >= self.units)


def parseText(text: str):
    tokens = tokenize(text)
    index = 0
    



def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """
    
    # TODO: COMPLETE THIS FUNCTION!!!
    
    return True





    