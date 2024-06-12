from typing import List, Union

from pydantic import BaseModel, Field

from fiddler.schemas.custom_features import Multivariate, VectorFeature, TextEmbedding, ImageEmbedding, Enrichment


class ModelSpec(BaseModel):
    """Model spec defines how model columns are used along with model task"""

    schema_version: int = 1
    """Schema version"""

    inputs: List[str] = Field(default_factory=list)
    """Feature columns"""

    outputs: List[str] = Field(default_factory=list)
    """Prediction columns"""

    targets: List[str] = Field(default_factory=list)
    """Label columns"""

    decisions: List[str] = Field(default_factory=list)
    """Decisions columns"""

    metadata: List[str] = Field(default_factory=list)
    """Metadata columns"""

    custom_features: List[Union[Multivariate, VectorFeature, TextEmbedding, ImageEmbedding, Enrichment]] = Field(
        default_factory=list
    )
    """Custom feature definitions"""
