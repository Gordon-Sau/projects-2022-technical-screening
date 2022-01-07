## NOTICE
1. ignore stuff before ':' (e.g. Prequisite:)
2. if the condition is a string of only numbers, turn it into "COMP????" (e.g. "4951" -> "COMP4951")
3. case insensitive
4. need to distinguish COMP courses and other courses
5. if the token is "oc", turns it into "of" (mispell "of" to "oc" in COMP9491)

## patterns
course code
? and ?
? or ?
x units of credit (can ignore "completion of")
x units of credit in y
y:
    COMP courses
    level n COMP courses
    (cousre code1, course code2, .....)

## structure:
course node {
    "course"
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
    units
}
evaluate: no. of course * 6 >= units

comp uoc node {
    units
}
evaluate: no. of course that starts with "COMP" * 6 >= units

level n comp uoc node {
    units
    n 
}
evaluate: no. of course that starts with ("COMP" + str(n)) * 6 >= units


set node {
    units
    set of courses
}
evaluate: no. of courses that are in both the courses list and the set of courses * 6 >= units