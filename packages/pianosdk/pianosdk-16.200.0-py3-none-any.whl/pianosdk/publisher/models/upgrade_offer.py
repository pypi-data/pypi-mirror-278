from datetime import date, datetime
from pydantic.main import BaseModel
from typing import Optional


class UpgradeOffer(BaseModel):
    offer_id: Optional[str] = None
    name: Optional[str] = None


UpgradeOffer.model_rebuild()
