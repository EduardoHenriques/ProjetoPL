import sys
import ply.yacc as yacc
from lexer import tokens


def p_grammar(p):
	"""
	gedcom  : divList
    divList : divList div
	divList :

    div : headFamily familyLineList
    div : headPerson personLineList

    headPerson : LEVEL POINTER INDI
    personLineList : personLineList LEVEL personLine
    personLineList :

    personLine : subtypeTag
    personLine : typeTag
    personLine : POINTER pointerTag

    headFamily : LEVEL POINTER FAM
    familyLineList : familyLineList LEVEL familyLine
    familyLineList :

    familyLine : familyTag POINTER
    familyLine : typeTag
	familyLine : subtypeTag
	"""


# campos : campo outrosC  # { PAL }
# outrosC : ',' campos     # { , }
# outrosC : €              # { '}' }


def p_error(p):
	print("Syntax error in input!", p)
	parser.success = False


def p_gedcom(p):
	"""gedcom : divList"""
	print(f"parse com sucesso: {p[1]}")


def p_divList_empty(p):
	"""divList : """
	print(f"parse com sucesso: {p[1]}")


def p_divList_content(p):
	"""divList : divList div"""
	print(f"parse com sucesso: {p[1]}")


def p_div_family(p):
	"""div : headFamily familyLineList 0"""
	print(f"parse com sucesso: {p[1]}")

parser = yacc.yacc()
parser.success = True
