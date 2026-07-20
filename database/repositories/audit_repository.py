"""
====================================================================
Audit Repository
====================================================================
"""

from database.models import AuditLog
from database.repositories.base_repository import BaseRepository


class AuditRepository(BaseRepository[AuditLog]):

    def __init__(self, session):
        super().__init__(session, AuditLog)

    def get_user_activity(self, user_id: int):

        return (
            self.query()
            .filter(AuditLog.user_id == user_id)
            .order_by(AuditLog.timestamp.desc())
            .all()
        )

    def get_by_action(self, action: str):

        return (
            self.query()
            .filter(AuditLog.action == action)
            .all()
        )