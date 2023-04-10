import ply.lex as lex
import re

level = 0
comm_level = 0
indi_level = 0
birth_level = 0
death_level = 0
burial_level = 0
marriage_level = 0


def t_error(t):
	t.lexer.skip(1)


def lexer_gen():
	states = [
		("comm", "inclusive"),
		("birth", "inclusive"),
		("death", "inclusive"),
		("burial", "inclusive"),
		("marriage", "inclusive"),
		("individual", "inclusive"),
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

	t_NAME = r"(?<=NAME).+"

	t_COMM = r"COMM"
	t_CONT = r"CONT"

	t_DATE = r"(?<=DATE).+"

	t_SEX = r"(?<=SEX)[MF]"

	t_BIRTH = "BIRT"
	t_DEATH = "DEAT"
	t_BURIAL = r"BURI"
	t_MAR = r"MARR"

	t_PLACE = r"(?<=PLAC).+"

	# FUNCOES PARA ESTADOS

	def t_LEVEL(t):
		r"""^(\d+)"""
		global level
		level = int(t.value)
		return t

	# individuo
	def t_OpenIndividual(t):
		r"""\s*\@\w+[^@]?\@\s*(?=INDI)"""
		global indi_level, level
		indi_level = level
		t.lexer.push_state("individual")

	def t_individual_CloseIndividual(t):
		r"""^\d+"""
		global level, indi_level
		level = int(t.value)
		if indi_level >= level:
			t.lexer.pop_state()
			print("---")

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

	# birth
	def t_OpenBirth(t):
		r"""BIRT"""
		global birth_level
		birth_level = level
		t.lexer.push_state("birth")

	def t_birth_CloseBirth(t):
		r"""^\d+"""
		global level, birth_level
		level = int(t.value)
		if birth_level >= level:
			t.lexer.pop_state()

	# death
	def t_OpenDeath(t):
		r"""DEAT"""
		global death_level
		death_level = level
		t.lexer.push_state("death")

	def t_death_CloseDeath(t):
		r"""^\d+"""
		global level, death_level
		level = int(t.value)
		if death_level >= level:
			t.lexer.pop_state()

	# burial
	def t_OpenBurial(t):
		r"""BURI"""
		global burial_level
		burial_level = level
		t.lexer.push_state("burial")

	def t_burial_CloseBurial(t):
		r"""^\d+"""
		global level, burial_level
		level = int(t.value)
		if burial_level >= level:
			t.lexer.pop_state()

	# marriage
	def t_OpenMarriage(t):
		r"""MARR"""
		global marriage_level
		marriage_level = level
		t.lexer.push_state("marriage")

	def t_marriage_CloseMarriage(t):
		r"""^\d+"""
		global level, marriage_level
		level = int(t.value)
		if marriage_level >= level:
			t.lexer.pop_state()

	return lex.lex()


if __name__ == "__main__":
	lexer = lexer_gen()
	with open("test/teste.txt", "r") as file:
		linhas = file.readlines(6000)
		for line in linhas:
			lexer.input(line)
			for token in lexer:
				print(f"TIPO: {token.type:<10} | VALOR: {token.value:<50} | ESTADO: {lexer.current_state():<10} (NIVEL {level})")
