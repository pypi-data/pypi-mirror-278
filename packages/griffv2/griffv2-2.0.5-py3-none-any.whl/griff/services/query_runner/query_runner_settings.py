from griff.utils.pydantic_types import DirectoryStr
from pydantic import BaseModel


class QueryRunnerSettings(BaseModel):
    project_dir: DirectoryStr
    driver: str
