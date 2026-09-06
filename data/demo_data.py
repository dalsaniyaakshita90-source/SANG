from backend.models import Person, Problem, Opportunity


people = [
    Person(
        id="P001",
        name="Priya",
        location="Surat",
        skills=["textile design", "sustainability", "graphic design"],
        interests=["circular economy", "social innovation"],
        availability="project-based"
    ),
    Person(
        id="P002",
        name="Rahul",
        location="Ahmedabad",
        skills=["Python", "data analysis", "machine learning"],
        interests=["AI", "agriculture"],
        availability="part-time"
    ),
    Person(
        id="P003",
        name="Meera",
        location="Rajkot",
        skills=["teaching", "Gujarati", "community outreach"],
        interests=["education", "rural development"],
        availability="weekends"
    )
]


problems = [
    Problem(
        id="PR001",
        title="Textile Waste Challenge",
        description="Find ways to reduce textile waste from production.",
        organization="Surat Textile Business",
        location="Surat",
        required_skills=["textile design", "sustainability"],
        category="sustainability"
    ),
    Problem(
        id="PR002",
        title="Agricultural Data Problem",
        description="Analyze agricultural data to improve decision-making.",
        organization="Gujarat Agriculture Initiative",
        location="Ahmedabad",
        required_skills=["Python", "data analysis"],
        category="agriculture"
    )
]


opportunities = [
    Opportunity(
        id="O001",
        title="Circular Economy Student Project",
        description="Student project focused on textile waste and circular economy.",
        organization="Innovation Lab",
        location="Surat",
        required_skills=["textile design", "sustainability"],
        eligibility=["students"],
        category="sustainability"
    )
]
