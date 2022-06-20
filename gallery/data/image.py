class Image:
    def __init__(self, file_name, owner, id):
        self.file_name = file_name
        self.owner = owner
        self.id = id


    def __repr__(self):
        return "Filename="+self.file_name+" owner= "+self.owner

