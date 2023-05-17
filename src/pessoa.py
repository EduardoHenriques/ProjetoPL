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
		self.linhas += '\n' + linha

	def add_id(self, ref):
		self.id = ref
		ID_line = "\t<ID>" + ref + "<ID>\t\n"
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
				self.linhas[:-1] += "\n\t<mae>" + family.wife + "</mae>"
				print("No mom?O_o")
			elif family.husband is not None:
				self.linhas[:-1] += "\n\t<pai>" + family.wife + "</pai>"
				print("No dad?o_O")
			else:
				print("found parents")
		else:
			print("Key Error:")
