from googleapiclient.discovery import build
import pprint
import json

my_api_key = "AIzaSyCj5T-EGDTTNI4lb4kv2ineO2pcaN54Gr0"
my_cse_id = "008718956744724044293:_6erfi4tylq"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def call_search(term):
    results = google_search(term, my_api_key, my_cse_id, num=2)
    result_string = ""
    for result in results:
        #pprint.pprint(result)
        parsed_json = json.loads(json.dumps(result))
        #print("TITLE : "+parsed_json['title'])
        #print("LINK :"+parsed_json['link'])
        #print("DESCRIPTION : "+parsed_json['snippet'])
        #print('\n')
        result_string += parsed_json['title']+"\n"+parsed_json['link']+"\n"+parsed_json['snippet']+"\n\n"
    return result_string

def get_link(term):
    results = google_search(term, my_api_key, my_cse_id, num=1)
    result_string = ""
    for result in results:
        #pprint.pprint(result)
        parsed_json = json.loads(json.dumps(result))
        #print("TITLE : "+parsed_json['title'])
        #print("LINK :"+parsed_json['link'])
        #print("DESCRIPTION : "+parsed_json['snippet'])
        #print('\n')
    return parsed_json['link']

#call_search('google')
