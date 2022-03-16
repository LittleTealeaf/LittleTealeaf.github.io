import os, json, requests
from sys import stdin
from resutil import *
from githubapi import *
from imageutil import *

# Run Initialization Scripts
clean_directory()


settings = {}
"Settings loaded from the pyconfig.json file in assets"
with open(os.path.join('.','assets','pyconfig.json')) as f:
    settings = json.load(f)

def save_json(asset,dict):
    "Directly saves a json to an asset object"
    with open(asset.path,'w') as w:
        w.write(json.dumps(dict))

def reference_json(asset,json):
    "Directly saves a json to an asset object and returns the reference"
    save_json(asset,json)
    return asset.ref

def fetch_json(asset,fetch,fetch_params={}):
    "Checks if that asset exists, calls `fetch` with `params` if it does not exist. Returns the reference"
    if not asset.exists():
        print(f'Fetching Asset: {asset.ref}')
        with open(asset.path,'w') as w:
            w.write(json.dumps(fetch(**fetch_params)))
    return asset.ref

def reference_image(img):
    "Saves an image based on the hash of it's contents, then returns the reference"
    asset = Asset(IMAGES,seed=image_hash(img),type=PNG)
    img.save(asset.path)
    return asset.ref
        
def reference_github_user(username=None,url=None,api=None):
    if not url:
        if username:
            url = f'https://api.github.com/users/{username}'
        elif api:
            url = api['url']

    asset = Asset(path=GITHUB_USER,seed=url,type=JSON)

    def fetchUser(user=None,url=None):
        if not user:
            user = api_github(url)
        user.update({
            'avatar': reference_image(image_format(image_src(user['avatar_url']),{'circular': True}))
        })

        return user

    return fetch_json(asset,fetchUser,{'url': url, 'user': api})

def reference_api_github(url,path=GITHUB):
    asset = Asset(path=path,seed=url,type=JSON)
    return fetch_json(asset,lambda: api_github(url))

def reference_json_seed(path=[],data=None):
    json_string = json.dumps(data)
    return reference_json(Asset(path=path,seed=json_string,type=JSON),data)

def reference_github_repository(url):
    asset = Asset(GITHUB_REPOSITORY,seed=url,type=JSON)
    if not asset.exists():
        repo = api_github(url)
        repo.update({
            'contributors': reference_json_seed(GITHUB_USER_LIST,[reference_github_user(api=user_api) for user_api in api_github(repo['contributors_url'])]),
            'subscribers': reference_json_seed(GITHUB_USER_LIST,[reference_github_user(api=user_api) for user_api in api_github(repo['subscribers_url'])]),
            'stargazers': reference_json_seed(GITHUB_USER_LIST,[reference_github_user(api=user_api) for user_api in api_github(repo['stargazers_url'])]),
            'languages': reference_json(Asset(GITHUB_LANGUAGES,type=JSON,seed=repo['languages_url']),api_github(repo['languages_url'])),
            'events': reference_api_github(repo['events_url'],GITHUB_EVENTS),
            'releases': reference_api_github(repo['releases_url'].replace('{/id}',''),GITHUB_RELEASES),
            'owner': reference_github_user(api=repo['owner'])
        })
        [repo.pop(key,None) for key in ['permissions','contributors_url','subscribers_url','stargazers_url','languages','events_url','releases_url']]
        save_json(asset,repo)
    return asset.ref

with open(os.path.join('.','assets','projects.json')) as p:
    projects = []

    for project_ref in json.load(p):
        project = {
            'repository': reference_github_repository(project_ref['repository_api'])
        }


        if 'attributes' in project_ref:
            project['attributes'] = reference_json_seed(PROJECT_ATTRIBUTES,project_ref['attributes'])
        
        projects.append(reference_json(Asset(path=PROJECT,seed=project_ref['repository_api'],type=JSON),project))
    
    save_json(Asset(name='projects.json'),projects)
