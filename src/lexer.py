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


#    states = [
#    	 ("pessoa", "exclusive"),
#    	 ("familia", "exclusive")
#    ]
#
tokens = [
	"BARRA",

	"LEVEL",

	"HEADER",
	"SOUR",  # approved system ID
	"DEST",  #
	"FILE",
	"CHAR",
	"ADDR",

	"COMM",
	"CONT",

	"ADDRESS",
	"PHONE",
	"NAME",

	"TITLE",
	"ID",
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
	"CONTENT",

	"FAM",
	"INDI",
	"CHR",
	"BEGIN",
	"TRLR"
]

# expressoes tokens e estados

t_ANY_ignore = r"\t\s\n"

t_BEGIN = r"\n(?=0)"
t_TRLR = r"TRLR"

t_ANY_POINTER = r"\@\w+[^@]?\@"
t_ANY_REFN = r"REFN"

t_ANY_COMM = r"COMM"
t_ANY_HEADER = r"\sHEAD"
t_ANY_CONT = r"CONT"
t_ANY_DEST = r"DEST"
t_ANY_FILE = r"FILE"
t_ANY_CHAR = r"CHAR"
t_ANY_ADDR = r"ADDR"
t_ANY_NAME = r"NAME"
t_ANY_SOUR = r"SOUR"
t_ANY_PHONE = r"PHON"


t_ANY_DATE = r"DATE"
t_ANY_ALIAS = r'ALIAS'
t_ANY_SEX = r"SEX"
t_ANY_CHR = r"CHR"

t_ANY_BIRTH = "BIRT"
t_ANY_DEATH = "DEAT"
t_ANY_BURIAL = r"BURI"
t_ANY_MAR = r"MARR"
t_ANY_TITLE = r"TITL"
t_ANY_PLACE = r"PLAC"

t_FAM = r"FAM\b"

t_ANY_INDI = r"INDI"
t_ANY_FAMS = r'FAMS'
t_FAMC = r'FAMC'


t_CHILD = r'CHIL'
t_HUSBAND = r'HUSB'
t_WIFE = r'WIFE'
t_DIV = r'DIV'


#def t_begin_pessoa(t):
#	r"""INDI"""
#	t.lexer.begin('pessoa')


#def t_pessoa_end(t):
#	r"""FAM"""
#	t.lexer.begin('familia')


#def t_familia_end(t):
#	r"""TRLR"""
#	t.lexer.begin('INITIAL')


def t_LEVEL(t):
	r"""\d"""
	return t


def t_CONTENT(t):
	r"""(?<=NAME|TITL|SEX\ |BIRT|DATE|PLAC|DEAT|BURI|REFN|FAMS|FAMC|WIFE|HUSB|CHIL|DIV\ |MARR)[^\n]+"""
	return t


lexer = lex.lex()

if __name__ == "__main__":

	with open("test/sintaxe.txt",'r') as f:
		lines = f.readlines()
		for line in lines:
			lexer.input(line)
			for token in lexer:
				print(f"{token.type:<10} | {token.value:<50}")
