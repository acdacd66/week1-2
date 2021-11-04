from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()
uri=os.getenv("uri")
user=os.getenv("user")
pwd=os.getenv("pwd")


class nodemodel(BaseModel):
    name:str
   

def connection():
    driver=GraphDatabase.driver(uri=uri,auth=(user,pwd))
    return driver

app=FastAPI()
@app.post("/create_music")
def createnode(node:nodemodel):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    q1="""
    merge(n:music{name:$name}) return n.name as name
    """
    x={"name":node.name}
    results=session.run(q1,x)
    data=[{"Name":row["name"]}for row in results][0]["Name"]
    return {"response":"node created with music name as: "+data}

@app.post("/create_album")
def createnode(node:nodemodel):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    q1="""
    merge(n:album{name:$name}) return n.name as name
    """
    x={"name":node.name}
    results=session.run(q1,x)
    data=[{"Name":row["name"]}for row in results][0]["Name"]
    return {"response":"node created with album name as: "+data}

@app.post("/create_musician")
def createnode(node:nodemodel):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    q1="""
    merge(n:musician{name:$name}) return n.name as name
    """
    x={"name":node.name}
    results=session.run(q1,x)
    data=[{"Name":row["name"]}for row in results][0]["Name"]
    return {"response":"node created with musician name as: "+data}