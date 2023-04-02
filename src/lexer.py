import ply.lex as lex


def t_error(t):
	t.lexer.skip(1)


def lexer_gen():
	tokens = [
		"BARRA",

		"LEVEL",

		"HEADER",
		"SOUR",	 # approved system ID
		"DEST",	 #
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
		"MAR",	 # casamento
		"PLACE",
		"BURIAL",

		"POINTER",
		"REFN",

		"FAMS",
		"FAMC",
		"CHILD",
		"HUSBAND",
		"WIFE",
		"DIV",	 # divorcio(opcional, T/F)



	]

	t_ignore = r"\t\s\n"

	t_POINTER = r"\@\w+[^@]?\@"

	t_LEVEL = r"^\d+"

	t_ID = t_LEVEL + r"\s*" + t_POINTER + r"\s*(?=INDI)"

	t_NAME = r"(?<=NAME).+"

	t_COMM = r"COMM"
	t_CONT = r"CONT"

	t_DATE = r"(?<=DATE).+"

	t_SEX = r"(?<=SEX)[MF]"

	t_BURIAL = r"(?<=BURI).+"

	t_PLACE = r"(?<=PLAC).+"


	return lex.lex()


if __name__ == "__main__":
	lexer = lexer_gen()
	with open("test/teste.txt", "r") as file:
		linhas = file.readlines(30000)
		for line in linhas:
			lexer.input(line)
			for token in lexer:
				print(f"TIPO: {token.type:<10} | VALOR: {token.value:<10}")
