"""Reproduce the old preflight/unconditional-write race in local memory."""
import copy
import json

import hearth
import agent_python_runner as runner


def example_request(request_id):
    return {
        "schema": "HEARTH_REQUEST_V1", "request_id": request_id,
        "action": "research_cycle", "expected_revision": 0,
        "payload": {
            "topic": "Synthetic concurrent research registration",
            "trace": {f"H{i}": {"text": f"fixture {i}"} for i in range(10)},
        },
    }


def reproduce():
    base = hearth.default_state("demo")
    plans = []
    for request_id in ("writer-a", "writer-b"):
        plans.append(runner.build_commit_plan({
            "schema": "HEARTH_AGENT_BATCH_V1", "state": copy.deepcopy(base),
            "inbox_rows": [{"row": 2, "request_id": request_id,
                            "status": "PENDING", "request_json": example_request(request_id)}],
        }))
    preflight = [runner.classify_commit_state(p, base) for p in plans]
    shared = copy.deepcopy(plans[0]["final_state"])
    shared = copy.deepcopy(plans[1]["final_state"])
    return {"preflight": preflight,
            "lost_first_request": "writer-a" not in shared["processed_request_ids"],
            "final_ids": shared["processed_request_ids"],
            "scope": "in-memory unconditional-write host model"}


if __name__ == "__main__":
    print(json.dumps(reproduce(), indent=2))
