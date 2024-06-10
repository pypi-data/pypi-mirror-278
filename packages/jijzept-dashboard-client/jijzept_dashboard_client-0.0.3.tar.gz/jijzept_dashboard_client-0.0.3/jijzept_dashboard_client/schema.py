from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class DecisionVarKind(str, Enum):
    model_config = ConfigDict(from_attributes=True)

    binary = "binary"
    continuous = "continuous"
    integer = "integer"
    semi_continuous = "semi_continuous"
    semi_integer = "semi_integer"


class RelatedVariable(BaseModel):
    name: str
    latex: str
    description: str


class DecisionVar(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    kind: DecisionVarKind
    lower_bound: str
    upper_bound: str
    shape: List[str]
    latex: str
    description: str


class Constant(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    ndim: int
    latex: str
    description: str


class Objective(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    latex: str
    description: str
    related_variables: list[RelatedVariable]


class Constraint(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    latex: str
    name: str
    description: str
    related_variables: list[RelatedVariable]


class Source(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
    )

    serializable: str  # jm.to_protobuf(problem) を文字列にしたもの
    objective: Objective
    constraints: List[Constraint]
    decision_vars: List[DecisionVar]
    constants: List[Constant]
    name: Optional[str] = None
