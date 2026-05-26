from datetime import datetime
from zoneinfo import ZoneInfo
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder


def resolve_birth_datetime(dob, birth_time, place):
    """
    Converts local birth date/time/place into:
    - latitude
    - longitude
    - IANA timezone
    - localized datetime
    - UTC datetime
    - UTC offset hours

    dob: Python date object
    birth_time: Python time object
    place: string like "New York, United States" or "Delhi, India"
    """

    geolocator = Nominatim(user_agent="astrea_birth_chart_app")
    location = geolocator.geocode(place, timeout=10)

    if location is None:
        raise ValueError(
            f"Could not find coordinates for place: {place}. "
            "Please enter city and country clearly."
        )

    latitude = location.latitude
    longitude = location.longitude

    tf = TimezoneFinder()
    timezone_name = tf.timezone_at(lat=latitude, lng=longitude)

    if timezone_name is None:
        raise ValueError(
            f"Could not determine timezone for place: {place}."
        )

    local_naive_datetime = datetime.combine(dob, birth_time)
    local_timezone = ZoneInfo(timezone_name)

    local_datetime = local_naive_datetime.replace(tzinfo=local_timezone)
    utc_datetime = local_datetime.astimezone(ZoneInfo("UTC"))

    utc_offset_hours = local_datetime.utcoffset().total_seconds() / 3600

    return {
        "place": place,
        "latitude": latitude,
        "longitude": longitude,
        "timezone_name": timezone_name,
        "local_datetime": local_datetime,
        "utc_datetime": utc_datetime,
        "utc_offset_hours": utc_offset_hours,
        "dst_active": bool(local_datetime.dst() and local_datetime.dst().total_seconds() != 0)
    }