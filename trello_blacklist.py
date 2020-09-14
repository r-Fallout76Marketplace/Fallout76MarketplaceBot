from trello import TrelloApi

import CONFIG


def get_lists_ids(old_list):
    new_list = list()
    for element in old_list:
        new_list.append(element.get('id'))
    return new_list


# searches the key in p_list and returns exact result
def search_in_platform_list(key, p_list):
    # Searches each card in list
    for card in p_list:
        # Splits the description
        desc_list = (card.get('desc').upper()).split("\n")
        # Compare each line in description
        for line in desc_list:
            # Skip empty and comment lines
            if ":" not in line:
                continue
            if key == line[line.index(":") + len(":"):].strip():
                return card
    return None


# searches the key in p_list and returns all possible results
def rough_search_in_platform_list(key, p_list):
    result_list = list()
    # Searches each card in list
    for card in p_list:
        # Splits the description
        desc_list = (card.get('desc').upper()).split("\n")
        # Compare each line in description
        for line in desc_list:
            # Skip empty and comment lines
            if ":" not in line:
                continue
            # If line contains key
            if key in line:
                result_list.append(card)
                break
    return result_list


# Class Trello
# Stores all the information from Market76Blacklist Board
# Also checks if a users is on blacklist
class TrelloBlacklist:
    def __init__(self):
        # Set-up board api settings
        self.trello = TrelloApi(CONFIG.TRELLO_APP_KEY)
        self.market76_blacklist = self.trello.boards.get(CONFIG.MARKET76_BLACKLIST_BOARD_ID)
        self.fallout76_marketplace_blacklist = self.trello.boards.get(CONFIG.FALLOUT76_MARKETPLACE_BOARD_ID)
        # declaring lists
        self.PC_list = list()
        self.XBOX_list = list()
        self.PS_list = list()
        self.refresh_blacklist()

    # Get all cards from list in trello
    def get_cards(self, list_ids):
        self.PC_list = self.PC_list + self.trello.lists.get_card(list_ids[0])
        self.XBOX_list = self.XBOX_list + self.trello.lists.get_card(list_ids[1])
        self.PS_list = self.PS_list + self.trello.lists.get_card(list_ids[2])

    # Do a precise search in the trello board
    def search_in_blacklist(self, search_query):
        # If search query is empty
        if len(search_query) <= 0:
            return list()
        self.refresh_blacklist()
        black_list_result = list()
        # Searches in all platforms
        black_list_result.append(search_in_platform_list(search_query, self.PS_list))
        black_list_result.append(search_in_platform_list(search_query, self.XBOX_list))
        black_list_result.append(search_in_platform_list(search_query, self.PC_list))
        # Removes if list contains None
        black_list_result = list(filter(None, black_list_result))
        return black_list_result

    # Do a rough search in trello and return all possible results
    def rough_search_in_blacklist(self, search_query):
        # If search query is empty
        if len(search_query) <= 0:
            return list()
        self.refresh_blacklist()
        black_list_result = list()
        # Searches in all platforms
        black_list_result = black_list_result + rough_search_in_platform_list(search_query, self.PS_list)
        black_list_result = black_list_result + rough_search_in_platform_list(search_query, self.XBOX_list)
        black_list_result = black_list_result + rough_search_in_platform_list(search_query, self.PC_list)
        return black_list_result

    # Refresh the content captured from trello board
    def refresh_blacklist(self):
        # Emptying all lists
        self.PC_list.clear()
        self.XBOX_list.clear()
        self.PS_list.clear()
        # Get all lists content from Market76
        market76_all_lists = self.trello.boards.get_list(CONFIG.MARKET76_BLACKLIST_BOARD_ID)
        list_ids = get_lists_ids(market76_all_lists)
        self.get_cards(list_ids)
        # Get all lists content from Fallout76 Marketplace
        fallout76_marketplace_all_lists = self.trello.boards.get_list(CONFIG.FALLOUT76_MARKETPLACE_BOARD_ID)
        list_ids = get_lists_ids(fallout76_marketplace_all_lists)
        self.get_cards(list_ids)
