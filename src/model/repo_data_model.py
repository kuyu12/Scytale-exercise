from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from utils.const import GITHUB


@dataclass
class RepoModel:
    id: str
    name: str
    full_name: str
    owner: str
    created_at: datetime


class RepoEnum(Enum):
    github = GITHUB


def RepoFactory(repo, provider: RepoEnum):
    """Factory Method"""
    providers = {
        GITHUB: RepoModel(id=repo.id,
                          name=repo.name,
                          full_name=repo.full_name,
                          owner=repo.owner.login,
                          created_at=repo.created_at)
    }

    return providers[provider]
