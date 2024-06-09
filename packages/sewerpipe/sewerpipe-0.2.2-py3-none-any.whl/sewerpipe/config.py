from pydantic import BaseModel
from confuk.parse import parse_config
from sewerpipe.task import Task
from typing import List


class Config(BaseModel):
    """Config for all workflows."""
    tasks: List[Task]

    @classmethod
    def from_file(cls, file_path: str):
        return parse_config(file_path, cls)
