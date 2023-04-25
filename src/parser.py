import ply.yacc as yacc
from lexer import tokens
import sys


global xml
global tipo


def p_gedcom(p):
	"""gedcom  	: conteudo"""
	print("li um ficheiro gedcom")


def p_conteudo_list(p):
	"""conteudo		: LEVEL restPerson conteudo
					| LEVEL restPerson"""


def p_restPerson_single(p):
	"""restPerson	: singTag CONTENT"""
	p[0] = '<' + str([p[1]][0]) + '>' + p[2] + '<\\' + str([p[1]][0]) + '>'
	print(p[0])


def p_restPerson_mult(p):
	"""restPerson	: multTag"""
	p[0] = p[1]


def p_singTag_burial(p):
	""" singTag		: BURIAL"""
	p[0] = p[1]


def p_singTag_name(p):
	""" singTag		: NAME"""
	p[0] = p[1]


def p_singTag_title(p):
	""" singTag		: TITLE"""
	p[0] = p[1]


def p_singTag_sex(p):
	""" singTag		: SEX"""
	p[0] = p[1]


def p_singTag_date(p):
	""" singTag		: DATE"""
	p[0] = p[1] + "  tipo=" + tipo


def p_singTag_place(p):
	"""singTag		: PLACE"""
	p[0] = p[1] + "  tipo=" + tipo


def p_multTag_birth(p):
	"""multTag		: BIRTH"""
	p[0] = p[1]
	global tipo
	tipo = p[0]


def p_multTag_death(p):
	"""multTag		: DEATH"""
	p[0] = p[1]
	global tipo
	tipo = p[0]


def p_multTag_burial(p):
	"""multTag		: BURIAL"""
	p[0] = p[1]
	global tipo 
	tipo = p[0]


def p_error(p):
	print(p)
	p.success = False
	print("Syntax Error!", p.value)
	exit()


parser = yacc.yacc()
parser.success = True

with open("test/sintaxe.txt",encoding="utf-8") as f:
	lines = f.read()
	print(lines)
	parser.parse(lines)
	if parser.success:
		print("Yes")
	else:
		print("No")
	print("End")