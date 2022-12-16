import pandas as pd
import matplotlib.pyplot as plt
import json
import requests
import urllib.request
from bs4 import BeautifulSoup 
import tweepy

echo "# EM-599-Final-Project" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:ahermsdorf/EM-599-Final-Project.git
git push -u origin main

#current water level  
cwl_response = requests.get("https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=latest&station=8518750&product=water_level&datum=NAVD&time_zone=lst_ldt&units=english&format=json")
current_water_level = pd.DataFrame.from_dict(cwl_response.json()['data'])
current_water_level = current_water_level.drop(labels=["s","f","q"], axis=1)
current_water_level['v'] = current_water_level['v'].astype(float)


#hourly mean water level historical 
hourly_mean_response = requests.get("https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=20221107&end_date=20221207&station=8518750&product=water_level&datum=NAVD&time_zone=lst_ldt&units=english&format=json")
hourly_mean_water_level = pd.DataFrame.from_dict(hourly_mean_response.json()['data']).drop(labels=["s","f",], axis=1)
hourly_mean_water_level['v'] = pd.to_numeric(hourly_mean_water_level['v'])
def plot_hourly_mean_water_level():
    hourly_mean_water_level_plot = hourly_mean_water_level.plot(kind = 'line',
            x = 't',
            y = 'v',
            color = 'green',)
    return(hourly_mean_water_level_plot)

#hourly precipitation
hourly_precipitation = pd.read_csv('C:\\Users\\StevensUser\\Downloads\\Hourly Precipitation.csv')
def plot_hourly_precipitation():
    hourly_precipitation_plot = hourly_precipitation.plot(kind = 'line',
            x = 't',
            y = 'p',
            color = 'blue',
            sharex=plt)
    return(hourly_precipitation_plot)

#hourly predicitions 
hourly_prediciton_response = requests.get("https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=20221212&end_date=20230112&station=8518750&product=predictions&datum=NAVD&time_zone=lst&interval=hilo&units=english&format=json")
hourly_prediction_water_level = pd.DataFrame.from_dict(hourly_prediciton_response.json()["predictions"])
hourly_prediction_water_level['v'] = pd.to_numeric(hourly_prediction_water_level['v'])
def plot_hourly_prediction_water_level():
    hourly_prediction_water_level_plot = hourly_prediction_water_level.plot(kind = 'line',
            x = 't',
            y = 'v',
            color = 'red')

    return(hourly_prediction_water_level_plot)

#current pricipitation data 
def getPrecData():
    html_data = [] 
    response = urllib.request.urlopen('https://waterdata.usgs.gov/nwis/current/?type=precip&group_key=state_cd&search_site_no_station_nm=pier%2025&site_no_name_select=station_nm')
    soup = BeautifulSoup(response, 'html.parser')
    for child in soup.find('tbody').children:
        for tr in child:
            for td in tr:
                html_data.append(td)  
    current_prec_data = html_data[12:16]
    current_prec_df = pd.DataFrame([current_prec_data], columns = ["1 Hour", "4 Hour", "24 Hour", "7 Days"], dtype=float)
    current_prec_df = current_prec_df.drop(labels=["7 Days"], axis=1)
    return(current_prec_df)

#Historical Flood Data 1
hist_flood_data = pd.read_csv('C:\\Users\\StevensUser\\Downloads\\Flood Data.csv')

flood_data = pd.read_csv("C:\\Users\\StevensUser\\Downloads\\Flood Locations.csv")
def curruntFloodWarning():
    for ind in flood_data.index:
        print("\n",flood_data["Location"][ind],":")
        currentWaterLevel = current_water_level['v'][0]
        if currentWaterLevel > flood_data['Max Flood '][ind]:
            print("\nThere is potential Major Flooding(24in) in",flood_data["Location"][ind] )
            #api.update_status("There is Major Flooding(24in) in",flood_data["Location"][ind])
        elif currentWaterLevel > flood_data['Mod. Flood '][ind]:
            print("\nThere is potential Moderate Flooding(12in) in ",flood_data["Location"][ind] )
            #api.update_status("There is Moderate Flooding(12in) in ",flood_data["Location"][ind])
        elif currentWaterLevel > flood_data['Min. Flood '][ind]:
            print("\nThere is potential Minimal Flooding(4in) in ",flood_data["Location"][ind])
            #api.update_status("There is Minimum Flooding(4in) in ",flood_data["Location"][ind])

def futureFloodWarning():
    for ind in flood_data.index:
        print("\n",flood_data["Location"][ind],":")
        for indx in hourly_prediction_water_level.index:
            if hourly_prediction_water_level['v'][indx] > flood_data['Max Flood '][ind]:
                print("\nThere will be potential Major Flooding(24in) in",flood_data["Location"][ind], "at", hourly_prediction_water_level['t'][indx])
            elif hourly_prediction_water_level['v'][indx] > flood_data['Mod. Flood '][ind]:
                print("\nThere will be potential Moderate Flooding(12in) in ",flood_data["Location"][ind],"at", hourly_prediction_water_level['t'][indx])
            elif hourly_prediction_water_level['v'][indx] > flood_data['Min. Flood '][ind]:
                print("\nThere will be potential Minimum Flooding(4in) in ",flood_data["Location"][ind],"at", hourly_prediction_water_level['t'][indx])

# place the twitter_secrets file under <User>/anaconda3/Lib
from twitter_secrets import twitter_secrets as ts

consumer_key = ts.CONSUMER_KEY
consumer_secret = ts.CONSUMER_SECRET
access_token = ts.ACCESS_TOKEN
access_secret = ts.ACCESS_SECRET

#authenticating to access the twitter API
auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
api=tweepy.API(auth)    

user_active = True
while user_active == True: 
    print("\nWelcome to our NYC Flood Warning system!",
          "\nPress 1 to see current conditions",
          "\nPress 2 to see historical data",
          "\nPress 3 to see estimated current flood conditions",
          "\nPress 4 to see estimated future flood conditions",
          "\nPress 5 to exit")
    Selector = int(input("Please input a selection:"))
    if Selector == 1:
        print("\nCurrent Conditions",
              "\nPress 1 to see current tide level",
              "\nPress 2 to see current precipitation",
              "\nPress 3 to see all current conditions",
              "\nPress 4 to return to homescreen")
        conditionsSelector = int(input("Please input a selection:"))
        if conditionsSelector == 1:
            print(current_water_level)
        elif conditionsSelector == 2:
            print("\n", getPrecData())
        elif conditionsSelector == 3:
            print("\nCurrent Water Level:\n",current_water_level)
            print("\nPrecipitation\n", getPrecData())
        elif conditionsSelector == 4:
            break 
        else:
            print("Invalid selection")
    elif Selector == 2:
        print("\nHistorical Data",
              "\nPress 1 to see historical tide level",
              "\nPress 2 to see historical precipitation",
              "\nPress 3 to see historical flood conditions",
              "\nPress 4 to see all historical conditions",
              "\nPress 5 to return to homescreen")
        historicalSelector = int(input("Please input a selection:"))
        if historicalSelector == 1:
            plot_hourly_mean_water_level()  
            plt.xticks(rotation = 90)
            plt.show()
        elif historicalSelector == 2:
            plot_hourly_precipitation()
            plt.xticks(rotation = 90)
            plt.show()
        elif historicalSelector == 3:
            listOfUniques = hist_flood_data['Location'].unique()
            for unique in listOfUniques:
                tempdf = hist_flood_data[hist_flood_data['Location'] == unique]
                plt.bar(tempdf['Date'], tempdf['Flood Level (in)'], label=unique)
                plt.xticks(rotation = 90)
                plt.title(unique, )
                plt.show()
        elif historicalSelector == 4:
            plot_hourly_mean_water_level()
            plt.xticks(rotation = 90)
            plt.show()
            #historical precipitation
            plot_hourly_precipitation()
            plt.xticks(rotation = 90)
            plt.show()
            #historical flood data
            listOfUniques = hist_flood_data['Location'].unique()
            for unique in listOfUniques:
                tempdf = hist_flood_data[hist_flood_data['Location'] == unique]
                plt.bar(tempdf['Date'], tempdf['Flood Level (in)'], label=unique)
                plt.xticks(rotation = 90)
                plt.title(unique, )
                plt.show()
        elif historicalSelector == 5:
            break 
        else:
            print("Invalid selection")
    elif Selector == 3:
        curruntFloodWarning()
    elif Selector == 4:
        futureFloodWarning()
    elif Selector ==5:
        break
    else:
        print("Invalid Selection")





