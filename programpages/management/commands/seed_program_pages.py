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

from programpages.models import ProgramPage, ProgramObjective, ProgramInfoItem, ProgramStat, ProgramWebinar

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
        "event_date": "December, Every Year",
        "venue": "Bishwambarpur, Sunamganj",
        "event_time": "6:00 PM – 11:00 PM",
        "register_label": "Register for Reunion",
        "cta_title": "Be Part of the Tradition",
        "cta_subtitle": "Register now and make this reunion our most memorable yet!",
        "objectives": [
            ("Reconnect", "Catch up with old friends and expand your network.", "users"),
            ("Inspiring Talks", "Engage with thought leaders and alumni achievers.", "mic"),
            ("Memorable Moments", "Enjoy entertainment, group activities and more.", "camera"),
            ("Alumni Recognition", "Honoring outstanding alumni and their contributions.", "award"),
            ("Dinner & Networking", "Share a meal and build meaningful connections.", "utensils"),
            ("Surprises & More", "Exciting surprises and memorable keepsakes.", "gift"),
        ],
        "stats": [
            ("Members attending", "500+"),
            ("Universities", "66"),
            ("Total Alumni Network", "67,777+"),
            ("Years of Reunion", "10+"),
        ],
    },
    {
        "slug": "schooling",
        "title": "Schooling Program",
        "tagline": "Empowering underprivileged students by making quality education accessible, inclusive, and sustainable.",
        "overview": (
            "PUSAB's Schooling Program is dedicated to providing financial support, learning "
            "materials, and a nurturing environment for students from underprivileged backgrounds.\n\n"
            "We work with schools, volunteers, and donors to ensure that every child can continue "
            "their education and dream of a better tomorrow."
        ),
        "eligibility": "Open to school students (classes VI–X) in Bishwambarpur Upazila.",
        "process": (
            "Sessions are organised through local schools in coordination with teachers and "
            "guardians. Volunteers are drawn from PUSAB's university-student membership."
        ),
        "schedule_note": "Weekly sessions, running throughout the academic year.",
        "register_label": "Learn More About Our Work",
        "cta_title": "Be a Part of Their Journey",
        "cta_subtitle": "Your support can help a child stay in school and build a better future.",
        "objectives": [
            ("Access to Education", "Ensuring every child gets the opportunity to learn.", "graduation-cap"),
            ("Support & Mentorship", "Guiding students to build skills and confidence.", "users"),
            ("Better Future", "Creating a generation of responsible leaders.", "sparkles"),
        ],
        "info_items": [
            ("graduation-cap", "Program Type", "Education Support"),
            ("users", "Beneficiaries", "School Students"),
            ("target", "Focus Areas", "Tuition Support, Books, School Supplies, Mentorship"),
            ("map-pin", "Coverage", "Bishwambarpur & Surrounding Areas"),
            ("users", "Target Group", "Underprivileged Students"),
            ("calendar", "Program Since", "2016"),
        ],
        "stats": [
            ("Students Supported", "850+"),
            ("Schools Reached", "120+"),
            ("Volunteers Involved", "200+"),
            ("Books & Supplies Distributed", "15,000+"),
            ("Students Continuing Education", "95%"),
        ],
    },
    {
        "slug": "scholarship",
        "title": "PUSAB Scholarship",
        "tagline": (
            "Empowering underprivileged and meritorious students to pursue higher education and "
            "become future leaders."
        ),
        "overview": (
            "The PUSAB Scholarship Program was established to support bright and motivated "
            "students from underprivileged backgrounds.\n\n"
            "We believe that financial limitations should never be a barrier to education.\n\n"
            "Through this program, we provide financial assistance, learning resources and "
            "continuous encouragement to help students achieve their academic goals and become "
            "future leaders."
        ),
        "eligibility": (
            "Underprivileged students with strong academic potential, currently enrolled in "
            "school, college or university, are eligible to apply."
        ),
        "process": (
            "Check the eligibility criteria carefully. Fill out the application form with "
            "required documents. Our team will review your application. Successful candidates "
            "will be notified and awarded."
        ),
        "schedule_note": "Applications open once a year — watch PUSAB's pages for the exact date.",
        "register_label": "Apply Now",
        "cta_title": "Your support can empower a student's future.",
        "cta_subtitle": "Contribute today and help create a better tomorrow.",
        "objectives": [
            ("Empower Education", "Removing financial barriers to education.", "graduation-cap"),
            ("Recognize Merit", "Rewarding hard work, dedication and potential.", "users"),
            ("Build Leaders", "Shaping confident individuals for a better tomorrow.", "award"),
        ],
        "info_items": [
            ("graduation-cap", "Who Can Apply?", "Underprivileged students with strong academic potential."),
            ("target", "What We Cover", "Tuition fees, books, supplies and other education expenses."),
            ("users", "Selection Process", "Application review, academic evaluation and interview."),
            ("award", "Renewal", "Based on academic performance and continued need."),
            ("users", "Mentorship", "Guidance from senior members and professionals."),
            ("sparkles", "More Than Scholarship", "Building confidence, leadership and a brighter tomorrow."),
        ],
        "stats": [
            ("Scholarships Awarded", "300+"),
            ("Educational Institutions", "20+"),
            ("Current Scholars", "50+"),
            ("Years of Impact", "8+"),
            ("Students Continuing Their Education", "95%"),
        ],
    },
    {
        "slug": "humanity",
        "title": "PUSAB for Humanity",
        "tagline": (
            "A movement of empathy, service and solidarity working towards a better and more "
            "compassionate society for all."
        ),
        "overview": (
            "PUSAB for Humanity is our promise to give back to society. Through collective "
            "efforts, we work for the welfare of underprivileged people and create opportunities "
            "for a dignified life.\n\n"
            "From food and relief distribution to education, health and environment initiatives, "
            "every effort is powered by PUSAB members and the partners who stand with us."
        ),
        "eligibility": "Relief and aid are directed at flood-affected and underserved families in Bishwambarpur Upazila.",
        "process": (
            "Members mobilise quickly during emergencies — coordinating collections, relief "
            "packages and on-the-ground distribution, often alongside local volunteers."
        ),
        "schedule_note": "Activated as needed — flood season relief, and periodic medical camps.",
        "register_label": "Learn More About Our Work",
        "cta_title": "Be a Part of the Change",
        "cta_subtitle": "Your small act of kindness can make a big difference in someone's life.",
        "objectives": [
            ("Serve", "Reaching out to those in need with care and compassion.", "heart"),
            ("Support", "Empowering communities through resources and human support.", "users"),
            ("Sustain", "Building a better future through sustainable and lasting impact.", "sparkles"),
        ],
        "info_items": [
            ("utensils", "Food & Relief Distribution", "Providing food, essentials, and emergency relief to families in need."),
            ("graduation-cap", "Education Support", "Helping underprivileged students with books, tuition support and learning resources."),
            ("heart", "Health & Blood Donation", "Organizing blood drives and health support programs for the well-being of communities."),
            ("sparkles", "Environment Care", "Promoting a cleaner and greener environment through awareness and action."),
            ("gift", "Clothing Support", "Distributing clothes and winter items to help people live with dignity."),
        ],
        "stats": [
            ("Lives Touched", "5000+"),
            ("Humanitarian Activities", "120+"),
            ("Community Partners", "50+"),
            ("Years of Service", "10+"),
            ("People Helped", "5000+"),
            ("Programs Conducted", "120+"),
            ("Districts Reached", "30+"),
            ("Volunteers", "200+"),
            ("Partner Organizations", "25+"),
        ],
    },
    {
        "slug": "picnic",
        "title": "Annual Picnic",
        "tagline": "A day of fun, friendship, and unforgettable memories with the PUSAB family.",
        "overview": (
            "The Annual Picnic is one of the most awaited events of PUSAB. It's a perfect "
            "opportunity to step away from the routine, enjoy nature, strengthen bonds, and "
            "create memories that last a lifetime."
        ),
        "eligibility": "All PUSAB members, alumni, and their families are warmly invited.",
        "process": "Members register ahead through the PUSAB group; the organizing team handles transport and venue.",
        "schedule_note": "Usually held once a year, in the winter months.",
        "event_date": "February, Every Year",
        "venue": "Narsingdi Recreation Park, Narsingdi",
        "event_time": "9:00 AM - 5:00 PM",
        "register_label": "Register Interest",
        "cta_title": "Let's make this picnic the best one yet!",
        "cta_subtitle": "Mark your calendar and get ready for a day full of joy and togetherness.",
        "objectives": [
            ("Build stronger connections", "", "users"),
            ("Enjoy games & fun", "", "music"),
            ("Delicious food & refreshments", "", "utensils"),
            ("A day full of smiles & memories", "", "heart"),
        ],
        "info_items": [
            ("target", "Exciting Games", "Fun outdoor games for all ages."),
            ("music", "Music & Entertainment", "Live music, DJ & entertaining performances."),
            ("utensils", "Delicious Food", "Tasty meals and snacks for everyone."),
            ("camera", "Photo Moments", "Capture beautiful memories together."),
            ("gift", "Lucky Draws", "Exciting prizes and surprises."),
            ("users", "Family Fun", "Activities for kids & family bonding."),
        ],
        "stats": [("Format", "Full-day"), ("Held", "Annually")],
    },
    {
        "slug": "iftar-mahfil",
        "title": "Iftar Mahfil",
        "tagline": "Breaking fast together, strengthening bonds of faith and friendship.",
        "overview": (
            "Every Ramadan, PUSAB brings members together for an evening Iftar Mahfil — a shared "
            "meal, reflection and community, right as the day's fast comes to an end."
        ),
        "eligibility": "Open to all PUSAB members, alumni, and their families.",
        "process": "Members register ahead through the PUSAB group; the organizing team handles venue and catering.",
        "schedule_note": "Held once a year, during Ramadan.",
        "event_date": "Ramadan, Every Year",
        "venue": "Bishwambarpur, Sunamganj",
        "event_time": "Just before Maghrib",
        "register_label": "Register Interest",
        "cta_title": "Join us this Ramadan for an evening of togetherness.",
        "cta_subtitle": "Mark your calendar and break your fast with the PUSAB family.",
        "objectives": [
            ("Shared Iftar", "Breaking fast together as one PUSAB family.", "utensils"),
            ("Community Bonding", "Strengthening ties among members and alumni.", "users"),
            ("Reflection & Dua", "A moment of gratitude and collective prayer.", "heart"),
        ],
        "info_items": [
            ("utensils", "Shared Meal", "A community Iftar spread for everyone."),
            ("users", "Open to All", "Members, alumni and their families welcome."),
            ("heart", "Dua & Reflection", "A shared moment of gratitude together."),
            ("camera", "Photo Moments", "Capturing the evening's warmth and togetherness."),
        ],
        "stats": [("Format", "Evening"), ("Held", "Annually, in Ramadan")],
    },
    {
        "slug": "online",
        "title": "Online Events",
        "tagline": "Bringing knowledge, inspiration and community together from anywhere in the world.",
        "overview": (
            "PUSAB runs a rolling calendar of online events — career webinars, admission AMAs, "
            "and one-to-one mentoring sessions — so members and aspirants can get guidance no "
            "matter where they are."
        ),
        "eligibility": "Open to PUSAB members and Bishwambarpur students preparing for admissions or careers.",
        "process": "Sessions are announced through PUSAB's social pages and group; joining links are shared ahead of each event.",
        "schedule_note": "Monthly AMAs, plus occasional special webinars.",
        "register_label": "Subscribe",
        "cta_title": "Stay Updated",
        "cta_subtitle": "Subscribe to get notified about our upcoming online events.",
        "objectives": [
            ("Open to All", "All PUSAB members, alumni and well-wishers can join.", "users"),
            ("Live & Interactive", "Engage in real-time sessions with experts and peers.", "calendar"),
            ("Learn & Grow", "Expand your knowledge and develop new skills.", "target"),
            ("Certificate Provided", "Get digital certificates for your participation.", "award"),
        ],
        "info_items": [
            ("users", "Expert Speakers", "Learn from experienced professionals and thought leaders."),
            ("target", "Global Community", "Connect with PUSAB members from around the world."),
            ("sparkles", "Flexible & Accessible", "Join from anywhere, anytime with ease."),
            ("graduation-cap", "Knowledge for Impact", "Gain insights that inspire and create positive change."),
        ],
        "stats": [("Frequency", "Monthly"), ("Reach", "Online")],
        "webinars": [
            ("Talk Show", "The Power of Education to Change Lives", "Dr. A.K.M. Rafiqul Islam", "Professor, DU", "20 May 2025", "08:00 PM (GMT+6)", "live"),
            ("Workshop", "Personal Growth & Leadership Skills", "Tasnim Haque", "Corporate Trainer", "24 May 2025", "07:00 PM (GMT+6)", "upcoming"),
            ("Seminar", "Financial Literacy for Students", "Mohammad Foysal", "Financial Advisor", "30 May 2025", "08:00 PM (GMT+6)", "upcoming"),
            ("Discussion", "Mental Health Awareness", "Dr. Farzana Islam", "Clinical Psychologist", "05 June 2025", "07:30 PM (GMT+6)", "upcoming"),
        ],
    },
    {
        "slug": "felicitation",
        "title": "Felicitation & Freshers Reception",
        "tagline": (
            "A memorable gathering to honor the outstanding achievers and warmly welcome the "
            "newest members to the PUSAB family."
        ),
        "overview": (
            "Each year PUSAB brings achievers and new entrants onto one stage — recognising "
            "members who carry Bishwambarpur's name forward, and formally welcoming freshers "
            "just beginning their university journey."
        ),
        "eligibility": "Achievers are selected by merit; all incoming freshers from Bishwambarpur are welcomed.",
        "process": "Held as a single combined ceremony, usually timed around the start of a new academic session.",
        "schedule_note": "Once a year, timed with the new academic session.",
        "event_date": "To Be Announced",
        "venue": "To Be Announced",
        "register_label": "I'm Excited!",
        "cta_title": "Be a Part of This Special Day!",
        "cta_subtitle": "Let's celebrate achievements and welcome new journeys together.",
        "objectives": [
            ("Recognize Achievements", "Honoring hard work and outstanding contributions.", "award"),
            ("Welcome New Members", "A warm welcome to our new members joining PUSAB.", "users"),
            ("Inspire Excellence", "Motivating everyone to aim higher and achieve more.", "sparkles"),
            ("Build Connections", "Bringing together members, alumni and well-wishers.", "heart"),
            ("Create Memories", "Cherishing moments that last a lifetime.", "camera"),
        ],
        "info_items": [
            ("award", "Honoring Excellence", "Celebrating the success and dedication of our achievers."),
            ("heart", "Warm Welcome", "A heartfelt welcome to our freshers and new family members."),
            ("mic", "Inspiring Speeches", "Words of wisdom and motivation from leaders and guests."),
            ("camera", "Memorable Moments", "Capturing smiles, achievements and beautiful memories."),
            ("music", "Cultural Vibes", "Enjoy amazing cultural performances and engaging activities."),
            ("users", "Stronger Together", "Building bonds and creating a stronger PUSAB community."),
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
                existing.info_items.all().delete()
                existing.stats.all().delete()
                existing.webinars.all().delete()
                page = existing
            else:
                page = ProgramPage(slug=slug, year=SEED_YEAR)

            page.title = data["title"]
            page.tagline = data["tagline"]
            page.overview = data["overview"]
            page.eligibility = data["eligibility"]
            page.process = data["process"]
            page.schedule_note = data["schedule_note"]
            page.event_date = data.get("event_date", "")
            page.venue = data.get("venue", "")
            page.event_time = data.get("event_time", "")
            page.register_label = data.get("register_label", "")
            page.register_url = data.get("register_url", "")
            page.cta_title = data.get("cta_title", "")
            page.cta_subtitle = data.get("cta_subtitle", "")
            page.save()

            for i, objective in enumerate(data["objectives"]):
                icon = objective[2] if len(objective) > 2 else ""
                ProgramObjective.objects.create(
                    page=page, title=objective[0], description=objective[1], icon=icon, order=i
                )
            for i, (icon, label, value) in enumerate(data.get("info_items", [])):
                ProgramInfoItem.objects.create(page=page, icon=icon, label=label, value=value, order=i)
            for i, (label, value) in enumerate(data["stats"]):
                ProgramStat.objects.create(page=page, label=label, value=value, order=i)
            for i, (tag, title, speaker_name, speaker_role, event_date, event_time, status) in enumerate(
                data.get("webinars", [])
            ):
                ProgramWebinar.objects.create(
                    page=page,
                    tag=tag,
                    title=title,
                    speaker_name=speaker_name,
                    speaker_role=speaker_role,
                    event_date=event_date,
                    event_time=event_time,
                    status=status,
                    order=i,
                )

            created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created} program page(s), skipped {skipped}."))
