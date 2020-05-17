# Class Trade
# Saves the attributes relevant to a trade for quick comparison


class Trade:

    def __init__(self, conversation_object):
        # Saves the conversation and user info
        self.conversation_object = conversation_object
        # Saves URL of post
        self.submission_link = conversation_object.comments[0].submission.url
        # User who gave karma
        self.from_user = conversation_object.comments[0].author
        # User who received it
        self.to_user = conversation_object.comments[1].author
