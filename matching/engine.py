from datetime import timedelta

from django.utils import timezone

from internships.models import InternshipListing
from matching.models import MatchRecord


def _split_interests(value):
    return {item.strip().lower() for item in value.split(",") if item.strip()}


def calculate_match(student, internship):
    student_skills = {skill.name.lower() for skill in student.skills.all()}
    required_skills = {skill.name.lower() for skill in internship.required_skills.all()}
    overlapping_skills = student_skills & required_skills
    skill_score = (len(overlapping_skills) / len(required_skills) * 40) if required_skills else 20

    interests = _split_interests(student.interests)
    domain_score = 25 if internship.domain.lower() in interests else 0

    location_score = 15 if student.preferred_location.lower() in internship.location.lower() else 0
    if not student.preferred_location:
        location_score = 8

    availability_score = 0
    if student.availability_start and student.availability_end:
        internship_end = internship.start_date + timedelta(weeks=internship.duration_weeks)
        if student.availability_start <= internship.start_date and student.availability_end >= internship_end:
            availability_score = 10
    else:
        availability_score = 5

    requirements_score = 10 if internship.available_positions > 0 and not internship.is_expired else 0
    total = round(skill_score + domain_score + location_score + availability_score + requirements_score)

    reasons = []
    if overlapping_skills:
        reasons.append(f"Skills matched: {', '.join(sorted(overlapping_skills))}.")
    if domain_score:
        reasons.append(f"Domain matched student interest in {internship.domain}.")
    if location_score >= 15:
        reasons.append(f"Location aligns with preference: {student.preferred_location}.")
    if availability_score == 10:
        reasons.append("Student availability covers the internship duration.")
    if requirements_score:
        reasons.append("Internship is open and has available positions.")
    if not reasons:
        reasons.append("General recommendation based on available approved internships.")
    return min(total, 100), " ".join(reasons)


def generate_matches_for_student(student, persist=True):
    results = []
    internships = (
        InternshipListing.objects.filter(status=InternshipListing.Status.APPROVED)
        .prefetch_related("required_skills")
        .select_related("employer")
    )
    for internship in internships:
        score, explanation = calculate_match(student, internship)
        item = {"internship": internship, "score": score, "explanation": explanation}
        results.append(item)
        if persist:
            MatchRecord.objects.update_or_create(
                student=student,
                internship=internship,
                defaults={"score": score, "explanation": explanation, "created_at": timezone.now()},
            )
    return sorted(results, key=lambda item: item["score"], reverse=True)
