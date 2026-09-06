from backend.resource_matching import find_resource_matches

def enrich_query_results(results):
    enriched = []

    for result in results:
        match = result["match"]

        if match["target_type"] == "Problem":
            problem = next(
                (problem for problem in problems if problem.id == match["target_id"]),
                None
            )

            if problem:
                result["resources"] = find_resource_matches(problem)

        enriched.append(result)

    return enriched
