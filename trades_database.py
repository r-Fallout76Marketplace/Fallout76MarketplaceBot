import sqlite3


# Class TradesDatabase
# Keeps record of previous Trades for record keeping


class TradesDatabase:

    # Constructor
    def __init__(self):
        self.trades = []
        self.conn = sqlite3.connect('trades.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE trades (
                                from text
                                to text
                                post_url text
                                  """)

    # Checks if trade has already occurred
    # Compares submission url and user name of both parties
    def has_occurred(self, conversation_object):
        submission_link = conversation_object.comments[0].submission.url
        from_user = conversation_object.comments[0].author
        to_user = conversation_object.comments[1].author

        # Loops though each negotiation to verify
        for trade in self.trades:
            if trade.from_user == from_user and trade.to_user == to_user:
                if trade.submission_link == submission_link:
                    return True
            return False

    # Adds successful trade to  trades database
    def add_trade(self, trade_object):
        self.trades.append(trade_object)
        pass

    def export_trades(self):
        # TO:DO
        pass
