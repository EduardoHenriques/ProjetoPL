class Familia:

    def __init__(self):
        self.id = None
        self.child_list = []
        self.wife = None
        self.husband = None
        self.linhas = []

    def add_id(self, ref):
        self.id = ref
        ID_line = "\t<ID>" + ref + "<ID>\t\n"
        self.linhas.insert(1, ID_line)

    def add_line(self, l):
        self.linhas += '\n' + l

    def __str__(self):
        res = ""
        for l in self.linhas:
            res += l
        return res + "\n"

    def add_wife(self, wife):
        self.wife = wife

    def add_husband(self, husb):
        self.husband = husb

    def add_child(self, child):
        self.child_list.append(child)
