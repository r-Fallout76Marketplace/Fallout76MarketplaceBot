import CONFIG
import CONSTANTS


# Replies to comment with text=body
def reply(comment, body):
    response = body + "\n\n*^(This action was performed by a bot, please contact the mods for any questions.)*"
    comment.reply(response)
    pass


# If checks failed sends reply appropriately
def check_failed(result, comment):
    comment_body = "Error: Failed to give Karma"
    if result == CONSTANTS.TOP_LEVEL_COMMENT:
        comment_body = "You cannot give karma to post."
    elif result == CONSTANTS.CANNOT_REWARD_YOURSELF:
        comment_body = "You cannot give karma to yourself."
    elif result == CONSTANTS.NOT_IN_CONVERSATION:
        comment_body = "You are not involved in the trade."
    elif result == CONSTANTS.MORE_THAN_TWO_USERS:
        comment_body = "More than people are involved in trade. Please separate out your conversation."
        comment_body = comment_body + "Create separate a post if the post is not related to your trade"
    elif result == CONSTANTS.TRADE_ALREADY_OCCURRED:
        comment_body = "You have already rewarded user karma. For more trades, please create a new post."
    reply(comment, comment_body)
    pass


# If checks pass give the parent comment karma
def check_passed(comment):
    p_comment = comment.parent()
    author_name = p_comment.author.name
    # if the author has no flair
    if p_comment.author_flair_css_class == '':
        # sets the flair to one
        CONFIG.reddit.subreddit(CONFIG.subreddit_name).flair.set(author_name, text='Karma: 1',
                                                                 flair_template_id=CONSTANTS.KARMA_ID)
    else:
        # Getting the flair and incrementing it by one
        karma = p_comment.author_flair_text
        # Splits Karma into two
        karma = karma.split()
        # Increments the int part
        karma[1] = int(karma[1])
        karma[1] += 1
        # Combines back string and int part
        karma = karma[0] + ' ' + str(karma[1])
        # Updates the user flair
        CONFIG.reddit.subreddit(CONFIG.subreddit_name).flair.set(author_name, text=str(karma),
                                                                 flair_template_id=CONSTANTS.KARMA_ID)
    # Sets the post flair to indicate that trade already happened
    # submission = p_comment.submission # Needs to be implemented later
    # submission.flair.select(CONSTANTS.TRADE_ENDED)
    # Replies with comment
    comment_body = "Hi " + comment.author.name + "! You have successfully rewarded "
    comment_body = comment_body + p_comment.author.name + " one karma point"
    reply(comment, comment_body)
    pass
