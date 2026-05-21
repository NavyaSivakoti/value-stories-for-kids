"""Input validation for Value Stories for Kids.

These checks run before any model call. They are pure functions with no
network access, which makes them easy to cover with PyTest unit tests.
"""

# Each value maps to a short three-word meaning. The meaning is shown to
# caregivers in the dropdown and passed to the model so it teaches the
# right idea. ALLOWED_VALUES is derived from these keys.
VALUE_MEANINGS = {
    "kindness": "being warm hearted",
    "honesty": "always telling truth",
    "courage": "facing fear bravely",
    "sharing": "giving toys gladly",
    "patience": "calmly waiting well",
    "gratitude": "feeling truly thankful",
    "perseverance": "never giving up",
    "respect": "honoring other people",
    "responsibility": "owning your actions",
    "empathy": "feeling others feelings",
    "forgiveness": "letting anger go",
    "humility": "staying modestly grounded",
    "generosity": "giving freely always",
    "self-control": "managing strong impulses",
    "focus": "keeping steady attention",
    "discipline": "doing what matters",
    "compassion": "easing others suffering",
    "loyalty": "standing by others",
    "fairness": "treating everyone equally",
    "curiosity": "eager to learn",
    "cooperation": "working well together",
    "determination": "pushing toward goals",
    "politeness": "using gentle manners",
    "helpfulness": "assisting those around",
    "confidence": "trusting your abilities",
    "contentment": "happy with enough",
    "creativity": "imagining fresh ideas",
    "calmness": "staying peacefully relaxed",
    "resilience": "bouncing back strong",
    "selflessness": "putting others first",
    "cleanliness": "keeping things tidy",
    "optimism": "hoping for good",
}

ALLOWED_VALUES = list(VALUE_MEANINGS.keys())

MIN_AGE = 1
MAX_AGE = 14
MAX_NAME_LENGTH = 30


class ValidationError(ValueError):
    """Raised when caregiver input fails validation."""


def validate_age(age):
    """Return the age as an int, or raise ValidationError."""
    try:
        age = int(age)
    except (TypeError, ValueError):
        raise ValidationError("Age must be a whole number.")
    if age < MIN_AGE or age > MAX_AGE:
        raise ValidationError(
            f"Stories are written for ages {MIN_AGE} to {MAX_AGE}."
        )
    return age


def validate_value(value):
    """Return a clean, supported value, or raise ValidationError."""
    if not value:
        raise ValidationError("Please choose a value to teach.")
    cleaned = str(value).strip().lower()
    if cleaned not in ALLOWED_VALUES:
        raise ValidationError("Please choose one of the supported values.")
    return cleaned


def validate_name(name):
    """Return a safe first name only, or raise ValidationError.

    The name is optional. To protect the child's privacy we keep only the
    first whitespace-separated token, so a full name can never be stored
    or sent to the model.
    """
    if name is None:
        return ""
    cleaned = str(name).strip()
    if cleaned == "":
        return ""
    if len(cleaned) > MAX_NAME_LENGTH:
        raise ValidationError("That name is too long.")
    first_name = cleaned.split()[0]
    if not first_name.replace("-", "").isalpha():
        raise ValidationError("Please enter a name using letters only.")
    return first_name


def age_band(age):
    """Return the story length band for an age."""
    if age <= 3:
        return "1-3"
    if age <= 6:
        return "4-6"
    if age <= 9:
        return "7-9"
    return "10-14"
