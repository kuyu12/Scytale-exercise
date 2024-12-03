import logging
import os
import time

from github import Github, RateLimitExceededException, BadCredentialsException, GithubException
from github.RateLimit import RateLimit
from github.Repository import Repository

from model.pull_request_data_model import PullRequestFactory
from model.repo_data_model import RepoFactory
from utils.const import GITHUB
from utils.errors import APIError
from utils.const import GITHUB_ACCESS_TOKEN_VAR_NAME

from providers.abstract.git_provider import GitProvider

logger = logging.getLogger(__name__)


def rate_safe_api_call(func):
    """Decorator to handle rate limit and authentication exceptions."""

    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RateLimitExceededException:
            rate_limit = self.__rate_limit()
            reset_time = rate_limit.core.reset.timestamp()
            current_time = time.time()
            wait_time = max(0, reset_time - current_time)
            logger.warning(f"Rate limit exceeded. Waiting for {wait_time} seconds.")
            time.sleep(wait_time)
            return func(self, *args, **kwargs)
        except BadCredentialsException:
            raise APIError(
                "Authentication Error: To proceed, please check your personal GitHub access token")

    return wrapper


class GithubProvider(GitProvider):

    def __init__(self, organization: str):
        super().__init__(GITHUB)
        self.organization = organization
        self.__check_valid_organization(organization)

    def _get_auth_obj(self) -> Github:
        """ get authentication object for GitHub from environment variable """
        try:
            api_token = os.environ[GITHUB_ACCESS_TOKEN_VAR_NAME]
            return Github(api_token)
        except KeyError:
            raise APIError(
                f"Authentication Error: To proceed, please set your personal GitHub access token as an environment variable named {GITHUB_ACCESS_TOKEN_VAR_NAME}")

    def __check_valid_organization(self, organization):
        """ get authentication object for GitHub from environment variable """
        try:
            repo = self.__get_repo(organization)
        except GithubException as e:
            if e.status == 422:  # repository validation issue - permission or not exist issue
                raise APIError(
                    f"organization cannot be searched either because the resources do not exist or you do not have permission to view them. organization:{organization}")
            else:
                raise e

    @rate_safe_api_call
    def __get_repo(self, repo_name: str) -> Repository:
        """Retrieve a repository object by name within the organization."""
        search_res = self._auth_obj.search_repositories(query=f'org:{self.organization} {repo_name}')
        return search_res

    @rate_safe_api_call
    def __get_all_repos(self) -> [Repository]:
        """Retrieve all repository objects within the organization."""
        return list(self._auth_obj.search_repositories(query=f'org:{self.organization}'))

    def __rate_limit(self) -> RateLimit:
        """Get the current rate limit status for the authenticated user."""
        return self._auth_obj.get_rate_limit()

    @rate_safe_api_call
    def list_pull_requests(self) -> dict:
        """List all pull requests for all repos in the organization."""
        repos = self.__get_all_repos()
        pulls_dict = {}

        for repo in repos:
            logger.info(f' - getting PRs from repo {repo.name}')
            pulls = repo.get_pulls(state='all')
            pulls = [PullRequestFactory(x, self.display_name) for x in pulls]
            repo_obj = RepoFactory(repo, self.display_name)
            pulls_dict[repo.name] = (repo_obj, pulls)
        return pulls_dict
