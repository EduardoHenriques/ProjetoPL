from parser import p_error

double_tags = ["DATE", "PLACE"]
single_tags = ["NAME", "TITL",
               "SEX",
               ]

# tipo -> morte, nascimento, batismo, etc...
def muda_tag(p, pessoa_atual, tipo):
	tag = p[1].split(" ", 1)[0]
	cont = p[1].split(" ", 1)[1]

	# tirar as barras do nome
	if tag == "NAME":
		tag.replace('/', '')

	# adicionar familia em que é Pai/Mae
	# caso nao exista, é caso de erro
	if pessoa_atual is not None:
		if tag == "FAMS":
			pessoa_atual.add_fams(cont.strip())
		elif tag == "FAMC":
			pessoa_atual.add_famc(cont.strip())
		else:
			pessoa_atual.add_line(p[0])
	else:
		p_error(p)

	# exemplo: <ID> ... <ID>
	p[0] = '\t' + '<' + tag + '>' + cont + '</' + tag + '>'

	# tags interligadas(ex: Data (de) Morte)

	print(p[0])