import requests
import json
import pprint
pp = pprint.PrettyPrinter()
headers = {
    'Connection': 'keep-alive',
    'Authorization': "$d1c40a72eafa33461ec8c81e396c5fc9",
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4558.0 Safari/537.36 Edg/93.0.946.1',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Origin': 'http://haulier.rincsdemo.com',
    'Referer': 'http://haulier.rincsdemo.com/',
    'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8'
}
bodyparams = {
    "id": 367,
    "Auth_token":"Barrier-token:Y2Q1NWY3MzNlMjEwYTY0YTY0YzhlZWU5ODY1ZGY3Nzc1MDRkMDVhOWM1ZDM4NzdmZGViZTczY2RmYzcxZTA1ZD8xLWEyNDdkMGUzMzJhYWY1MTk3MmQwYWEwMDAzMjAwOTAwOTNmYThjM2Q4MzNjZmI3ODZmZWI0Yjk0YTM0MjM4NTE/MC00OWRjNTJlNmJmMmFiZTVlZjZlMmJiNWIwZjFlZTJkNzY1YjkyMmFlNmNjOGI5NWQzOWRjMDZjMjFjODQ4Zjhj"
    }

s = requests.sessions.Session()
data = json.dumps(bodyparams)
print(data)
res1 = s.post('http://77.68.118.222:3001/job/get-job-list', data=data, headers=headers)
# res2 = s.post('http://77.68.118.222:3001/job/pod', data=data, headers=headers)
with open("randomfile.json", 'w+') as f:
    json.dump(res1.json(),f, indent=4)
pp.pprint(res1.json())
print(res1.json())




#Need to install requests package for python
#easy_install requests
# import requests

# # Set the request parameters
# url = 'https://dev61381.service-now.com/api/now/table/x_676855_cloudtdms_test?sysparm_limit=1'

# # Eg. User name="admin", Password="admin" for this code sample.
# # user = 'cloudtdms'
# # pwd = ''

# # Set proper headers
# headers = {
#     "Content-Type":"application/json",
#     "Accept":"application/json"
# }

# # Do the HTTP request
# response = requests.get(url, auth=(user, pwd), headers=headers )

# # Check for HTTP codes other than 200
# if response.status_code != 200: 
#     print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
#     exit()

# # Decode the JSON response into a dictionary and use the data
# data = response.json()
# print(data)
