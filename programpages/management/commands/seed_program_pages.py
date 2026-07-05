"""
Seed the 7 program detail pages with starter content, so /programs/<slug>
isn't blank before real content is added from the dashboard.

Usage (from the backend/ directory):

    python manage.py seed_program_pages
    python manage.py seed_program_pages --replace   # overwrite existing pages
"""
from __future__ import annotations

from datetime import date

from django.core.management.base import BaseCommand

from programpages.models import ProgramPage, ProgramObjective, ProgramStat

SEED_YEAR = date.today().year

PAGES = [
    {
        "slug": "reunion",
        "title": "Annual Reunion",
        "tagline": "One evening, hundreds of members, a lifetime of memories.",
        "overview": (
            "The Annual Reunion is PUSAB's flagship gathering — the one evening each year when "
            "members from every batch and every university come back to Bishwambarpur to "
            "reconnect. It brings together cross-batch networking, recognition of the year's "
            "achievers, and a cultural programme that closes out the night."
        ),
        "eligibility": "Open to all PUSAB members, alumni, and their families.",
        "process": (
            "Registration opens a few weeks before the event through the PUSAB group and social "
            "pages. Members confirm attendance, and the organizing committee handles venue, "
            "catering and the programme lineup."
        ),
        "schedule_note": "Held once a year, typically in December.",
        "objectives": [
            ("Cross-batch networking", "Connect members across different universities and graduation years."),
            ("Recognise achievers", "Honour members who brought pride to Bishwambarpur that year."),
            ("Cultural programme", "An evening of performances, games and shared food."),
        ],
        "stats": [("Members attending", "500+"), ("Years running", "10+")],
    },
    {
        "slug": "schooling",
        "title": "Schooling Program",
        "tagline": "Free tutoring and mentoring for the upazila's school students.",
        "overview": (
            "PUSAB members run free tutoring and mentoring sessions for school students across "
            "Bishwambarpur — helping with coursework, exam prep, and early career guidance from "
            "students who've walked the same path."
        ),
        "eligibility": "Open to school students (classes VI–X) in Bishwambarpur Upazila.",
        "process": (
            "Sessions are organised through local schools in coordination with teachers and "
            "guardians. Volunteers are drawn from PUSAB's university-student membership."
        ),
        "schedule_note": "Weekly sessions, running throughout the academic year.",
        "objectives": [
            ("Academic support", "Tutoring in core subjects for school students."),
            ("Career mentoring", "Early exposure to higher-education and career paths."),
            ("Olympiad preparation", "Guidance for students competing in academic olympiads."),
        ],
        "stats": [("Schools covered", "12"), ("Format", "Weekly")],
    },
    {
        "slug": "scholarship",
        "title": "PUSAB Scholarship",
        "tagline": "Merit and need-based support for deserving students.",
        "overview": (
            "The PUSAB Scholarship provides financial aid to deserving students from underserved "
            "families in Bishwambarpur. Alongside the scholarship, PUSAB also arranges a "
            "Scholarship Exam for students of classes VIII, IX and X to identify and support "
            "promising talent early."
        ),
        "eligibility": (
            "Students of classes VIII, IX and X from Bishwambarpur Upazila are eligible to sit "
            "the Scholarship Exam. Financial aid is awarded on a mix of merit and need."
        ),
        "process": (
            "Applications open annually. Eligible students sit the Scholarship Exam; results and "
            "awards are announced afterward, with stipends disbursed directly."
        ),
        "schedule_note": "Applications open once a year — watch PUSAB's pages for the exact date.",
        "objectives": [
            ("Scholarship Exam", "An annual exam for students of classes VIII, IX and X."),
            ("Need-based aid", "Financial support prioritising underserved families."),
            ("Mentor pairing", "Awardees are paired with a PUSAB member mentor."),
        ],
        "stats": [("Classes eligible", "VIII–X"), ("Disbursed", "Annually")],
    },
    {
        "slug": "humanity",
        "title": "PUSAB for Humanity",
        "tagline": "Standing with Bishwambarpur through floods, illness and hardship.",
        "overview": (
            "PUSAB for Humanity is the association's humanitarian response arm — organising "
            "disaster relief, free medical camps and blanket distribution whenever the community "
            "needs it most, particularly during Sunamganj's recurring floods."
        ),
        "eligibility": "Relief and aid are directed at flood-affected and underserved families in Bishwambarpur Upazila.",
        "process": (
            "Members mobilise quickly during emergencies — coordinating collections, relief "
            "packages and on-the-ground distribution, often alongside local volunteers."
        ),
        "schedule_note": "Activated as needed — flood season relief, and periodic medical camps.",
        "objectives": [
            ("Flood relief", "Emergency food, shelter and support during flooding."),
            ("Medical camps", "Free health check-ups and medicine for the community."),
            ("Blanket & winter aid", "Distribution during the cold season for those in need."),
        ],
        "stats": [("Families helped", "100s"), ("Response", "Rapid")],
    },
    {
        "slug": "picnic",
        "title": "Annual Picnic",
        "tagline": "A full day outdoors, games, and food across generations of members.",
        "overview": (
            "The Annual Picnic is a lighter, family-friendly counterpart to the Reunion — a "
            "full day out with games, shared meals and casual bonding across generations of "
            "PUSAB members, usually somewhere scenic near Sunamganj."
        ),
        "eligibility": "Open to all PUSAB members and their families.",
        "process": "Members register ahead through the PUSAB group; the organizing team handles transport and venue.",
        "schedule_note": "Usually held once a year, in the winter months.",
        "objectives": [
            ("Community bonding", "A relaxed day for members and families to connect."),
            ("Games & activities", "Outdoor games and friendly competitions for all ages."),
        ],
        "stats": [("Format", "Full-day"), ("Held", "Annually")],
    },
    {
        "slug": "online",
        "title": "Online Events",
        "tagline": "Webinars and AMAs that reach members wherever they are.",
        "overview": (
            "PUSAB runs a rolling calendar of online events — career webinars, admission AMAs, "
            "and one-to-one mentoring sessions — so members and aspirants can get guidance no "
            "matter where they are."
        ),
        "eligibility": "Open to PUSAB members and Bishwambarpur students preparing for admissions or careers.",
        "process": "Sessions are announced through PUSAB's social pages and group; joining links are shared ahead of each event.",
        "schedule_note": "Monthly AMAs, plus occasional special webinars.",
        "objectives": [
            ("Admission mentoring", "One-to-one guidance for university aspirants."),
            ("Career webinars", "Live Q&A with alumni across different professions."),
        ],
        "stats": [("Frequency", "Monthly"), ("Reach", "Online")],
    },
    {
        "slug": "felicitation",
        "title": "Felicitation & Freshers' Reception",
        "tagline": "Honouring achievers, welcoming the next generation — one stage, two celebrations.",
        "overview": (
            "Each year PUSAB brings achievers and new entrants onto one stage — recognising "
            "members who carry Bishwambarpur's name forward, and formally welcoming freshers "
            "just beginning their university journey."
        ),
        "eligibility": "Achievers are selected by merit; all incoming freshers from Bishwambarpur are welcomed.",
        "process": "Held as a single combined ceremony, usually timed around the start of a new academic session.",
        "schedule_note": "Once a year, timed with the new academic session.",
        "objectives": [
            ("Felicitate achievers", "Recognise members who achieved academic or professional milestones."),
            ("Welcome freshers", "Formally welcome new students into the PUSAB family."),
        ],
        "stats": [("Ceremony", "Combined"), ("Held", "Annually")],
    },
]


class Command(BaseCommand):
    help = "Seed the 7 program detail pages with starter content."

    def add_arguments(self, parser):
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Overwrite existing pages (and their objectives/stats) instead of skipping them.",
        )

    def handle(self, *args, **options):
        replace = options["replace"]
        created, skipped = 0, 0

        for data in PAGES:
            slug = data["slug"]
            existing = ProgramPage.objects.filter(slug=slug, year=SEED_YEAR).first()
            if existing and not replace:
                skipped += 1
                continue

            if existing:
                existing.objectives.all().delete()
                existing.stats.all().delete()
                page = existing
            else:
                page = ProgramPage(slug=slug, year=SEED_YEAR)

            page.title = data["title"]
            page.tagline = data["tagline"]
            page.overview = data["overview"]
            page.eligibility = data["eligibility"]
            page.process = data["process"]
            page.schedule_note = data["schedule_note"]
            page.save()

            for i, (title, desc) in enumerate(data["objectives"]):
                ProgramObjective.objects.create(page=page, title=title, description=desc, order=i)
            for i, (label, value) in enumerate(data["stats"]):
                ProgramStat.objects.create(page=page, label=label, value=value, order=i)

            created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created} program page(s), skipped {skipped}."))
