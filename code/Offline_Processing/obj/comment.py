class Comment:

    """
    This object represents an SO comment.
    """

    def __init__(self, row):
        self.id = row.get('Id')
        self.post_id = row.get('PostId')
        if row.get('Score') is not None:
            self.score = row.get('Score')
        else:
            self.score = ''
        self.text = row.get('Text')

    def to_dict_i(self):  # to a dict with integers
        return {
            'Id': int(self.id),
            'PostId': int(self.post_id),
            'Score': int(self.score) if self.score != '' else 0,
            'Text': self.text,
        }

    def to_dict_s(self):  # to a dict with all strings
        return {
            'Id': self.id,
            'PostId': self.post_id,
            'Score': self.score,
            'Text': self.text,
        }
