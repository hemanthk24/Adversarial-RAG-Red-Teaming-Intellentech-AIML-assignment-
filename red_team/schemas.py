from typing import Literal
from pydantic import BaseModel, Field



class FailureEvaluation(BaseModel):

    failure_detected: bool = Field(
        description="Whether the RAG response contains the targeted failure."
    )

    confidence: float = Field(
        description="Confidence from 0 to 1."
    )

    reason: str = Field(
        description="Short explanation of why the response is or is not a failure."
    )

    unsupported_claims: list[str] = Field(
        default_factory=list,
        description="Claims in the answer that are not supported by retrieved evidence."
    )

    citation_problems: list[str] = Field(
        default_factory=list,
        description="Citation/source attribution problems."
    )


class ContradictionEvaluation(BaseModel):

    contradiction_detected: bool = Field(
        description="Whether the two answers contradict each other on the same underlying fact."
    )

    confidence: float = Field(
        description="Confidence from 0 to 1."
    )

    reason: str = Field(
        description="Explanation of the contradiction or lack of contradiction."
    )