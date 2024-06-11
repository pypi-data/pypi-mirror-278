class Report:
    def __init__(self):
        self.notes = []


    def __str__(self):
        return f'{self.__class__.__name__}: ({", ".join((str(v) for v in self.__dict__.values()))})'

    def add_note(self, note):
        self.notes.append(note)
