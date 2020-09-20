# AwardeeAwarder
# Stores information about who gave karma to who and submission
class AwardeeAwarder:

    # Constructor
    def __init__(self, comment):
        # Saving the parameter
        self.comment = comment
        # Person who awarded the karma
        self.awarder = self.comment.author
        # Who received karma
        parent_comment = self.comment.parent()
        self.awardee = parent_comment.author
        # submission
        self.submission = self.comment.submission

    # Compares the authors name and submissions
    def __cmp__(self, other):
        if self.awarder == other.awarder:
            if self.awardee == other.awardee:
                if self.submission == other.submission:
                    return True
        return False
