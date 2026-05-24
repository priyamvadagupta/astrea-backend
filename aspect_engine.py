SPECIAL_ASPECTS = {
    "Sun": [7],
    "Moon": [7],
    "Mercury": [7],
    "Venus": [7],
    "Mars": [4, 7, 8],
    "Jupiter": [5, 7, 9],
    "Saturn": [3, 7, 10],
    "Rahu": [5, 7, 9],
    "Ketu": [5, 7, 9],
}


def get_aspected_houses(planet, planet_house):
    """
    Returns houses aspected by a planet based on its placement.
    Example:
    Mars in 4th aspects 7th, 10th, 11th.
    """
    aspects = SPECIAL_ASPECTS.get(planet, [7])

    aspected_houses = []
    for aspect in aspects:
        target_house = ((planet_house + aspect - 2) % 12) + 1
        aspected_houses.append(target_house)

    return aspected_houses


def build_house_analysis_context(chart):
    planets = chart["planets"]
    house_chart = chart["house_chart"]

    # Planet -> houses it aspects
    planet_aspects = {}

    for planet, details in planets.items():
        planet_house = details["house"]
        planet_aspects[planet] = get_aspected_houses(planet, planet_house)

    # House -> planets aspecting that house
    house_aspected_by = {house: [] for house in range(1, 13)}

    for planet, houses in planet_aspects.items():
        for house in houses:
            house_aspected_by[house].append(planet)

    # Planet -> planets conjunct with it
    planet_conjunct_with = {planet: [] for planet in planets.keys()}

    for planet_a, details_a in planets.items():
        for planet_b, details_b in planets.items():
            if planet_a != planet_b and details_a["house"] == details_b["house"]:
                planet_conjunct_with[planet_a].append(planet_b)

    # Planet -> planets aspecting it
    # A planet is aspected ONLY if another planet aspects the HOUSE where it sits.
    planet_aspected_by = {planet: [] for planet in planets.keys()}

    for target_planet, target_details in planets.items():
        target_house = target_details["house"]

        for aspecting_planet, aspected_houses in planet_aspects.items():
            if aspecting_planet == target_planet:
                continue

            if target_house in aspected_houses:
                planet_aspected_by[target_planet].append(aspecting_planet)

    # House-wise context
    house_analysis = []

    for house in range(1, 13):
        sign = house_chart[house]["sign"]
        sitting_planets = house_chart[house]["planets"]
        aspecting_planets = house_aspected_by[house]

        house_analysis.append({
            "house": house,
            "sign_in_house": sign,
            "planets_sitting": sitting_planets,
            "planets_aspecting_house": aspecting_planets
        })

    # Planet-wise context
    planet_analysis = {}

    for planet, details in planets.items():
        planet_analysis[planet] = {
            "sign": details["sign"],
            "house": details["house"],
            "houses_aspected_by_this_planet": planet_aspects[planet],
            "planets_conjunct_with_this_planet": planet_conjunct_with[planet],
            "planets_aspecting_this_planet": planet_aspected_by[planet]
        }

    return {
        "planet_aspects": planet_aspects,
        "house_aspected_by": house_aspected_by,
        "planet_conjunct_with": planet_conjunct_with,
        "planet_aspected_by": planet_aspected_by,
        "house_analysis": house_analysis,
        "planet_analysis": planet_analysis
    }