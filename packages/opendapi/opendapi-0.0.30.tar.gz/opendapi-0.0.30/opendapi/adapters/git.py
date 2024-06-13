# pylint: disable=too-many-instance-attributes, too-many-branches, too-many-boolean-expressions
"""Git adapter for OpenDapi"""
import subprocess  # nosec: B404
from dataclasses import dataclass
from typing import List, Optional

from opendapi.defs import ALL_OPENDAPI_SUFFIXES


def run_git_command(cwd: str, command_split: List[str]) -> str:
    """Run a git command."""
    try:
        return subprocess.check_output(
            command_split,
            cwd=cwd,
        )  # nosec
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"git command {command_split}: {exc}") from exc


def get_changed_opendapi_filenames(cwd: str) -> List[str]:
    """Get the list of changed opendapi files."""
    files_patterns = ["*" + suffix for suffix in ALL_OPENDAPI_SUFFIXES]
    all_files_command = [
        "git",
        "status",
        *files_patterns,
    ]
    result = run_git_command(cwd, all_files_command)
    if not result:
        return []
    result = result.decode("utf-8").replace("'", "")
    return [r.split(" ", 2)[-1] for r in result.split("\n") if r]


def add_untracked_opendapi_files(cwd: str) -> int:
    """Add opendapi relevant untracked files to git and return number of files added."""
    files_patterns = ["*" + suffix for suffix in ALL_OPENDAPI_SUFFIXES]
    all_files_command = [
        "git",
        "add",
        "--dry-run",
        "--ignore-missing",
        *files_patterns,
    ]
    result = run_git_command(cwd, all_files_command)
    if result:
        result = result.decode("utf-8").replace("'", "")
        all_files = [r.split(" ", 2)[-1] for r in result.split("\n") if r]
        run_git_command(cwd, ["git", "add", *all_files])
        return len(all_files)
    return 0


def get_git_diff_filenames(
    root_dir: str,
    base_ref: str,
    current_ref: Optional[str] = None,
) -> List[str]:
    """Get the list of files changed between current and main branch"""
    commands = ["git", "diff", "--name-only", base_ref]
    if current_ref:
        commands.append(current_ref)
    files = run_git_command(root_dir, commands)
    return [filename for filename in files.decode("utf-8").split("\n") if filename]


def check_if_uncommitted_changes_exist(cwd: str) -> bool:
    """Check if uncommitted changes exist."""
    if run_git_command(cwd, ["git", "diff", "--name-only"]):
        return True
    return False


@dataclass
class ChangeTriggerEvent:
    """Change trigger event, e.g. from Github Actions"""

    where: str
    before_change_sha: str = None
    event_type: Optional[str] = None
    after_change_sha: Optional[str] = None
    repo_api_url: Optional[str] = None
    repo_html_url: Optional[str] = None
    repo_owner: Optional[str] = None
    git_ref: Optional[str] = None
    pull_request_number: Optional[int] = None
    auth_token: Optional[str] = None
    markdown_file: Optional[str] = None

    def __post_init__(self):
        """Post init checks"""
        if self.where not in ["local", "github"] or self.before_change_sha is None:
            raise ValueError(
                "Where should be either local or github."
                " Before change SHA is required"
            )

        if self.is_github_event:
            if (
                self.event_type is None
                or self.after_change_sha is None
                or self.repo_api_url is None
                or self.repo_html_url is None
                or self.repo_owner is None
                or self.auth_token is None
            ):
                raise ValueError(
                    "Event type, after change SHA, repo API URL, repo HTML URL, "
                    "repo owner and auth token are required"
                )

        if self.is_pull_request_event:
            if self.pull_request_number is None:
                raise ValueError("Pull request number is required")

        if self.is_push_event:
            if self.git_ref is None:
                raise ValueError("Git ref is required")

    @property
    def is_local_event(self) -> bool:
        """Check if the event is a local event"""
        return self.where == "local"

    @property
    def is_github_event(self) -> bool:
        """Check if the event is a github event"""
        return self.where == "github"

    @property
    def is_pull_request_event(self) -> bool:
        """Check if the event is a pull request event"""
        return self.event_type == "pull_request"

    @property
    def is_push_event(self) -> bool:
        """Check if the event is a push event"""
        return self.event_type == "push"
