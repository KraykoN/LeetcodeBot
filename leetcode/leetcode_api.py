import datetime

import requests
from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from utils import load_query


def get_user_progress(leetcode_login):
    query = load_query("leetcode/gql_scripts/get_user_progress.gql")

    params = {"leetcode_login": leetcode_login}

    transport = RequestsHTTPTransport(url="https://leetcode.com/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=False)
    result = client.execute(query, variable_values=params)

    difficulty_counts = {
        item["difficulty"]: item["count"]
        for item in result["matchedUser"]["submitStats"]["acSubmissionNum"]
    }

    return {result["matchedUser"]["username"]: difficulty_counts}


def get_new_problems(top_n_problems, paid_only, level_num):
    url = "https://leetcode.com/api/problems/all/"
    response = requests.get(url)
    response.raise_for_status()
    new_problems = []
    for problem in response.json()["stat_status_pairs"]:
        if (
            problem["paid_only"] is paid_only
            and problem["difficulty"]["level"] is level_num
        ):
            new_problems.append(
                {
                    "question_id": problem["stat"]["question_id"],
                    "total_accepted_solutions": problem["stat"]["total_acs"],
                    "total_submitted_solutions": problem["stat"]["total_submitted"],
                    "title": problem["stat"]["question__title"],
                    "level_num": problem["difficulty"]["level"],
                    "url": f"https://leetcode.com/problems/{problem['stat']['question__title_slug']}/",
                    "has_video": problem["stat"][
                        "question__article__has_video_solution"
                    ],
                }
            )
        if len(new_problems) == top_n_problems:  # return at most 3 problems
            break
    return new_problems


def get_latest_news(theme, num_top_news):
    query = load_query("leetcode/gql_scripts/get_news.gql")

    params = {
        "orderBy": "hot",
        "query": "",
        "skip": 0,
        "first": num_top_news,
        "tags": [],
        "categories": [f"{theme}"],
    }

    transport = RequestsHTTPTransport(url="https://leetcode.com/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=False)
    result = client.execute(query, variable_values=params)

    difficulty_counts = [
        [
            int(node_data["id"]),
            node_data["title"],
            node_data["commentCount"],
            node_data["viewCount"],
            node_data["pinned"],
            datetime.datetime.fromtimestamp(node_data["post"]["creationDate"]),
            node_data["post"]["author"]["username"],
        ]
        for node_data in (edge["node"] for edge in result["categoryTopicList"]["edges"])
    ]

    return difficulty_counts


# def get_available_contests(current_date?)

# def get_tasks_of_contset(contest_name)

# def get_user's_solved_tasks_in_details(username)

# def get_task_in_details(task_num)

if __name__ == "__main__":
    print(get_user_progress(leetcode_login="krayko13"))
    # {'krayko13': {'All': 12, 'Easy': 8, 'Medium': 4, 'Hard': 0}}

    # problems_lst = get_new_problems(top_n_problems=3, paid_only=False, level_num=1)
    # print(problems_lst)
    # print(len(problems_lst))
    # print(get_latest_news(theme="career", num_top_news=2))
