from libs import *

# TODO build home page

def build():
  return page("Home",{
    "classList": ["_home"],
    "children": [
      {
        "tag": "h1",
        "text": "hello world"
      }
    ]
  })
