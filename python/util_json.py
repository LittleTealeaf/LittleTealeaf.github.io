import os, json
import util_assets as assets
from util_assets import Asset
from list_filetypes import *

DIR = ['json']

def load(asset: Asset=None,path: str=None):
    data = None
    with open(asset.path if asset else path) as file:
        data = json.load(file)
    return data

def save(data,asset: Asset=None,path: list=None):
    with open(asset.path if asset else path,'w') as file:
        file.write(json.dumps(data))

def ref(dict,asset: Asset=None,dir: list=None):
    string = json.dumps(dict)
    if not asset:
        asset = Asset(dir=(dir if dir else DIR),seed=string,type=JSON)
    with open(asset.path,'w') as file:
        file.write(string)
    return asset.ref
    