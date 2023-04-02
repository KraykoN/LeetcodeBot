import requests


def get_username_from_database(user_id):
    """_summary_

    Args:
        user_id (_type_): _description_

    Returns:
        _type_: _description_
    """    
    # TODO: Implement this function to retrieve
    # the user's LeetCode username from the database
    return "example_username"


def get_user_progress(username):
    url = f"https://leetcode.com/{username}/"
    response = requests.get(url)
    response.raise_for_status()
    progress = {}
    for line in response.text.splitlines():
        if 'title="Solved' in line:
            _, problem_count, _ = line.strip().split()
            progress["solved"] = int(problem_count)
        elif 'title="Accepted' in line:
            _, problem_count, _ = line.strip().split()
            progress["accepted"] = int(problem_count)
    return progress


def get_daily_problems():
    url = "https://leetcode.com/api/problems/all/"
    response = requests.get(url)
    response.raise_for_status()
    daily_problems = []
    for problem in response.json()['stat_status_pairs']:
        if problem['status'] == 'ac' and not problem['paid_only'] and not problem['is_favor']:
            daily_problems.append({
                'title': problem['stat']['question__title'],
                'url': f"https://leetcode.com/problems/{problem['stat']['question__title_slug']}/"
            })
        if len(daily_problems) == 3:  # return at most 3 problems
            break
    return daily_problems


def get_latest_news():
    url = "https://leetcode.com/discuss/"
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
            start_index = line.index('>', end_index) + 1
            end_index = line.index('</a>', start_index)
            discussion_title = line[start_index:end_index].strip()
            latest_news.append({
                'title': discussion_title,
                'url': discussion_url
            })
        if len(latest_news) == 3:  # return at most 3 news items
            break
    return latest_news