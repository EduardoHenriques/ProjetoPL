import sys
import ply.yacc as yacc
from lexer import tokens


def p_grammar(p):
	"""
	gedcom       : headerLevels content
	
	headerLevels : headerLevels headerCont
	             | headerCont
	             
	headerCont  : LEVEL headerAttr
	headerAttr  : DEST | CHAR | FILE | SOUR
	
	referencia  : TIPOreg '{' PAL ',' campos '}'
	campos      : campos ',' campo
	campos      : campo
	campo       : PAL SEP  TEXTO
	"""


# campos : campo outrosC  # { PAL }
# outrosC : ',' campos     # { , }
# outrosC : €              # { '}' }


def p_error(p):
	print("Syntax error in input!", p)
	parser.success = False

def p_gedcom

parser = yacc.yacc()
parser.success = True

