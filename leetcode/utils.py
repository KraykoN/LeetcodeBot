from itertools import dropwhile

from gql import gql


def load_query(path):
    with open(path) as f:
        return gql(f.read())


def is_comment(s):
    """function to check if a line
    starts with some character.
    Here # for comment
    """
    # return true if a line starts with #
    return s.startswith("#")


# TODO Put example of output query to .gql file
# https://stackoverflow.com/questions/1706198/python-how-to-ignore-comment-lines-when-reading-in-a-file
# TODO Modify reading https://plainenglish.io/blog/graphql-queries-in-python-f658b74f29e9
