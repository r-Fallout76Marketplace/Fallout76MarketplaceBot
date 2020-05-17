import CONSTANTS


# Conversation class
# Stores all the comments in the conversations
# Also performs checks on them
class Conversation:

    # Constructor
    def __init__(self, comment):
        self.comments = []
        self.users_involved = set()
        self.is_top_level = False
        self.more_than_two_users = False
        self.load_comments(comment)

    # Loads all comments till top level and performs
    # some necessary checks
    def load_comments(self, comment):
        # Looping and storing all comments till top level
        # Also keeps track of how many users are involved in the thread
        while not comment.is_root:
            self.comments.append(comment)
            self.users_involved.add(comment.parent().author)
            comment = comment.parent()
        # The top level comment does get stored so adds last comment
        self.comments.append(comment)
        self.users_involved.add(comment.parent().author)

        # If len is one meaning the comment is top level
        if len(self.comments) == 1:
            self.is_top_level = True

        # If there are more than two people involved
        if len(self.users_involved) > 2:
            self.more_than_two_users = True

    # If author is in users_involved meaning the author is
    # in conversation
    def is_in_conversation(self, author):
        return author not in self.users_involved

    # Performs all the necessary checks
    def check_passed(self, comment):
        output = CONSTANTS.PASSED
        # Checks if comment is top level
        if self.is_top_level:
            output = CONSTANTS.TOP_LEVEL_COMMENT
        # If author tries to give itself karma
        elif comment.author == comment.parent().author:
            output = CONSTANTS.CANNOT_REWARD_YOURSELF
        # If author is not involved in conversation
        elif self.is_in_conversation(comment.author):
            output = CONSTANTS.NOT_IN_CONVERSATION
        # If more than two people are involved
        elif self.more_than_two_users:
            output = CONSTANTS.MORE_THAN_TWO_USERS
        return output
