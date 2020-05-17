import CONFIG
import CONSTANTS
import conversation
import response
import trade
import trades_database

# Only works in the subreddit mentioned in CONFIG
subreddit = CONFIG.reddit.subreddit(CONFIG.subreddit_name)

# Looks for this word
plus_karma = "+Karma".capitalize()
minus_karma = "-Karma"

# Create instance of trades database
trades_database_object = trades_database.TradesDatabase()

# Looks for comment in comments stream
for comment in subreddit.stream.comments():
    # Makes the comment body uppercase so we don't have to worry about case sensitivity
    comment_body = comment.body.capitalize()
    # If comment is +Karma
    if plus_karma in comment_body:
        # Creates object of class Conversation and Loads all the comments
        conversation_object = conversation.Conversation(comment)
        # Performs necessary checks
        result = conversation_object.check_passed(comment)

        has_occurred = False
        if result == CONSTANTS.PASSED:
            # Checks if trade has already happened
            # The check needs to be done to make sure we don't have wrong data, otherwise comparison fails
            has_occurred = trades_database_object.has_occurred(conversation_object)

        if result == CONSTANTS.PASSED and not has_occurred:
            # If everything passes
            response.check_passed(comment)
            # Stores trade in database
            tradeObject = trade.Trade(conversation_object)
            trades_database_object.add_trade(tradeObject)
        else:
            # If checks fails
            if has_occurred:
                result = CONSTANTS.TRADE_ALREADY_OCCURRED
            response.check_failed(result, comment)
    # If comment is -Karma
    elif minus_karma in comment_body:
        print("TO:DO")

    trades_database_object.export_trades()
