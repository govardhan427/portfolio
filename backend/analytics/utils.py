import requests
import json
from django.core.cache import cache

# Define how long to cache the IP lookup result (24 hours = 86400 seconds)
IP_CACHE_TIMEOUT = 86400

def get_client_ip(request):
    """
    Retrieves the real client IP address, handling proxy headers.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Note: Render provides the user IP as the first IP in the list
        ip = x_forwarded_for.split(',')[0].strip() 
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_ip_location(ip):
    # 3. Define safe fallback data (Used if API fails or rate limits)
    FALLBACK_DATA = {
        "city": "Unknown",
        "country_name": "Unknown",
        "lat": None,
        "lng": None
    }
    
    # 1. Skip local IPs and return structured Localhost data
    if ip == '127.0.0.1' or ip.startswith('192.168.') or ip == 'localhost':
        return {
            "city": "Localhost",
            "country_name": "Local Dev",
            "lat": 23.5937, 
            "lng": 78.9629
        }

    # 2. Check Cache First (The FIX for rate limiting)
    cached_data = cache.get(f"ip_location_{ip}")
    if cached_data:
        return cached_data # Return cached data immediately

    # 4. Call Geo-IP API with robust error handling
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        
        # --- FIX: Handle 429 Rate Limit Explicitly ---
        if response.status_code == 429: 
            print("GeoIP Error: Rate limit hit (429). Serving fallback data.")
            # Cache the fallback data briefly (1 hour) to avoid spamming the API
            cache.set(f"ip_location_{ip}", FALLBACK_DATA, timeout=3600) 
            return FALLBACK_DATA
        
        # Handle other non-200 errors (e.g., 404, 500)
        if response.status_code != 200:
            print(f"GeoIP Error: Non-200 Status Code ({response.status_code})")
            return FALLBACK_DATA
        
        # Attempt to decode JSON
        data = response.json()
        
        # Handle API's internal error response structure
        if 'error' in data or not data.get('city'):
            print(f"GeoIP Error: API returned error/missing city data: {data.get('reason', 'N/A')}")
            return FALLBACK_DATA

        # Construct successful result
        result = {
            "city": data.get('city'),
            "region": data.get('region'),
            "country_name": data.get('country_name'),
            "lat": data.get('latitude'),
            "lng": data.get('longitude'),
            "org": data.get('org')
        }
        
        # 5. Store result in cache before returning
        cache.set(f"ip_location_{ip}", result, timeout=IP_CACHE_TIMEOUT)
        return result
        
    except json.JSONDecodeError as e: # Catch the specific JSON error
        print(f"GeoIP Error: Failed to decode JSON (Likely empty/malformed body): {e}")
        return FALLBACK_DATA # <--- CORRECT RETURN
        
    except requests.RequestException as e: # Catch connection errors/timeouts
        print(f"GeoIP Request Error: {e}")
        return FALLBACK_DATA # <--- CORRECT RETURN
        
    except Exception as e: # Catch any other unexpected error
        print(f"GeoIP Unexpected Error: {e}")
        return FALLBACK_DATA # <--- CORRECT RETURN