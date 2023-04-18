import gql
import pytest

from leetcode.leetcode_api import get_user_progress

"""
Code Analysis

Objective:
- The objective of the function is to retrieve the progress of a user on LeetCode problems by making a request to the LeetCode GraphQL API and returning a named tuple containing the user's LeetCode login and the number of problems solved at each difficulty level.

Inputs:
- leetcode_login (str): LeetCode login for the user.

Flow:
- Load the user progress query from the gql_scripts directory.
- Set the parameter for the query.
- Set the endpoint for the GraphQL API.
- Create a transport object for making requests to the GraphQL API.
- Instantiate a client using the transport object for executing the query.
- Execute the query with the provided parameters.
- Create a dictionary of difficulty counts for each problem.
- Return a named tuple of user's name and progress by problem levels.

Outputs:
- UserProgress: A named tuple containing the username and difficulty counts.

Additional aspects:
- The function uses the load_query function from the utils module to load the user progress query from a file.
- The function catches and handles exceptions that may occur during the execution of the query.
- The function uses the RequestsHTTPTransport and Client classes from the gql.transport.requests module to make requests to the GraphQL API and execute the query, respectively.
"""


class TestGetUserProgress:
    # Tests that the function returns a named tuple containing the username and difficulty counts when a valid leetcode login is provided.
    def test_happy_path_get_user_progress(self, mocker):
        # Setup
        mock_result = {
            "matchedUser": {
                "username": "test_user",
                "submitStats": {
                    "acSubmissionNum": [
                        {"difficulty": "Easy", "count": 5},
                        {"difficulty": "Medium", "count": 3},
                        {"difficulty": "Hard", "count": 1},
                    ]
                },
            }
        }
        mocker.patch("main.Client.execute", return_value=mock_result)

        # Exercise
        result = get_user_progress("test_user")

        # Assert
        assert result.username == "test_user"
        assert result.difficulty_counts == {"Easy": 5, "Medium": 3, "Hard": 1}

    # Tests that the function returns an empty named tuple when an empty string is provided as input.
    def test_edge_case_empty_string(self, mocker):
        # Exercise
        result = get_user_progress("")

        # Assert
        assert result.username == ""
        assert result.difficulty_counts == {}

    # Tests that the function returns an empty named tuple when a non-existent leetcode login is provided.
    def test_edge_case_nonexistent_login(self, mocker):
        # Setup
        mocker.patch(
            "main.Client.execute",
            side_effect=gql.transport.exceptions.TransportQueryError,
        )

        # Exercise
        result = get_user_progress("nonexistent_user")

        # Assert
        assert result.username == ""
        assert result.difficulty_counts == {}

    # Tests that the function handles exceptions and returns an empty named tuple in case of errors.
    def test_general_behavior_handle_exceptions(self, mocker):
        # Test that the function returns an empty named tuple in case of errors
        mocker.patch(
            "main.Client.execute",
            side_effect=gql.transport.exceptions.TransportQueryError,
        )
        result = get_user_progress("test_user")
        assert result.username == ""
        assert result.difficulty_counts == {}

    # Tests that the function handles unexpected responses from the GraphQL API.
    def test_general_behavior_unexpected_responses(self, mocker):
        # Test that the function handles unexpected responses from the GraphQL API
        mocker.patch(
            "main.Client.execute", return_value={"matchedUser": {"submitStats": {}}}
        )
        result = get_user_progress("test_user")
        assert result.username == ""
        assert result.difficulty_counts == {}

    # Tests that the function handles unexpected data types in the response.
    def test_general_behavior_unexpected_data_types(self, mocker):
        # Test that the function handles unexpected data types in the response
        mocker.patch(
            "main.Client.execute",
            return_value={
                "matchedUser": {"submitStats": {"acSubmissionNum": "invalid_data"}}
            },
        )
        result = get_user_progress("test_user")
        assert result.username == ""
        assert result.difficulty_counts == {}
