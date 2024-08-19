from django.shortcuts import render
import urllib.request
import json

"""
{
	"coord": {
		"lon": -0.1257,
		"lat": 51.5085
	},
	"weather": [
		{
			"id": 802,
			"main": "Clouds",
			"description": "scattered clouds",
			"icon": "03d"
		}
	],
	"base": "stations",
	"main": {
		"temp": 19.96,
		"feels_like": 19.76,
		"temp_min": 18.75,
		"temp_max": 21.18,
		"pressure": 1013,
		"humidity": 67,
		"sea_level": 1013,
		"grnd_level": 1009
	},
	"visibility": 10000,
	"wind": {
		"speed": 5.36,
		"deg": 125,
		"gust": 7.6
	},
	"clouds": {
		"all": 40
	},
	"dt": 1724083380,
	"sys": {
		"type": 2,
		"id": 2075535,
		"country": "GB",
		"sunrise": 1724043182,
		"sunset": 1724094925
	},
	"timezone": 3600,
	"id": 2643743,
	"name": "London",
	"cod": 200
}"""

def index(request):
    weather_data = None
    error_message = None

    if request.method == "POST":
        city = request.POST.get("city", "")
        if city:
            city = city.strip()
            api_key = "d7ea5364585677bbfe3d356b2bc97693"
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            try:
                with urllib.request.urlopen(url) as response:
                    res = response.read()
                    # Print raw response for debugging
                    print("Raw API Response:", res.decode("utf-8"))
                    weather_data = json.loads(res)
                    data = {
                        "country": weather_data["sys"]["country"],
                        "city": city,
                        "current_temp": weather_data["main"]["temp"],
                        'feels_like': weather_data["main"]['feels_like'],
                        'max_temp': weather_data["main"]["temp_max"],
                        'min_temp': weather_data["main"]["temp_min"],
                    }
            except urllib.error.HTTPError as e:
                error_message = f"HTTPError: {e.code} - {e.reason}"
            except Exception as e:
                error_message = str(e)
        else:
            error_message = "City name is required."

    return render(
        request,
        "index.html",
        {"weather_data": data, "error_message": error_message},
    )


