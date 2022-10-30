
''' This code gets the updated location of the inernational space station which moves very fast at about 28000km/h
	via the ISS api and then the cardinal coordinate location is parsed into the google geolocation api to give
	us the actual readable physical location of the ISS via a web browser.
'''
# First we import the necessary modules
import sys
import json
import requests
import webbrowser
# Get a google api key from the google developer web portal. I did not put my key public here, instead i parsed it into an argument 
# If you have your key, you can uncomment line 14 and comment out line 13 so you can run the script directly.
YOUR_GOOGLE_API_KEY = sys.argv[1]
#YOUR_GOOGLE_API_KEY = '********************************'

# This function converts a python object into a json string.
def json_print(obj):
	text = json.dumps(obj, sort_keys=True, indent = 4)
	return text

# We make a call to the ISS api to get its updated location
response = requests.get("http://api.open-notify.org/iss-now")
print(response.status_code)
print(response.json())
json_print(response.json())

# This line is probably not necessary, but it just shows how to convert a json string back to a python object
data = json.loads(json_print(response.json()))

# We convert our python object into a list so we can easily grab our longitude and latitude coordinates.
position = list(data.values())[0]
print(position)
actual_latitude = float(position["latitude"])
actual_longitude = float(position["longitude"])

# The cordinates are parsed into the google geolocation api server.
location = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?latlng={actual_latitude},{actual_longitude}&key={YOUR_GOOGLE_API_KEY}')
print(location.json()) 

# Get the important location parameter from the python object i.e ["global_code"]
myquery = list(location.json().values())[0]["global_code"]


# Now we open it with a google search via chrome browser. The problem with this part is that google search with the webbrowser python module always
# escapes the "+" sign in the global_code string and replaces it with a space character. So in other to get the actual location in the opened google search
# Tab, then you have to replace the space with '+'.
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
url = "http://google.com/search?q="+myquery
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
webbrowser.get('chrome').open_new_tab(url)



