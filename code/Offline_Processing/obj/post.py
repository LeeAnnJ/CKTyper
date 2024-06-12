class Post:

    """
    This object represents an SO Post.
    """
    def __lt__(self, other):
        if int(self.parent_id) == int(other.parent_id):
            return int(self.id) < int(other.id)
        return int(self.parent_id) < int(other.parent_id)

    def __init__(self, row):
        self.id = row.get('Id')
        self.post_type_id = row.get('PostTypeId')
        if row.get('ParentId') is not None:
            self.parent_id = row.get('ParentId')
        else:
            self.parent_id = ''

        self.body = row.get('Body')
        self.last_activity_date = row.get('LastActivityDate')

        if row.get('Title') is not None:
            self.body = row.get('Title') + '\n' + self.body

        if row.get('Tags') is not None:
            self.tags = row.get('Tags')
        else:
            self.tags = ''

    def to_dict_i(self):  # to a dict with integers
        return {
            'Id': int(self.id),
            'PostTypeId': int(self.post_type_id),
            'ParentId': int(self.parent_id) if self.parent_id != '' else 0,
            'Body': self.body,
        }

    def to_dict_s(self):  # to a dict with all strings
        return {
            'Id': self.id,
            'PostTypeId': self.post_type_id,
            'ParentId': self.parent_id,
            'Body': self.body,
        }