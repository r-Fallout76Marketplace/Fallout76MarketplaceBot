import re

import CONFIG
import CONSTANTS
import conversation_check
import response


# Checks if submission is eligible for trading
# Checks that need to be passed are
# Submission must have right flair and trade should not be closed
def submission_flair_checks(comment):
    regex = re.compile('XB1|PS4|PC', re.IGNORECASE)
    submission = comment.submission
    submission_flair_text = submission.link_flair_text
    match = re.match(regex, str(submission_flair_text))
    # If No match found match is None
    if match is None:
        return False
    else:
        return True


# Increments karma by 1
def increment_karma(comment):
    p_comment = comment.parent()
    author_name = p_comment.author.name
    # if the author has no flair
    if p_comment.author_flair_css_class == '' or p_comment.author_flair_css_class is None:
        # sets the flair to one
        CONFIG.reddit.subreddit(CONFIG.subreddit_name).flair.set(author_name, text='Karma: 1',
                                                                 flair_template_id=CONSTANTS.KARMA_ID)
    else:
        # Getting the flair and adding the value
        user_flair = p_comment.author_flair_text
        # Splits Karma into two
        user_flair_split = user_flair.split()
        # Increments the int part
        user_flair_split[-1] = int(user_flair_split[-1])
        user_flair_split[-1] += 1
        # Combines back string and int part
        user_flair = ' '.join(map(str, user_flair_split))

        # Updates the user flair
        CONFIG.reddit.subreddit(CONFIG.subreddit_name).flair.set(author_name, text=str(user_flair),
                                                                 flair_template_id=CONSTANTS.KARMA_ID)


# Decrements karma by 1
def decrement_karma(comment):
    p_comment = comment.parent()
    author_name = p_comment.author.name
    # if the author has no flair
    if p_comment.author_flair_css_class == '' or p_comment.author_flair_css_class is None:
        # sets the flair to one
        CONFIG.reddit.subreddit(CONFIG.subreddit_name).flair.set(author_name, text='Karma: -1',
                                                                 flair_template_id=CONSTANTS.KARMA_ID)
    else:
        # Getting the flair and adding the value
        user_flair = p_comment.author_flair_text
        # Splits Karma into two
        user_flair_split = user_flair.split()
        # Increments the int part
        user_flair_split[-1] = int(user_flair_split[-1])
        user_flair_split[-1] -= 1
        # Combines back string and int part
        user_flair = ' '.join(map(str, user_flair_split))

        # Updates the user flair
        CONFIG.reddit.subreddit(CONFIG.subreddit_name).flair.set(author_name, text=str(user_flair),
                                                                 flair_template_id=CONSTANTS.KARMA_ID)


# Changes the flair to Trade Closed and locks submission
def close_post_trade(comment):
    submission = comment.submission
    submission.flair.select(CONSTANTS.TRADE_ENDED_ID)
    submission.mod.lock()


# Processes the comment body and determines what action to take
# In case of 'Karma++' more checks needs to be performed
# For !CLOSE_TRADE only thing we need to check if author is OP
def process_commands(comment, is_mod):
    if not is_mod:
        # If comment says Karma++
        if CONSTANTS.KARMA_PP in comment.body.upper():
            # You can close trading posts only
            if submission_flair_checks(comment):
                # If parent is already saved meaning we already processed the comment
                if comment.parent().saved:
                    response.dictionary_response(CONSTANTS.ALREADY_PROCESSED, comment)
                    return None
                comments_thread_obj = conversation_check.CommentsThread(comment)
                # Returns the output of checks
                output = comments_thread_obj.checks_output()
                # If all checks pass saves the parent comment of the comment
                if output == CONSTANTS.REWARD_PLUS_KARMA:
                    comment.parent().save()
                    increment_karma(comment)
                    response.karma_rewarded_comment(comment)
                else:
                    response.dictionary_response(output, comment)
            else:
                response.karma_rewarded_failed(comment)

        # If comment says Karma--
        elif CONSTANTS.KARMA_MM in comment.body.upper():
            response.karma_subtract_failed(comment)

        # Close submission
        elif CONSTANTS.CLOSE in comment.body.upper():
            # Only OP can close the trade
            if comment.author == comment.submission.author:
                # You can close trading posts only
                if submission_flair_checks(comment):
                    close_post_trade(comment)
                    response.close_submission_comment(comment.submission)
                else:
                    # If post isn't trading post
                    response.close_submission_failed(comment, False)
            else:
                # If the close submission is requested by someone other than op
                response.close_submission_failed(comment, True)
    else:
        # Mods commands will be executed without checks
        # Increase Karma
        if CONSTANTS.KARMA_PP in comment.body.upper():
            increment_karma(comment)
            response.karma_rewarded_comment(comment)
        # Decrease Karma
        elif CONSTANTS.KARMA_MM in comment.body.upper():
            decrement_karma(comment)
            response.karma_subtract_comment(comment)
        # Close Submission
        elif CONSTANTS.CLOSE in comment.body.upper():
            close_post_trade(comment)
            response.close_submission_comment(comment.submission)
