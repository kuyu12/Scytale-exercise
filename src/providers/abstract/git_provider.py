from abc import abstractmethod

from providers.abstract.base_provider import BaseProvider


class GitProvider(BaseProvider):

    def __init__(self, display_name: str):
        BaseProvider.__init__(self, display_name)

    @abstractmethod
    def __get_repo(self, repo_name: str):
        """
        Retrieve a specific repository from the Git provider.

        Args:
            repo_name (str): The name of the repository to retrieve.

        Returns:
            A repository object representing the requested repository.
        """
        pass

    @abstractmethod
    def __get_all_repos(self):
        """
        Retrieve a list of all repositories associated with the Git provider.

        Returns:
             A list of repository objects representing all available repositories.
        """
        pass

    @abstractmethod
    def list_pull_requests(self):
        """
            Retrieve a list of all open pull requests across all repositories associated with the Git provider.

            Returns:
                A list of pull request objects representing all open pull requests.
        """
        pass

    def __rate_limit(self):
        return 0
