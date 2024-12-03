from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from utils.const import GITHUB


@dataclass
class PullRequestModel:
    title: str
    state: str
    url: str
    merged: bool
    create_at: datetime
    last_modified: datetime


class PullProviderEnum(Enum):
    github = GITHUB


def PullRequestFactory(pr, provider: PullProviderEnum):
    """Factory Method"""
    providers = {
        GITHUB: PullRequestModel(title=pr.title,
                                 state=pr.state,
                                 url=pr.url,
                                 merged=pr.merged,
                                 create_at=pr.created_at,
                                 last_modified=pr.last_modified_datetime)
    }

    return providers[provider]
