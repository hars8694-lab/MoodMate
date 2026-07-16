CRISIS_PATTERNS = [
     "kill myself", "end my life", "suicide", "self harm",
     "hurt myself", "don't want to live", "no reason to live",
]

CRISIS_RESPONSE = (
     "I'm really glad you told me, and I'm concerned about you. "
     "I'm not equipped to help with this, but people who care are "
      "available right now.\n\n"
     "**India:** Tele-MANAS 14416 (24/7, free) - iCall +91 9152987821\n"
     "**International:** find your local helpline at findahelpline.com\n\n"
     "Please consider reaching out to one of them, or to someone you trust."
)

def check(text: str):
    lowered = text.lower()
    if any(p in lowered for p in CRISIS_PATTERNS):
        return CRISIS_RESPONSE
    return None