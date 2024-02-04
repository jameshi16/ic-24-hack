from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config

@dataclass_json
@dataclass
class ScoreResponse:
    overall: list[int]
    activity: list[int]
    sleep: list[int]
    # fitness: list[int]


@dataclass_json
@dataclass
class GetUserResponse:
    userid: str
    start_time: int = field(metadata=config(field_name='startTime'))
    scores: ScoreResponse
