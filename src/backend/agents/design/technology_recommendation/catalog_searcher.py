from __future__ import annotations

from typing import Any, List, Dict, Optional


def search_catalog(domain: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return a deterministic list of candidate technologies for the domain.

    In production this would query a knowledge catalog via `context.knowledge`.
    Here we return curated examples with citations.
    """
    base = [
        {
            "id": "tech-redis",
            "name": "Redis",
            "maturity": 0.9,
            "fit": 0.8,
            "citation": "catalog:cache#redis",
        },
        {
            "id": "tech-postgres",
            "name": "Postgres",
            "maturity": 0.95,
            "fit": 0.9,
            "citation": "catalog:db#postgres",
        },
        {
            "id": "tech-kafka",
            "name": "Kafka",
            "maturity": 0.8,
            "fit": 0.7,
            "citation": "catalog:stream#kafka",
        },
    ]
    if domain and "analytics" in domain.lower():
        base.append(
            {
                "id": "tech-spark",
                "name": "Spark",
                "maturity": 0.7,
                "fit": 0.85,
                "citation": "catalog:compute#spark",
            }
        )
    return base
