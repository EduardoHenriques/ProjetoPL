import ply.yacc as yacc
from pessoa import Pessoa
from familia import Familia
from lexer import tokens
from tag_handler import muda_tag
import os
import re

# contem todas as pessoas
lista_pessoas = dict()
familiy_tree = dict()

tag_atual = None
pessoa_atual = Pessoa()  # pessoa vazia
familia_atual = Familia()  # Familia vazia
tipo = None


def p_gedcom(p):
	"""gedcom  	: START_FILE header BEGIN people families"""
	print("li um ficheiro gedcom")


# ---------------------------------------------------- PESSOA------------------------------------------------------------


def p_header(p):
	"""header : header LEVEL restHeader
			  | LEVEL restHeader"""


def p_header_rest(p):
	"""restHeader : CONTENT
				  | multTag"""


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
	#print(p[0])
	pessoa_atual.add_id(p[2])  # associar ID á pessoa
	lista_pessoas[id_int] = pessoa_atual  # guardar pessoa na lista
	pessoa_atual = Pessoa()  # dar reset a pessoal atual


def p_conteudo_list(p):
	"""conteudo		: conteudo LEVEL restPerson
					| LEVEL restPerson  """
	global pessoa_atual

	#if len(p) == 4 :
	#	p[0] = p[3][0]
	#	pessoa_atual.currentLevel = int(p[2])
	#else:
	#	p[0] = p[2][0]
	#	pessoa_atual.currentLevel = int(p[1])


def p_restPerson_single(p):
	"""restPerson	: CONTENT"""
	global pessoa_atual
	global tag_atual
	tag = p[1].split(" ", 1)[0]

	# atraves do tipo(nascimento, morte, etc.) e da tag que analisou,
	# substitui a tag. Exemplo: muda_tag("DATE", "Nasc") = "DataNasc"
	#                           muda_tag("NAME", tipo_irrelevante) = "Nome"

	tag = muda_tag(tag, tipo, pessoa_atual.currentLevel)
	cont = p[1].split(" ", 1)[1]

	if tag == "Nome":        # tirar as barras ('/') do nome
		tag.replace('/', '')

	# nao escrevemos notas
	if pessoa_atual is not None:
		p[0] = '\t' + '<' + tag + '>' + cont + '</' + tag + '>'
		print(p[0])
		if tag == "FAMS":
			pessoa_atual.add_fams(cont.strip())
		elif tag == "FAMC":
			pessoa_atual.add_famc(cont.strip())
		elif tag == "CONT":
			if tag_atual != "NOTE":
				pessoa_atual.add_cont(cont, tag_atual)
		else:
			tag_atual = tag
			if tag != "NOTE":
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
						| LEVEL restFams
						| """
	global pessoa_atual

	#if len(p) == 4:
	#	pessoa_atual.currentLevel = int(p[2])
	#else:
	#	pessoa_atual.currentLevel = int(p[1])


def p_restFams_single(p):
	"""restFams	: CONTENT"""
	global familia_atual
	global familiy_tree

	tag = p[1].split(" ", 1)[0]
	cont = p[1].split(" ", 1)[1]

	print(tag, muda_tag(tag, tipo, pessoa_atual.currentLevel))
	tag = muda_tag(tag, tipo, pessoa_atual.currentLevel)

	# escape do '&'
	mod = re.sub(r'&', r'&amp;', cont)

	p[0] = '\t' + '<' + tag + '>' + mod + '</' + tag + '>'
	print(p[0])

	if familia_atual is not None:
		if tag == "Mulher":
			familia_atual.add_wife(cont.strip())
		elif tag == "Marido":
			familia_atual.add_husband(cont.strip())
		elif tag == "Descendente":
			familia_atual.add_child(cont.strip())

		familia_atual.add_line(p[0])
	else:
		print("familia nula")


def p_restFams_mult(p):
	"""restFams	: multTag"""
	p[0] = p[1]


# -------------------------------------------------- TAGS-------------------------------------------------------------


def p_multTag_birth(p):
	"""multTag		: BIRTH"""
	p[0] = "Nasc"
	global tipo
	tipo = p[0]


def p_multTag_change(p):
	"""multTag		: CHAN"""
	p[0] = "Mudanca"
	global tipo
	tipo = p[0]


def p_multTag_death(p):
	"""multTag		: DEATH"""
	p[0] = "Obito"
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


def p_multTag_gedc(p):
	"""multTag		: GEDC"""


def p_multTag_cont(p):
	"""multTag  : CONT"""




def p_error(p):
	print(p)
	p.success = False
	print("Syntax Error!", p)
	exit()


parser = yacc.yacc()
parser.success = True

# FAMILIAS BIBLIA

with open("test/familias_biblia.txt", encoding="utf-8") as f:
	lines = f.read()
	parser.parse(lines)
	if parser.success:
		print("Yes")
	else:
		print("No")
	print("End")

print('%' * 50)


with open("output/output_Biblia.xml", "w") as f:
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

# FAMILIAS REAIS

with open("test/familias_reais.txt", encoding="utf-8") as f:
	lines = f.read()
	parser.parse(lines)
	if parser.success:
		print("Yes")
	else:
		print("No")
	print("End")

print('%' * 50)


with open("output/output_Reais.xml", "w") as f:
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


# FAMILIAS ROMANAS

with open("test/familias_romanas.txt", encoding="utf-8") as f:
	lines = f.read()
	parser.parse(lines)
	if parser.success:
		print("Yes")
	else:
		print("No")
	print("End")

print('%' * 50)


with open("output/output_Romanas.xml", "w") as f:
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


# FAMILIAS GREGAS

with open("test/familias_gregas.txt", encoding="utf-8") as f:
	lines = f.read()
	parser.parse(lines)
	if parser.success:
		print("Yes")
	else:
		print("No")
	print("End")

print('%' * 50)


with open("output/output_Gregas.xml", "w") as f:
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
