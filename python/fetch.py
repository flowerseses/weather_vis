import json
import requests

# Api url and endpoints that we might need
url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/'
locations = 'locations'
stations = 'stations'
data = 'data'
destination = 'CITY:NO000004' # id of Oslo in the NCDC dataset. Find and replace with desired id.
stationid = 'GHCND:NOM00001492' # Blindern station

def read_token():
    f = open('../token', 'r')
    result = f.readline();
    f.close
    return result

def main():
    token = read_token()
    headers = {'token' : token}
    data_url = url + data + '?stationid=' + stationid + '&datasetid=GHCND&datatypeid=TMAX&datatypeid=TMIN&startdate=2016-01-01&enddate=2016-12-31&units=metric&limit=1000'
    r = requests.get(data_url, headers=headers)
    json_results = r.json()
    json_result = json_results['results']
    final_data = {}
    for entry in json_result:
        date = entry['date'][:10]
        value = entry['value']
        datatype = entry['datatype']
        if date in final_data:
            if datatype == 'TMAX':
                final_data[date].append(value)
            else:
                final_data[date].insert(0, value)
        else:
            final_data[date] = [value]
    
    print(json.dumps(final_data))
    out = open('../data/2016-daily-summary', 'w')
    json.dump(final_data, out)
    out.close

if __name__ == "__main__":
    main()
