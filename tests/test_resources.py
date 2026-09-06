from backend.models import Resource

from data.resources import resources

print(f"Total resources: {len(resources)}")

for resource in resources:
    print(f"{resource.id} | {resource.name} | {resource.location}")
