from flask import Flask, render_template,request, jsonify
import urllib.request
import json

from math import radians, sin, cos, sqrt, asin


app = Flask(__name__)

@app.route('/')
def index():

#importing necessary libraries




#obtaining ISS location info
    req = urllib.request.Request("http://api.open-notify.org/iss-now.json")
    response = urllib.request.urlopen(req)


#reading info and defining dictionary with info
    iss_location = json.loads(response.read())



#obtaining IP address
    if not request.headers.getlist("X-Forwarded-For"):
        ip = request.remote_addr
    else:
        ip = request.headers.getlist("X-Forwarded-For")[0]

#defining ISS Lat/Long variables
    ISS_lat = (iss_location['iss_position']['latitude'])
    ISS_long = (iss_location['iss_position']['longitude'])

  

#defining URL for location API
    ipurl = 'http://api.ipstack.com/'+ip+'?access_key=8f55a29a90e2a665cd50a73057988b64'

#defining and reading Location info from API
    IPlocation = urllib.request.urlopen(ipurl)
    json_string = IPlocation.read()
    IPlocation.close()

#Creating location dictionary/defining laction lat/long variables
    location = json.loads(json_string)
    location_lat = location['latitude']
    location_long = location['longitude']
    

    

#define constant of earth radius
    earth_radius = 3959

#defininf the difference in radians of latitudes and longitudes
    latdiff = radians(float(location_lat)-float(ISS_lat))
    longdiff = radians(float(location_long)-float(ISS_long))


#defining lat and long in radians
    lat1 = radians(float(ISS_lat))
    lat2 = radians(float(location_lat))

#defining haversine and center angle equations
    haversine= sin(latdiff/2)**2 + cos(lat1)*cos(lat2)*sin(longdiff/2)**2
    centerangle= 2*asin(sqrt(haversine))

#determining distance value +240 for distance above earth
    distance = sqrt(((earth_radius*centerangle)**2)+ (240**2))
    value1 ='You are about '+str(round(distance,2))+ ' miles away from the ISS!'
    value2 = 'The ISS is located at '+str(ISS_lat)+ ' latitude, and '+str(ISS_long)+ ' longitude!'
    value3 = 'You are located at '+str(location_lat)+' latitude, and '+str(location_long)+' longitude!'
    
    
    return render_template("profile.html", value1=value1,value2=value2,value3=value3)
	


@app.route("/resume")
def resume():
    return render_template("resume.html")



if __name__ =="__main__":
	app.run(debug=True)