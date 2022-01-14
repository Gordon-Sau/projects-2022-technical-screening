## NOTICE
1. ignore stuff before ':' (e.g. Prequisite:)
2. if the condition is a string of only numbers, turn it into "COMP????" (e.g. "4951" -> "COMP4951")
3. case insensitive
4. need to distinguish COMP courses and other courses
5. ignore the two words after units (redundant and mispell "of" to "oc" in COMP9491)

## patterns
course code

? and ?

? or ?

x units (of credit) (can ignore "completion of")

x units (of credit) in y

y:
    COMP (courses)

    level n COMP (courses)

    (cousre code1, course code2, .....)

## structure:
course node {

    course_code: str

}

evaluate: true if the course is in the course list


and node {

    left node

    right node

}

evaluate: true if both left and right evaluate to true


or node {

    left node 

    right node

}

evaluate: true if left or right evaluate to true

total uoc node {

    units: int

}

evaluate: no. of course * 6 >= units

prefix node {

    units: int

    prefix: str

}

evaluate: (no. of course that starts with prefix) * 6 >= units


set node {

    units: int

    set of courses: set[str]

}

evaluate: no. of courses that are in both the courses list and the set of courses * 6 >= units

# grammar after tokenize
```
expr := [term]
    | [term] and [expr] 
    | [term] or [expr] 

term := ([expr])
    | [course_code]
    | [digits] units
    | [digits] units in [course_prefix]
    | [digits] units in level [digit] [course_prefix]
    | [digits] units in ([course_codes])

course_codes := [course_code], [course_codes] 
    | [course_code]

course_code := ^[A-Z]{4}\d{4}$

digits := ^\d+$

course_prefix := ^[A-Z]{4}$
```
