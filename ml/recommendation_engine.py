"""
====================================================================
File: recommendation_engine.py

Project : ConfigVista AI

Purpose
-------
Generates operational recommendations based on
Risk Assessment and extracted features.

Future:
Replace rules with LLM + Historical Context + RAG while
keeping the output structure unchanged.

====================================================================
"""


class RecommendationEngine:

    def __init__(self, features, risk):

        self.features = features
        self.risk = risk

    # ----------------------------------------------------------
    # Safe Feature Access
    # ----------------------------------------------------------

    def _get(self, key, default=0):

        if isinstance(self.features, dict):
            return self.features.get(key, default)

        return getattr(self.features, key, default)

    # ----------------------------------------------------------
    # Recommendation Engine
    # ----------------------------------------------------------

    def generate(self):

        recommendations = []

        priority = {
            "High": "P1",
            "Medium": "P2",
            "Low": "P3"
        }.get(self.risk.get("risk_label", "Low"), "P3")

        # ======================================================
        # BGP
        # ======================================================

        if self._get("has_bgp", False):

            recommendations.append({

                "category": "Pre-Check",

                "action": "Verify current BGP neighbor status.",

                "reason": "Neighbor establishment validates routing health."

            })

            recommendations.append({

                "category": "Post-Validation",

                "action": "Confirm all BGP neighbors are established.",

                "reason": "Ensures routing convergence completed successfully."

            })

        # ======================================================
        # OSPF
        # ======================================================

        if self._get("has_ospf", False):

            recommendations.append({

                "category": "Post-Validation",

                "action": "Verify OSPF adjacency.",

                "reason": "Neighbor adjacency confirms topology stability."

            })

        # ======================================================
        # EIGRP
        # ======================================================

        if self._get("has_eigrp", False):

            recommendations.append({

                "category": "Post-Validation",

                "action": "Verify EIGRP neighbor status.",

                "reason": "Confirms routing convergence."

            })

        # ======================================================
        # Static Routes
        # ======================================================

        if self._get("static_route_count", 0):

            recommendations.append({

                "category": "Post-Validation",

                "action": "Validate static route reachability.",

                "reason": "Confirms expected forwarding behavior."

            })

        # ======================================================
        # ACL
        # ======================================================

        if self._get("acl_count", 0):

            recommendations.append({

                "category": "Implementation",

                "action": "Review ACL impact.",

                "reason": "ACL modifications may block production traffic."

            })

        # ======================================================
        # VRF
        # ======================================================

        if self._get("vrf_count", 0):

            recommendations.append({

                "category": "Post-Validation",

                "action": "Verify VRF routing tables.",

                "reason": "Ensures traffic isolation remains intact."

            })

        # ======================================================
        # NAT
        # ======================================================

        if self._get("has_nat", False):

            recommendations.append({

                "category": "Post-Validation",

                "action": "Validate NAT translations.",

                "reason": "Confirms expected address translation."

            })

        # ======================================================
        # QoS
        # ======================================================

        if self._get("has_qos", False):

            recommendations.append({

                "category": "Post-Validation",

                "action": "Validate QoS policies.",

                "reason": "Ensures traffic prioritization remains intact."

            })

        # ======================================================
        # Generic Recommendations
        # ======================================================

        recommendations.extend([

            {

                "category": "Pre-Check",

                "action": "Capture configuration snapshot.",

                "reason": "Provides rollback baseline."

            },

            {

                "category": "Implementation",

                "action": "Record implementation timestamps.",

                "reason": "Improves auditability."

            },

            {

                "category": "Monitoring",

                "action": "Monitor CPU, memory and interface health after change.",

                "reason": "Detect abnormal behavior early."

            },

            {

                "category": "Rollback",

                "action": "Keep rollback configuration ready.",

                "reason": "Reduces recovery time if validation fails."

            }

        ])

        return {

            "priority": priority,

            "recommendation_count": len(recommendations),

            "recommendations": recommendations

        }