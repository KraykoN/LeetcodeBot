import requests
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport


def get_username_from_database(user_id):
    # TODO: Implement this function to retrieve
    # the user's LeetCode username from the database
    return "example_username"


def get_user_progress(leetcode_login):
    query = gql(
        f"""
        {{
            matchedUser(username: {leetcode_login})
                {{
                    username
                    submitStats: submitStatsGlobal
                    {{
                        acSubmissionNum
                        {{
                            difficulty
                            count
                            submissions
                        }}
                    }}
                }}
        }}
        """
    )
    transport = RequestsHTTPTransport(url="https://leetcode.com/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=False)
    result = client.execute(query)

    return result


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
    url = f"https://leetcode.com/discuss/{theme}"
    response = requests.get(url)
    response.raise_for_status()
    latest_news = []
    for line in response.text.splitlines():
        if 'href="/discuss/announcement"' in line:
            break
        if 'href="/discuss/' in line:
            start_index = line.index('href="/discuss/') + len('href="')
            end_index = line.index('"', start_index)
            discussion_url = "https://leetcode.com" + line[start_index:end_index]
            start_index = line.index(">", end_index) + 1
            end_index = line.index("</a>", start_index)
            discussion_title = line[start_index:end_index].strip()
            latest_news.append({"title": discussion_title, "url": discussion_url})
        if len(latest_news) == 3:  # return at most 3 news items
            break


# def get_available_contests()

# def get_tasks_of_contset(contest_name)

# def get_user's_solved_tasks_in_details(username)

# def get_task_in_details(task_num)

if __name__ == "__main__":
    # name = '"krayko13"'
    # raw_data = get_user_progress(leetcode_login=name)
    # # response:
    # #     {'matchedUser': {'username': 'krayko13', 'submitStats': {'acSubmissionNum': [
    # #                 {'difficulty': 'All', 'count': 12, 'submissions': 17
    # #                 },
    # #                 {'difficulty': 'Easy', 'count': 8, 'submissions': 9
    # #                 },
    # #                 {'difficulty': 'Medium', 'count': 4, 'submissions': 8
    # #                 },
    # #                 {'difficulty': 'Hard', 'count': 0, 'submissions': 0
    # #                 }
    # #             ]
    # #         }
    # #     }
    # # }

    # difficulty_counts = {
    #     item["difficulty"]: item["count"]
    #     for item in raw_data["matchedUser"]["submitStats"]["acSubmissionNum"]
    # }
    # print(
    #     raw_data["matchedUser"]["username"] + " " + str(difficulty_counts)
    # )  # Output: krayko13 {'All': 12, 'Easy': 8, 'Medium': 4, 'Hard': 0}

    # problems_lst = get_new_problems(top_n_problems=3, paid_only=False, level_num=1)
    # print(problems_lst)
    # print(len(problems_lst))
    print(get_latest_news())
