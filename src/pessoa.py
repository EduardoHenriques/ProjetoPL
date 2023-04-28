from familia import Familia


class Pessoa:

	def __init__(self, ID):
		self.id = ID
		self.linhas = ["<pessoa>\n", "<\\pessoa>"]
		self.currentLevel = 1
		self.fams = None
		self.famc = None

	def add_line(self, linha):
		self.linhas[:-1] += linha + '\n'

	def add_id(self, ref):
		self.id = ref

	def add_fams(self, ref):
		self.fams = ref

	def add_famc(self, ref):
		self.famc = ref

	def __str__(self):
		res = ""
		for l in self.linhas:
			res += l
		return res + "\n"

	def lookup(self, family_tree, famID, isChild):
		family = family_tree[famID]
		self.linhas[:-1] += "<mae>\n" + family.wife + "<\\mae>"
		self.linhas[:-1] += "<pai>\n" + family.wife + "<\\pai>"
