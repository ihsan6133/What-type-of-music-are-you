QUESTIONS = [
    (
        "What is your ideal weekend plan?",
        [
            "Visiting a museum",   # Classical
            "Attending a live concert",   # Rock
            "Going to a quiet café",  # Jazz
            "Gaming at home"  # Electronic
        ]
    ),
    (
        "Choose a colour that represents you:",
        [
            "White or gold",  # Classical
            "Red or black",   # Rock
            "Purple or navy", # Jazz
            "Neon blue or pastel pink"  # Electronic
        ]
    ),
    (
        "Your approach to problems:",
        [
            "Analyze systematically",  # Classical
            "Confront directly with force",  # Rock
            "Adapt creatively and improvise",  # Jazz
            "Find tech-based shortcuts"  # Electronic
        ]
    ),
    (
        "Your ideal working environment:",
        [
            "Quiet study room",  # Classical
            "Loud and lively space",  # Rock
            "Dim-lit café with ambience",  # Jazz
            "Futuristic minimalist setup"  # Electronic
        ]
    ),
    (
        "Pick a quote that resonates with you:",
        [
            "Discipline is freedom.",  # Classical
            "Rules are made to be broken.",  # Rock
            "Life's best when you improvise.",  # Jazz
            "Innovation is the future",  # Electronic
        ]
    ),
    (
        "Your favourite drink:",
        [
            "Herbal tea",  # Classical
            "Black coffee or energy drink",  # Rock
            "Smooth latte or mocha",  # Jazz
            "Bubble tea or flavoured soda"  # Electronic
        ]
    ),
    (
        "Your social style is:",
        [
            "Reserved and formal",  # Classical
            "Loud and expressive",  # Rock
            "Calm and friendly",  # Jazz
            "Quiet but deeply connected"  # Electronic
        ]
    ),
    (
        "Preferred time of day:",
        [
            "Early morning",  # Classical
            "Late night",  # Rock
            "Evening twilight",  # Jazz
            "Your schedule is flexible"  # Electronic
        ]
    ),
    (
        "Choose a hobby:",
        [
            "Reading philosophy or history",  # Classical
            "Playing guitar or extreme sports",  # Rock
            "Sketching or photography",  # Jazz
            "Gaming, coding, or digital art"  # Electronic
        ]
    ),
    (
        "Your life motto:",
        [
            "Practice makes perfect.",  # Classical
            "No regrets.",  # Rock
            "Go with the flow.",  # Jazz
            "Upgrade constantly."  # Electronic
        ]
    )
]

RESULTS = [
    (
        "Classical",
        "You are a person of discipline and tradition. You value structure, order, and the beauty of classical music. Your ideal environment is calm and serene, where you can focus on your thoughts and creativity."
    ),
    (
        "Rock",
        "You are bold, expressive, and love to live life on the edge. You thrive in energetic environments and enjoy the thrill of loud music and dynamic experiences."
    ),
    (
        "Jazz",
        "You are creative, adaptable, and appreciate the nuances of life. You enjoy improvisation and find beauty in spontaneity. Your ideal setting is relaxed yet inspiring."
    ),
    (
        "Electronic",
        "You are tech-savvy, innovative, and always looking for the next big thing. You enjoy futuristic aesthetics and thrive in environments that stimulate your mind with new ideas."
    )
]



def get_result(responses):
    scores = [0, 0, 0, 0]  # Classical, Rock, Jazz, Electronic
    
    for i, response in enumerate(responses):
        option = QUESTIONS[i][1].index(response)
        scores[option] += 1

    max_score = max(scores)
    max_index = scores.index(max_score)
    return RESULTS[max_index]

def music_sample(result):
    if result == "Classical":
        return "sounds/moonlight-sonata.mp3"
    elif result == "Rock":
        return "sounds/rock.mp3"
    elif result == "Jazz":
        return "sounds/dargolan-jazz.mp3"
    elif result == "Electronic":
        return "sounds/loop-edm.mp3"
    else:
        return None