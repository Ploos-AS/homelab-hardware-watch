from __future__ import annotations

from hhw.ai_score import ai_host_action, score_ai_host
from hhw.enterprise_score import enterprise_action, score_enterprise
from hhw.models import Candidate
from hhw.runner_score import VALID_ROLES as RUNNER_ROLES
from hhw.runner_score import runner_action, score_runner
from hhw.switch_score import managed_switch_action, score_managed_switch
from hhw.ups_score import score_ups, ups_action


ENTERPRISE_ROLES = {"proxmox_compute", "storage"}
SPECIAL_ROLES = {"ai_server", "ai_host", "managed_switch", "ups"}
VALID_ROLES = ENTERPRISE_ROLES | RUNNER_ROLES | SPECIAL_ROLES


def decide(candidate: Candidate, role: str) -> dict:
    """Return one consistent BUY/WATCH/PASS decision for a hardware role."""
    if role in ENTERPRISE_ROLES:
        result = score_enterprise(candidate, role)
        action = enterprise_action(result)
    elif role in RUNNER_ROLES:
        result = score_runner(candidate, role)
        action = runner_action(result)
    elif role in {"ai_server", "ai_host"}:
        result = score_ai_host(candidate)
        if role == "ai_server":
            result = {**result, "role": "ai_server"}
        action = ai_host_action(result)
    elif role == "managed_switch":
        result = score_managed_switch(candidate)
        action = managed_switch_action(result)
    elif role == "ups":
        result = score_ups(candidate)
        action = ups_action(result)
    else:
        raise ValueError(f"unknown decision role: {role}")

    return {
        **result,
        "action": action,
    }
