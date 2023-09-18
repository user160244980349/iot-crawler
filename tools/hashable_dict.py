class HashableDict(dict):
    def __key(self):
        return self["website"]

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()
