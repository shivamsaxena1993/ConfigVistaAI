"""
====================================================================
Recommendation Repository
====================================================================
"""

from typing import List

from database.models import Recommendation
from database.repositories.base_repository import BaseRepository


class RecommendationRepository(BaseRepository[Recommendation]):

    def __init__(self, session):
        super().__init__(session, Recommendation)

    def get_by_change(self, change_id: int) -> List[Recommendation]:

        return (
            self.query()
            .filter(Recommendation.change_id == change_id)
            .all()
        )

    def get_latest(self):

        return (
            self.query()
            .order_by(Recommendation.generated_at.desc())
            .first()
        )