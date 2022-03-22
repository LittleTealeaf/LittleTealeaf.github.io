import os
from urllib.request import Request
import requests
import sys
import time
import datetime
import util_analytics as analytics
import util_images as images
import util_json as json
from util_assets import Asset
from list_filetypes import *
import util_config as configs

DIR = ['github']
DIR_USER = DIR + ['user']
DIR_EVENT = DIR + ['event']
DIR_REPO = DIR + ['repo']

TOKEN = None
if os.path.exists(os.path.join('.', 'github_token')):
    with open(os.path.join('.', 'github_token')) as f:
        TOKEN = f.readline()
else:
    TOKEN = os.getenv('API_GITHUB')

if not TOKEN:
    print("ERROR: NO GITHUB API TOKEN PROVIDED")
    sys.exit(1)


def GET(url: str, parameters: dict = {}, headers: dict = {}) -> requests.Response:
    "Authenticates and sends a GET request to the specified url with the provided parameters and headers"
    print(f'API: {url} {parameters}')

    headers = headers.copy()
    headers.update({
        'authorization': f'token {TOKEN}'
    })
    analytics.ping_api()
    wait_time = configs.config('github','api','timeout_delay')
    max_attempts = 60 / wait_time
    request: requests.Response = None
    current_attempt = 0
    while (not request or request.status_code != 200) and current_attempt < max_attempts:
        current_attempt = current_attempt + 1
        request = requests.get(url,headers=headers,params=parameters)

        if request.status_code != 200:
            print(f'Error Attempt {current_attempt}: {request.json()["message"]}')
            
            if request.status_code == 403:
                print(f'Waiting {wait_time} seconds before reattempting...')
                time.sleep(wait_time)
    
    if current_attempt < max_attempts:
        print(f'Unable to get API')
        sys.exit(1)
    return request

def api_requests_remaining() -> int:
    "Returns the number of authenticated requests remaining for the api token"
    return GET('https://api.github.com').headers['x-ratelimit-remaining']

def api(url: str, parameters: dict = {}) -> dict:
    "Fetches and returns the json object from the url with the specified parameters"
    result = GET(url, parameters=parameters).json()
    if isinstance(result, dict):
        [result.pop(key, None) for key in configs.config('github','remove_keys')]
    return result

def api_list(url: str, parameters: dict = {}, count: int=30) -> list:
    "Fetches and returns a list of json objects from the specified url with the given parameters. If the count is over 100, then it will attempt to load pages until the count is fulfilled. It will stop sending requests when the total count is met"
    obj = []
    page = 1
    per_page = min(100, count)
    params = {}
    params.update(parameters)
    params['per_page'] = per_page
    while len(obj) < count:
        params['page'] = page
        api_segment = api(url, params)
        items_left = count - len(obj)
        if len(api_segment) == per_page and items_left < per_page:
            obj.extend(api_segment[:items_left])
        else:
            obj.extend(api_segment)
            if len(api_segment) < per_page:
                break
        page = page + 1
    return obj


def api_ref(url: str, parameters: dict={}, asset=None) -> str:
    "Fetches and stores the data from a url with the specified parameters to a json file, storing that data in an asset"
    data = api(url, parameters)
    if not asset:
        asset = Asset(dir=DIR, type=JSON, seed=url)

    return json.ref(data, asset)


def ref_user(username: str = None, url: str = None, obj: dict = None, config: dict = {}) -> str:
    "Creates a user reference from a username, url, or obj. Must have one of those in order to complete"
    config = configs.compile(config,'github','users')
    key_followers = 'followers_list'
    key_following = 'following_list'

    if not url:
        if username:
            url = f'https://api.github.com/users/{username}'
        elif obj:
            url = obj['url']

    asset = Asset(dir=DIR_USER, seed=url, type=JSON)

    if asset.exists():
        cache = json.load(asset=asset)
        if obj:
            cache.update(obj)
        obj = cache
    else:
        analytics.ping_user()

    if not obj:
        obj = api(url)
    elif config['force_api']:
        obj.update(api(url))

    if 'avatar' not in obj:
        obj['avatar'] = images.ref(obj['avatar_url'], circular=True)
    
    if config['followers']['include'] and key_followers not in obj:
        obj[key_followers] = ref_user_list(obj['followers_url'],count=config['followers']['count'])
    
    if config['following']['include'] and key_following not in obj:
        obj[key_following] = ref_user_list(obj['following_url'].replace('{/other_user}',''),count=config['following']['count'])

    if config['events']['include'] and 'events' not in obj:
        obj['events'] = ref_event_list(obj['events_url'].replace('{/privacy}','/public'),count=config['events']['count'], load_repo=config['events']['load_repo'])

    [obj.pop(key,None) for key in config['remove_keys']]

    return json.ref(obj, asset)


def ref_user_list(url: str, config: dict={},count: int = configs.config('github','users','count')) -> str:
    return json.ref([ref_user(obj=i,config=config.copy()) for i in api_list(url,count=count)])


def ref_repository(url: str=None, obj: dict=None, config: dict={}) -> str:
    "Creates a reference to a repository from a url or object. Must have one of those to complete"

    config = configs.compile(config,'github','repositories')

    if not url:
        url = obj['url']

    asset = Asset(dir=DIR_REPO,type=JSON,seed=(url if url else obj['url']))

    if asset.exists():
        cache = json.load(asset=asset)
        if obj:
            for key in obj:
                if key not in cache:
                    cache[key] = obj[key]
        obj = cache
    else:
        analytics.ping_repo()
    
    if not obj:
        obj = api(url)
        obj['api_loaded'] = True
        
    elif config['force_api'] and ('api_loaded' not in obj or not obj['api_loaded']):
        obj.update(api(url))
        obj['api_loaded'] = True

    if isinstance(obj['owner'],dict):
        obj['owner'] = ref_user(obj=obj['owner'])
    
    if 'languages' not in obj:
        languages = api(obj['languages_url'])
        obj['languages'] = json.ref([{'name':key,'value':languages[key]} for key in languages])
    

    if config['subscribers']['include'] and 'subscribers' not in obj:
        obj['subscribers'] = ref_user_list(obj['subscribers_url'],count=config['subscribers']['count'])
    
    if config['stargazers']['include'] and 'stargazers' not in obj:
        obj['stargazers'] = ref_user_list(obj['stargazers_url'],count=config['stargazers']['count'])

    if config['events']['include'] and 'events' not in obj:
        obj['events'] = ref_event_list(obj['events_url'],load_repo=False,count=config['events']['count'])
    
    if config['contributors']['include'] and 'contributors' not in obj:
        contributors = []
        for contributor in api_list(obj['contributors_url'], count=config['contributors']['count']):
            if '[bot]' not in contributor['login'] or config['contributors']['include_bots']:
                contributors.append(contributor)
        obj['contributors'] = json.ref([{'contributions': i['contributions'],'user':ref_user(obj=i)} for i in contributors])
    
    if config['template']['include'] and 'template_repository' in obj and isinstance(obj['template_repository'],dict):
        obj['template_repository'] = ref_repository(obj=obj['template_repository'])
    
    if config['parent']['include'] and 'parent' in obj and isinstance(obj['parent'],dict):
        obj['parent'] = ref_repository(obj=obj['parent'])
    
    if config['source']['include'] and 'source' in obj and isinstance(obj['source'],dict):
        obj['source'] = ref_repository(obj=obj['source'])

    [obj.pop(key,None) for key in config['remove_keys']]
    
    return json.ref(obj,asset=asset)

        
    

def ref_event(obj: dict,load_repo: bool=False) -> str:
    "Creates an event reference from an object"
    asset = Asset(dir=DIR_EVENT,type=JSON,seed=obj['id'])
    if not asset.exists():
        analytics.ping_event()
        if 'repo' in obj:
            if load_repo:
                obj['repo'] = ref_repository(obj=obj['repo'])
            else:
                repo_asset = Asset(dir=DIR_REPO,seed=obj['repo']['url'],type=JSON)
                if repo_asset.exists():
                    obj['repo'] = repo_asset.ref
                else:
                    obj['repo'] = json.ref(obj['repo'],asset=repo_asset)
        if 'actor' in obj:
            obj['actor'] = ref_user(url=obj['actor']['url'])
        json.save(obj,asset=asset)
    return asset.ref
                


def ref_event_list(url: str,count: int=configs.config('github','events','count'), load_repo: bool=False) -> str:
    "Gets a reference list"
    return json.ref([ref_event(i,load_repo=load_repo) for i in api_list(url,count=count)])
