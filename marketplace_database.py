import re
import praw
import time

import CONFIG
import CONSTANTS
import karma_system
import response


# To extract the text from curly brackets
def extract_frm_curly_brackets(input_text):
    # Check for the curly braces
    regex_extract = re.search(r"\{(.*)?\}", input_text)
    if regex_extract is not None:
        return regex_extract.group(1).upper()
    return None


# Checks if the post have correct flair
def is_correct_flair(submission):
    if submission.link_flair_template_id == CONSTANTS.PS_ID:
        return True
    elif submission.link_flair_template_id == CONSTANTS.XBOX_ID:
        return True
    elif submission.link_flair_template_id == CONSTANTS.PC_ID:
        return True
    else:
        return False


class MarketplaceDatabase:
    def __init__(self, blacklist):
        self.blacklist = blacklist
        self.reddit = CONFIG.reddit

    # Loads the whole conversation thread from a comment and performs checks
    def load_comment(self, comment):
        # Ignore all Auto moderator comments
        if comment.author.name == "AutoModerator":
            return None
        # blacklist from searching comment text
        blacklist_comment = self.check_comment_in_blacklist(comment)
        output = extract_frm_curly_brackets(comment.body)
        if output is not None:
            response.comment_blacklist_search_result(output, blacklist_comment, comment)

        # blacklist from searching authors name
        if not self.is_mod(comment.author):
            blacklist_author = self.check_author_in_blacklist(comment)
            if len(blacklist_author) > 0:
                response.comment_blacklist_search_result(comment.author.name, blacklist_author, comment)
        # Process the commands in comment, such as karma++ or !close
        karma_system.process_commands(comment, self.is_mod(comment.author))

    # Checks if the user is in blacklist
    def load_submission(self, submission):
        if not self.is_mod(submission.author):
            blacklist = self.check_author_in_blacklist(submission)
            response.comment_blacklist_search_result(submission.author.name, blacklist, submission)
        regex = re.compile('XB1|PS4|PC', re.IGNORECASE)
        submission_flair_text = submission.link_flair_text
        match = re.match(regex, submission_flair_text)
        # If No match found match is None
        if match is not None:
            submission.save()

    # Checks the blacklist for keywords that appear in comment
    def check_comment_in_blacklist(self, comment):
        blacklist_result = list()
        output = extract_frm_curly_brackets(comment.body)
        # If there are no curly braces
        if output is not None:
            # -all indicates to do a rough search
            if "-all" in comment.body:
                blacklist_result = self.blacklist.rough_search_in_blacklist(output)
            else:
                # This is to do exact search
                blacklist_result = blacklist_result + self.blacklist.search_in_blacklist(output)
        return blacklist_result

    # Check for the author of comment or submission in blacklist
    def check_author_in_blacklist(self, comment_or_submission):
        # searches the username of the author
        blacklist_result = self.blacklist.search_in_blacklist(('u/' + comment_or_submission.author.name).upper())
        return blacklist_result

    def is_mod(self, author):
        moderators_list = self.reddit.subreddit(CONFIG.subreddit_name).moderator()
        for moderator in moderators_list:
            if author == moderator:
                return True
        return False

    def delete_old_saved_items(self):
        saved_list = self.reddit.redditor(CONFIG.username).saved(limit=None)
        for saved in saved_list:
            if type(saved) == praw.models.Submission:
                # If submission is locked, delete it
                if saved.locked:
                    saved.unsave()
                else:
                    # If submission is week old, lock and delete it
                    now = time.time()
                    age = now - saved.created_utc
                    if age >= 604800:
                        saved.locked()
                        response.close_submission_comment(saved)
                        saved.unsave()

