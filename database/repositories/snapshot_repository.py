"""
====================================================================
Snapshot Repository
====================================================================
"""

from typing import List, Optional

from database.models import Snapshot
from database.repositories.base_repository import BaseRepository


class SnapshotRepository(BaseRepository[Snapshot]):

    def __init__(self, session):
        super().__init__(session, Snapshot)

    def get_latest_snapshot(self, device_id: int) -> Optional[Snapshot]:

        return (
            self.query()
            .filter(Snapshot.device_id == device_id)
            .order_by(Snapshot.collected_at.desc())
            .first()
        )

    def get_snapshot_history(self, device_id: int) -> List[Snapshot]:

        return (
            self.query()
            .filter(Snapshot.device_id == device_id)
            .order_by(Snapshot.collected_at.desc())
            .all()
        )

    def get_by_snapshot_type(self, snapshot_type: str) -> List[Snapshot]:

        return (
            self.query()
            .filter(Snapshot.snapshot_type == snapshot_type)
            .all()
        )