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
    new_comment = comment_or_submission.reply(response)
    new_comment.mod.distinguish(how="yes")


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
        response_text = "The user *" + username.lower() + "* has been found on blacklist " + str(len(blacklist))
        response_text = response_text + " time(s). The links for each time when the user appeared in blacklist are:\n\n"
        for item in blacklist:
            response_text = response_text + item.get('shortUrl') + "\n\n"
        response_text = response_text + "If \"-all\" is used then the results maybe false positive. Please check " \
                                        "each link to verify. "
    else:
        response_text = "The bot has performed a preliminary search and has determined that the user *\"" + username.lower() + "\"* is not "
        response_text = response_text + "in present in Market76 or our blacklist.\n\n^(Please take precautions if the user account is "
        response_text = response_text + "very new or has low trade karma. You may also check their gamertag using the bot command "
        response_text = response_text + "(See example in Automoderator comment\).) "
        response_text = response_text + "^(If you are doing a high value trade, consider using an official courier. You can find links "
        response_text = response_text + "to all couriers in the subreddit wiki or sidebar.)"
    reply(comment_or_submission, response_text)
