import ply.yacc as yacc
from pessoa import Pessoa
from familia import Familia
from lexer import tokens
import os

# contem todas as pessoas
lista_pessoas = dict()
familiy_tree = dict()

pessoa_atual = None
familia_atual = None


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
	p[0] = "<ID>" + id_int + "<\\ID>"


# pessoa_atual = Pessoa(id_int)  # criar pessoa nova e associar ID
# pessoa_atual.add_line('\t' + p[0])
# lista_pessoas[id_int] = pessoa_atual  # guardar pessoa na lista


def p_conteudo_list(p):
	"""conteudo		: conteudo LEVEL restPerson
					| LEVEL restPerson  """
	print("li uma pessoa")
	global pessoa_atual


# if len(p) == 4:
#	pessoa_atual.currentLevel = int(p[2])
# else:
#	pessoa_atual.currentLevel = int(p[1])


def p_restPerson_single(p):
	"""restPerson	: singTag CONTENT"""
	global pessoa_atual
	p[0] = '\t' + '<' + str([p[1]][0]) + '>' + p[2] + '<\\' + str([p[1]][0]) + '>'
	print(p[0])


# if str([p[1]][0]) == "FAMS":
# pessoa_atual.add_fams(str([p[1]][0]))
# elif str([p[1]][0]) == "FAMC":
# pessoa_atual.add_famc(str([p[1]][0]))
# else:
# pessoa_atual.add_line(p[0])


# -------------------------------------------------- FAMILIA-------------------------------------------------------------


def p_families(p):
	"""families : families family
	 			| family """
	print("comecei a ler familias")


def p_family(p):
	"""family : LEVEL POINTER FAM conteudoF BEGIN
			  | LEVEL POINTER FAM conteudoF"""
	global familiy_tree
	global familia_atual
	print("li uma familia")


# print("li uma familia")
# id_int = p[2].replace("@", '')
# familia_atual = Familia(id_int)
# familiy_tree[id_int] = familia_atual


def p_conteudo_fam(p):
	"""conteudoF		: conteudoF LEVEL restFams
						| LEVEL restFams"""
	print("li uma familia")
	global pessoa_atual


# if len(p) == 4:
# pessoa_atual.currentLevel = int(p[2])
# else:
# pessoa_atual.currentLevel = int(p[1])


def p_restFams_single(p):
	"""restFams	: singTag CONTENT"""
	global familia_atual
	global familiy_tree
	p[0] = '\t' + '<' + str([p[1]][0]) + '>' + p[2] + '<\\' + str([p[1]][0]) + '>'
	print(p[0])


# if str([p[1]][0]) == "WIFE":
#	familia_atual.add_wife(p[2])
# elif str([p[1]][0]) == "HUSBAND":
#	familia_atual.add_husband(p[2])
# elif str([p[1]][0]) == "CHILD":
#	familia_atual.add_child(p[2])


# -------------------------------------------------- ENDING ----------------------------------------------------------


def p_end(p):
	"""end : LEVEL TRLR"""
	print("Acabou")


# -------------------------------------------------- TAGS-------------------------------------------------------------


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


def p_singTag_refn(p):
	""" singTag		: REFN"""
	p[0] = p[1]


def p_singTag_fams(p):
	""" singTag		: FAMS"""
	p[0] = p[1]


def p_singTag_famc(p):
	""" singTag		: FAMC"""
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


def p_multTag_chr(p):
	"""multTag		: CHR"""
	p[0] = p[1]
	global tipo
	tipo = p[0]


def p_multTag_burial(p):
	"""multTag		: BURIAL"""
	p[0] = p[1]
	global tipo
	tipo = p[0]


# tags da family tree


def p_singTag_wife(p):
	""" singTag		: WIFE"""
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

os.system("clear")
with open("test/output.txt", "w") as f:
	for elem in lista_pessoas.keys():
		p = lista_pessoas[elem]
		f.write(p.__str__())
	print("End")
