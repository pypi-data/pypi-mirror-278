import click
import requests
from tabulate import tabulate

from models import GithubInfo, Issue, IssueWithUsersAndTeams, User
from utils import issue_to_tabulate, HEADERS

API_URL = "https://api.github.com/"


def get_headers(token: str) -> dict:
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }


def retrieve_github_info(user: str, org: str, team_name: str, token: str) -> GithubInfo:
    issues_url = f"{API_URL}/orgs/{org}/teams/{team_name}/members"
    response = requests.get(issues_url, headers=get_headers(token))
    team_users = {User(login=team_user["login"]) for team_user in response.json()}
    return GithubInfo(user=User(login=user), org=org, team=team_users, token=token)


def get_issues(github_info: GithubInfo) -> list[Issue]:
    issues_url = f"{API_URL}/search/issues?q=is:pr+is:open+review-requested:{github_info.user.login}"
    response = requests.get(issues_url, headers=get_headers(github_info.token))
    prs = response.json()["items"]
    return [Issue.from_dict(pr) for pr in prs]


def get_reviewers(issue: Issue, github_info: GithubInfo) -> IssueWithUsersAndTeams:
    reviewers_url = f"{API_URL}/repos/{github_info.org}/{issue.repo.name}/pulls/{issue.number}/requested_reviewers"
    response = requests.get(reviewers_url, headers=get_headers(github_info.token))
    reviewers = response.json()
    users = {User.from_dict(user) for user in reviewers["users"]}

    return IssueWithUsersAndTeams.from_issue(
        issue, users, github_info.user, github_info.team
    )


def pretty_print_issues_with_users_and_teams(
    issues: list[IssueWithUsersAndTeams], github_info: GithubInfo
):
    sorted_issues = sorted(issues, key=lambda x: (not x.user_in_users, x.updated_at))

    tabulate_ready_issues = [
        issue_to_tabulate(issue, github_info.user) for issue in sorted_issues
    ]
    if index := [i for i, issue in enumerate(sorted_issues) if not issue.user_in_users]:
        tabulate_ready_issues.insert(index[0], ["", "", "", "", "", "", "", ""])

    print(tabulate(tabulate_ready_issues, HEADERS, tablefmt="pretty"))


@click.command()
@click.option("--user", help=f"User name from github", required=True)
@click.option("--org", help=f"Org name from github", required=True)
@click.option("--token", help=f"Token from github", required=True)
@click.option("--team", help=f"Team name from github", required=True)
def git_assigned_pr_viewer(user: str, org: str, token: str, team: str):
    github_info = retrieve_github_info(user, org, team, token)
    issues = get_issues(github_info)
    issues_with_users_and_teams = [
        get_reviewers(issue, github_info) for issue in issues
    ]
    pretty_print_issues_with_users_and_teams(issues_with_users_and_teams, github_info)


if __name__ == "__main__":
    git_assigned_pr_viewer()
