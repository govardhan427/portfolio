import requests
import json # Ensure json is imported for exception handling

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
    """
    Fetches location details (City, Lat, Lng) for a given IP.
    """
    # 1. Skip local IPs (they don't have locations)
    if ip == '127.0.0.1' or ip.startswith('192.168.') or ip == 'localhost':
        return {
            "city": "Localhost",
            "country_name": "Local Dev",
            "lat": 23.5937, # Default Center of India
            "lng": 78.9629
        }

    # 2. Define safe fallback data
    FALLBACK_DATA = {
        "city": "Unknown",
        "country_name": "Unknown",
        "lat": None,
        "lng": None
    }

    # 3. Call Geo-IP API with robust error handling
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        
        # CRITICAL FIX 1: Check status code before parsing JSON
        if response.status_code != 200:
            print(f"GeoIP Error: Non-200 Status Code ({response.status_code})")
            return FALLBACK_DATA
        
        # CRITICAL FIX 2: Handle empty response body (the likely cause of "Expecting value")
        data = response.json()
        
        if 'error' in data or not data.get('city'):
            print(f"GeoIP Error: API returned error message or missing data: {data.get('reason', 'N/A')}")
            return FALLBACK_DATA

        return {
            "city": data.get('city'),
            "region": data.get('region'),
            "country": data.get('country_name'),
            "lat": data.get('latitude'),
            "lng": data.get('longitude'),
            "org": data.get('org')
        }
        
    except json.JSONDecodeError:
        # Catch the explicit error 'Expecting value: line 1 column 1 (char 0)'
        print("GeoIP Error: Failed to decode JSON (Likely empty/malformed response body)")
        return FALLBACK_DATA
        
    except requests.RequestException as e:
        # Catch connection errors, timeouts, etc.
        print(f"GeoIP Request Error: {e}")
        return FALLBACK_DATA
        
    except Exception as e:
        # Catch any other unexpected error
        print(f"GeoIP Unexpected Error: {e}")
        return FALLBACK_DATA