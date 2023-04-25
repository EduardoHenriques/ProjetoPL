import sys
import ply.yacc as yacc

from lexer import tokens


def p_grammar(p):
	"""
	linha	: LEVEL NAME CONTENT

	"""


def p_error(p):
	print("Syntax error in input!", p)
	parser.success = False
	exit()


parser = yacc.yacc()
parser.success = True

parser.parse("1 NAME Victoria  /Hanover/")
print(parser.success)
