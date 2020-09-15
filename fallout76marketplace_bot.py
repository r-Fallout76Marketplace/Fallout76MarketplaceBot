import schedule
import traceback

import CONFIG
from marketplace_database import MarketplaceDatabase
from trello_blacklist import TrelloBlacklist

# Only works in the subreddit mentioned in CONFIG
subreddit = CONFIG.reddit.subreddit(CONFIG.subreddit_name)

# Gets 100 historical comments
comment_stream = subreddit.stream.comments(pause_after=-1, skip_existing=True)
# Gets 100 historical submission
submission_stream = subreddit.stream.submissions(pause_after=-1, skip_existing=True)

# Creating Trello Blacklist object
blacklist = TrelloBlacklist()
# Creating Marketplace Database object
database = MarketplaceDatabase(blacklist)


def refresh_memory():
    print("Refresh")
    database.delete_old_saved_items()


schedule.every(1).days.do(refresh_memory)

print("The bot has started running...")

while True:
    schedule.run_pending()
    # Gets comments and if it receives None, it switches to posts
    for comment in comment_stream:
        if comment is None:
            break
        try: 
            database.load_comment(comment)
        except Exception:
            # Sends a message to mods in case of error
            tb = traceback.format_exc()
            CONFIG.reddit.redditor("is_fake_Account").message(CONFIG.subreddit_name, tb, from_subreddit=CONFIG.subreddit_name)
            print(tb)
            
    # Gets posts and if it receives None, it switches to comments
    for submission in submission_stream:
        if submission is None:
            break
        try:
            database.load_submission(submission)
        except Exception:
            # Sends a message to mods in case of error
            tb = traceback.format_exc()
            CONFIG.reddit.redditor("is_fake_Account").message(CONFIG.subreddit_name, tb, from_subreddit=CONFIG.subreddit_name)
            print(tb)

print("The bot has stopped...")