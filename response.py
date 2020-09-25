# Replies to comment with text=body
def reply(comment_or_submission, body):
    response = body + "\n\n ^(This action was performed by a bot, please contact the mods for any questions.)"
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
    # Replies with comment
    comment_body = "Hi " + comment.author.name + "! You can only give karma to others under a trading post i.e "
    comment_body = comment_body + "submission with PS4, XB1 or PC flair. Please refer to wiki page for more information."
    reply(comment, comment_body)


# If the users is already awarded in a submission
def already_rewarded_comment(comment, awardee_awarder_obj):
    comment_body = "Hi " + comment.author.name + "! You have already rewarded " + comment.parent().author.name
    comment_body = comment_body + " in this submission [here](" + awardee_awarder_obj.comment.permalink + ")"
    reply(comment, comment_body)


# Cannot award yourself
def cannot_reward_yourself_comment(comment):
    comment_body = "Hi " + comment.author.name + "! You cannot reward yourself karma."
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
def close_submission_comment(submission, time_expired):
    comment_body = "The submission has been closed and comments have been locked. "
    if time_expired:
        comment_body = comment_body + "**All trading submission gets locked automatically after 3 days.** "
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
def comment_blacklist_search_result(keyword, blacklist, comment_or_submission):
    response_text = "Error! Please message mods!"
    if len(blacklist) > 0:
        response_text = "The user *" + keyword + "* has been found on blacklist " + str(len(blacklist)) + " "
        response_text = response_text + "time(s). The links for each time when the user appeared in blacklist are:\n\n "
        for item in blacklist:
            # Url of card/s
            response_text = response_text + "[" + item.labels[
                0].name + ": " + item.name + "](" + item.short_url + ")\n\n"
            # Checks the description for offense and add them to comment
            desc_list = item.desc.split("\n\n")
            match = [element for element in desc_list if "offense" in element.lower()]
            for element in match:
                response_text += element + "\n\n"
        response_text = response_text + "^(Please check each link to verify.)"
    else:
        response_text = "The bot has performed a search and has determined that the user *\"" + keyword + "\"* is not "
        response_text = response_text + "in present in our blacklist.\n\n^(Please take precautions if the user account "
        response_text = response_text + "is very new, has low trade karma or actively delete submissions/comments. "
        response_text = response_text + " You may also check their gamertag using the bot commands (see Automod pinned comment). "
        response_text = response_text + "^(If you are doing a high value trade, consider using an official courier. "
        response_text = response_text + "You can find links to all couriers in the subreddit wiki or sidebar.)"
    reply(comment_or_submission, response_text)
