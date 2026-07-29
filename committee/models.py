from django.db import models

# Canonical Executive Committee designation hierarchy — members should list
# President down to Executive Member in this order, not alphabetically.
# Keep this in sync with src/lib/designation.ts on the frontend.
DESIGNATION_ORDER = [
    "President",
    "Vice President",
    "General Secretary",
    "Joint General Secretary",
    "Treasurer",
    "Organizing Secretary",
    "Office Secretary",
    "Assistant Office Secretary",
    "Publicity Secretary",
    "Assistant Publicity Secretary",
    "Human Resource Development Secretary",
    "Assistant Human Resource Development Secretary",
    "Compilation and Publication Secretary",
    "Assistant Compilation and Publication Secretary",
    "Schooling Secretary",
    "Assistant Schooling Secretary",
    "Scholarship Secretary",
    "Assistant Scholarship Secretary",
    "Information and Technology Secretary",
    "Assistant Information and Technology Secretary",
    "Hospitality Secretary",
    "Assistant Hospitality Secretary",
    "Cultural Secretary",
    "Assistant Cultural Secretary",
    "Sports Secretary",
    "Assistant Sports Secretary",
    "Health Secretary",
    "Assistant Health Secretary",
    "Assistant Secretary",
    "Executive Member",
]

DESIGNATION_RANK = {role.lower(): i for i, role in enumerate(DESIGNATION_ORDER)}


def designation_rank(role: str) -> int:
    """Rank of a role in the designation hierarchy — unknown roles sort last."""
    return DESIGNATION_RANK.get(role.strip().lower(), len(DESIGNATION_ORDER))


class EcMember(models.Model):
    """An Executive Committee member for a given session year."""

    name = models.CharField(max_length=150)
    role = models.CharField(max_length=120)  # designation / podobi
    university = models.CharField(max_length=200, blank=True)
    year = models.PositiveIntegerField()  # session
    is_current = models.BooleanField(default=False)
    is_convening = models.BooleanField(default=False)  # founding convening committee (2014)
    photo_url = models.URLField(max_length=600, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year", "name"]

    def __str__(self):
        return f"{self.name} — {self.role} ({self.year})"


class LeaderMessage(models.Model):
    """A message from a leader (President / General Secretary). One row per role."""

    ROLE_CHOICES = [
        ("president", "President"),
        ("secretary", "General Secretary"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    name = models.CharField(max_length=150, blank=True)
    designation = models.CharField(max_length=120, blank=True)  # e.g. "President, PUSAB"
    session = models.CharField(max_length=40, blank=True)  # e.g. "Session 2026"
    photo_url = models.URLField(max_length=600, blank=True)
    quote = models.TextField(blank=True)  # the highlighted pull-quote
    body = models.TextField(blank=True)  # message paragraphs separated by blank lines
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["role"]

    def __str__(self):
        return f"{self.get_role_display()} message — {self.name}"
