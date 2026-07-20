"""
====================================================================
History Service

Project : ConfigVista AI

Purpose
-------
Provides Assessment Repository functionality.

====================================================================
"""

from database.database import SessionLocal
from database.models import (
    Change,
    FeatureStore,
    Recommendation
)


class HistoryService:

    def __init__(self):

        self.session = SessionLocal()

    def get_all_assessments(self):

        return (

            self.session.query(Change)

            .order_by(Change.created_at.desc())

            .all()

        )

    def get_assessment(self, change_id):

        return (

            self.session.query(Change)

            .filter(Change.change_id == change_id)

            .first()

        )

    def get_features(self, change_id):

        rows = (

            self.session.query(FeatureStore)

            .filter(FeatureStore.change_id == change_id)

            .all()

        )

        return {

            row.feature_name: row.feature_value

            for row in rows

        }

    def get_recommendations(self, change_id):

        return (

            self.session.query(Recommendation)

            .filter(Recommendation.change_id == change_id)

            .all()

        )

    def close(self):

        self.session.close()