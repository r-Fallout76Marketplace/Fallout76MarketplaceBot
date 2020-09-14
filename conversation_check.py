import CONSTANTS


# CommentsThread
# Performs checks on the whole comment thread
class CommentsThread:

    # Constructor
    def __init__(self, comment):
        self.comment_thread = []  # Stores all comments in a thread
        self.users_involved = set()  # Stores all the users involved
        self.is_top_level = False  # Check if @param comment is top level
        self.more_than_two_users = False  # If more than two users are in conversation
        self.is_last_author_involved = False  # Is the author of comment is involved in conversation
        self.self_reply = False  # If author of comment replied to its own comment
        self.load_comments(comment)  # Loads all comments in comment_thread and performs checks

    # Loads all comments till top level and performs some necessary checks
    # Keeps track of how many users are involved in the thread
    def load_comments(self, comment):
        # Load all comments till it hits top level
        while not comment.is_root:
            self.comment_thread.append(comment)
            self.users_involved.add(comment.author)
            comment = comment.parent()
        # The top level comment does get stored so adds last comment
        self.comment_thread.append(comment)
        self.users_involved.add(comment.author)

        # If len is one meaning the comment is top level
        if len(self.comment_thread) <= 1:
            self.is_top_level = True
        else:
            # Checking if author replied to its own comment
            if self.comment_thread[0].author == self.comment_thread[1].author:
                self.self_reply = True

        # If there are more than two people involved
        if len(self.users_involved) > 2:
            self.more_than_two_users = True

    # Based on checks returns the output value
    def checks_output(self):
        output = CONSTANTS.REWARD_PLUS_KARMA
        # Checks if comment is top level
        if self.is_top_level:
            output = CONSTANTS.TOP_LEVEL_COMMENT
        # If author tries to give itself karma
        elif self.self_reply:
            output = CONSTANTS.CANNOT_REWARD_YOURSELF
        # If more than two people are involved
        elif self.more_than_two_users:
            output = CONSTANTS.MORE_THAN_TWO_USERS
        return output
