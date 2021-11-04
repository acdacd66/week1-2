import os

from fastapi  import FastAPI
from pydantic import BaseModel
from dotenv   import load_dotenv
from neo4j    import GraphDatabase

load_dotenv()
uri=os.getenv("uri")
user=os.getenv("user")
pwd=os.getenv("pwd")


class song(BaseModel):
    title    : str
    musician : str

class album(BaseModel):
    title    : str
    song     : str
    musician : str

class musician(BaseModel):
    name : str

def connection():
    driver=GraphDatabase.driver(uri=uri,auth=(user,pwd))
    return driver

app=FastAPI()
@app.post("/create_song")
def createnode(node:song):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    q1="""
    merge(song:song{title:$title, musician:$musician}) return song.title as title
    """
    x={"title":node.title, "musician":node.musician}
    results=session.run(q1,x)
    data=[{"Title":row["title"]}for row in results][0]["Title"]
    return {"response":"node created with song name as: "+data}

@app.post("/create_album")
def createnode(node:album):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    q1="""
    merge(album:album{title:$title, song:$song, musician:$musician}) return album.title as title
    """
    x={"title":node.title, "song":node.song, "musician":node.musician}
    results=session.run(q1,x)
    data=[{"Title":row["title"]}for row in results][0]["Title"]
    return {"response":"node created with album name as: "+data}

@app.post("/create_musician")
def createnode(node:musician):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    q1="""
    merge(musician:musician{name:$name}) return musician.name as name
    """
    x={"name":node.name}
    results=session.run(q1,x)
    data=[{"Name":row["name"]}for row in results][0]["Name"]
    return {"response":"node created with musician name as: "+data}



@app.get("/get_song")
def getnode(request):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    q1="""
    match(song) where song.musician = "$param" return song.title as title
    """
    x={"param":request}
    results=session.run(q1,x)
    return {"response":[
        {
            "Title":row["title"]
        } for row in results
    ]}
