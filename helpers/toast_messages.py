# List of toast messages paired with their icons
TOAST_MESSAGES = [
    ("Ready to test your YouTube knowledge?", "🎥"),
    ("QuizGPT welcomes you!", "🚀"),
    ("Think you caught all the details? Let's find out!", "🔍"),
    ("It's quiz time! No spoilers allowed.", "⏳"),
    ("Popped in for a quiz? You're in the right place!", "🍿"),
    ("Get your thinking cap on!", "🎓"),
    ("Your next quiz challenge awaits!", "🏆"),
    ("Another document, another quiz!", "🔄"),
    ("Turn those document reads into victories!", "🎖️"),
    ("Did you pay attention? It's quiz o'clock!", "⏰"),
    ("Reading is fun, but quizzes? Even better!", "🎉"),
    ("Unleash your prowess here!", "🦸"),
    ("Knowledge check: Engage!", "🚦"),
    ("Book read? Check. Quiz taken? Pending...", "✅"),
    ("Dive deeper into your book content.", "🌊"),
    ("Up for a book revision in quiz form?", "⏪"),
    ("Let's decode your recent book knowledge!", "🧩"),
    ("Adding some quiz spice to your book binge!", "🌶️"),
    ("Transform your read time into quiz time!", "🔄"),
    ("Here to validate your reading expertise?", "🔍")
]

def get_random_toast():
    """Returns a random toast message and icon."""
    import random
    return random.choice(TOAST_MESSAGES)