from functools import lru_cache
import requests

BASE_URL = "http://ergast.com/api/f1"

#a single shared session is faster than creating a new one for each request
_session = requests.Session()
_session.headers.update({ "User-Agent": "F1-FastestLap-Predictor/0.1"})

def _get(url: str, params: None):
    """Helper function to make GET requests to the Ergast API."""
    params = params or {}
    # Ergast paginates; set a high limit to reduce number of requests
    params.setdefault("limit", "1000")
    r = _session.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

@lru_cache(maxsize=2048)
def results(year: int, round: int):
    """
    Race results for a given year and round.
    """
    return _get(f"{BASE_URL}/{year}/{round}/results.json", params={})