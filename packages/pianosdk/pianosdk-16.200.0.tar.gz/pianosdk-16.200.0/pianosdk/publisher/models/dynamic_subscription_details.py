from datetime import date, datetime
from pydantic.main import BaseModel
from typing import Optional
from pianosdk.publisher.models.access_period import AccessPeriod
from typing import List


class DynamicSubscriptionDetails(BaseModel):
    renewal_type: Optional[str] = None
    next_amount: Optional[str] = None
    term_periods: Optional['List[AccessPeriod]'] = None
    scheduled_period_id: Optional[str] = None


DynamicSubscriptionDetails.model_rebuild()
