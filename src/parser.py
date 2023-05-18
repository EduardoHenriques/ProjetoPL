import ply.yacc as yacc
from pessoa import Pessoa
from familia import Familia
from lexer import tokens
import os
import re

# contem todas as pessoas
lista_pessoas = dict()
familiy_tree = dict()

pessoa_atual = Pessoa()  # pessoa vazia
familia_atual = Familia()  # Familia vazia


def p_gedcom(p):
	"""gedcom  	: START_FILE header BEGIN people families"""
	print("li um ficheiro gedcom")


# ---------------------------------------------------- PESSOA------------------------------------------------------------


def p_header(p):
	"""header : header LEVEL CONTENT
			  | LEVEL CONTENT """
	if len(p) == 4:
		print(p[3])
	else:
		print(p[2])


def p_people(p):
	"""people : people person
			  | person"""
	print("ENTERED PEOPLE")


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
		pessoa_atual.currentLevel = int(p[2])
	else:
		p[0] = p[2][0]
		pessoa_atual.currentLevel = int(p[1])


def p_restPerson_single(p):
	"""restPerson	: CONTENT"""
	global pessoa_atual
	tag = p[1].split(" ", 1)[0]
	cont = p[1].split(" ", 1)[1]
	p[0] = '\t' + '<' + tag + '>' + cont + '</' + tag + '>'
	print(p[0])

	if tag == "NAME":        # tirar as barras ('/') do nome
		tag.replace('/', '')

	if pessoa_atual is not None:
		if tag == "FAMS":
			pessoa_atual.add_fams(cont.strip())
		elif tag == "FAMC":
			pessoa_atual.add_famc(cont.strip())
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
	"""family : LEVEL POINTER FAM conteudoF BEGIN
			  | LEVEL POINTER FAM conteudoF END_FILE"""
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
	"""restFams	: CONTENT"""
	global familia_atual
	global familiy_tree

	tag = p[1].split(" ", 1)[0]
	cont = p[1].split(" ", 1)[1]

	# escape do '&'
	mod = re.sub(r'&', r'&amp;', cont)

	p[0] = '\t' + '<' + tag + '>' + mod + '</' + tag + '>'
	print(p[0])

	if familia_atual is not None:
		if tag == "WIFE":
			familia_atual.add_wife(cont.strip())
		elif tag == "HUSB":
			familia_atual.add_husband(cont.strip())
		elif tag == "CHIL":
			familia_atual.add_child(cont.strip())

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


#def p_multTag_fim(p):
	#"""multTag		: TRLR"""
	#print("chegou ao fim")
	#p[0] = "FIM"
	#global tipo
	#tipo = p[0]

# tags da family tree


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


with open("test/output.xml", "w") as f:
	f.write("<genoa>\n")
	for elem in lista_pessoas.keys():
		p = lista_pessoas[elem]
		p.lookup(familiy_tree, p.famc)
		f.write("\t<pessoa>" + p.__str__() + "\t</pessoa>\n")
	for familia in familiy_tree.keys():
		fam = familiy_tree[familia]
		f.write("\t<familia>" + fam.__str__() + "\t</familia>\n")
	print("End")
	f.write("</genoa>\n")
