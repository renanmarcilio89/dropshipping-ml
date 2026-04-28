from app.models.auth import MeliCredential
from app.models.base import Base
from app.models.market import Candidate, OpportunityScore, TrendSnapshot
from app.models.raw import ApiPayload

__all__ = [
    "Base",
    "MeliCredential",
    "ApiPayload",
    "TrendSnapshot",
    "Candidate",
    "OpportunityScore",
    "CommercialOpportunityAnalysis",
]
