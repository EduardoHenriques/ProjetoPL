from familia import Familia
# ["<pessoa>\n", "<\\pessoa>"]


class Pessoa:
	def __init__(self):
		self.id = None  # sem ID atribuido
		self.linhas = []
		self.currentLevel = 1
		self.fams = None
		self.famc = None

	def add_line(self, linha):
		self.linhas += '\n\t' + linha

	def add_cont(self, linha, tag_atual):
		back = len(tag_atual) + 3
		self.linhas[:-back] += linha.replace('>>', '')

	def add_id(self, ref):
		self.id = ref
		ID_line = "\t\t<ID>" + ref + "</ID>\t\n"
		self.linhas.insert(1, ID_line)

	def add_fams(self, ref):
		self.fams = ref

	def add_famc(self, ref):
		self.famc = ref

	def __str__(self):
		res = ""
		for l in self.linhas:
			res += l
		return res + "\n"

	def lookup(self, family_tree, famID):
		if famID is not None:
			family = family_tree[famID]
			if family.wife is not None:
				self.linhas += "\n\t\t<mae>" + family.wife + "</mae>"
			if family.husband is not None:
				self.linhas += "\n\t\t<pai>" + family.husband + "</pai>"
			if len(family.child_list) != 0:
				for irmao in family.child_list:
					if self.id != irmao:
						self.linhas += "\n\t\t<irmao>" + irmao + "</irmao>"
