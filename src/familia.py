class Familia:

    def __init__(self, ID):
        self.id = ID
        self.child_list = []
        self.wife = None
        self.husband = None

    def add_wife(self, wife):
        self.wife = wife

    def add_husband(self, husb):
        self.husband = husb

    def add_child(self, child):
        self.child_list.append(child)
