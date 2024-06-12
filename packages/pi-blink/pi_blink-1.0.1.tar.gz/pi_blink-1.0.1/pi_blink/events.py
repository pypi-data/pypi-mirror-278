from typing import Any, Optional

from pydantic import BaseModel, Field


class StopEvent(BaseModel):
    stopped_by: Optional[str] = Field(default=None, description="A note about who stopped.")
    stopped_reason: Optional[str] = Field(default=None, description="A note about why stopped.")
    additional_info: Optional[dict[str, Any]] = Field(
        default_factory=dict, description="Additional information."
    )
