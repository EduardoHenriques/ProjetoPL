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


def p_person_pointer_indi(p):
	"""person :  LEVEL POINTER INDI conteudo BEGIN"""
	global lista_pessoas
	global pessoa_atual
	id_int = p[2].replace("@", '')  # obter ID
	p[0] = "<ID>" + p[2] + "</ID>"
	print(p[0] + "\n")
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

	print(f"{tag} -> {muda_tag(tag, tipo, pessoa_atual.currentLevel)}")

	tag = muda_tag(tag, tipo, pessoa_atual.currentLevel)
	cont = p[1].split(" ", 1)[1]

	if tag == "Nome":        # tirar as barras ('/') do nome
		tag.replace('/', '')

	# nao escrevemos notas
	if pessoa_atual is not None:
		p[0] = '\t' + '<' + tag + '>' + cont + '</' + tag + '>'
		print(p[0] + "\n")
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

	print(f"{tag} -> {muda_tag(tag, tipo, pessoa_atual.currentLevel)}")
	tag = muda_tag(tag, tipo, pessoa_atual.currentLevel)

	# escape do '&'
	mod = re.sub(r'&', r'&amp;', cont)

	p[0] = '\t' + '<' + tag + '>' + mod + '</' + tag + '>'
	print(p[0] + "\n")

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


def gedcomToXML():
	menuStr = '''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% PROCESSAMENTO DE LINGUAGENS 22-23 %
%                                   %
%     CONVERSOR GEDCOM -> XML       %  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
                          
Selecione a opção:

1 => FAMÍLIAS DA BIBLIA
2 => FAMÍLIAS ROMANAS                           
3 => FAMÍLIAS GREGAS                           
4 => FAMÍLIAS REAIS
                        
5 => SAIR
'''

	errorMsg = '''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%           OPCAO INVALIDA!!!       %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
'''

	opt = None

	while opt != 5:
		opt = input(menuStr)
		match opt:
			case "1":
				parse("test/familias_biblia.ged.txt", "output/output_Biblia.xml", opt)
			case "2":
				parse("test/familias_romanas.ged.txt", "output/output_Romanas.xml", opt)
			case "3":
				parse("test/familias_gregas.ged.txt", "output/output_Gregas.xml", opt)
			case "4":
				parse("test/familias_reais.ged.txt", "output/output_Reais.xml", opt)
			case "5":
				print("TERM...")
				exit()
			case _:
				print(errorMsg)
				opt = None


def parse(gedcom_path, output_path, opt):

	success_msg = f'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   OPCAO  {opt} EFETUADA COM SUCESSO     %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''

	# dar parse ao ficheiro
	f_gedcom = open(gedcom_path, encoding="utf-8")
	lines = f_gedcom.read()
	parser.parse(lines)
	f_gedcom.close()
	print('%' * 50)

	# colocar as tags <genoa></genoa> dentro do ficheiro completo, <pessoa></pessoa> em torno de cada pessoa
	# e as tags <familia></familia> em torno de cada familia enquanto adiciona
	# as tags <pai></pai> e <mae></mae> ás pessoas que deu parse

	f_xml = open(output_path, "w")
	f_xml.write("<genoa>\n")
	for elem in lista_pessoas.keys():
		p = lista_pessoas[elem]
		p.lookup(familiy_tree, p.famc)
		f_xml.write("\t<pessoa>" + p.__str__() + "\t</pessoa>\n")
	for familia in familiy_tree.keys():
		fam = familiy_tree[familia]
		f_xml.write("\t<familia>" + fam.__str__() + "\t</familia>\n")
	f_xml.write("</genoa>\n")

	print(success_msg)


if __name__ == "__main__":
	gedcomToXML()
