from datetime import datetime

import humanize

from models import User, IssueWithUsersAndTeams

HEADERS = [
    "Title",
    "Updated",
    "Creator",
    "Creator in team",
    "Not a draft",
    "Team user",
    "Url",
    "Created",
    "State",
]


def issue_to_tabulate(issue: IssueWithUsersAndTeams, user: User) -> list[str]:
    return [
        issue.title,
        humanize_date(issue.updated_at),
        str(issue.creator),
        bool_to_emoji(issue.creator_in_team),
        bool_to_emoji(not issue.draft),
        sort_assigned_team_user(issue.assigned_team_user, user),
        issue.html_url,
        humanize_date(issue.created_at),
        issue.state,
    ]


def bool_to_emoji(variable: bool) -> str:
    return "✅" if variable else "❌"


def sort_assigned_team_user(assigned_team_user: set[User], user: User) -> str:
    str_assigned_team_user = [str(u) for u in assigned_team_user]
    if user in assigned_team_user:
        str_assigned_team_user.remove(str(user))
        str_assigned_team_user = [f"\033[1m{str(user)}\033[0m"] + str_assigned_team_user
    return ", ".join(str_assigned_team_user)


def humanize_date(date: datetime) -> str:
    now = datetime.now()
    diff = now - date
    return humanize.naturaltime(now - diff)
