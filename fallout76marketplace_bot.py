import traceback

import praw
import prawcore
import schedule

import time

import CONFIG
import marketplace_database

# Only works in the subreddit mentioned in CONFIG
subreddit = CONFIG.reddit.subreddit(CONFIG.subreddit_name)

# Gets 100 historical comments
comment_stream = subreddit.stream.comments(pause_after=-1, skip_existing=True)
# Gets 100 historical submission
submission_stream = subreddit.stream.submissions(pause_after=-1, skip_existing=True)
# inbox stream
inbox_stream = praw.models.util.stream_generator(CONFIG.reddit.inbox.mentions, pause_after=-1, skip_existing=True)

# Creating Marketplace Database object
database = marketplace_database.MarketplaceDatabase()

# Read database file
try:
    awarder_db_file = open("awarder_db.txt", "r+")
except IOError:
    awarder_db_file = open("awarder_db.txt", "w+")
lines = awarder_db_file.readlines()
database.import_data(lines)


def refresh_memory():
    print("Deleting old items " + time.ctime())
    try:
        marketplace_database.delete_old_saved_items(database)
        database.export_to_txt(awarder_db_file)
    except Exception:
        tb = traceback.format_exc()
        CONFIG.reddit.redditor("is_fake_Account").message(CONFIG.subreddit_name, tb,
                                                          from_subreddit=CONFIG.subreddit_name)
        print(tb)


schedule.every(5).hours.do(refresh_memory)
print("The bot has started running...")

# Boolean variable to make sure error message is sent only once
message_sent = False

while True:
    message_sent = False
    # Try catch to make sure bot doesn't go down during Error 503
    try:
        schedule.run_pending()
        # Gets comments and if it receives None, it switches to posts
        for comment in comment_stream:
            if comment is None:
                break
            marketplace_database.load_comment(comment, database, False)

        # Gets posts and if it receives None, it switches to mentions
        for submission in submission_stream:
            if submission is None:
                break
            marketplace_database.load_submission(submission)

        # Gets mentions and if it receives None, it switches to comments
        for mentions in inbox_stream:
            if mentions is None:
                break
            marketplace_database.load_comment(mentions, database, True)
    except Exception:
        # Sends a message to mods in case of error
        if not message_sent:
            tb = traceback.format_exc()
            try:
                CONFIG.reddit.redditor("is_fake_Account").message(CONFIG.subreddit_name, tb,
                                                              from_subreddit=CONFIG.subreddit_name)
            except prawcore.ServerError:
                pass
            print(tb)
            message_sent = True
