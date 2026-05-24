def map_house_to_life_events(house: int):
    house_events = {
        1: ["self", "health", "identity", "new beginnings"],
        2: ["money", "family", "speech", "values"],
        3: ["communication", "skills", "siblings", "effort"],
        4: ["home", "mother", "property", "emotional security"],
        5: ["children", "romance", "creativity", "education", "intelligence"],
        6: ["health routines", "work pressure", "debts", "conflict", "service"],
        7: ["relationship", "marriage", "partnerships", "clients"],
        8: ["transformation", "sudden events", "shared resources", "healing"],
        9: ["luck", "higher education", "teachers", "father", "dharma"],
        10: ["career", "status", "profession", "public image"],
        11: ["gains", "networks", "income", "fulfilment of desires"],
        12: ["foreign lands", "sleep", "isolation", "spirituality", "expenses"]
    }

    return house_events.get(house, [])


def create_timing_windows(transit_analysis: list):
    """
    Creates broad timing windows based on slow planet transits.
    This is intentionally conservative for a visitor-facing website.
    """
    windows = []

    for item in transit_analysis:
        planet = item["transit_planet"]
        house = item["activated_house"]
        sign = item["transit_sign"]
        events = map_house_to_life_events(house)

        if not house:
            continue

        if planet == "Jupiter":
            timing_strength = "supportive growth window"
            time_window = "next 6 to 12 months"
        elif planet == "Saturn":
            timing_strength = "slow but important karmic development"
            time_window = "next 12 to 24 months"
        elif planet in ["Rahu", "Ketu"]:
            timing_strength = "karmic shift and inner reorientation"
            time_window = "next 6 to 18 months"
        else:
            timing_strength = "active period"
            time_window = "next few months"

        windows.append({
            "planet": planet,
            "house": house,
            "sign": sign,
            "life_areas": events,
            "time_window": time_window,
            "timing_quality": timing_strength,
            "interpretation": (
                f"{planet} transiting {sign} activates the {house} house, "
                f"bringing focus to {', '.join(events)}. This suggests a "
                f"{timing_strength} over the {time_window}."
            ),
            "why": (
                f"The timing is inferred from {planet}'s slow transit through "
                f"the sign that corresponds to the native's {house} house."
            )
        })

    return windows