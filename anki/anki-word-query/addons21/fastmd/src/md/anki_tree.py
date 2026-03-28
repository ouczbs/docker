class AnkiTree:
    def __init__(self, name, level, parent = None):
        self.childList = []
        self.attrList = []
        self.name = name
        self.level = level
        self.parent = parent
        pass
    def push(self, name, level):
        child = AnkiTree(name, level, self)
        self.childList.append(child)
        return child
    def appendAttr(self, attr):
        self.attrList.append(attr)
class AnkiData:
    def __init__(self):
        self.tree = AnkiTree("root", 0)
        self.node = self.tree
        pass
    def parse(self, tree, parent):
        tags = []
        tags.append(parent.name)
        note = {"name":tree.name , "tags":tags}
        for child in tree.childList:
            if child.name not in note:
                note[child.name] = []
            for attr in child.attrList:
                note[child.name].append(attr)
        return note
    def __call__(self):
        tree = self.tree
        note_list = []
        for child in tree.childList:
            for child2 in child.childList:
                note = self.parse(child2, child)
                note_list.append(note)
        return note_list
    def enterScope(self, name, level):
        while self.node:
            if self.node.level < level:
                self.node = self.node.push(name, level)
                return
            self.node = self.node.parent
    def appendAttr(self, attr):
        self.node.appendAttr(attr)