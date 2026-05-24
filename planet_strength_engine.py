# planet_strength_engine.py

EXALTATION_SIGNS = {
    "Sun": "Aries",
    "Moon": "Taurus",
    "Mars": "Capricorn",
    "Mercury": "Virgo",
    "Jupiter": "Cancer",
    "Venus": "Pisces",
    "Saturn": "Libra",
    "Rahu": "Taurus",
    "Ketu": "Scorpio",
}

DEBILITATION_SIGNS = {
    "Sun": "Libra",
    "Moon": "Scorpio",
    "Mars": "Cancer",
    "Mercury": "Pisces",
    "Jupiter": "Capricorn",
    "Venus": "Virgo",
    "Saturn": "Aries",
    "Rahu": "Scorpio",
    "Ketu": "Taurus",
}

OWN_SIGNS = {
    "Sun": ["Leo"],
    "Moon": ["Cancer"],
    "Mars": ["Aries", "Scorpio"],
    "Mercury": ["Gemini", "Virgo"],
    "Jupiter": ["Sagittarius", "Pisces"],
    "Venus": ["Taurus", "Libra"],
    "Saturn": ["Capricorn", "Aquarius"],
    "Rahu": [],
    "Ketu": [],
}

MOOLTRIKONA_SIGNS = {
    "Sun": "Leo",
    "Moon": "Taurus",
    "Mars": "Aries",
    "Mercury": "Virgo",
    "Jupiter": "Sagittarius",
    "Venus": "Libra",
    "Saturn": "Aquarius",
    "Rahu": None,
    "Ketu": None,
}

COMBUSTION_ORBS = {
    "Moon": 12,
    "Mars": 17,
    "Mercury": 14,
    "Jupiter": 11,
    "Venus": 10,
    "Saturn": 15,
    # Sun cannot be combust.
    # Rahu/Ketu are not treated as combust in standard Parashari practice.
}

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]


def angular_distance(deg1, deg2):
    """
    Smallest angular distance between two planets.
    """
    diff = abs(deg1 - deg2) % 360
    return min(diff, 360 - diff)


def get_navamsa_sign(longitude):
    """
    Calculates D9/Navamsha sign from sidereal longitude.

    Each sign = 30 degrees.
    Each navamsha = 3 degrees 20 minutes = 3.333333 degrees.

    Movable signs start from same sign.
    Fixed signs start from 9th sign from itself.
    Dual signs start from 5th sign from itself.
    """

    sign_index = int(longitude // 30)
    degree_in_sign = longitude % 30
    navamsa_part = int(degree_in_sign // (30 / 9))

    # Movable signs: Aries, Cancer, Libra, Capricorn
    movable = [0, 3, 6, 9]

    # Fixed signs: Taurus, Leo, Scorpio, Aquarius
    fixed = [1, 4, 7, 10]

    # Dual signs: Gemini, Virgo, Sagittarius, Pisces
    dual = [2, 5, 8, 11]

    if sign_index in movable:
        navamsa_start = sign_index
    elif sign_index in fixed:
        navamsa_start = (sign_index + 8) % 12
    elif sign_index in dual:
        navamsa_start = (sign_index + 4) % 12
    else:
        navamsa_start = sign_index

    navamsa_sign_index = (navamsa_start + navamsa_part) % 12
    return SIGNS[navamsa_sign_index]


def get_dignity(planet, sign):
    """
    Returns broad dignity status of planet in sign.
    """

    if EXALTATION_SIGNS.get(planet) == sign:
        return "Exalted"

    if DEBILITATION_SIGNS.get(planet) == sign:
        return "Debilitated"

    if sign in OWN_SIGNS.get(planet, []):
        return "Own Sign"

    if MOOLTRIKONA_SIGNS.get(planet) == sign:
        return "Mooltrikona"

    return "Neutral/Other"


def get_combustion_status(planet, planet_degree, sun_degree):
    """
    Checks combustion by distance from Sun.
    """

    if planet in ["Sun", "Rahu", "Ketu"]:
        return {
            "is_combust": False,
            "distance_from_sun": None,
            "combustion_orb": None
        }

    orb = COMBUSTION_ORBS.get(planet)

    if orb is None:
        return {
            "is_combust": False,
            "distance_from_sun": None,
            "combustion_orb": None
        }

    distance = angular_distance(planet_degree, sun_degree)

    return {
        "is_combust": distance <= orb,
        "distance_from_sun": round(distance, 2),
        "combustion_orb": orb
    }


def enrich_planet_conditions(chart):
    """
    Adds dignity, navamsha, vargottama, combustion and retrograde interpretation fields.
    Requires chart['planets'][planet] to contain:
    degree, sign, house, is_retrograde
    """

    planets = chart["planets"]
    sun_degree = planets["Sun"]["degree"]

    for planet, details in planets.items():
        sign = details["sign"]
        degree = details["degree"]

        dignity = get_dignity(planet, sign)
        navamsa_sign = get_navamsa_sign(degree)
        is_vargottama = sign == navamsa_sign

        combustion = get_combustion_status(planet, degree, sun_degree)

        details["dignity"] = dignity
        details["navamsa_sign"] = navamsa_sign
        details["is_vargottama"] = is_vargottama
        details["is_combust"] = combustion["is_combust"]
        details["distance_from_sun"] = combustion["distance_from_sun"]
        details["combustion_orb"] = combustion["combustion_orb"]

        # Add simple interpretation tag
        condition_notes = []

        if dignity == "Exalted":
            condition_notes.append("Planet is exalted and can express its significations strongly.")
        elif dignity == "Debilitated":
            condition_notes.append("Planet is debilitated and may need support or maturity to express well.")
        elif dignity == "Own Sign":
            condition_notes.append("Planet is in own sign and has strength to protect its significations.")
        elif dignity == "Mooltrikona":
            condition_notes.append("Planet is in mooltrikona and functions with strong natural authority.")

        if details.get("is_retrograde"):
            condition_notes.append("Planet is retrograde, making its results more internalized, delayed, intensified or karmically revisited.")

        if combustion["is_combust"]:
            condition_notes.append("Planet is combust, so its significations may be overshadowed by the Sun.")

        if is_vargottama:
            condition_notes.append("Planet is vargottama, meaning it occupies the same sign in D1 and D9, strengthening its sign-based expression.")

        details["condition_notes"] = condition_notes

    chart["planets"] = planets
    return chart