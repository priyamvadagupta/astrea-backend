# rahu_ketu_engine.py

NAKSHATRAS = [
    ("Ashwini", "Ketu"),
    ("Bharani", "Venus"),
    ("Krittika", "Sun"),
    ("Rohini", "Moon"),
    ("Mrigashira", "Mars"),
    ("Ardra", "Rahu"),
    ("Punarvasu", "Jupiter"),
    ("Pushya", "Saturn"),
    ("Ashlesha", "Mercury"),
    ("Magha", "Ketu"),
    ("Purva Phalguni", "Venus"),
    ("Uttara Phalguni", "Sun"),
    ("Hasta", "Moon"),
    ("Chitra", "Mars"),
    ("Swati", "Rahu"),
    ("Vishakha", "Jupiter"),
    ("Anuradha", "Saturn"),
    ("Jyeshtha", "Mercury"),
    ("Mula", "Ketu"),
    ("Purva Ashadha", "Venus"),
    ("Uttara Ashadha", "Sun"),
    ("Shravana", "Moon"),
    ("Dhanishta", "Mars"),
    ("Shatabhisha", "Rahu"),
    ("Purva Bhadrapada", "Jupiter"),
    ("Uttara Bhadrapada", "Saturn"),
    ("Revati", "Mercury"),
]

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]


def get_nakshatra(longitude):
    """
    Each nakshatra = 13°20' = 13.333333 degrees.
    Each pada = 3°20' = 3.333333 degrees.
    """
    nakshatra_size = 360 / 27
    pada_size = nakshatra_size / 4

    nak_index = int(longitude // nakshatra_size)
    degree_in_nakshatra = longitude % nakshatra_size
    pada = int(degree_in_nakshatra // pada_size) + 1

    nak_name, nak_lord = NAKSHATRAS[nak_index]

    return {
        "nakshatra": nak_name,
        "nakshatra_lord": nak_lord,
        "pada": pada
    }


def get_axis_name(rahu_house, ketu_house):
    axis = tuple(sorted([rahu_house, ketu_house]))

    axis_names = {
        (1, 7): "Self vs Relationships Axis",
        (2, 8): "Resources vs Transformation Axis",
        (3, 9): "Effort vs Dharma Axis",
        (4, 10): "Home vs Career Axis",
        (5, 11): "Creativity/Children vs Gains/Networks Axis",
        (6, 12): "Service/Conflict vs Liberation/Isolation Axis",
    }

    return axis_names.get(axis, "Rahu-Ketu Axis")


def get_axis_interpretation(rahu_house, ketu_house):
    if rahu_house == 1 and ketu_house == 7:
        return "Rahu in the 1st pushes the native toward self-development, identity, independence and personal visibility, while Ketu in the 7th shows detachment or karmic familiarity around partnerships."

    if rahu_house == 7 and ketu_house == 1:
        return "Rahu in the 7th pushes the native toward relationships, partnerships and public dealings, while Ketu in the 1st shows past-life familiarity with independence and self-orientation."

    if rahu_house == 2 and ketu_house == 8:
        return "Rahu in the 2nd emphasizes wealth, speech, family, food, values and resource-building, while Ketu in the 8th shows detachment from hidden fears, occult intensity and deep transformation."

    if rahu_house == 8 and ketu_house == 2:
        return "Rahu in the 8th intensifies transformation, occult knowledge, research, joint assets, vulnerability and sudden events, while Ketu in the 2nd shows detachment or karmic familiarity with family, speech and accumulated wealth."

    if rahu_house == 3 and ketu_house == 9:
        return "Rahu in the 3rd pushes effort, courage, communication, skills and self-made growth, while Ketu in the 9th shows karmic familiarity with gurus, dharma, father, religion and higher wisdom."

    if rahu_house == 9 and ketu_house == 3:
        return "Rahu in the 9th pushes expansion through dharma, higher wisdom, father, gurus, religion, travel and fortune, while Ketu in the 3rd shows detachment from repetitive effort, siblings or self-driven struggle."

    if rahu_house == 4 and ketu_house == 10:
        return "Rahu in the 4th intensifies home, mother, emotional security, property and inner life, while Ketu in the 10th shows detachment or karmic familiarity with career, authority and public status."

    if rahu_house == 10 and ketu_house == 4:
        return "Rahu in the 10th pushes career, public status, visibility and karma, while Ketu in the 4th shows detachment or karmic familiarity with home, mother and private emotional life."

    if rahu_house == 5 and ketu_house == 11:
        return "Rahu in the 5th intensifies children, creativity, romance, intelligence, education, mantra and self-expression, while Ketu in the 11th shows detachment from networks, gains and social validation."

    if rahu_house == 11 and ketu_house == 5:
        return "Rahu in the 11th pushes gains, income, networks, ambitions and social expansion, while Ketu in the 5th shows karmic familiarity or detachment around children, romance, creativity and past-life merit."

    if rahu_house == 6 and ketu_house == 12:
        return "Rahu in the 6th pushes discipline, service, competition, disease management, debt handling and conflict resolution, while Ketu in the 12th shows spiritual detachment, isolation, foreign lands and moksha tendencies."

    if rahu_house == 12 and ketu_house == 6:
        return "Rahu in the 12th intensifies foreign lands, sleep, isolation, expenses, hospitals, ashrams and spiritual withdrawal, while Ketu in the 6th shows detachment from conflict, enemies, debts and daily service."

    return "This Rahu-Ketu axis shows the life area where desire and karmic growth meet detachment and past-life familiarity."


def build_rahu_ketu_context(chart):
    rahu = chart["planets"]["Rahu"]
    ketu = chart["planets"]["Ketu"]

    rahu_nak = get_nakshatra(rahu["degree"])
    ketu_nak = get_nakshatra(ketu["degree"])

    rahu_house = rahu["house"]
    ketu_house = ketu["house"]

    return {
        "rahu": {
            "sign": rahu["sign"],
            "house": rahu_house,
            "degree": rahu["degree"],
            "nakshatra": rahu_nak["nakshatra"],
            "nakshatra_lord": rahu_nak["nakshatra_lord"],
            "pada": rahu_nak["pada"],
            "navamsha_sign": rahu.get("navamsa_sign", "-"),
            "dignity": rahu.get("dignity", "-"),
            "is_vargottama": rahu.get("is_vargottama", False),
            "is_retrograde": rahu.get("is_retrograde", True)
        },
        "ketu": {
            "sign": ketu["sign"],
            "house": ketu_house,
            "degree": ketu["degree"],
            "nakshatra": ketu_nak["nakshatra"],
            "nakshatra_lord": ketu_nak["nakshatra_lord"],
            "pada": ketu_nak["pada"],
            "navamsha_sign": ketu.get("navamsa_sign", "-"),
            "dignity": ketu.get("dignity", "-"),
            "is_vargottama": ketu.get("is_vargottama", False),
            "is_retrograde": ketu.get("is_retrograde", True)
        },
        "axis": {
            "rahu_house": rahu_house,
            "ketu_house": ketu_house,
            "axis_name": get_axis_name(rahu_house, ketu_house),
            "axis_interpretation": get_axis_interpretation(rahu_house, ketu_house)
        }
    }