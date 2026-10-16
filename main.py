"""
SEO Backlink Quality & Link Farm Detector
Author: Linkoster (Rajesh Kumar Nitharwal)
License: MIT
"""

import sys
from typing import Dict, Any


class BacklinkAuditor:
    """
    Audits domain targets for SEO quality, distinguishing between true authority
    and artificial/inflated Domain Rating (DR) link farms.
    """

    def __init__(self, min_organic_traffic: int = 2000, max_outbound_ratio: float = 0.35):
        self.min_organic_traffic = min_organic_traffic
        self.max_outbound_ratio = max_outbound_ratio

    def audit_domain(self, domain_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates a target domain based on traffic, DR, and outbound link health.
        
        :param domain_data: Dictionary containing domain metrics
        :return: Audit decision and risk breakdown
        """
        domain = domain_data.get("domain", "Unknown")
        dr = domain_data.get("domain_rating", 0)
        organic_traffic = domain_data.get("monthly_organic_traffic", 0)
        outbound_link_ratio = domain_data.get("outbound_link_ratio", 1.0)
        spam_flags = domain_data.get("spam_niches_detected", False)

        risk_score = 0
        reasons = []

        # 1. Traffic vs. DR Discrepancy Check (Inflated Domain Check)
        if dr >= 50 and organic_traffic < self.min_organic_traffic:
            risk_score += 50
            reasons.append(f"High DR ({dr}) but low organic traffic ({organic_traffic}). Likely inflated/PBN.")

        # 2. Outbound Link Ratio Check
        if outbound_link_ratio > self.max_outbound_ratio:
            risk_score += 25
            reasons.append(f"Excessive outbound link ratio ({outbound_link_ratio:.2f}). High link dilution.")

        # 3. Niche Spam Check
        if spam_flags:
            risk_score += 30
            reasons.append("Topical contamination detected (Casino/Crypto/Essay link mill patterns).")

        # Decision Logic
        is_approved = risk_score < 40

        return {
            "domain": domain,
            "approved": is_approved,
            "risk_score": min(risk_score, 100),
            "status": "APPROVED" if is_approved else "REJECTED",
            "reasons": reasons if reasons else ["Clean domain profile with verified search traffic."]
        }


if __name__ == "__main__":
    # Sample test dataset representing target publishing domains
    sample_targets = [
        {
            "domain": "tech-authority-journal.com",
            "domain_rating": 68,
            "monthly_organic_traffic": 14500,
            "outbound_link_ratio": 0.18,
            "spam_niches_detected": False
        },
        {
            "domain": "cheap-guest-post-farm.net",
            "domain_rating": 72,
            "monthly_organic_traffic": 120,  # High DR, no traffic = Red Flag
            "outbound_link_ratio": 0.65,
            "spam_niches_detected": True
        }
    ]

    auditor = BacklinkAuditor()
    print("\n--- B2B SEO Backlink Audit Results ---\n")

    for target in sample_targets:
        result = auditor.audit_domain(target)
        print(f"Domain: {result['domain']}")
        print(f"Status: [{result['status']}] (Risk Score: {result['risk_score']}/100)")
        print("Audit Notes:")
        for note in result["reasons"]:
            print(f" - {note}")
        print("-" * 50)
