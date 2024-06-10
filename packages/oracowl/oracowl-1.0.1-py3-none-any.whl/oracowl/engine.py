from timezonefinder import TimezoneFinder
from pytz import timezone, utc
import math
import os
import sys
import ephem
from datetime import datetime, timedelta
from .dso_db import dso_list

current_path = os.path.dirname(os.path.abspath(__file__))
root_path = current_path
sys.path.append(root_path)


planets = {
    "sun": ephem.Sun(),
    "moon": ephem.Moon(),
    "mercury": ephem.Mercury(),
    "venus": ephem.Venus(),
    "mars": ephem.Mars(),
    "jupiter": ephem.Jupiter(),
    "saturn": ephem.Saturn(),
    "uranus": ephem.Uranus(),
    "neptune": ephem.Neptune(),
    "pluto": ephem.Pluto(),
}

tf = TimezoneFinder()

timezone_cache = {}


def _rad2deg(rad: float) -> float:
    """
    Convert radians to degrees

    :param rad: radians
    :type rad: float

    :return: degrees
    :rtype: float
    """
    return rad * 180 / math.pi


def _today():
    """
    Get the current date at 13:00 UTC

    :return: datetime
    :rtype: datetime
    """
    return datetime.now(tz=utc).replace(hour=13, minute=0, second=0, microsecond=0)


def _get_timezone(lat: float, lon: float) -> int:
    """
    Get the timezone offset in seconds for a given latitude and longitude

    :param lat: latitude
    :type lat: float

    :param lon: longitude
    :type lon: float

    :return: timezone offset in seconds
    :rtype: int

    :raises: Exception if it cannot find the timezone for the given latitude and longitude
    """
    try:
        lat = round(float(lat), 2)
        lon = round(float(lon), 2)
        if (lat, lon) in timezone_cache:
            return timezone_cache[(lat, lon)]

        tz = tf.timezone_at(lng=lon, lat=lat)
        if tz is None:
            return 0

        location_now = datetime.now(tz=timezone(tz))
        time_offset = location_now.utcoffset().total_seconds()
        timezone_cache[(lat, lon)] = time_offset
        return time_offset
    except Exception as e:
        print(f"Error in get_timezone: {e}")
        return 0


def compute_dso_by_id(dso_id: int, lat: float, lon: float, dt: datetime = None):
    """
    Compute the DSO with the given id at the given latitude and longitude

    :param dso_id: DSO id
    :type dso_id: str

    :param lat: latitude
    :type lat: float

    :param lon: longitude
    :type lon: float

    :param dt: datetime
    :type dt: datetime

    :return: DSO data as a dictionary
    :rtype: dict
    """
    try:
        # find the dso dictionary with the given id inside the dso_list
        dso = next((dso for dso in dso_list if dso["id"] == dso_id), None)
        if dso is None:
            return None
        return compute_dso(dso, lat, lon, dt)
    except Exception as e:
        print(f"Error in compute_dso_by_id: {e}")
        return None


def compute_dso(
    dso: dict, lat: float, lon: float, dt: datetime = None, skip_neverup: bool = False
) -> dict:
    """
    Compute the DSO with the given data at the given latitude and longitude for the given datetime

    :param dso: DSO data from the dso_list
    :type dso: dict

    :param lat: latitude
    :type lat: float

    :param lon: longitude
    :type lon: float

    :param dt: datetime
    :type dt: datetime

    :param skip_neverup: skip the DSOs if it never goes above the horizon
    :type skip_neverup: bool

    :return: DSO data as a dictionary
    :rtype: dict
    """
    try:
        observer = ephem.Observer()
        observer.lat = ephem.degrees(lat)
        observer.lon = ephem.degrees(lon)
        observer.date = dt if dt is not None else _today()

        time_offset = _get_timezone(lat, lon)

        body = ephem.FixedBody()
        body._ra = str(dso["ra"])
        body._dec = str(dso["dec"])

        body.compute(observer)

        sun = ephem.Sun()
        sunrise_time = ephem.Date(observer.next_rising(sun).datetime())
        sunset_time = ephem.Date(observer.next_setting(sun).datetime())

        if sunrise_time < sunset_time:
            sunrise_time = ephem.Date(sunrise_time.datetime() + timedelta(days=1))

        if sunset_time > sunrise_time:
            sunset_time = ephem.Date(sunset_time.datetime() - timedelta(days=1))

        night_duration = (
            sunrise_time.datetime() - sunset_time.datetime()
        ).total_seconds()

        rising_time = (
            observer.next_rising(body)
            if not body.neverup and not body.circumpolar
            else None
        )
        setting_time = (
            observer.next_setting(body)
            if not body.neverup and not body.circumpolar
            else None
        )
        if (
            setting_time is not None
            and rising_time is not None
            and setting_time < rising_time
        ):
            setting_time = ephem.Date(setting_time.datetime() + timedelta(days=1))

        transit_time = observer.next_transit(body) if not body.neverup else None

        if not body.neverup:
            observer.date = observer.next_transit(body)
            body.compute(observer)
            max_altitude = body.alt

            observer.date = observer.next_rising(sun)
            body.compute(observer)
            sunrise_altitude = body.alt

            observer.date = observer.next_setting(sun)
            body.compute(observer)
            sunset_altitude = body.alt

            if transit_time < sunset_time:
                max_altitude = sunset_altitude
            elif transit_time > sunrise_time:
                max_altitude = sunrise_altitude
        else:
            if skip_neverup:
                return None

            max_altitude = 0
            sunrise_altitude = 0
            sunset_altitude = 0

        sunset_altitude_deg = round(_rad2deg(sunset_altitude))
        sunrise_altitude_deg = round(_rad2deg(sunrise_altitude))
        max_altitude_deg = round(_rad2deg(max_altitude))

        visible_start_time = (
            rising_time.datetime()
            if rising_time is not None
            else sunrise_time.datetime()
        )
        if visible_start_time < sunset_time.datetime():
            visible_start_time = sunset_time.datetime()

        visible_end_time = (
            setting_time.datetime()
            if setting_time is not None
            else sunrise_time.datetime()
        )
        if visible_end_time > sunrise_time.datetime():
            visible_end_time = sunrise_time.datetime()

        visible_total_time = (visible_end_time - visible_start_time).total_seconds()
        elevation_delta = sunrise_altitude_deg - sunset_altitude_deg

        is_visible = (
            visible_total_time > 3600 * 3
            and (sunrise_altitude_deg > 20 or sunset_altitude_deg > 20)
            and (elevation_delta > 0 or max_altitude_deg > 40)
        )

        if not is_visible and skip_neverup:
            return None

        magnitude_inverted = 14 - dso["apparent_magnitude"]
        oracowl_rank = (
            (visible_total_time / night_duration) * magnitude_inverted * max_altitude
        )
        rising_time = (
            (rising_time.datetime() + timedelta(seconds=time_offset)).strftime("%H:%M")
            if rising_time is not None
            else "-"
        )
        setting_time = (
            (setting_time.datetime() + timedelta(seconds=time_offset)).strftime("%H:%M")
            if setting_time is not None
            else "-"
        )

        dso_image_id = dso["main_dso_alias"].replace(" ", "-")
        response = {
            "alias": dso["main_dso_alias"],
            "rising": rising_time,
            "setting": setting_time,
            "transit": (
                transit_time.datetime() + timedelta(seconds=time_offset)
            ).strftime("%H:%M"),
            "altitude_at_sunset": sunset_altitude_deg,
            "altitude_at_sunrise": sunrise_altitude_deg,
            "altitude_max": max_altitude_deg,
            "magnitude": (
                round(dso["apparent_magnitude"], 1)
                if dso["apparent_magnitude"] is not None
                else "N/A"
            ),
            "is_visible": is_visible,
            "visible_total_time": visible_total_time,
            "size": dso["size_string"],
            "constellation": dso["constellation_name"],
            "familiar_name": dso["main_name"],
            "image_url": f"https://oracowl.io/thumbs/{dso_image_id}.jpg",
            "telescopius_url": dso["url"],
            "oracowl_rank": oracowl_rank,
        }
        return response
    except Exception as e:
        print(f"Error in compute_dso: {e}")
        return None


def _compute_planet_with_observer(planet_id: str, observer: ephem.Observer) -> dict:
    """
    Compute the planet with the given id for the given latutide and longitude defined in the observer

    :param planet_id: planet id (e.g. "sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto")
    :type planet_id: str

    :param observer: observer
    :type observer: ephem.Observer

    :return: planet data as a dictionary
    :rtype: dict
    """
    try:
        lat = _rad2deg(observer.lat)
        lon = _rad2deg(observer.lon)

        time_offset = _get_timezone(lat, lon)

        planet = planets[planet_id]
        planet.compute(observer)

        phase_string = ""
        if planet.name.lower() == "moon":
            sun = planets["sun"]
            sun.compute(observer)

            tau = 2.0 * ephem.pi
            sunlon = ephem.Ecliptic(sun).lon
            moonlon = ephem.Ecliptic(planet).lon

            angle = (moonlon - sunlon) % tau
            quarter = int(angle * 4.0 // tau)
            phase_string = "waxing" if quarter < 2 else "waning"

        response = {
            "name": planet.name.lower(),
            "rise_time": (
                (planet.rise_time.datetime() + timedelta(seconds=time_offset)).strftime(
                    "%H:%M"
                )
                if planet.rise_time is not None
                else "-"
            ),
            "set_time": (
                (planet.set_time.datetime() + timedelta(seconds=time_offset)).strftime(
                    "%H:%M"
                )
                if planet.set_time is not None
                else "-"
            ),
            "max_altitude": (
                round(_rad2deg(planet.transit_alt))
                if planet.transit_alt is not None
                else "-"
            ),
            "max_altitude_time": (
                (
                    planet.transit_time.datetime() + timedelta(seconds=time_offset)
                ).strftime("%H:%M")
                if planet.transit_alt is not None
                else "-"
            ),
            "earth_distance": round(planet.earth_distance, 4),
            "phase": round(planet.phase),
            "phase_string": phase_string,
        }
        return response
    except Exception as e:
        print(f"Error in _compute_planet_with_observer: {e}")
        return None


def compute_planet(planet_id: str, lat: float, lon: float, dt: datetime = None) -> dict:
    """
    Compute the planet with the given id at the given latitude and longitude for the given datetime

    :param planet_id: planet id (e.g. "sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto")
    :type planet_id: str

    :param lat: lat
    :type lat: float

    :param lon: lon
    :type lon: float

    :param dt: datetime
    :type dt: datetime

    :return: planet data as a dictionary
    :rtype: dict
    """
    try:
        observer = ephem.Observer()
        observer.lat = ephem.degrees(lat)
        observer.lon = ephem.degrees(lon)
        observer.date = dt if dt is not None else _today()

        return _compute_planet_with_observer(planet_id, observer)
    except Exception as e:
        print(f"Error in compute_planet: {e}")
        return None


def compute_planets(lat: float, lon: float, dt: datetime = None) -> list:
    """
    Compute all the planets at the given latitude and longitude for the given datetime

    :param lat: latitude
    :type lat: float

    :param lon: longitude
    :type lon: float

    :param dt: datetime
    :type dt: datetime

    :return: list of planet data as dictionaries
    :rtype: list
    """
    try:
        return [compute_planet(planet_id, lat, lon, dt) for planet_id in planets.keys()]
    except Exception as e:
        print(f"Error in compute_planets: {e}")
        return None


def compute_polaris(lat: float, lon: float, dt: datetime = None) -> dict:
    """
    Compute the Polaris data at the given latitude and longitude for the given datetime

    :param lat: latitude
    :type lat: float

    :param lon: longitude
    :type lon: float

    :param dt: datetime
    :type dt: datetime

    :return: Polaris data as a dictionary
    :rtype: dict
    """
    try:
        observer = ephem.Observer()
        observer.lat = ephem.degrees(lat)
        observer.lon = ephem.degrees(lon)
        observer.date = dt if dt is not None else datetime.now(tz=utc)

        sidereal_time = observer.sidereal_time()

        polaris = ephem.readdb("Polaris,f|M|F7,2:31:48.704,89:15:50.72,2.02,2000")
        polaris.compute(observer)
        local_hour_angle = sidereal_time - polaris.g_ra
        response = {
            "hour_angle_radians": local_hour_angle,
            "hour_angle_angle": round(float(local_hour_angle) * 180 / math.pi, 2),
            "hour_angle_ra": str(ephem.hours(local_hour_angle)),
            "sidereal_time": str(sidereal_time),
        }
        return response
    except Exception as e:
        print(f"Error in compute_polaris: {e}")
        return None


def compute_night(lat: float, lon: float, dt: datetime = None) -> dict:
    """
    Calculates the astronomical data for the given date and location, suggesting the top 20 DSOs to observe based on the Oracowl rank

    :param lat: latitude
    :type lat: float

    :param lon: longitude
    :type lon: float

    :param dt: datetime
    :type dt: datetime

    :return: astronomical data as a dictionary
    :rtype: dict
    """
    try:
        polaris = compute_polaris(lat, lon)
        result = {"polaris": polaris, "dso": []}
        dso_list_top_list = sorted(
            dso_list,
            key=lambda x: (
                14 - x["apparent_magnitude"]
                if x["apparent_magnitude"] is not None
                else -100
            ),
            reverse=True,
        )[:100]
        for dso in dso_list_top_list:
            computed = compute_dso(dso, lat, lon, dt, skip_neverup=True)
            if (
                computed is not None
                and computed["is_visible"]
                and computed["magnitude"] != "N/A"
            ):
                result["dso"].append(computed)

        # filter only the top 20 dso by Oracowl rank
        result["dso"] = sorted(
            result["dso"],
            key=lambda x: (x["oracowl_rank"],),
            reverse=True,
        )[:20]
        planets = compute_planets(lat, lon, dt)
        result["planets"] = planets

        return result
    except Exception as e:
        print(f"Error in compute_tonight: {e}")
        raise
