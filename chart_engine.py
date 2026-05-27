import swisseph as swe
from datetime import datetime
import pytz
from birth_time_resolver import resolve_birth_datetime

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE
}

def get_sign(degree):
    return SIGNS[int(degree // 30)]

def get_sign_index(degree):
    return int(degree // 30)

def get_house_from_lagna(planet_sign_index, lagna_sign_index):
    return ((planet_sign_index - lagna_sign_index) % 12) + 1

def calculate_chart(dob, birth_time, place, latitude=None, longitude=None, timezone=None):
    birth_info = resolve_birth_datetime(
        dob,
        birth_time,
        place,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
    )

    utc_dt = birth_info["utc_datetime"]
    lat = birth_info["latitude"]
    lon = birth_info["longitude"]

    jd = swe.julday(
        utc_dt.year,
        utc_dt.month,
        utc_dt.day,
        utc_dt.hour + utc_dt.minute / 60 + utc_dt.second / 3600
    )

    # Lahiri ayanamsa
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ayanamsa = swe.get_ayanamsa_ut(jd)

    # Tropical ascendant from Swiss Ephemeris
    houses, ascmc = swe.houses_ex(jd, lat, lon, b'P')
    tropical_asc = ascmc[0]

    # Convert tropical ascendant to sidereal ascendant
    sidereal_asc = (tropical_asc - ayanamsa) % 360

    lagna_sign_index = get_sign_index(sidereal_asc)
    lagna_sign = get_sign(sidereal_asc)

    planets = {}

    for name, pid in PLANETS.items():
        result = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL | swe.FLG_SPEED)
        degree = result[0][0] % 360
        speed = result[0][3]
        is_retrograde = speed < 0

        sign_index = get_sign_index(degree)
        sign = get_sign(degree)
        house = get_house_from_lagna(sign_index, lagna_sign_index)

        planets[name] = {
        "degree": round(degree, 2),
        "sign": sign,
        "house": house,
        "is_retrograde": is_retrograde
    }

        if name == "Rahu":
            ketu_degree = (degree + 180) % 360
            ketu_sign_index = get_sign_index(ketu_degree)
            ketu_sign = get_sign(ketu_degree)
            ketu_house = get_house_from_lagna(ketu_sign_index, lagna_sign_index)
            planets[name]["is_retrograde"] = True

            planets["Ketu"] = {
        "degree": round(ketu_degree, 2),
        "sign": ketu_sign,
        "house": ketu_house,
        "is_retrograde": True
    }

    # Whole sign house chart
    house_chart = {}
    for i in range(12):
        house_num = i + 1
        sign_index = (lagna_sign_index + i) % 12
        house_chart[house_num] = {
            "sign": SIGNS[sign_index],
            "planets": []
        }

    for planet, details in planets.items():
        house_chart[details["house"]]["planets"].append(planet)

    return {
        "birth_date": str(dob),
        "birth_time": str(birth_time),
        "place": place,
        "ayanamsa": "Lahiri",
        "ascendant": lagna_sign,
        "asc_degree": round(sidereal_asc, 2),
        "planets": planets,
        "house_chart": house_chart,
        "birth_time_info": {
            "place": birth_info["place"],
            "latitude": birth_info["latitude"],
            "longitude": birth_info["longitude"],
            "timezone_name": birth_info["timezone_name"],
            "local_datetime": str(birth_info["local_datetime"]),
            "utc_datetime": str(birth_info["utc_datetime"]),
            "utc_offset_hours": birth_info["utc_offset_hours"],
            "dst_active": birth_info["dst_active"]
        }
    }