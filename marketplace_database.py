import re
import time

import praw

import CONFIG
import CONSTANTS
import awardeeawarder
import karma_system
import response
import trello_blacklist


# Checks if the author is mod
def is_mod(author):
    moderators_list = CONFIG.reddit.subreddit(CONFIG.subreddit_name).moderator()
    for moderator in moderators_list:
        if author == moderator:
            return True
    return False


def load_comment(comment, database):
    # Ignore all Auto moderator comments
    if comment.author.name == "AutoModerator":
        return None
    # Checks in blacklist for both curly brackets keyword and author of comment
    trello_blacklist.check_comment_in_blacklist(comment)
    # Process the commands in comment, such as karma++ or !close
    karma_system.process_commands(comment, is_mod(comment.author), database)


def load_submission(submission):
    regex = re.compile('XB1|PS4|PC', re.IGNORECASE)
    submission_flair_text = submission.link_flair_text
    match = re.match(regex, str(submission_flair_text))
    # If No match found match is None
    if match is not None:
        trello_blacklist.check_submission_in_blacklist(submission)
        # save submission so it can be closed after 3 days
        submission.save()


# delete locked items
def delete_old_saved_items(database):
    saved_list = CONFIG.reddit.redditor(CONFIG.username).saved(limit=None)
    for saved in saved_list:
        if type(saved) == praw.models.Submission:
            # If submission is locked, delete it
            if saved.locked:
                saved.unsave()
            else:
                # If submission is 3 old, lock and delete it
                now = time.time()
                age = now - saved.created_utc
                if age >= 259200:
                    saved.mod.lock()
                    saved.flair.select(CONSTANTS.TRADE_ENDED_ID)
                    response.close_submission_comment(saved, time_expired=True)
                    saved.unsave()
    # Delete all comments with locked submission
    for item in database.awarder_list:
        if CONFIG.reddit.submission(id=item.submission.id).locked:
            database.awarder_list.remove(item)


class MarketplaceDatabase:
    def __init__(self):
        # Keeps record awarders and awardee
        self.awarder_list = list()

    def search(self, comment):
        # Creates object from comment
        obj_awardee_awarder = awardeeawarder.AwardeeAwarder(comment)
        # If name is between a and m
        if ord(obj_awardee_awarder.awarder.name[0]) in range(ord('A'), ord('N')):
            # compares to each object in list from start
            for awardee_awarder_list_obj in self.awarder_list:
                if awardee_awarder_list_obj.__cmp__(obj_awardee_awarder):
                    return awardee_awarder_list_obj
        else:
            # compares to each object in list from end
            for awardee_awarder_list_obj in reversed(self.awarder_list):
                if awardee_awarder_list_obj.__cmp__(obj_awardee_awarder):
                    return awardee_awarder_list_obj
        # If the object is not found in the list
        self.awarder_list.append(obj_awardee_awarder)
        self.awarder_list.sort(key=lambda awardee_awarder_l: awardee_awarder_l.awarder.name, reverse=True)
        return None