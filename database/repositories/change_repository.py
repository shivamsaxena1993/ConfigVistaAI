"""
====================================================================
Change Repository
====================================================================
"""

from typing import Optional

from database.models import Change
from database.repositories.base_repository import BaseRepository


class ChangeRepository(BaseRepository[Change]):

    def __init__(self, session):
        super().__init__(session, Change)

    def get_by_reference(self, reference: str) -> Optional[Change]:

        return (
            self.query()
            .filter(Change.change_reference == reference)
            .first()
        )

    def get_by_status(self, status: str):

        return (
            self.query()
            .filter(Change.change_status == status)
            .all()
        )

    def get_high_risk_changes(self):

        return (
            self.query()
            .filter(Change.risk_label == "High")
            .all()
        )

    def get_pending_approvals(self):

        return (
            self.query()
            .filter(Change.approval_status == "Pending")
            .all()
        )