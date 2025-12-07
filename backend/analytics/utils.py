import requests

def get_client_ip(request):
    """
    Retrieves the real client IP address, handling proxy headers.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
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

    # 2. Call Free Geo-IP API
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        data = response.json()
        
        if 'error' in data:
            return {}

        return {
            "city": data.get('city'),
            "region": data.get('region'),
            "country": data.get('country_name'),
            "lat": data.get('latitude'),
            "lng": data.get('longitude'),
            "org": data.get('org') # ISP Name
        }
    except Exception as e:
        print(f"GeoIP Error: {e}")
        return {}