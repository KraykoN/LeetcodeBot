import datetime
from typing import Dict, List, NamedTuple

import gql
import requests
from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from utils import load_query


class UserProgress(
    NamedTuple(
        "UserProgress", [("username", str), ("difficulty_counts", Dict[str, int])]
    )
):
    """
    A named tuple representing a user's progress on LeetCode problems.

    Attributes:
        username (str): The user's LeetCode login.
        difficulty_counts (dict): A dictionary containing the number of problems
            solved at each difficulty level (Easy, Medium, Hard).
    """


class Problem(
    NamedTuple(
        "Problem",
        [
            ("question_id", str),
            ("total_accepted_solutions", int),
            ("total_submitted_solutions", int),
            ("title", str),
            ("level_num", str),
            ("url", str),
            ("has_video", bool),
        ],
    )
):
    # TODO Make docstring
    """_summary_

    Args:
        namedtuple (_type_): _description_
    """


class NewsItem(
    NamedTuple(
        "NewsItem",
        [
            ("id", str),
            ("title", str),
            ("comment_count", int),
            ("view_count", int),
            ("pinned", bool),
            ("date", datetime.datetime),
            ("username", str),
        ],
    )
):
    # TODO Make docstring
    """_summary_

    Args:
        namedtuple (_type_): _description_
    """


def get_user_progress(leetcode_login: str) -> UserProgress:
    """
    This function gets the user progress of given leetcode login from leetcode GraphQL API.

    Args:
        leetcode_login (str): Leetcode login for the user.

    Returns:
        UserProgress: A named tuple containing the username and difficulty counts.
    """

    # Load the user progress query from gql_scripts directory.
    USER_PROGRESS_QUERY = load_query("leetcode/gql_scripts/get_user_progress.gql")

    # Set the parameter for the query
    params = {"leetcode_login": leetcode_login}

    # Set the endpoint for the GraphQL API
    LEETCODE_GRAPHQL_ENDPOINT = "https://leetcode.com/graphql"

    # Create a transport object for making requests to the GraphQL API
    transport = RequestsHTTPTransport(url=LEETCODE_GRAPHQL_ENDPOINT)

    # Instantiate a client using the transport object for executing the query
    with Client(transport=transport, fetch_schema_from_transport=False) as client:
        # Execute the query with the provided parameters
        try:
            result = client.execute(USER_PROGRESS_QUERY, variable_values=params)
        except gql.transport.exceptions.TransportQueryError as e:
            print(f"Error executing query: {e}")
            return UserProgress(username="", difficulty_counts={})

        # Create a dictionary of difficulty counts for each problem
        difficulty_counts = {
            item["difficulty"]: item["count"]
            for item in result["matchedUser"]["submitStats"]["acSubmissionNum"]
        }

        # Return a named tuple of user's name and progress by problem levels
        return UserProgress(result["matchedUser"]["username"], difficulty_counts)


def get_new_problems(
    top_n_problems: int, paid_only: bool, level_num: int
) -> List[Problem]:
    """
    This function returns the top n new problems based on paid status and difficulty level.

    Args:
        top_n_problems (int): The number of new problems to return.
        paid_only (bool): Whether to include only paid problems.
        level_num (int): The difficulty level of the problems to include.

    Returns:
        list: A list of Problem objects.
    """

    # API endpoint for LeetCode problems
    url = "https://leetcode.com/api/problems/all/"

    try:
        # Send GET request to API endpoint and raise an exception if there's an error
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        # If there's an exception, print the error message and return an empty list
        print(f"Error: {e}")
        return []

    # Create an empty list to hold the new problems
    new_problems = []

    # Loop through each problem in the response
    for problem in response.json()["stat_status_pairs"]:
        # Check if the problem meets the criteria based on paid status and difficulty level
        if (
            problem["paid_only"] is paid_only
            and problem["difficulty"]["level"] is level_num
        ):
            # If the problem meets the criteria, create a new Problem object and add it to the list
            new_problems.append(
                Problem(
                    question_id=problem["stat"]["question_id"],
                    total_accepted_solutions=problem["stat"]["total_acs"],
                    total_submitted_solutions=problem["stat"]["total_submitted"],
                    title=problem["stat"]["question__title"],
                    level_num=problem["difficulty"]["level"],
                    url=f"https://leetcode.com/problems/{problem['stat']['question__title_slug']}/",
                    has_video=problem["stat"]["question__article__has_video_solution"],
                )
            )

        # Check if the desired number of new problems have been found
        if len(new_problems) == top_n_problems:
            # If the desired number have been found, break out of the loop
            break

    # Return the list of new problems
    return new_problems


def get_latest_news(theme: str, num_top_news: int) -> List[NewsItem]:
    """_summary_

    Args:
        theme (str): A string representing the category of news to retrieve.
        num_top_news (int): An integer representing the number of top news to retrieve.

    Returns:
        list: A list of namedtuples representing the latest news.
    """
    # TODO Best practice for check datatype in input params

    # if not isinstance(theme, str):
    #     raise TypeError("theme must be a string")
    # if not isinstance(num_top_news, int) or num_top_news <= 0:
    #     raise ValueError("num_top_news must be a positive integer")

    query = load_query("leetcode/gql_scripts/get_news.gql")

    params = {
        "orderBy": "hot",
        "query": "",
        "skip": 0,
        "first": num_top_news,
        "tags": [],
        "categories": [f"{theme}"],
    }

    GRAPHQL_URL = "https://leetcode.com/graphql"
    transport = RequestsHTTPTransport(url=GRAPHQL_URL)
    client = Client(transport=transport, fetch_schema_from_transport=False)

    try:
        result = client.execute(query, variable_values=params)
    except gql.transport.exceptions.TransportQueryError as e:
        raise RuntimeError(f"Error executing query: {e}") from e

    # TODO  Best Practice for except raise
    # except GraphQLError as e:
    #     raise RuntimeError(f"GraphQL error: {e}") from e

    # Convert the list comprehension to use namedtuples and datetime.fromtimestamp()
    news_list = [
        NewsItem(
            id=int(news["id"]),
            title=news["title"],
            comment_count=news["commentCount"],
            view_count=news["viewCount"],
            pinned=news["pinned"],
            date=datetime.datetime.fromtimestamp(news["post"]["creationDate"]),
            username=news["post"]["author"]["username"],
        )
        for news in (edge["node"] for edge in result["categoryTopicList"]["edges"])
    ]

    return news_list


# def get_available_contests(current_date?)

# def get_tasks_of_contset(contest_name)

# def get_user's_solved_tasks_in_details(username)

# def get_task_in_details(task_num)

if __name__ == "__main__":
    # print(get_user_progress(leetcode_login="krayko13"))
    # print(get_user_progress(leetcode_login="krayko1366"))
    # print(get_user_progress(leetcode_login=""))
    # {'krayko13': {'All': 12, 'Easy': 8, 'Medium': 4, 'Hard': 0}}

    # problems_lst = get_new_problems(top_n_problems=3, paid_only=False, level_num=1)
    # print(problems_lst)
    # print(len(problems_lst))
    # print(problems_lst[0].question_id)
    # print(problems_lst[1].question_id)
    # print(problems_lst[2].question_id)
    news = get_latest_news(theme="career", num_top_news=2)
    print(news)
    print(news[0].title)
    print(news[1].title)
