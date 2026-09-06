from backend.models import Resource

resources = [
    Resource(
        id="R001",
        name="Textile Recycling Unit",
        resource_type="facility",
        description="Facility that can process textile waste into reusable material.",
        location="Surat"
    ),
    Resource(
        id="R002",
        name="Agricultural Data Repository",
        resource_type="data",
        description="Dataset containing agricultural and crop information for Gujarat.",
        location="Ahmedabad"
    ),
    Resource(
        id="R003",
        name="Community Learning Centre",
        resource_type="space",
        description="Community space available for weekend education and outreach activities.",
        location="Gujarat"
    ),
]
