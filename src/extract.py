import dataclasses
import json
import logging
import os

from providers.github_provider import GithubProvider
from utils.const import PR_OUTPUT_FOLDER, ORGANIZATION_VAR_NAME
from utils.utils import json_serial

logger = logging.getLogger(__name__)


def extract(organization: str) -> None:
    """
    Extracts pull request data for a specified GitHub organization and saves it to JSON files.

    This function retrieve all pull requests for each repository
    within the given organization. It then converts the repository and pull request data
    into dictionaries and serializes them into JSON format. The serialized data is saved
    into files organized by the organization and repository names.

    :param organization: The name of the GitHub organization from which to extract pull request data.
    :type organization: str

    :raises APIError: If there is an issue with GitHub API authentication or access.
    :raises OSError: If there is an issue creating directories or writing files.

    :return: None
    """
    provider = GithubProvider(organization)
    pr = provider.list_pull_requests()

    logger.info(f"Repo count: {len(pr)}")
    for repo_data in pr.keys():
        repo, pulls = pr[repo_data]
        full_repo_dict = dataclasses.asdict(repo)
        full_repo_dict['pulls'] = list(map(lambda x: dataclasses.asdict(x), pulls))

        file_path_folder = f'{PR_OUTPUT_FOLDER}/{organization}'
        logger.info(f' - Save PRs for:{repo_data}')
        os.makedirs(file_path_folder, exist_ok=True)
        with open(f'{file_path_folder}/{repo_data}.json', 'w') as fp:
            json.dump(full_repo_dict, fp, default=json_serial)


if __name__ == "__main__":
    # Local Testing
    organization = os.environ[ORGANIZATION_VAR_NAME]
    extract(organization)
