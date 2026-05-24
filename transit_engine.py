from datetime import date


SIGN_ORDER = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]


def get_house_from_sign(ascendant_sign: str, target_sign: str) -> int:
    """
    Whole-sign house calculation.
    If Ascendant is Leo and target sign is Pisces, Pisces becomes 8th house.
    """
    if ascendant_sign not in SIGN_ORDER or target_sign not in SIGN_ORDER:
        return None

    asc_index = SIGN_ORDER.index(ascendant_sign)
    target_index = SIGN_ORDER.index(target_sign)

    return ((target_index - asc_index) % 12) + 1


def get_current_slow_transits():
    """
    Placeholder/current transit layer.
    Later this can be replaced by true ephemeris calculations.
    For now, manually maintain slow planet signs.
    """
    return {
        "Jupiter": {
            "sign": "Gemini",
            "themes": "growth, learning, guidance, expansion, opportunity"
        },
        "Saturn": {
            "sign": "Pisces",
            "themes": "discipline, responsibility, delay, maturity, karmic lessons"
        },
        "Rahu": {
            "sign": "Aquarius",
            "themes": "desire, ambition, unconventional growth, obsession, future direction"
        },
        "Ketu": {
            "sign": "Leo",
            "themes": "detachment, past karma, spiritualization, release, inner mastery"
        }
    }


def analyze_transits_for_native(chart: dict):
    """
    Adds transit interpretation based on ascendant sign.
    Expected chart contains:
    chart["ascendant"] = "Leo"
    """
    ascendant = chart.get("ascendant") or chart.get("ascendant_sign")

    if not ascendant:
        return []

    transits = get_current_slow_transits()
    output = []

    for planet, data in transits.items():
        transit_sign = data["sign"]
        activated_house = get_house_from_sign(ascendant, transit_sign)

        output.append({
            "transit_planet": planet,
            "transit_sign": transit_sign,
            "activated_house": activated_house,
            "themes": data["themes"],
            "why": (
                f"For a {ascendant} ascendant, {transit_sign} falls in the "
                f"{activated_house} house. Therefore, the transit of {planet} "
                f"activates matters of the {activated_house} house."
            )
        })

    return output