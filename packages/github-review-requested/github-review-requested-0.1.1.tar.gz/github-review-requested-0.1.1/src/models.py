from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    login: str

    @classmethod
    def from_dict(cls, d: dict) -> "User":
        return cls(login=d["login"])

    def __str__(self):
        return self.login


@dataclass
class GithubInfo:
    user: User
    team: set[User]
    org: str
    token: str


@dataclass
class Repo:
    url: str

    @property
    def owner(self) -> str:
        return self.url.split("/")[4]

    @property
    def name(self) -> str:
        return self.url.split("/")[5]


@dataclass
class Issue:
    id: str
    title: str
    url: str
    html_url: str
    state: str
    draft: bool
    number: int
    created_at: datetime
    updated_at: datetime
    repo: Repo
    creator: User

    @classmethod
    def from_dict(cls, d: dict) -> "Issue":
        return cls(
            id=d["id"],
            title=d["title"].strip(),
            url=d["url"],
            html_url=d["html_url"],
            state=d["state"],
            draft=d["draft"],
            number=d["number"],
            created_at=datetime.strptime(d["created_at"], "%Y-%m-%dT%H:%M:%SZ"),
            updated_at=datetime.strptime(d["updated_at"], "%Y-%m-%dT%H:%M:%SZ"),
            repo=Repo(d["repository_url"]),
            creator=User.from_dict(d["user"]),
        )


@dataclass
class IssueWithUsersAndTeams(Issue):
    users: set[User]
    user_in_users: bool
    assigned_team_user: set[User]
    creator_in_team: bool

    @classmethod
    def from_issue(
        cls,
        issue: Issue,
        users: set[User],
        user: User,
        team_users: set[User],
    ) -> "IssueWithUsersAndTeams":
        return cls(
            id=issue.id,
            title=issue.title,
            url=issue.url,
            html_url=issue.html_url,
            state=issue.state,
            draft=issue.draft,
            number=issue.number,
            created_at=issue.created_at,
            updated_at=issue.updated_at,
            repo=issue.repo,
            creator=issue.creator,
            users=users,
            user_in_users=user in users,
            assigned_team_user=users.intersection(team_users),
            creator_in_team=issue.creator in team_users,
        )
