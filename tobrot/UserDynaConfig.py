class UserDynaConfig:

    def __init__(self, user_id, upload_as_doc=False):
        self.user_id = user_id
        self.upload_as_doc = upload_as_doc

    def __hash__(self):
        return hash((self.user_id, self.upload_as_doc))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.user_id == other.user_id
