import re

import CONFIG
import response

import trello


# To extract the text from curly brackets
def extract_frm_curly_brackets(input_text):
    # Check for the curly braces
    regex_extract = re.search(r"\{(.*)?\}", input_text)
    if regex_extract is not None:
        return regex_extract.group(1)
    return None


# Checks the blacklist for keywords that appear in comment
# or checks for the author of comment
def check_comment_in_blacklist(comment, is_explicit_call):
    output = extract_frm_curly_brackets(comment.body_html)
    search_requested = True
    # If there are no curly braces
    if output is not None:
        # Checks for the word enclosed in brackets if any
        search_in_blacklist(output, search_requested, is_explicit_call, comment)
    search_requested = False
    # checks for the author of the comment
    search_in_blacklist(comment.author.name, search_requested, is_explicit_call, comment)


# Check for the author of submission in blacklist
def check_submission_in_blacklist(submission):
    search_requested = False
    is_explicit_call = False
    # Explicit calls cannot be made in submissions
    search_in_blacklist(submission.author.name, search_requested, is_explicit_call, submission)


# Removes the archived cards from list
def delete_archived_cards_and_check_desc(search_result, search_query):
    for card in search_result:
        if card.__class__ != trello.Card:
            search_result.remove(card)
            continue
        if card.closed:
            search_result.remove(card)
        # Double check to make sure that search query is in card description
        if search_query.lower() not in card.description.lower():
            search_result.remove(card)
    return search_result


# Searches in trello board using trello api
def search_in_blacklist(search_query, search_requested, is_explicit_call, comment_or_submission):
    search_result = list()
    try:
        # escapes the special characters so the search result is exact not from wildcard
        search_result = CONFIG.trello_client.search(query=re.escape(search_query), cards_limit=10)
        search_result = delete_archived_cards_and_check_desc(search_result, search_query)
    except NotImplementedError:
        raise NotImplementedError(search_query)

    # If nothing is returned by search result
    if len(search_result) == 0:
        # If search is requested only then the response is required
        if search_requested:
            response.comment_blacklist_search_result(search_query, search_result, is_explicit_call,
                                                     comment_or_submission)
    # If search result returns something
    else:
        response.comment_blacklist_search_result(search_query, search_result, is_explicit_call, comment_or_submission)
