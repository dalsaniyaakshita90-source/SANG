from backend.models import Person, Problem, Opportunity, Resource


farmers = [
    Person(
        id="F001",
        name="Ramesh",
        location="Rajkot",
        skills=["farming"],
        interests=["agriculture"],
        availability="full-time",
    ),
    Person(
        id="F002",
        name="Meena",
        location="Ahmedabad",
        skills=["farming"],
        interests=["agriculture", "sustainability"],
        availability="full-time",
    ),
    Person(
        id="F003",
        name="Arjun",
        location="Surat",
        skills=["farming"],
        interests=["agriculture"],
        availability="full-time",
    ),
]


problems = [
    Problem(
        id="AP001",
        title="Crop Pest Infestation",
        description="Farmer reports pest damage affecting crops.",
        organization="SANG Agriculture Network",
        location="Rajkot",
        required_skills=["agriculture", "pest management"],
        category="agriculture",
    ),
    Problem(
        id="AP002",
        title="Irrigation Challenge",
        description="Farmer needs help improving water management.",
        organization="SANG Agriculture Network",
        location="Ahmedabad",
        required_skills=["agriculture", "water management"],
        category="agriculture",
    ),
    Problem(
        id="AP003",
        title="Soil Health Problem",
        description="Farmer needs support understanding declining soil quality.",
        organization="SANG Agriculture Network",
        location="Surat",
        required_skills=["agriculture", "soil management"],
        category="agriculture",
    ),
]


helpers = [
    Person(
        id="H001",
        name="Agricultural Extension Worker",
        location="Rajkot",
        skills=["agriculture", "pest management"],
        interests=["agriculture"],
        availability="full-time",
    ),
    Person(
        id="H002",
        name="Water Management Specialist",
        location="Ahmedabad",
        skills=["agriculture", "water management"],
        interests=["agriculture", "sustainability"],
        availability="full-time",
    ),
    Person(
        id="H003",
        name="Soil Health Specialist",
        location="Surat",
        skills=["agriculture", "soil management"],
        interests=["agriculture", "sustainability"],
        availability="full-time",
    ),
]


opportunities = [
    Opportunity(
        id="AO001",
        title="Small Farmer Irrigation Support",
        description="Support opportunity for farmers seeking improved irrigation practices.",
        organization="Agriculture Support Network",
        location="Ahmedabad",
        required_skills=["agriculture", "water management"],
        eligibility=["smallholder farmer"],
        category="agriculture",
    ),
    Opportunity(
        id="AO002",
        title="Sustainable Farming Support",
        description="Opportunity focused on sustainable agricultural practices.",
        organization="Sustainable Agriculture Network",
        location="Rajkot",
        required_skills=["agriculture", "sustainability"],
        eligibility=["smallholder farmer"],
        category="agriculture",
    ),
]


resources = [
    Resource(
        id="AR001",
        name="Crop Pest Management Guide",
        resource_type="guide",
        description="Practical information for identifying and managing common crop pests.",
        location="Rajkot",
    ),
    Resource(
        id="AR002",
        name="Water-Efficient Irrigation Guide",
        resource_type="guide",
        description="Information about water-efficient irrigation practices.",
        location="Ahmedabad",
    ),
    Resource(
        id="AR003",
        name="Soil Health Management Guide",
        resource_type="guide",
        description="Basic guidance for monitoring and improving soil health.",
        location="Surat",
    ),
]