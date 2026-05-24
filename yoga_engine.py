# yoga_engine.py

KENDRA_HOUSES = [1, 4, 7, 10]
TRIKONA_HOUSES = [1, 5, 9]
DUSTHANA_HOUSES = [6, 8, 12]

PLANET_NATURE = {
    "Sun": "Natural malefic",
    "Moon": "Conditional benefic",
    "Mars": "Natural malefic",
    "Mercury": "Conditional benefic",
    "Jupiter": "Natural benefic",
    "Venus": "Natural benefic",
    "Saturn": "Natural malefic",
    "Rahu": "Natural malefic",
    "Ketu": "Natural malefic",
}

SIGN_LORDS = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}

EXALTATION_SIGNS = {
    "Sun": "Aries",
    "Moon": "Taurus",
    "Mars": "Capricorn",
    "Mercury": "Virgo",
    "Jupiter": "Cancer",
    "Venus": "Pisces",
    "Saturn": "Libra",
}

OWN_SIGNS = {
    "Sun": ["Leo"],
    "Moon": ["Cancer"],
    "Mars": ["Aries", "Scorpio"],
    "Mercury": ["Gemini", "Virgo"],
    "Jupiter": ["Sagittarius", "Pisces"],
    "Venus": ["Taurus", "Libra"],
    "Saturn": ["Capricorn", "Aquarius"],
}


def get_house_lords(chart):
    """
    Returns house lord based on sign occupying each house.
    Example:
    House 1 Leo -> Sun is lagna lord.
    """
    house_lords = {}

    for house, details in chart["house_chart"].items():
        sign = details["sign"]
        house_lords[house] = SIGN_LORDS.get(sign)

    return house_lords


def get_planet_house(chart, planet):
    return chart["planets"].get(planet, {}).get("house")


def get_planet_sign(chart, planet):
    return chart["planets"].get(planet, {}).get("sign")


def is_own_or_exalted(chart, planet):
    sign = get_planet_sign(chart, planet)

    if not sign:
        return False

    if sign in OWN_SIGNS.get(planet, []):
        return True

    if EXALTATION_SIGNS.get(planet) == sign:
        return True

    return False


def detect_budha_aditya_yoga(chart):
    """
    Budha-Aditya Yoga:
    Sun and Mercury conjunct in the same house.
    """
    yogas = []

    sun_house = get_planet_house(chart, "Sun")
    mercury_house = get_planet_house(chart, "Mercury")

    if sun_house == mercury_house:
        yogas.append({
            "Yoga": "Budha-Aditya Yoga",
            "Formed By": "Sun and Mercury",
            "Condition": f"Sun and Mercury are conjunct in House {sun_house}.",
            "Meaning for Native": "Supports intelligence, communication, analytical ability, administrative capacity, learning, strategy and advisory skill. If Mercury is combust, the result may become more internalized or pressured by ego/authority themes.",
            "Strength Factors": f"Sun: {get_strength_flags(chart, 'Sun')} | Mercury: {get_strength_flags(chart, 'Mercury')}"
        })

    return yogas


def detect_chandra_mangal_yoga(chart):
    """
    Chandra-Mangal Yoga:
    Moon and Mars conjunct or in mutual 7th aspect.
    """
    yogas = []

    moon_house = get_planet_house(chart, "Moon")
    mars_house = get_planet_house(chart, "Mars")

    if moon_house == mars_house:
        yogas.append({
            "Yoga": "Chandra-Mangal Yoga",
            "Formed By": "Moon and Mars",
            "Condition": f"Moon and Mars are conjunct in House {moon_house}.",
            "Meaning for Native": "Creates emotional drive, business instinct, financial initiative, courage and action-oriented mind. Can also create emotional impatience or intensity.",
            "Strength Factors": f"Moon: {get_strength_flags(chart, 'Moon')} | Mars: {get_strength_flags(chart, 'Mars')}"
        })

    # Mutual 7th aspect by house opposition
    if ((moon_house - mars_house) % 12) + 1 == 7:
        yogas.append({
            "Yoga": "Chandra-Mangal Yoga",
            "Formed By": "Moon and Mars",
            "Condition": f"Moon and Mars are in mutual 7th relation. Moon is in House {moon_house}; Mars is in House {mars_house}.",
            "Meaning for Native": "Creates strong emotional action, entrepreneurial instinct, financial initiative and capacity to act on feelings. Needs emotional regulation.",
            "Strength Factors": f"Moon: {get_strength_flags(chart, 'Moon')} | Mars: {get_strength_flags(chart, 'Mars')}"
        })

    return yogas


def detect_amala_yoga(chart):
    """
    Amala Yoga:
    Benefic planet in 10th house from Lagna or Moon.
    Basic version from Lagna only.
    """
    yogas = []
    benefics = ["Jupiter", "Venus", "Mercury", "Moon"]

    for planet in benefics:
        house = get_planet_house(chart, planet)

        if house == 10:
            yogas.append({
                "Yoga": "Amala Yoga",
                "Formed By": planet,
                "Condition": f"{planet} is placed in the 10th house from Lagna.",
                "Meaning for Native": "Supports reputation, good conduct, public respect, career visibility and a cleaner professional image. The result depends on the strength and condition of the planet.",
                "Strength Factors": get_strength_flags(chart, planet)
            })

    return yogas


def detect_sunapha_anapha_durudhara_yogas(chart):
    """
    Sunapha: planets in 2nd from Moon
    Anapha: planets in 12th from Moon
    Durudhara: planets in both 2nd and 12th from Moon
    Excludes Sun, Rahu, Ketu by common classical convention.
    """
    yogas = []

    moon_house = get_planet_house(chart, "Moon")
    excluded = ["Sun", "Moon", "Rahu", "Ketu"]

    second_from_moon = ((moon_house + 2 - 2) % 12) + 1
    twelfth_from_moon = ((moon_house + 12 - 2) % 12) + 1

    planets_2nd = []
    planets_12th = []

    for planet, details in chart["planets"].items():
        if planet in excluded:
            continue

        if details["house"] == second_from_moon:
            planets_2nd.append(planet)

        if details["house"] == twelfth_from_moon:
            planets_12th.append(planet)

    if planets_2nd:
        yogas.append({
            "Yoga": "Sunapha Yoga",
            "Formed By": ", ".join(planets_2nd),
            "Condition": f"Planets other than Sun, Rahu and Ketu are placed in the 2nd house from Moon. Moon is in House {moon_house}; 2nd from Moon is House {second_from_moon}.",
            "Meaning for Native": "Supports self-earned wealth, skill, intelligence, speech, initiative and ability to build resources through personal effort.",
            "Strength Factors": " | ".join([f"{p}: {get_strength_flags(chart, p)}" for p in planets_2nd])
        })

    if planets_12th:
        yogas.append({
            "Yoga": "Anapha Yoga",
            "Formed By": ", ".join(planets_12th),
            "Condition": f"Planets other than Sun, Rahu and Ketu are placed in the 12th house from Moon. Moon is in House {moon_house}; 12th from Moon is House {twelfth_from_moon}.",
            "Meaning for Native": "Supports self-contained personality, reflective nature, independence, inner resources and capacity to work from behind the scenes.",
            "Strength Factors": " | ".join([f"{p}: {get_strength_flags(chart, p)}" for p in planets_12th])
        })

    if planets_2nd and planets_12th:
        yogas.append({
            "Yoga": "Durudhara Yoga",
            "Formed By": f"2nd from Moon: {', '.join(planets_2nd)}; 12th from Moon: {', '.join(planets_12th)}",
            "Condition": "Planets are present on both sides of the Moon, excluding Sun, Rahu and Ketu.",
            "Meaning for Native": "Supports stability of mind, resources, status, self-effort and capacity to manage both external and internal life pressures.",
            "Strength Factors": " | ".join([f"{p}: {get_strength_flags(chart, p)}" for p in planets_2nd + planets_12th])
        })

    return yogas


def detect_vesi_vasi_ubhayachari_yogas(chart):
    """
    Vesi: planets in 2nd from Sun
    Vasi: planets in 12th from Sun
    Ubhayachari: planets on both sides of Sun
    Excludes Moon, Rahu, Ketu by common convention.
    """
    yogas = []

    sun_house = get_planet_house(chart, "Sun")
    excluded = ["Sun", "Moon", "Rahu", "Ketu"]

    second_from_sun = ((sun_house + 2 - 2) % 12) + 1
    twelfth_from_sun = ((sun_house + 12 - 2) % 12) + 1

    planets_2nd = []
    planets_12th = []

    for planet, details in chart["planets"].items():
        if planet in excluded:
            continue

        if details["house"] == second_from_sun:
            planets_2nd.append(planet)

        if details["house"] == twelfth_from_sun:
            planets_12th.append(planet)

    if planets_2nd:
        yogas.append({
            "Yoga": "Vesi Yoga",
            "Formed By": ", ".join(planets_2nd),
            "Condition": f"Planets excluding Moon, Rahu and Ketu are placed in the 2nd house from Sun. Sun is in House {sun_house}; 2nd from Sun is House {second_from_sun}.",
            "Meaning for Native": "Supports initiative, visibility, self-expression, resourcefulness and capacity to act after self-definition.",
            "Strength Factors": " | ".join([f"{p}: {get_strength_flags(chart, p)}" for p in planets_2nd])
        })

    if planets_12th:
        yogas.append({
            "Yoga": "Vasi Yoga",
            "Formed By": ", ".join(planets_12th),
            "Condition": f"Planets excluding Moon, Rahu and Ketu are placed in the 12th house from Sun. Sun is in House {sun_house}; 12th from Sun is House {twelfth_from_sun}.",
            "Meaning for Native": "Supports inner discipline, controlled expression, background effort, planning and introspective strength.",
            "Strength Factors": " | ".join([f"{p}: {get_strength_flags(chart, p)}" for p in planets_12th])
        })

    if planets_2nd and planets_12th:
        yogas.append({
            "Yoga": "Ubhayachari Yoga",
            "Formed By": f"2nd from Sun: {', '.join(planets_2nd)}; 12th from Sun: {', '.join(planets_12th)}",
            "Condition": "Planets are placed on both sides of the Sun, excluding Moon, Rahu and Ketu.",
            "Meaning for Native": "Supports balanced self-expression, capability, leadership development, practical intelligence and ability to operate both publicly and privately.",
            "Strength Factors": " | ".join([f"{p}: {get_strength_flags(chart, p)}" for p in planets_2nd + planets_12th])
        })

    return yogas


def detect_parivartana_yoga(chart):
    """
    Parivartana Yoga:
    Mutual exchange of signs between two planets.
    Example: Mars in Venus sign and Venus in Mars sign.
    """
    yogas = []

    planets = list(chart["planets"].keys())

    # Exclude nodes for now
    planets = [p for p in planets if p not in ["Rahu", "Ketu"]]

    for i, p1 in enumerate(planets):
        for p2 in planets[i + 1:]:
            p1_sign = get_planet_sign(chart, p1)
            p2_sign = get_planet_sign(chart, p2)

            p1_sign_lord = SIGN_LORDS.get(p1_sign)
            p2_sign_lord = SIGN_LORDS.get(p2_sign)

            if p1_sign_lord == p2 and p2_sign_lord == p1:
                yogas.append({
                    "Yoga": "Parivartana Yoga",
                    "Formed By": f"{p1} and {p2}",
                    "Condition": f"{p1} is in {p2}'s sign {p1_sign}, and {p2} is in {p1}'s sign {p2_sign}.",
                    "Meaning for Native": "Creates strong exchange between the houses ruled and occupied by the two planets. The result depends on whether the involved houses are auspicious, difficult or mixed.",
                    "Strength Factors": f"{p1}: {get_strength_flags(chart, p1)} | {p2}: {get_strength_flags(chart, p2)}"
                })

    return yogas


def detect_neecha_bhanga_raja_yoga(chart):
    """
    Basic Neecha Bhanga Raja Yoga:
    A debilitated planet gets cancellation if:
    - Lord of debilitation sign is in kendra from Lagna
    - Planet exalted in that sign is in kendra from Lagna
    Basic version only.
    """
    yogas = []

    EXALTATION_LORD_FOR_DEBILITATION_SIGN = {
        "Aries": "Sun",
        "Taurus": "Moon",
        "Cancer": "Jupiter",
        "Virgo": "Mercury",
        "Libra": "Saturn",
        "Scorpio": "Ketu",
        "Capricorn": "Mars",
        "Pisces": "Venus",
    }

    for planet, details in chart["planets"].items():
        dignity = details.get("dignity")

        if dignity != "Debilitated":
            continue

        debilitation_sign = details["sign"]
        debilitation_sign_lord = SIGN_LORDS.get(debilitation_sign)
        exalted_planet_for_sign = EXALTATION_LORD_FOR_DEBILITATION_SIGN.get(debilitation_sign)

        cancellation_reasons = []

        if debilitation_sign_lord:
            lord_house = get_planet_house(chart, debilitation_sign_lord)
            if lord_house in KENDRA_HOUSES:
                cancellation_reasons.append(
                    f"Lord of the debilitation sign, {debilitation_sign_lord}, is in kendra House {lord_house}."
                )

        if exalted_planet_for_sign:
            exalted_planet_house = get_planet_house(chart, exalted_planet_for_sign)
            if exalted_planet_house in KENDRA_HOUSES:
                cancellation_reasons.append(
                    f"Planet exalted in {debilitation_sign}, {exalted_planet_for_sign}, is in kendra House {exalted_planet_house}."
                )

        if cancellation_reasons:
            yogas.append({
                "Yoga": "Neecha Bhanga Raja Yoga",
                "Formed By": planet,
                "Condition": f"{planet} is debilitated in {debilitation_sign}, but debility cancellation factors exist: {' '.join(cancellation_reasons)}",
                "Meaning for Native": "Initial weakness, struggle or insecurity connected to the planet can transform into maturity, rise and capability after effort and time.",
                "Strength Factors": get_strength_flags(chart, planet)
            })

    return yogas


def detect_kalasarpa_yoga_basic(chart):
    """
    Basic Kalasarpa Yoga:
    All seven classical planets lie between Rahu and Ketu on one side of the zodiac.
    This is a simplified longitude-based check.
    """
    yogas = []

    rahu_deg = chart["planets"]["Rahu"]["degree"]
    ketu_deg = chart["planets"]["Ketu"]["degree"]

    classical_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    def is_between(start, end, point):
        if start <= end:
            return start <= point <= end
        return point >= start or point <= end

    between_rahu_ketu = []
    between_ketu_rahu = []

    for planet in classical_planets:
        deg = chart["planets"][planet]["degree"]

        if is_between(rahu_deg, ketu_deg, deg):
            between_rahu_ketu.append(planet)

        if is_between(ketu_deg, rahu_deg, deg):
            between_ketu_rahu.append(planet)

    if len(between_rahu_ketu) == 7 or len(between_ketu_rahu) == 7:
        yogas.append({
            "Yoga": "Kalasarpa Yoga Basic Check",
            "Formed By": "Rahu and Ketu enclosing all classical planets",
            "Condition": "All seven classical planets appear to fall between Rahu and Ketu on one side of the zodiac.",
            "Meaning for Native": "Can indicate intense karmic focus, concentrated life direction, psychological pressure and strong nodal themes. This should be judged carefully and not treated fatalistically.",
            "Strength Factors": f"Rahu: {get_strength_flags(chart, 'Rahu')} | Ketu: {get_strength_flags(chart, 'Ketu')}"
        })

    return yogas


def detect_daridra_yoga_basic(chart):
    """
    Basic Daridra Yoga indicators:
    2nd or 11th lord placed in 6/8/12, or afflicted by difficult placement.
    This is only an indicator, not final judgement.
    """
    yogas = []
    house_lords = get_house_lords(chart)

    for wealth_house in [2, 11]:
        lord = house_lords.get(wealth_house)
        lord_house = get_planet_house(chart, lord)

        if lord and lord_house in DUSTHANA_HOUSES:
            yogas.append({
                "Yoga": "Daridra Yoga Basic Indicator",
                "Formed By": lord,
                "Condition": f"Lord of wealth/gains House {wealth_house}, {lord}, is placed in Dusthana House {lord_house}.",
                "Meaning for Native": "Can create pressure around savings, income, gains or financial stability. This must be balanced against Dhana yogas, strength of the lord and benefic influences.",
                "Strength Factors": get_strength_flags(chart, lord)
            })

    return yogas


def detect_pancha_mahapurusha_yoga(chart):
    """
    Pancha Mahapurusha Yoga:
    Mars, Mercury, Jupiter, Venus, Saturn in own/exalted sign in kendra.
    """
    yoga_planets = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    yogas = []

    yoga_names = {
        "Mars": "Ruchaka Yoga",
        "Mercury": "Bhadra Yoga",
        "Jupiter": "Hamsa Yoga",
        "Venus": "Malavya Yoga",
        "Saturn": "Shasha Yoga",
    }

    for planet in yoga_planets:
        house = get_planet_house(chart, planet)
        sign = get_planet_sign(chart, planet)

        if house in KENDRA_HOUSES and is_own_or_exalted(chart, planet):
            yogas.append({
                "Yoga": yoga_names[planet],
                "Formed By": planet,
                "Condition": f"{planet} is in {sign} in House {house}, a kendra, and is in own or exalted sign.",
                "Meaning for Native": get_pancha_mahapurusha_meaning(planet),
                "Strength Factors": get_strength_flags(chart, planet)
            })

    return yogas


def get_pancha_mahapurusha_meaning(planet):
    meanings = {
        "Mars": "Strong courage, initiative, technical ability, command, competitiveness and capacity to overcome obstacles.",
        "Mercury": "Strong intellect, communication, analytics, business skill, learning ability and advisory capacity.",
        "Jupiter": "Wisdom, ethics, teaching capacity, grace, protection, dharma and spiritual/intellectual expansion.",
        "Venus": "Charm, refinement, comforts, artistic ability, relationships, luxury and aesthetic intelligence.",
        "Saturn": "Discipline, endurance, authority through persistence, organizational strength and capacity to handle responsibility.",
    }
    return meanings.get(planet, "")


def detect_dharma_karma_adhipati_yoga(chart):
    """
    Dharma-Karma Adhipati Yoga:
    Connection between 9th lord and 10th lord.
    Basic detection:
    - 9th lord and 10th lord conjunct in same house
    - 9th lord placed in 10th house
    - 10th lord placed in 9th house
    """
    yogas = []
    house_lords = get_house_lords(chart)

    lord_9 = house_lords.get(9)
    lord_10 = house_lords.get(10)

    if not lord_9 or not lord_10:
        return yogas

    house_9_lord = get_planet_house(chart, lord_9)
    house_10_lord = get_planet_house(chart, lord_10)

    if lord_9 == lord_10:
        yogas.append({
            "Yoga": "Dharma-Karma Adhipati Yoga",
            "Formed By": f"{lord_9} as lord of both 9th and 10th related houses",
            "Condition": f"The same planet, {lord_9}, connects dharma and karma houses through lordship.",
            "Meaning for Native": "A strong connection between fortune, dharma, mentors and professional karma. Career may be supported by ethics, learning, guidance, teaching or destiny-driven work.",
            "Strength Factors": get_strength_flags(chart, lord_9)
        })
        return yogas

    if house_9_lord == house_10_lord:
        yogas.append({
            "Yoga": "Dharma-Karma Adhipati Yoga",
            "Formed By": f"9th lord {lord_9} and 10th lord {lord_10}",
            "Condition": f"9th lord {lord_9} and 10th lord {lord_10} are conjunct in House {house_9_lord}.",
            "Meaning for Native": "Dharma, fortune, teachers and higher principles combine with career, status and public karma. This can support rise through meaningful work.",
            "Strength Factors": f"{lord_9}: {get_strength_flags(chart, lord_9)} | {lord_10}: {get_strength_flags(chart, lord_10)}"
        })

    if house_9_lord == 10:
        yogas.append({
            "Yoga": "Dharma-Karma Adhipati Yoga",
            "Formed By": f"9th lord {lord_9}",
            "Condition": f"9th lord {lord_9} is placed in the 10th house.",
            "Meaning for Native": "Fortune, father/guru blessings, higher learning and dharma flow into career and public status.",
            "Strength Factors": get_strength_flags(chart, lord_9)
        })

    if house_10_lord == 9:
        yogas.append({
            "Yoga": "Dharma-Karma Adhipati Yoga",
            "Formed By": f"10th lord {lord_10}",
            "Condition": f"10th lord {lord_10} is placed in the 9th house.",
            "Meaning for Native": "Career, karma and public role are influenced by higher wisdom, teachers, dharma, law, spirituality or long-distance themes.",
            "Strength Factors": get_strength_flags(chart, lord_10)
        })

    return yogas


def detect_raja_yoga(chart):
    """
    Simple Raja Yoga detection:
    connection between kendra lords and trikona lords.
    Basic detection:
    - Kendra lord and trikona lord conjunct
    - Trikona lord in kendra
    - Kendra lord in trikona
    """
    yogas = []
    house_lords = get_house_lords(chart)

    for kendra in KENDRA_HOUSES:
        for trikona in TRIKONA_HOUSES:
            kendra_lord = house_lords.get(kendra)
            trikona_lord = house_lords.get(trikona)

            if not kendra_lord or not trikona_lord:
                continue

            kendra_lord_house = get_planet_house(chart, kendra_lord)
            trikona_lord_house = get_planet_house(chart, trikona_lord)

            if kendra_lord == trikona_lord:
                yogas.append({
                    "Yoga": "Raja Yoga",
                    "Formed By": f"{kendra_lord} as lord connecting House {kendra} and House {trikona}",
                    "Condition": f"{kendra_lord} connects a kendra house and a trikona house through lordship.",
                    "Meaning for Native": "Supports rise, recognition, capability and constructive life direction when the planet is strong.",
                    "Strength Factors": get_strength_flags(chart, kendra_lord)
                })

            elif kendra_lord_house == trikona_lord_house:
                yogas.append({
                    "Yoga": "Raja Yoga",
                    "Formed By": f"{kendra_lord} and {trikona_lord}",
                    "Condition": f"Kendra lord {kendra_lord} and trikona lord {trikona_lord} are conjunct in House {kendra_lord_house}.",
                    "Meaning for Native": "A kendra-trikona connection can create capacity for achievement, visibility, authority and meaningful success.",
                    "Strength Factors": f"{kendra_lord}: {get_strength_flags(chart, kendra_lord)} | {trikona_lord}: {get_strength_flags(chart, trikona_lord)}"
                })

            elif trikona_lord_house in KENDRA_HOUSES:
                yogas.append({
                    "Yoga": "Raja Yoga",
                    "Formed By": f"Trikona lord {trikona_lord}",
                    "Condition": f"Trikona lord {trikona_lord} is placed in kendra House {trikona_lord_house}.",
                    "Meaning for Native": "Fortune, intelligence or dharma supports action, stability, relationship or career areas.",
                    "Strength Factors": get_strength_flags(chart, trikona_lord)
                })

            elif kendra_lord_house in TRIKONA_HOUSES:
                yogas.append({
                    "Yoga": "Raja Yoga",
                    "Formed By": f"Kendra lord {kendra_lord}",
                    "Condition": f"Kendra lord {kendra_lord} is placed in trikona House {kendra_lord_house}.",
                    "Meaning for Native": "Practical life structures support fortune, creativity, wisdom and dharmic development.",
                    "Strength Factors": get_strength_flags(chart, kendra_lord)
                })

    return deduplicate_yogas(yogas)


def detect_dhana_yoga(chart):
    """
    Basic Dhana Yoga:
    connections involving 2nd, 5th, 9th, 11th lords.
    """
    yogas = []
    house_lords = get_house_lords(chart)

    wealth_houses = [2, 5, 9, 11]

    for i, h1 in enumerate(wealth_houses):
        for h2 in wealth_houses[i + 1:]:
            lord_1 = house_lords.get(h1)
            lord_2 = house_lords.get(h2)

            if not lord_1 or not lord_2:
                continue

            lord_1_house = get_planet_house(chart, lord_1)
            lord_2_house = get_planet_house(chart, lord_2)

            if lord_1 == lord_2:
                yogas.append({
                    "Yoga": "Dhana Yoga",
                    "Formed By": lord_1,
                    "Condition": f"{lord_1} connects wealth-related houses {h1} and {h2} through lordship.",
                    "Meaning for Native": "Potential for resource-building, income, family wealth, gains or wealth through intelligence/fortune depending on planet strength.",
                    "Strength Factors": get_strength_flags(chart, lord_1)
                })

            elif lord_1_house == lord_2_house:
                yogas.append({
                    "Yoga": "Dhana Yoga",
                    "Formed By": f"{lord_1} and {lord_2}",
                    "Condition": f"Lords of wealth houses {h1} and {h2} are conjunct in House {lord_1_house}.",
                    "Meaning for Native": "Wealth houses are connected, supporting earning, accumulation, gains or prosperity when supported by strength.",
                    "Strength Factors": f"{lord_1}: {get_strength_flags(chart, lord_1)} | {lord_2}: {get_strength_flags(chart, lord_2)}"
                })

    return deduplicate_yogas(yogas)


def detect_vipareeta_raja_yoga(chart):
    """
    Basic Vipareeta Raja Yoga:
    6th, 8th, or 12th lord placed in 6th, 8th, or 12th.
    """
    yogas = []
    house_lords = get_house_lords(chart)

    for house in DUSTHANA_HOUSES:
        lord = house_lords.get(house)
        lord_house = get_planet_house(chart, lord)

        if lord and lord_house in DUSTHANA_HOUSES:
            yogas.append({
                "Yoga": "Vipareeta Raja Yoga",
                "Formed By": lord,
                "Condition": f"Lord of Dusthana House {house}, {lord}, is placed in Dusthana House {lord_house}.",
                "Meaning for Native": "Can produce rise after struggle, ability to overcome enemies, debts, disease, crises or losses, especially after maturity and effort.",
                "Strength Factors": get_strength_flags(chart, lord)
            })

    return yogas


def detect_guru_chandala_yoga(chart):
    """
    Guru Chandala Yoga:
    Jupiter conjunct Rahu or Ketu.
    """
    yogas = []

    jupiter_house = get_planet_house(chart, "Jupiter")
    rahu_house = get_planet_house(chart, "Rahu")
    ketu_house = get_planet_house(chart, "Ketu")

    if jupiter_house == rahu_house:
        yogas.append({
            "Yoga": "Guru Chandala Yoga",
            "Formed By": "Jupiter and Rahu",
            "Condition": f"Jupiter and Rahu are conjunct in House {jupiter_house}.",
            "Meaning for Native": "Can create unconventional wisdom, non-traditional beliefs, intense desire for knowledge, but may also challenge orthodox guidance, teachers or ethics unless purified by maturity.",
            "Strength Factors": f"Jupiter: {get_strength_flags(chart, 'Jupiter')} | Rahu: {get_strength_flags(chart, 'Rahu')}"
        })

    if jupiter_house == ketu_house:
        yogas.append({
            "Yoga": "Guru Chandala Yoga",
            "Formed By": "Jupiter and Ketu",
            "Condition": f"Jupiter and Ketu are conjunct in House {jupiter_house}.",
            "Meaning for Native": "Can create spiritualized wisdom, detachment from conventional learning, and deep philosophical insight, but may create distance from conventional teachers.",
            "Strength Factors": f"Jupiter: {get_strength_flags(chart, 'Jupiter')} | Ketu: {get_strength_flags(chart, 'Ketu')}"
        })

    return yogas


def detect_gaja_kesari_yoga(chart):
    """
    Basic Gaja Kesari Yoga:
    Jupiter in kendra from Moon.
    """
    yogas = []

    moon_house = get_planet_house(chart, "Moon")
    jupiter_house = get_planet_house(chart, "Jupiter")

    if not moon_house or not jupiter_house:
        return yogas

    relative_house = ((jupiter_house - moon_house) % 12) + 1

    if relative_house in [1, 4, 7, 10]:
        yogas.append({
            "Yoga": "Gaja Kesari Yoga",
            "Formed By": "Moon and Jupiter",
            "Condition": f"Jupiter is in a kendra from Moon. Moon is in House {moon_house}; Jupiter is in House {jupiter_house}.",
            "Meaning for Native": "Can support wisdom, reputation, emotional intelligence, learning, protection and capacity to guide others, depending on strength and affliction.",
            "Strength Factors": f"Moon: {get_strength_flags(chart, 'Moon')} | Jupiter: {get_strength_flags(chart, 'Jupiter')}"
        })

    return yogas


def detect_harsha_sarala_vimala_yogas(chart):
    """
    Harsha, Sarala and Vimala Yogas are the three classic Vipareeta Raja Yogas.

    Harsha Yoga:
    6th lord placed in 6th, 8th or 12th house.

    Sarala Yoga:
    8th lord placed in 6th, 8th or 12th house.

    Vimala Yoga:
    12th lord placed in 6th, 8th or 12th house.
    """

    yogas = []
    house_lords = get_house_lords(chart)

    vipareeta_rules = {
        6: {
            "name": "Harsha Yoga",
            "meaning": (
                "Can give ability to defeat enemies, overcome debts, handle disease, "
                "win competitions, manage conflict and rise through service or discipline."
            )
        },
        8: {
            "name": "Sarala Yoga",
            "meaning": (
                "Can give resilience through crisis, interest in hidden knowledge, "
                "ability to survive sudden changes, research ability and transformation through adversity."
            )
        },
        12: {
            "name": "Vimala Yoga",
            "meaning": (
                "Can give spiritual detachment, ability to manage losses, foreign connections, "
                "controlled expenditure, withdrawal from unnecessary attachments and strength in isolation."
            )
        }
    }

    for dusthana_house, rule in vipareeta_rules.items():
        lord = house_lords.get(dusthana_house)

        if not lord:
            continue

        lord_house = get_planet_house(chart, lord)
        lord_sign = get_planet_sign(chart, lord)

        if lord_house in DUSTHANA_HOUSES:
            yogas.append({
                "Yoga": rule["name"],
                "Formed By": lord,
                "Condition": (
                    f"Lord of House {dusthana_house}, {lord}, is placed in Dusthana House {lord_house} "
                    f"in {lord_sign} sign."
                ),
                "Meaning for Native": rule["meaning"],
                "Strength Factors": get_strength_flags(chart, lord)
            })

    return yogas


def get_strength_flags(chart, planet):
    details = chart["planets"].get(planet, {})

    flags = []

    dignity = details.get("dignity")
    if dignity:
        flags.append(f"Dignity: {dignity}")

    if details.get("is_retrograde"):
        flags.append("Retrograde")

    if details.get("is_combust"):
        flags.append("Combust")

    if details.get("is_vargottama"):
        flags.append("Vargottama")

    sign = details.get("sign")
    house = details.get("house")

    if sign:
        flags.append(f"Sign: {sign}")

    if house:
        flags.append(f"House: {house}")

    return ", ".join(flags) if flags else "No additional strength data available"


def deduplicate_yogas(yogas):
    seen = set()
    unique = []

    for yoga in yogas:
        key = (
            yoga.get("Yoga"),
            yoga.get("Formed By"),
            yoga.get("Condition")
        )

        if key not in seen:
            seen.add(key)
            unique.append(yoga)

    return unique


def detect_yogas(chart):
    """
    Main function to detect yogas.
    """
    yogas = []

    # Existing yogas
    yogas.extend(detect_pancha_mahapurusha_yoga(chart))
    yogas.extend(detect_dharma_karma_adhipati_yoga(chart))
    yogas.extend(detect_raja_yoga(chart))
    yogas.extend(detect_dhana_yoga(chart))
    yogas.extend(detect_vipareeta_raja_yoga(chart))
    yogas.extend(detect_harsha_sarala_vimala_yogas(chart))
    yogas.extend(detect_guru_chandala_yoga(chart))
    yogas.extend(detect_gaja_kesari_yoga(chart))

    # Newly added yogas
    yogas.extend(detect_budha_aditya_yoga(chart))
    yogas.extend(detect_chandra_mangal_yoga(chart))
    yogas.extend(detect_amala_yoga(chart))
    yogas.extend(detect_sunapha_anapha_durudhara_yogas(chart))
    yogas.extend(detect_vesi_vasi_ubhayachari_yogas(chart))
    yogas.extend(detect_parivartana_yoga(chart))
    yogas.extend(detect_neecha_bhanga_raja_yoga(chart))
    yogas.extend(detect_kalasarpa_yoga_basic(chart))
    yogas.extend(detect_daridra_yoga_basic(chart))

    return deduplicate_yogas(yogas)