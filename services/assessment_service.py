"""
====================================================================
File: assessment_service.py

Project : ConfigVista AI

Purpose
-------
Runs the complete ConfigVista AI assessment workflow.

Workflow
--------
Configuration
    ↓
Parser
    ↓
Feature Extraction
    ↓
Risk Prediction
    ↓
Recommendation Engine
    ↓
Persistence Service
    ↓
Assessment Result

====================================================================
"""

from parser.parsers.config_parser import ConfigParser, load_config

from parser.feature_extractor import FeatureExtractor

from ml.risk_engine import RiskEngine

from ml.recommendation_engine import RecommendationEngine

from services.persistence_service import PersistenceService

from services.feature_validator import FeatureValidator

from datetime import datetime


class AssessmentService:

    def __init__(self):

        self.persistence = PersistenceService()

    def run(self, file_path):

        # --------------------------------------------------
        # Load Configuration
        # --------------------------------------------------

        config = load_config(file_path)

        # --------------------------------------------------
        # Parse Configuration
        # --------------------------------------------------

        parsed = ConfigParser(config).parse()

        # --------------------------------------------------
        # Feature Engineering
        # --------------------------------------------------
        
        features = FeatureExtractor(parsed).extract()
        
        # --------------------------------------------------
        # Feature Validation
        # --------------------------------------------------
        
        features = FeatureValidator.validate(features)
        
        # --------------------------------------------------
        # Risk Prediction
        # --------------------------------------------------
        
        risk = RiskEngine(features).calculate()
        
        # --------------------------------------------------
        # Recommendation Generation
        # --------------------------------------------------
        
        recommendation = RecommendationEngine(
            features,
            risk
        ).generate()

        # --------------------------------------------------
        # Persist Assessment
        # --------------------------------------------------

        change_reference = self.persistence.save(
            features,
            risk,
            recommendation
        )

        # --------------------------------------------------
        # Final Assessment
        # --------------------------------------------------

        assessment = {

            "change_reference": change_reference,

            "generated_at": datetime.now().strftime(
                "%d-%b-%Y %H:%M:%S"
            ),

            "hostname": features["hostname"],

            "features": features,

            "risk": risk,

            "recommendation": recommendation

        }

        return assessment