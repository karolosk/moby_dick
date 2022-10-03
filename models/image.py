class ImageModel(object):

    def __init__(self, id="", tag="", date=""):
        self.id = id
        self.tag = tag
        self.date = date

    def to_json(self):
        return {
            "id": self.id,
            "tag": self.tag,
            "date": self.date,
        }