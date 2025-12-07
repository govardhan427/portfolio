import requests
import json
from django.conf import settings
from django.core.cache import cache
import ipaddress # Used for accurate private IP checking (recommended library)

IP_CACHE_TIMEOUT = 86400  # 24 hours

# ------------------------------
# Utilities
# ------------------------------

def safe_log(*args):
    """Logs only when DEBUG=True to avoid polluting production logs."""
    if getattr(settings, "DEBUG", False):
        print("GeoIP DEBUG:", *args)


def get_client_ip(request):
    """
    Retrieves the real client IP, respecting proxy headers.
    Fully production-safe.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        # User IP is the first one in the list provided by proxy/load balancer
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR") or "0.0.0.0"
        
    safe_log("Client IP found:", ip)
    return ip


# ------------------------------
# Normalizer: Convert ANY provider into one standard structure
# ------------------------------

def normalize_geoip_response(data):
    """
    Converts different provider JSON formats into ONE clean structure.
    Returns None if unusable.
    """

    # ipapi.co structure (first provider)
    if "city" in data and "country_name" in data:
        return {
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country_name"),
            "lat": data.get("latitude"),
            "lng": data.get("longitude"),
            "org": data.get("org"),
        }

    # ip-api.com structure (fallback provider)
    if data.get("status") == "success":
        return {
            "city": data.get("city"),
            "region": data.get("regionName"),
            "country": data.get("country"),
            "lat": data.get("lat"),
            "lng": data.get("lon"),
            "org": data.get("org"),
        }

    return None


# ------------------------------
# MAIN: IP → Location
# ------------------------------

def get_ip_location(ip):
    """
    Intelligent, cached, multi-provider GeoIP with guaranteed safe output.
    """
    # ✨ Standardized return format
    FALLBACK = {
        "city": "Unknown",
        "region": "Unknown",
        "country": "Unknown",
        "lat": None,
        "lng": None,
        "org": "Unknown",
    }
    LOCAL_IP_FALLBACK = {
        "city": "Localhost",
        "region": "Local Dev",
        "country": "Local Dev",
        "lat": 23.5937,
        "lng": 78.9629,
        "org": "Local Machine",
    }

    # 1️⃣ Ignore local / private IPs using the ipaddress module (CRITICAL FIX)
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private or ip == "127.0.0.1" or ip == "localhost":
            safe_log("IP is private/local. Skipping API call.")
            return LOCAL_IP_FALLBACK
    except ValueError:
        # Handle invalid IP addresses gracefully
        safe_log("IP is invalid.")
        return FALLBACK

    # 2️⃣ Check cache (fastest path)
    CACHE_KEY = f"geoip_{ip}"
    cached = cache.get(CACHE_KEY)
    if cached:
        safe_log("Serving from cache.")
        return cached

    # 3️⃣ Providers (priority order)
    PROVIDERS = [
        f"https://ipapi.co/{ip}/json/",
        f"http://ip-api.com/json/{ip}",  # fallback provider
    ]

    # 4️⃣ Try each provider until one works
    for api in PROVIDERS:
        try:
            res = requests.get(api, timeout=4)
            safe_log("Attempting API:", api, "Status:", res.status_code)

            if res.status_code == 429:
                safe_log("Rate limit hit:", api, "Caching fallback for 1 hour.")
                # Cache the fallback data briefly (1 hour) to avoid spamming the API
                cache.set(CACHE_KEY, FALLBACK, 3600) 
                return FALLBACK

            if res.status_code != 200:
                continue

            data = res.json()

            # -------- Normalize to consistent format --------
            normalized = normalize_geoip_response(data)
            if normalized:
                safe_log("Success. Caching result.")
                cache.set(CACHE_KEY, normalized, IP_CACHE_TIMEOUT)
                return normalized

        except Exception as e:
            safe_log("GeoIP provider failed:", api, e)
            continue

    # 5️⃣ All providers failed → fallback
    safe_log("All providers failed. Caching fallback for 1 hour.")
    cache.set(CACHE_KEY, FALLBACK, 3600)  
    return FALLBACK