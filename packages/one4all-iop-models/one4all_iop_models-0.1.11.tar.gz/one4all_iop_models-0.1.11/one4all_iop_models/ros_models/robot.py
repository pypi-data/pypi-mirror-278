from typing import List, Union, Literal
from enum import Enum

from pydantic import BaseModel, Field


class RobotPosition(BaseModel):
    amcl_positions: List[float] = Field(..., min_length=3, max_length=3)
    amcl_orientations: List[float] = Field(..., min_length=4, max_length=4)
    odom_pose_positions: List[float] = Field(..., min_length=3, max_length=3)
    odom_pose_orientations: List[float] = Field(..., min_length=4, max_length=4)
    odom_twist_linear: List[float] = Field(..., min_length=3, max_length=3)
    odom_twist_angular: List[float] = Field(..., min_length=3, max_length=3)
    path_positions: List[List[float]] = Field(..., min_length=3, max_length=3)
    path_orientations: List[List[float]] = Field(..., min_length=4, max_length=4)


class RobotData(BaseModel):
    batery_data: float = Field(..., ge=0, le=100)
    position_data: RobotPosition


class RobotAction(BaseModel):
    subtask_id: int
    action_id: int


class AWCombo(RobotAction):
    name: Literal["awcombo"] = "awcombo"
    x: float = Field(..., ge=-5, le=5)
    y: float = Field(..., ge=-5, le=5)
    angle: float = Field(..., ge=0, le=360)


class Joint(RobotAction):
    name: Literal["joint"] = "joint"
    j1: float = Field(..., ge=-1, le=1)
    j2: float = Field(..., ge=-1, le=1)
    j3: float = Field(..., ge=-1, le=1)
    j4: float = Field(..., ge=-1, le=1)
    j5: float = Field(..., ge=-1, le=1)
    j6: float = Field(..., ge=-1, le=1)


class Carte(RobotAction):
    name: Literal["carte"] = "carte"
    x: float = Field(..., ge=-1, le=1)
    y: float = Field(..., ge=-1, le=1)
    z: float = Field(..., ge=-1, le=1)


class Increm(RobotAction):
    name: Literal["increm"] = "increm"
    axis: Literal["x", "y", "z"]
    delta: float


class Effector(RobotAction):
    name: Literal["effector"] = "effector"
    state: bool
    index: int = Field(..., ge=0, le=255)


class SubTask(BaseModel):
    subtask_id: int
    actions: List[Union[Increm, AWCombo, Carte, Joint, Effector]]


class RobotActionStatus(Enum):
    RECIEVED = 0
    INPROGRESS = 1
    FINISHED = 2
    FAILED = 3


class RobotActionResponse(BaseModel):
    subtask_id: int
    action_id: int
    status: RobotActionStatus
    log: str
