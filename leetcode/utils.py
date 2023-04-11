from gql import gql


def load_query(path):
    with open(path) as f:
        return gql(f.read())


# TODO Modify reading https://plainenglish.io/blog/graphql-queries-in-python-f658b74f29e9
