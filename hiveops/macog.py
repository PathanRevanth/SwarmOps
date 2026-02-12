from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class IacPlan:
    provider: str
    architecture: str
    terraform: str
    policy_checks: list[str]
    estimated_monthly_cost_usd: int


class MacogGenerator:
    """Phase 3: simplified multi-agent IaC generation surface."""

    def generate(self, intent: str, provider: str = "aws") -> IacPlan:
        intent_l = intent.lower()
        high_availability = any(t in intent_l for t in ("ha", "high availability", "multi-az"))

        architecture = "multi_az_web_app" if high_availability else "single_region_web_app"
        replicas = 3 if high_availability else 2
        monthly_cost = 1800 if high_availability else 900

        terraform = f'''resource "{provider}_vpc" "main" {{
  cidr_block = "10.0.0.0/16"
}}

resource "{provider}_ecs_service" "api" {{
  desired_count = {replicas}
}}
'''

        policy_checks = [
            "opa:no_public_s3_buckets",
            "opa:encryption_at_rest_required",
            "sentinel:approved_instance_families",
        ]

        return IacPlan(
            provider=provider,
            architecture=architecture,
            terraform=terraform,
            policy_checks=policy_checks,
            estimated_monthly_cost_usd=monthly_cost,
        )
