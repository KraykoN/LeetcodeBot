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


def get_daily_problems():
    url = "https://leetcode.com/api/problems/all/"
    response = requests.get(url)
    response.raise_for_status()
    daily_problems = []
    for problem in response.json()["stat_status_pairs"]:
        if (
            problem["status"] == "ac"
            and not problem["paid_only"]
            and not problem["is_favor"]
        ):
            daily_problems.append(
                {
                    "title": problem["stat"]["question__title"],
                    "url": f"https://leetcode.com/problems/{problem['stat']['question__title_slug']}/",
                }
            )
        if len(daily_problems) == 3:  # return at most 3 problems
            break
    return daily_problems


def get_latest_news():
    # url = "https://leetcode.com/discuss/"
    # response = requests.get(url)
    # response.raise_for_status()
    # latest_news = []
    # for line in response.text.splitlines():
    #     if 'href="/discuss/announcement"' in line:
    #         break
    #     if 'href="/discuss/' in line:
    #         start_index = line.index('href="/discuss/') + len('href="')
    #         end_index = line.index('"', start_index)
    #         discussion_url = "https://leetcode.com" + line[start_index:end_index]
    #         start_index = line.index(">", end_index) + 1
    #         end_index = line.index("</a>", start_index)
    #         discussion_title = line[start_index:end_index].strip()
    #         latest_news.append({"title": discussion_title, "url": discussion_url})
    #     if len(latest_news) == 3:  # return at most 3 news items
    #         break
    query = gql(
        """
        query {
            userRecentTopics(count: 3) { "userRecentTopics", "contestTopics", "allTopics" or "questionTopics
                ... on TopicNode {
                    title
                    url
                }
            }
        }
    """
    )

    transport = RequestsHTTPTransport(url="https://leetcode.com/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=False)
    result = client.execute(query)

    news_list = []

    for news in result["data"]["userRecentTopics"]:
        news_title = news["title"]
        news_url = news["url"]
        news_list.append((news_title, news_url))

    return news_list


if __name__ == "__main__":
    name = '"krayko13"'
    raw_data = get_user_progress(leetcode_login=name)
    # response:
    #     {'matchedUser': {'username': 'krayko13', 'submitStats': {'acSubmissionNum': [
    #                 {'difficulty': 'All', 'count': 12, 'submissions': 17
    #                 },
    #                 {'difficulty': 'Easy', 'count': 8, 'submissions': 9
    #                 },
    #                 {'difficulty': 'Medium', 'count': 4, 'submissions': 8
    #                 },
    #                 {'difficulty': 'Hard', 'count': 0, 'submissions': 0
    #                 }
    #             ]
    #         }
    #     }
    # }

    difficulty_counts = {
        item["difficulty"]: item["count"]
        for item in raw_data["matchedUser"]["submitStats"]["acSubmissionNum"]
    }
    print(raw_data["matchedUser"]["username"] + " " + str(difficulty_counts))

    print(get_latest_news())
