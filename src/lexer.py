import ply.lex as lex
import re
import json

level = 0  # nivel
comm_level = 0  #
indi_level = 0  #

name = ""  # nome da pessoa
pointer = ""  # pointer para uma pessoa
dic = dict()  # dicionario que associa o pointer ao nome da pessoa


def t_error(t):
	t.lexer.skip(1)


states = [
	("comm", "inclusive"),
	("birth", "inclusive"),
	("death", "inclusive"),
	("burial", "inclusive"),
	("marriage", "inclusive"),
	("individual", "inclusive"),
	("family", "inclusive")
]

tokens = [
	"BARRA",

	"LEVEL",

	"HEADER",
	"SOUR",  # approved system ID
	"DEST",  #
	"FILE",
	"CHAR",

	"COMM",
	"CONT",

	"ADDRESS",
	"PHONE",

	"TITLE",
	"ID",
	"NAME",
	"ALIAS",
	"SEX",
	"DATE",
	"BIRTH",
	"DEATH",
	"MAR",  # casamento
	"PLACE",
	"BURIAL",

	"POINTER",
	"REFN",

	"FAMS",
	"FAMC",
	"CHILD",
	"HUSBAND",
	"WIFE",
	"DIV",  # divorcio(opcional, T/F)

]

# expressoes tokens

t_ignore = r"\t\s\n"

t_POINTER = r"\@\w+[^@]?\@"

t_ID = r"^\d+" + r"\s*" + t_POINTER + r"\s*(?=INDI)"

t_COMM = r"COMM"
t_CONT = r"(?<=CONT).*"

t_DATE = r"(?<=DATE).+"
t_ALIAS = r'(?<=ALIAS).+'
t_SEX = r"(?<=SEX)\s*[MF]"

t_BIRTH = "BIRT"
t_DEATH = "DEAT"
t_BURIAL = r"BURI"
t_MAR = r"MARR"
t_TITLE = r"(?<=TITL)\s*.*"
t_PLACE = r"(?<=PLAC)\s*.+"
t_FAMS = r'(?<=FAMS).*'
t_FAMC = r'(?<=FAMC).*'
t_CHILD = r'(?<=CHILD).*'
t_HUSBAND = r'(?<=HUSBAND).*'
t_WIFE = r'(?<=WIFE).*'
t_DIV = r'(?<=DIV)[T|F]'
t_HEADER = r'\sHEAD'


# o nivel é atualizado em cada linha lida
def t_LEVEL(t):
	r"""^(\d+)"""
	global level
	level = int(t.value)
	return t


# individuo é guardado num dicionario de acordo c/ o pointer correspondente
def t_individual_NAME(t):
	r"""(?<=NAME).+"""
	global name, dic
	name = t.value
	dic[pointer] = name
	return t


#									#
#		 FUNCOES PARA ESTADOS		#
#									#


# pessoa
def t_OpenIndividual(t):
	r"""\s*\@\w+[^@]?\@\s*(?=INDI)"""
	global indi_level, level, pointer
	indi_level = level
	t.lexer.push_state("individual")
	pointer = re.sub(r"\s*", "", t.value)
	print(pointer)


def t_individual_CloseIndividual(t):
	r"""^\d+"""
	global level, indi_level
	level = int(t.value)
	if indi_level >= level:
		t.lexer.pop_state()


# familia
def t_OpenFamily(t):
	r"""\s*\@\w+[^@]?\@\s*(?=FAM)"""
	global indi_level, level, pointer
	indi_level = level
	t.lexer.push_state("family")
	pointer = re.sub(r"\s*", "", t.value)
	print(pointer)


def t_family_CloseFamily(t):
	r"""^\d+"""
	global level, indi_level
	level = int(t.value)
	if indi_level >= level:
		t.lexer.pop_state()


# comentario
def t_OpenComm(t):
	r"""COMM"""
	global comm_level, level
	comm_level = level
	t.lexer.push_state("comm")


def t_comm_CloseComm(t):
	r"""^\d+"""
	global level, comm_level
	level = int(t.value)
	if comm_level >= level:
		t.lexer.pop_state()


# nascimento
def t_OpenBirth(t):
	r"""BIRT"""
	global comm_level
	comm_level = level
	t.lexer.push_state("birth")


def t_birth_CloseBirth(t):
	r"""^\d+"""
	global level, comm_level
	level = int(t.value)
	if comm_level >= level:
		t.lexer.pop_state()


# morte
def t_OpenDeath(t):
	r"""DEAT"""
	global comm_level
	comm_level = level
	t.lexer.push_state("death")


def t_death_CloseDeath(t):
	r"""^\d+"""
	global level, comm_level
	level = int(t.value)
	if comm_level >= level:
		t.lexer.pop_state()


# enterro
def t_OpenBurial(t):
	r"""BURI"""
	global comm_level
	comm_level = level
	t.lexer.push_state("burial")


def t_burial_CloseBurial(t):
	r"""^\d+"""
	global level, comm_level
	level = int(t.value)
	if comm_level >= level:
		t.lexer.pop_state()


# casamento
def t_OpenMarriage(t):
	r"""MARR"""
	global comm_level
	comm_level = level
	t.lexer.push_state("marriage")


def t_marriage_CloseMarriage(t):
	r"""^\d+"""
	global level, comm_level
	level = int(t.value)
	if comm_level >= level:
		t.lexer.pop_state()


lexer = lex.lex()

if __name__ == "__main__":

	with open("test/teste.txt", "r") as file:
		linhas = file.readlines(100)
		for line in linhas:
			lexer.input(line)
			for token in lexer:
				print(
					f"{token.type:<10} | {token.value:<50}")
# print(json.dumps(dic, indent=2))
