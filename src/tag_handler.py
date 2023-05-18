double_tags = {
			"DATE": "Data",
			"PLAC": "Local",
			"TIME": "Hora"
}

single_tags = {
			"NAME": "Nome",
			"TITL": "Título",
			"SEX": "Sexo",
			"ALIAS": "Alcunha",
			"DIV": "Divorcio",
			"REFN": "Ref",
			"HUSB": "Marido",
			"WIFE": "Mulher",
			"CHIL": "Descendente",
			"GIVN": "NomeDado"
}


# tipo -> Obito, Nasc, Batismo, Enterro, Casamento,...


def muda_tag(tag, tipo, level):
	if tag in double_tags.keys():
		return double_tags[tag] + tipo
	elif tag in single_tags.keys():
		return single_tags[tag]
	else:
		return tag

