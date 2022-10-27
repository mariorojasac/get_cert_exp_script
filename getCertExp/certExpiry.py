from urllib.request import Request, urlopen, ssl, socket
from urllib.error import URLError, HTTPError
import datetime
from datetime import date
import json
from trycourier import Courier
import os
from dotenv import load_dotenv


#Getting .env variables -------------->
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


#Site URL checking  ------------------->
base_url = 'fssabenefits.in.gov'
port = '443'



#Getting SSL info -------------------->
hostname = base_url
context = ssl.create_default_context()
experiation_date = ''

with socket.create_connection((hostname, port)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print('Socket Version: '+ ssock.version())
        data = ssock.getpeercert()
        #experiation_date is str
        experiation_date = data['notAfter']
        # dic of json data
        data = json.dumps(ssock.getpeercert())
       
print ("This is the expiration date of the SSL Cert: " + experiation_date)




#Getting Current Time  ----------------->
 
# Function to convert string to datetime
def convert_str_date(date):
    format = '%b %d %H:%M:%S %Y %Z'  # The format month day hour:minute:second year zone 
    datetime_str = datetime.datetime.strptime(date, format)
 
    return datetime_str

date_time = convert_str_date(experiation_date)
print("converted to date time, output is: ")
print(date_time)
print(type(date_time))

datetime_object = datetime.datetime.now()
print("Todays Date is: ")
print(datetime_object)
print(type(datetime_object))



#Date Conditionals ------------------>
def check_expiration():
    if datetime_object > date_time:
        return "Date missed"                                                                                                                                        
    else:
        return "Date not missed"
    
validate_experiration = check_expiration()
    

#Notification Service -------------------->

client = Courier(auth_token=API_TOKEN) #or set via COURIER_AUTH_TOKEN env var

resp = client.send_message(
  message={
    'to': {
      'email': 'mario.rojas@moserit.com',
      'data': {'name': 'DevOps Team'}
    },
    'content': {
      'title': 'SSL Certificate Alert',
      'body': 'Hey {{name}}, take a look at the upcomming SSL experiation dates: BP will expire on ' + experiation_date + 'Experation ' + validate_experiration,
    },
    'routing': {
      'method': 'single',
      'channels': ['email'],
    }
  }
)
print(resp['requestId'])


