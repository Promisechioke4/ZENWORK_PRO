import random

QUOTES = [
    "Small steps every day lead to big results.",
    "Stay focused. You’re doing great!",
    "Discipline is choosing what you want most.",
    "Work hard in silence, let your success make the noise.",
    "You’re one Pomodoro closer to your goal!",
    "Progress, not perfection. Keep going.",
    "Breathe. Focus. Win the day.",
    "No pressure, just presence. You got this!",
    "Greatness is a lot of small things done well.",
    "Rest is part of the work. Don't skip it."
]

def get_random_quote():
    return random.choice(QUOTES)
