import os
import util_json as json
import datetime
import util_temp as tmp

FILE_NAME = tmp.tmp_path('analytics.json')

class Keys:
    GITHUB_API_CALLS = 'Github API Calls'
    IMAGE_REQUESTS = 'Image Requests'
    LAST_UPDATED = 'Last Updated'
    REPOSITORY_REQUESTS = 'Repository APIs'
    USER_REQUESTS = 'User APIs'
    EVENT_REQUESTS = 'Event APIs'

DEFAULTS: dict = {
    Keys.GITHUB_API_CALLS: 0,
    Keys.REPOSITORY_REQUESTS: 0,
    Keys.USER_REQUESTS: 0,
    Keys.EVENT_REQUESTS: 0,
    Keys.IMAGE_REQUESTS: 0,
}

INCREMENT = lambda item: item + 1

def load() -> dict:
    if os.path.exists(FILE_NAME):
        return json.load(path=FILE_NAME)
    else:
        return DEFAULTS.copy()

def update(updater) -> None:
    data = load()
    updater(data)
    json.save(data,path=FILE_NAME)

def update_value(key: str, value_updater) -> None:
    data = load()
    data[key] = value_updater(data[key])
    json.save(data,path=FILE_NAME)

def compile() -> dict:
    data = load()
    data[Keys.LAST_UPDATED] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M")

    analytics = [{'name':key,'value':data[key]} for key in data]
    return analytics

def ref() -> str:
    return json.ref(compile())

def ping_api() -> None:
    update_value(Keys.GITHUB_API_CALLS,INCREMENT)

def ping_image() -> None:
    update_value(Keys.IMAGE_REQUESTS, INCREMENT)

def ping_user() -> None:
    update_value(Keys.USER_REQUESTS,INCREMENT)

def ping_event() -> None:
    update_value(Keys.EVENT_REQUESTS,INCREMENT)

def ping_repo() -> None:
    update_value(Keys.REPOSITORY_REQUESTS,INCREMENT)