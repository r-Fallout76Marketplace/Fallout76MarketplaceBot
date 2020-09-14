
# Fallout 76 Marketplace Bot
This is a reddit bot for [r/Fallout76Marketplace](https://www.reddit.com/r/Fallout76Marketplace/). The bot implements the subreddit own karma system, which is recorded in the flair of each user. The bot also actively and on request checks usernames or gamertag on [Market76](https://trello.com/b/0eCDKYHr/market76-blacklist) and [Fallout76Marketplace](https://trello.com/b/ZzWVOSNd/fallout76marketplace-trading-blacklist) blacklist on trello.

### Features: 
- Karma System
- Blacklist searching
### How to use the bot
In order to run the bot, you need to create CONFIG.py using the template given below
```
import praw  
  
# Login information  
username = ''  
password = ''  
  
# API information  
client_id = ''  
client_secret = ''  
user_agent = ''  
  
# Trello API INFO  
TRELLO_APP_KEY = ''  
MARKET76_BLACKLIST_BOARD_ID = ''  
FALLOUT76_MARKETPLACE_BOARD_ID = ''  
  
# Put the name of your subreddit here  
subreddit_name = ""  
  
# Login Api  
reddit = praw.Reddit(client_id=client_id,  
  client_secret=client_secret,  
  username=username,  
  password=password,  
  user_agent=user_agent)
```
After adding the config file, make sure that the flair IDs in CONSTANTS.py are correct and updated.

*For more questions, contact the mods of r/Fallout76Marketplace*