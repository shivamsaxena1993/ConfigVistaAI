"""
====================================================================
File: risk_engine.py

Project : ConfigVista AI

Purpose
-------
Rule-based Risk Prediction Engine.

Current:
    Rule-based scoring.

Future:
    Replace calculate() with ML model inference while keeping the
    output format unchanged.

====================================================================
"""


class RiskEngine:

    def __init__(self, features):
        """
        features may be:

        - dictionary (current implementation)

        Future:
        - FeatureModel
        """
        self.f = features

    # ----------------------------------------------------------
    # Safe Feature Access
    # ----------------------------------------------------------

    def _get(self, key, default=0):
        """
        Safely retrieve feature values.

        Prevents KeyError when a feature is missing.
        """

        if isinstance(self.f, dict):
            return self.f.get(key, default)

        return getattr(self.f, key, default)

    # ----------------------------------------------------------
    # Risk Calculation
    # ----------------------------------------------------------

    def calculate(self):

        score = 0

        explanations = []

        # ======================================================
        # Routing Protocols
        # ======================================================

        routing_rules = [

            (
                "has_bgp",
                20,
                "BGP",
                "Major",
                "BGP changes may impact routing convergence."
            ),

            (
                "has_ospf",
                10,
                "OSPF",
                "Moderate",
                "OSPF topology changes require adjacency validation."
            ),

            (
                "has_eigrp",
                8,
                "EIGRP",
                "Moderate",
                "EIGRP configuration affects route exchange."
            ),

            (
                "has_rip",
                5,
                "RIP",
                "Low",
                "Legacy routing protocol detected."
            )

        ]

        for feature, points, name, impact, reason in routing_rules:

            if self._get(feature, False):

                score += points

                explanations.append({

                    "factor": name,

                    "impact": impact,

                    "score": points,

                    "reason": reason

                })

        # ======================================================
        # Interfaces
        # ======================================================

        interface_count = self._get("interface_count", 0)

        interface_score = min(interface_count, 20)

        score += interface_score

        explanations.append({

            "factor": "Interfaces",

            "impact": "Minor",

            "score": interface_score,

            "reason": f"{interface_count} interfaces detected."

        })

        # ======================================================
        # ACL
        # ======================================================

        acl_count = self._get("acl_count", 0)

        acl_score = acl_count * 2

        if acl_score:

            score += acl_score

            explanations.append({

                "factor": "ACL",

                "impact": "Moderate",

                "score": acl_score,

                "reason": "ACL configuration increases policy complexity."

            })

        # ======================================================
        # Static Routes
        # ======================================================

        static_routes = self._get("static_route_count", 0)

        static_score = static_routes * 2

        if static_score:

            score += static_score

            explanations.append({

                "factor": "Static Routes",

                "impact": "Moderate",

                "score": static_score,

                "reason": "Static routing affects forwarding decisions."

            })

        # ======================================================
        # Route Maps
        # ======================================================

        route_maps = self._get("route_map_count", 0)

        route_map_score = route_maps * 3

        if route_map_score:

            score += route_map_score

            explanations.append({

                "factor": "Route Maps",

                "impact": "Moderate",

                "score": route_map_score,

                "reason": "Routing policy manipulation detected."

            })

        # ======================================================
        # VRFs
        # ======================================================

        vrf_count = self._get("vrf_count", 0)

        vrf_score = vrf_count * 4

        if vrf_score:

            score += vrf_score

            explanations.append({

                "factor": "VRF",

                "impact": "Moderate",

                "score": vrf_score,

                "reason": "Multiple VRFs increase routing complexity."

            })

        # ======================================================
        # QoS
        # ======================================================

        if self._get("has_qos", False):

            score += 5

            explanations.append({

                "factor": "QoS",

                "impact": "Minor",

                "score": 5,

                "reason": "QoS policies require careful validation."

            })

        # ======================================================
        # NAT
        # ======================================================

        if self._get("has_nat", False):

            score += 5

            explanations.append({

                "factor": "NAT",

                "impact": "Moderate",

                "score": 5,

                "reason": "NAT configuration can affect application reachability."

            })

        # ======================================================
        # VPN
        # ======================================================

        if self._get("has_vpn", False):

            score += 6

            explanations.append({

                "factor": "VPN",

                "impact": "Moderate",

                "score": 6,

                "reason": "VPN changes may impact remote connectivity."

            })

        # ======================================================
        # Complexity
        # ======================================================

        complexity = self._get("complexity_score", 0)

        if complexity > 70:

            score += 10

            explanations.append({

                "factor": "Configuration Complexity",

                "impact": "Moderate",

                "score": 10,

                "reason": "Large configuration footprint detected."

            })

        # ======================================================
        # Final Score
        # ======================================================

        score = min(score, 100)

        if score >= 70:
            label = "High"

        elif score >= 40:
            label = "Medium"

        else:
            label = "Low"

        confidence = round(

            min(
                60 + score * 0.4,
                98
            ),

            2

        )

        return {

            "risk_score": score,

            "risk_label": label,

            "confidence_score": confidence,

            "summary": f"{label} Risk Change",

            "explanations": explanations

        }