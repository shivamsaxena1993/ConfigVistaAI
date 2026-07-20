"""
====================================================================
File: persistence_service.py

Project : ConfigVista AI

Purpose
-------
Stores completed assessments into SQLite.

Current MVP saves:

1. Change
2. Feature Store
3. Recommendations

====================================================================
"""

from datetime import datetime

from database.database import SessionLocal

from uuid import uuid4

from database.models import (
    Change,
    FeatureStore,
    Recommendation
)


class PersistenceService:

    def __init__(self):

        self.session = SessionLocal()

    # --------------------------------------------------
    # Convert FeatureModel / dict to dictionary
    # --------------------------------------------------

    def _feature_dict(self, features):

        if isinstance(features, dict):
            return features

        if hasattr(features, "to_dict"):
            return features.to_dict()

        raise TypeError(
            "Unsupported feature object passed to PersistenceService."
        )

    def save(self, features, risk, recommendation):

        features = self._feature_dict(features)

        try:

            # --------------------------------------------------
            # Create Change
            # --------------------------------------------------

            change = Change(

                change_reference=(
                    f"CHG-{datetime.now():%Y%m%d%H%M%S}-"
                    f"{uuid4().hex[:8].upper()}"
                ),
                device_id=None,

                submitted_by=None,

                change_type="Configuration Assessment",

                description=f"Assessment for {features['hostname']}",

                risk_label=risk["risk_label"],

                risk_score=risk["risk_score"],

                confidence_score=risk["confidence_score"],

                approval_status="Pending",

                change_status="Analyzed"

            )

            self.session.add(change)

            self.session.commit()

            self.session.refresh(change)

            # --------------------------------------------------
            # Save Features
            # --------------------------------------------------

            for name, value in features.items():

                feature = FeatureStore(

                    change_id=change.change_id,

                    feature_name=name,

                    feature_value=str(value)

                )

                self.session.add(feature)

            # --------------------------------------------------
            # Save Recommendations
            # --------------------------------------------------

            for rec in recommendation["recommendations"]:

                row = Recommendation(

                    change_id=change.change_id,

                    recommendation_text=rec["action"],

                    explanation=rec["reason"],

                    llm_summary=rec["category"]

                )

                self.session.add(row)

            self.session.commit()

            return change.change_reference

        except Exception:

            self.session.rollback()

            raise

        finally:

            self.session.close()