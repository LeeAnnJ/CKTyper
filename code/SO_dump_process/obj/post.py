class Post:

    """
    This object represents an SO Post.
    """

    def __init__(self, row):
        self.id = row.get('Id')
        self.post_type_id = row.get('PostTypeId')
        if row.get('ParentId') is not None:
            self.parent_id = row.get('ParentId')
        else: self.parent_id = ''

        if row.get('AcceptedAnswerId') is not None:
            self.accepted_answer_id = row.get('AcceptedAnswerId')
        else: self.accepted_answer_id = ''

        self.creation_date = row.get('CreationDate')

        if row.get('Score') is not None:
            self.score = row.get('Score')
        else: self.score = ''

        if row.get('ViewCount') is not None:
            self.view_count = row.get('ViewCount')
        else: self.view_count = ''

        self.body = row.get('Body')
        self.last_activity_date = row.get('LastActivityDate')

        if row.get('ClosedDate') is not None:
            self.closed_date = row.get('ClosedDate')
        else: self.closed_date = ''

        if row.get('Title') is not None:
            self.title = row.get('Title')
        else: self.title = ''

        if row.get('Tags') is not None:
            self.tags = row.get('Tags')
        else: self.tags = ''

        if row.get('AnswerCount') is not None:
            self.answer_count = row.get('AnswerCount')
        else: self.answer_count = ''

        if row.get('CommentCount') is not None:
            self.comment_count = row.get('CommentCount')
        else: self.comment_count = ''

        if row.get('FavoriteCount') is not None:
            self.favorite_count = row.get('FavoriteCount')
        else: self.favorite_count = ''

        if row.get('OwnerUserId') is not None:
            self.owner_userid = row.get('OwnerUserId')
        else: self.owner_userid = ''

        if row.get('P-Title') is not None:
            self.preprocessed_title = row.get('P-Title')
        else: self.preprocessed_title = ''

        if row.get('P-Body') is not None:
            self.preprocessed_body = row.get('P-Body')
        else: self.preprocessed_body = ''

        if row.get('P-Tags') is not None:
            self.preprocessed_tags = row.get('P-Tags')
        else: self.preprocessed_tags = ''

    def set_preprocessed_title(self, ptitle):
        self.preprocessed_title = ptitle

    def set_preprocessed_body(self, pbody):
        self.preprocessed_body = pbody

    def set_preprocessed_tags(self, ptags):
        self.preprocessed_tags = ptags

    def to_dict_i(self):  # to a dict with integers
        return {
            'Id': int(self.id),
            'PostTypeId': int(self.post_type_id),
            'ParentId': int(self.parent_id) if self.parent_id != '' else 0,
            'AcceptedAnswerId': int(self.accepted_answer_id) if self.accepted_answer_id != '' else 0,
            'CreationDate': self.creation_date,
            'Score': int(self.score) if self.score != '' else 0,
            'ViewCount': int(self.view_count) if self.view_count != '' else 0,
            'Body': self.body,
            'P-Body': self.preprocessed_body,
            'LastActivityDate': self.last_activity_date,
            'ClosedDate': self.closed_date,
            'Title': self.title,
            'P-Title': self.preprocessed_title,
            'Tags': self.tags,
            'P-Tags': self.preprocessed_tags,
            'AnswerCount': int(self.answer_count) if self.answer_count != '' else 0,
            'CommentCount': int(self.comment_count) if self.comment_count != '' else 0,
            'FavoriteCount': int(self.favorite_count) if self.favorite_count != '' else 0,
            'OwnerUserId': int(self.owner_userid) if self.owner_userid != '' else 0
        }

    def to_dict_s(self):  # to a dict with all strings
        return {
            'Id': self.id,
            'PostTypeId': self.post_type_id,
            'ParentId': self.parent_id,
            'AcceptedAnswerId': self.accepted_answer_id,
            'CreationDate': self.creation_date,
            'Score': self.score,
            'ViewCount': self.view_count,
            'Body': self.body,
            'P-Body': self.preprocessed_body,
            'LastActivityDate': self.last_activity_date,
            'ClosedDate': self.closed_date,
            'Title': self.title,
            'P-Title': self.preprocessed_title,
            'Tags': self.tags,
            'P-Tags': self.preprocessed_tags,
            'AnswerCount': self.answer_count,
            'CommentCount': self.comment_count,
            'FavoriteCount': self.favorite_count,
            'OwnerUserId': self.owner_userid
        }