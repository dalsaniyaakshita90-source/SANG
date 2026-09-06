from data.resources import resources

def find_resource_matches(target):
    matches = []

    target_location = target.location.lower()

    for resource in resources:
        resource_location = resource.location.lower()

        if resource_location == target_location:
            matches.append({
                "resource_id": resource.id,
                "resource_name": resource.name,
                "resource_type": resource.resource_type,
                "location": resource.location,
                "reason": "Location match"
            })

        elif resource_location == "gujarat" or target_location == "gujarat":
            matches.append({
                "resource_id": resource.id,
                "resource_name": resource.name,
                "resource_type": resource.resource_type,
                "location": resource.location,
                "reason": "Regional match"
            })

    return matches
