import googlemaps
import time
import winsound
import requests

# Defining the Google API Key
APIKEY = "AIzaSyDUX0IzOLGu-gKkO5vf5Ot6zQlEuSp5d9o"

# Initialize GMaps Client
gmaps = googlemaps.Client(key=APIKEY)


def main():
    targetLocation = getTargetLocation()
    threshold = setThreshold()
    if targetLocation:
        try:
            while True:
                currentLocation = getCurrentLocation(APIKEY)
                #currentLocation = 40.171998, -74.834069
                distance = getDistance(currentLocation, targetLocation)
                if distance is not None and distance <= threshold:
                    print("Alarm is activated. You are near the Target Location.")
                    alarm()
                    break
                else:
                    print(f"Distance to target: {distance} meters")
                time.sleep(10)
        except KeyboardInterrupt:
            print("Program Terminated.")

# Gets Current Location in Real-Time
def getCurrentLocation(APIKEY):
    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={APIKEY}'
    headers = {'Content-Type': 'application/json'}
    data = {}
    response = requests.post(url, headers=headers, json=data)
    if(response.status_code == 200):
        locationData = response.json()
        latitude = locationData['location']['lat']
        longitude = locationData['location']['lng']
        return latitude, longitude
    else:
        print(f"Error getting current location: {response.status_code} - {response.text}")
        return None, None
    

# Gets Target Location
def getTargetLocation():
    try:
        targetLatitude = float(input("Enter the desired Target Latitude: "))
        targetLongitude = float(input("Enter the desired Target Longitude: "))
        return targetLatitude, targetLongitude
    except ValueError:
        print("Invalid input. Enter a valid desired Target Latitude and Longitude")
        return None, None
    

# Gets Distance from Current Location to Target Location in Real-Time
def getDistance(origin, destination):
    distance_matrix = gmaps.distance_matrix(origin, destination, mode="walking", units="metric")["rows"][0]["elements"][0]
    distance_value = distance_matrix["distance"]["value"] if "distance" in distance_matrix else None
    return distance_value

# Sounds Alarm when activated
def alarm():
    while True:
        winsound.Beep(1000,5000)
        user_input = input("Press 'q' + Enter to stop the alarm: ")
        if user_input.lower() == 'q':
            print("Alarm stopped.")
            break

def setThreshold():
    threshold = input("Set the threshold distance for the Alarm: ")
    return int(threshold)

if __name__ == "__main__":
    print("Starting program...")
    main()
