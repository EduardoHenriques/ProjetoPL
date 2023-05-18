import ply.yacc as yacc
from pessoa import Pessoa
from familia import Familia
from lexer import tokens
import os

# contem todas as pessoas
lista_pessoas = dict()
familiy_tree = dict()

pessoa_atual = Pessoa()  # pessoa vazia
familia_atual = Familia()  # Familia vazia


def p_gedcom(p):
	"""gedcom  	: people families end"""
	print("li um ficheiro gedcom")


# ---------------------------------------------------- PESSOA------------------------------------------------------------


def p_people(p):
	"""people : people person
			  | person"""


def p_person_pointer_indi(p):
	"""person :  LEVEL POINTER INDI conteudo BEGIN"""
	global lista_pessoas
	global pessoa_atual
	id_int = p[2].replace("@", '')  # obter ID
	p[0] = "<ID>" + p[2] + "</ID>"
	print(p[0])
	pessoa_atual.add_id(p[2])  # associar ID á pessoa
	lista_pessoas[id_int] = pessoa_atual  # guardar pessoa na lista
	pessoa_atual = Pessoa()  # dar reset a pessoal atual


def p_conteudo_list(p):
	"""conteudo		: conteudo LEVEL restPerson
					| LEVEL restPerson  """
	global pessoa_atual

	if len(p) == 4:
		p[0] = p[3][0]
	# pessoa_atual.currentLevel = int(p[2])
	else:
		p[0] = p[2][0]
	# pessoa_atual.currentLevel = int(p[1])


def p_restPerson_single(p):
	"""restPerson	: singTag CONTENT"""
	global pessoa_atual
	if str([p[1]][0]) == "NAME":        # tirar as barras ('/') do nome
		p[2] = p[2].replace('/', '')

	p[0] = '\t' + '<' + str([p[1]][0]) + '>' + p[2] + '</' + str([p[1]][0]) + '>'
	print(p[0])
	if pessoa_atual is not None:
		if str([p[1]][0]) == "FAMS":
			pessoa_atual.add_fams(str(p[2]).strip())
		elif str([p[1]][0]) == "FAMC":
			pessoa_atual.add_famc(str(p[2]).strip())
		else:
			pessoa_atual.add_line(p[0])
	else:
		print("null person")


def p_restPerson_mult(p):
	"""restPerson	: multTag"""
	p[0] = p[1]


# -------------------------------------------------- FAMILIA-------------------------------------------------------------


def p_families(p):
	"""families : families family
				| family """


def p_family(p):
	"""family : LEVEL POINTER FAM conteudoF BEGIN"""
	global familiy_tree
	global familia_atual

	id_int = p[2].replace("@", '')
	familia_atual.add_id(id_int)
	familiy_tree[p[2]] = familia_atual
	familia_atual = Familia()


def p_conteudo_fam(p):
	"""conteudoF		: conteudoF LEVEL restFams
						| LEVEL restFams"""
	global pessoa_atual

	if len(p) == 4:
		pessoa_atual.currentLevel = int(p[2])
	else:
		pessoa_atual.currentLevel = int(p[1])


def p_restFams_single(p):
	"""restFams	: singTag CONTENT"""
	global familia_atual
	global familiy_tree
	p[0] = '\t' + '<' + str([p[1]][0]) + '>' + p[2] + '</' + str([p[1]][0]) + '>'
	print(p[0])

	if familia_atual is not None:
		if str([p[1]][0]) == "WIFE":
			familia_atual.add_wife(str(p[2]).strip())
		elif str([p[1]][0]) == "HUSB":
			familia_atual.add_husband(str(p[2]).strip())
		elif str([p[1]][0]) == "CHIL":
			familia_atual.add_child(str(p[2]).strip())

		familia_atual.add_line(p[0])
	else:
		print("familia nula")


def p_restFams_mult(p):
	"""restFams	: multTag"""
	p[0] = p[1]


# -------------------------------------------------- ENDING ----------------------------------------------------------


def p_end(p):
	"""end : LEVEL TRLR"""
	print("Acabou")


# -------------------------------------------------- TAGS-------------------------------------------------------------


def p_singTag_burial(p):
	""" singTag		: BURIAL"""
	p[0] = p[1]


def p_singTag_name(p):
	""" singTag		: NAME"""
	p[0] = "Nome"


def p_singTag_title(p):
	""" singTag		: TITLE"""
	p[0] = "Titulo"


def p_singTag_sex(p):
	""" singTag		: SEX"""
	p[0] = "Sexo"


def p_singTag_refn(p):
	""" singTag		: REFN"""
	p[0] = "Ref"


def p_singTag_fams(p):
	""" singTag		: FAMS"""
	p[0] = p[1]


def p_singTag_famc(p):
	""" singTag		: FAMC"""
	p[0] = p[1]


def p_singTag_date(p):
	""" singTag		: DATE"""
	p[0] = "Data" + tipo


def p_singTag_place(p):
	"""singTag		: PLACE"""
	p[0] = "Local" + tipo


def p_multTag_birth(p):
	"""multTag		: BIRTH"""
	p[0] = "Nasc"
	global tipo
	tipo = p[0]


def p_multTag_death(p):
	"""multTag		: DEATH"""
	p[0] = "Óbito"
	global tipo
	tipo = p[0]


def p_multTag_chr(p):
	"""multTag		: CHR"""
	p[0] = "Batismo"
	global tipo
	tipo = p[0]


def p_multTag_burial(p):
	"""multTag		: BURIAL"""
	p[0] = "Enterro"
	global tipo
	tipo = p[0]


def p_multTag_marriage(p):
	"""multTag		: MAR"""
	p[0] = "Casamento"
	global tipo
	tipo = p[0]


# tags da family tree


def p_singTag_wife(p):
	""" singTag		: WIFE"""
	p[0] = p[1]


def p_singTag_div(p):
	""" singTag		: DIV"""
	p[0] = p[1]


def p_singTag_husband(p):
	""" singTag		: HUSBAND"""
	p[0] = p[1]


def p_singTag_child(p):
	""" singTag		: CHILD"""
	p[0] = p[1]


def p_error(p):
	print(p)
	p.success = False
	print("Syntax Error!", p)
	exit()


parser = yacc.yacc()
parser.success = True

with open("test/sintaxe.txt", encoding="utf-8") as f:
	lines = f.read()
	parser.parse(lines)
	if parser.success:
		print("Yes")
	else:
		print("No")
	print("End")

print('%' * 50)


with open("test/output.txt", "w") as f:
	for elem in lista_pessoas.keys():
		p = lista_pessoas[elem]
		p.lookup(familiy_tree, p.famc)
		f.write("<pessoa>" + p.__str__() + "</pessoa>\n")
	for familia in familiy_tree.keys():
		fam = familiy_tree[familia]
		f.write("<familia>" + fam.__str__() + "</familia>\n")
	print("End")
	for idF in familiy_tree.keys():
		fam = familiy_tree[idF]
		print(fam.child_list)
