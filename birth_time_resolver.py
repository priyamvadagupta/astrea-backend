from datetime import datetime
from zoneinfo import ZoneInfo
from geopy.geocoders import Nominatim
from geopy.exc import (
    GeocoderRateLimited,
    GeocoderServiceError,
    GeocoderTimedOut,
    GeocoderUnavailable,
    GeopyError,
)
from timezonefinder import TimezoneFinder


_PLACE_RESOLUTION_CACHE: dict[str, tuple[float, float, str]] = {}


def _normalize_place(place: str) -> str:
    return " ".join((place or "").strip().lower().split())


def resolve_birth_datetime(dob, birth_time, place, latitude=None, longitude=None, timezone=None):
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

    if latitude is not None and longitude is not None and timezone is not None:
        resolved_latitude = float(latitude)
        resolved_longitude = float(longitude)
        timezone_name = str(timezone)
    else:
        normalized_place = _normalize_place(place)
        cached = _PLACE_RESOLUTION_CACHE.get(normalized_place)
        if cached is not None:
            resolved_latitude, resolved_longitude, timezone_name = cached
        else:
            try:
                geolocator = Nominatim(user_agent="astrea_birth_chart_app")
                location = geolocator.geocode(place, timeout=10)
            except (GeocoderRateLimited, GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError, GeopyError):
                location = None

            if location is None:
                raise ValueError("Could not resolve this birth place. Please enter city, state, country.")

            resolved_latitude = float(location.latitude)
            resolved_longitude = float(location.longitude)

            tf = TimezoneFinder()
            timezone_name = tf.timezone_at(lat=resolved_latitude, lng=resolved_longitude)

            if timezone_name is None:
                raise ValueError("Could not resolve this birth place. Please enter city, state, country.")

            _PLACE_RESOLUTION_CACHE[normalized_place] = (resolved_latitude, resolved_longitude, timezone_name)

    local_naive_datetime = datetime.combine(dob, birth_time)
    try:
        local_timezone = ZoneInfo(timezone_name)
    except Exception as e:
        raise ValueError("Could not resolve this birth place. Please enter city, state, country.") from e

    local_datetime = local_naive_datetime.replace(tzinfo=local_timezone)
    utc_datetime = local_datetime.astimezone(ZoneInfo("UTC"))

    utc_offset_hours = local_datetime.utcoffset().total_seconds() / 3600

    return {
        "place": place,
        "latitude": resolved_latitude,
        "longitude": resolved_longitude,
        "timezone_name": timezone_name,
        "local_datetime": local_datetime,
        "utc_datetime": utc_datetime,
        "utc_offset_hours": utc_offset_hours,
        "dst_active": bool(local_datetime.dst() and local_datetime.dst().total_seconds() != 0)
    }