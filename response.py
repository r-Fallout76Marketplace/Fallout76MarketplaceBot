import CONSTANTS

response_dictionary = {
    CONSTANTS.TOP_LEVEL_COMMENT: "You cannot give karma to post.",
    CONSTANTS.CANNOT_REWARD_YOURSELF: "You cannot give karma to yourself.",
    CONSTANTS.MORE_THAN_TWO_USERS: "More than two people are involved in trade. Please separate out your conversation. "
                                   "Create a new post if the current post is not related to your trade.",
    CONSTANTS.ALREADY_PROCESSED: "This comment has already been processed and given Karma.",
}


# Replies from dictionary
def dictionary_response(index, comment):
    try:
        comment_body = response_dictionary[index]
    except KeyError:
        comment_body = "Error: Please notify the mods of the subreddit."
    reply(comment, comment_body)


# Replies to comment with text=body
def reply(comment_or_submission, body):
    response = body + "\n\n ^(This action was performed by a bot, please contact the mods for any questions.)"
    response = response + " ^(If you receive this more than once please ignore the comment.)"
    comment_or_submission.reply(response)


# Give the parent comment karma
def karma_rewarded_comment(comment):
    p_comment = comment.parent()
    # Replies with comment
    comment_body = "Hi " + comment.author.name + "! You have successfully rewarded "
    comment_body = comment_body + p_comment.author.name + " one karma point! "
    comment_body = comment_body + "Please note that karma may take sometime to update."
    reply(comment, comment_body)


# Failed to give parent comment karma
def karma_rewarded_failed(comment):
    p_comment = comment.parent()
    # Replies with comment
    comment_body = "Hi " + comment.author.name + "! You can only give karma to others under a trading post i.e "
    comment_body = comment_body + "submission with PS4, XB1 or PC flair. Please refer to wiki page for more information."
    reply(comment, comment_body)


# Subtract parent comment karma
def karma_subtract_comment(comment):
    p_comment = comment.parent()
    # Replies with comment
    comment_body = p_comment.author.name + " karma has been decremented by one. "
    comment_body = comment_body + "Please note that karma may take sometime to update."
    reply(comment, comment_body)


# Subtract parent comment karma failed
def karma_subtract_failed(comment):
    comment_body = "Karma can only be subtracted by mods only. Please contact mods if you have been scammed."
    reply(comment, comment_body)


# Close the submission comment
def close_submission_comment(submission):
    comment_body = "The submission has been closed and comments have been locked. "
    comment_body = comment_body + "Please contact mods, if you want to open the submission."
    reply(submission, comment_body)


# Submission closed failed
def close_submission_failed(comment, is_trading_post):
    comment_body = "Error: Please Contact Mods"
    if is_trading_post:
        comment_body = "The submission can only be close by OP or the mods. Please report post if it is breaking rules."
    else:
        comment_body = "This type of submission cannot be closed. Please refer to wiki page for more information."
    reply(comment, comment_body)


# comments the blacklist search result
def comment_blacklist_search_result(username, blacklist, comment_or_submission):
    response_text = "Error! Please message mods!"
    if len(blacklist) > 0:
        response_text = "The user " + username + " has been found on blacklist " + str(len(blacklist))
        response_text = response_text + " time(s). The links for each time when the user appeared in blacklist are:\n\n"
        for item in blacklist:
            response_text = response_text + item.get('shortUrl') + "\n\n"
        response_text = response_text + "If \"-all\" is used then the results maybe false positive. Please check " \
                                        "each link to verify. "
    else:
        response_text = "The user " + username + " is not in the blacklist. "
        response_text = response_text + "However, this doesn\'t guarantee that the user is in clear. "
        response_text = response_text + "Please refer the the user\'s previous posts in Fallout76 subreddits. "
        response_text = response_text + "If the account is completely new, avoid doing big trades without using a " \
                                        "verified courier. "
    reply(comment_or_submission, response_text)
