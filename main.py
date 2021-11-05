from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()
uri=os.getenv("uri")
user=os.getenv("user")
pwd=os.getenv("pwd")


class nodeModel(BaseModel):
    name:str

class musicianSongRelationModel(BaseModel):
    musician_name:str
    music_name:str

class albumSongRelationModel(BaseModel):
    album_name:str
    music_name:str

def connection():
    driver=GraphDatabase.driver(uri=uri,auth=(user,pwd))
    return driver

app=FastAPI()
@app.post("/create/music")
def createNode(node:nodeModel):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    x={"name":node.name}
    q1="""
    match(s:music{name:$name}) WITH COUNT(s) > 0  as node_exists
    RETURN node_exists
    """
    results1=session.run(q1,x)
   
    exists=[{"Name":row["node_exists"]}for row in results1][0]["Name"]
    if exists == True:
        raise HTTPException(status_code=404, detail="이미 등록된 음악입니다.")
    
       
    q2="""
    merge(s:music{name:$name}) set s.album_name = null return s.name as name
    """
    results2=session.run(q2,x)
            
    data=[{"Name":row["name"]}for row in results2][0]["Name"]
 
    return {"response":"해당 음악이 등록되었습니다. : "+data}

@app.post("/create/album")
def createNode(node:nodeModel):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    x={"name":node.name}
    q1="""
    match(a:album{name:$name}) WITH COUNT(a) > 0  as node_exists
    RETURN node_exists
    """
    results1=session.run(q1,x)
   
    exists=[{"Name":row["node_exists"]}for row in results1][0]["Name"]
    if exists == True:
        raise HTTPException(status_code=404, detail="이미 등록된 앨범입니다.")
    

    q2="""
    merge(a:album{name:$name}) return a.name as name
    """
    
    results2=session.run(q2,x)
    data=[{"Name":row["name"]}for row in results2][0]["Name"]
    return {"response":"해당 앨범이 등록되었습니다.: "+data}

@app.post("/create/musician")
def createNode(node:nodeModel):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    x={"name":node.name}
    q1="""
    match(m:musician{name:$name}) WITH COUNT(m) > 0  as node_exists
    RETURN node_exists
    """
    results1=session.run(q1,x)
   
    exists=[{"Name":row["node_exists"]}for row in results1][0]["Name"]
    if exists == True:
        raise HTTPException(status_code=404, detail="이미 등록된 음악가입니다.")

    q2="""
    merge(m:musician{name:$name}) return m.name as name
    """
    
    results2=session.run(q2,x)
    data=[{"Name":row["name"]}for row in results2][0]["Name"]
    return {"response":"해당 음악가는 등록되었습니다.: "+data}

@app.post("/connect/musician-song")
def createRelationship(node:musicianSongRelationModel):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    x={"musician_name":node.musician_name, "music_name":node.music_name}
    q1="""
    match(s:music{name:$music_name}) WITH COUNT(s) > 0  as node_exists
    RETURN node_exists
    """
    results1=session.run(q1,x)
   
    exists=[{"Name":row["node_exists"]}for row in results1][0]["Name"]
    if exists == False:
        raise HTTPException(status_code=404, detail="등록되지 않은 음악입니다.")
    
    q2="""
    match(m:musician{name:$musician_name}) WITH COUNT(m) > 0  as node_exists
    RETURN node_exists
    """
    results2=session.run(q2,x)
   
    exists=[{"Name":row["node_exists"]}for row in results2][0]["Name"]
    if exists == False:
        raise HTTPException(status_code=404, detail="등록되지 않은  음악가입니다.")
    
    q3="""
    MATCH  (m:musician {name:$musician_name}),(s:music {name: $music_name}) 
    RETURN exists( (s)-[:sings]->(m) ) as relation_exists
    """
    results3=session.run(q3,x)
    
    exists=[{"Name":row["relation_exists"]}for row in results3][0]["Name"]
    if exists == True:
        raise HTTPException(status_code=404, detail="이미 등록된 relation입니다..")
    
    q4="""
   MATCH (m:musician{name:$musician_name}),(s:music{name:$music_name})
    MERGE (s)-[:sings]->(m)
    """
    
    session.run(q4,x)
    return {"response":"relation이 등록되었습니다."}

@app.delete("/disconnect/musician-song")
def deleteRelationship(node:musicianSongRelationModel):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    x={"musician_name":node.musician_name, "music_name":node.music_name}
    q1="""
    match(s:music{name:$music_name}) WITH COUNT(s) > 0  as node_exists
    RETURN node_exists
    """
    results1=session.run(q1,x)
   
    exists=[{"Name":row["node_exists"]}for row in results1][0]["Name"]
    if exists == False:
        raise HTTPException(status_code=404, detail="등록되지 않은 음악입니다.")
    
    q2="""
    match(m:musician{name:$musician_name}) WITH COUNT(m) > 0  as node_exists
    RETURN node_exists
    """
    results2=session.run(q2,x)
   
    exists=[{"Name":row["node_exists"]}for row in results2][0]["Name"]
    if exists == False:
        raise HTTPException(status_code=404, detail="등록되지 않은  음악가입니다.")
    
    q3="""
    MATCH  (m:musician {name:$musician_name}),(s:music {name: $music_name}) 
    RETURN exists( (s)-[:sings]->(m) ) as relation_exists
    """
    results3=session.run(q3,x)
    
    exists=[{"Name":row["relation_exists"]}for row in results3][0]["Name"]
    if exists == False:
        raise HTTPException(status_code=404, detail="등록이 안된 relation입니다.")
    
    q4="""
    MATCH (s)-[rel:sings]->(m) 
    WHERE s.name= $music_name  AND m.name= $musician_name 
    DELETE rel
    """
    
    session.run(q4,x)
    return {"response":"relation이 연결 해제되었습니다."}

@app.post("/connect/album-song")
def createRelationship(node:albumSongRelationModel):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    x={"album_name":node.album_name, "music_name":node.music_name}

    q1="""
    match(a:album{name:$album_name}) WITH COUNT(a) > 0  as node_exists
    RETURN node_exists
    """
    results1=session.run(q1,x)
   
    exists=[{"Name":row["node_exists"]}for row in results1][0]["Name"]
    if exists == False:
        raise HTTPException(status_code=404, detail="등록되지 않은 앨범입니다.")

    q2="""
    match(s:music{name:$music_name}) WITH COUNT(s) > 0  as node_exists
    RETURN node_exists
    """
    results2=session.run(q2,x)
   
    exists=[{"Name":row["node_exists"]}for row in results2][0]["Name"]
    if exists == False:
        raise HTTPException(status_code=404, detail="등록되지 않은 음악입니다.")
    
    q3="""
    MATCH  (a:album {name:$album_name}),(s:music {name: $music_name}) 
    RETURN exists( (a)-[:has]->(s) ) as relation_exists
    """
    results3=session.run(q3,x)
    
    exists=[{"Name":row["relation_exists"]}for row in results3][0]["Name"]
    if exists == True:
        raise HTTPException(status_code=404, detail="이미 등록된 relation입니다..")

    q4="""
   match(a:album{name:$album_name}) match(s:music{name:$music_name}) where s.album_name is null set s.album_name = a.name
    """
    q5="""
   match(a:album{name:$album_name}) match(s:music{name:$music_name}) where s.album_name = a.name merge (a) -[:has]->(s)
    """
    
    session.run(q4,x)
    session.run(q5,x)
   
    return {"response":"relation이 등록되었습니다."}



@app.delete("/disconnect/album-song")
def deleteRelationship(node:albumSongRelationModel):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    x={"album_name":node.album_name, "music_name":node.music_name}

    q1="""
    match(a:album{name:$album_name}) WITH COUNT(a) > 0  as node_exists
    RETURN node_exists
    """
    results1=session.run(q1,x)
   
    exists=[{"Name":row["node_exists"]}for row in results1][0]["Name"]
    if exists == False:
        raise HTTPException(status_code=404, detail="등록되지 않은 앨범입니다.")

    q2="""
    match(s:music{name:$music_name}) WITH COUNT(s) > 0  as node_exists
    RETURN node_exists
    """
    results2=session.run(q2,x)
   
    exists=[{"Name":row["node_exists"]}for row in results2][0]["Name"]
    if exists == False:
        raise HTTPException(status_code=404, detail="등록되지 않은 음악입니다.")
    
    q3="""
    MATCH  (a:album {name:$album_name}),(s:music {name: $music_name}) 
    RETURN exists( (a)-[:has]->(s) ) as relation_exists
    """
    results3=session.run(q3,x)
    
    exists=[{"Name":row["relation_exists"]}for row in results3][0]["Name"]
    if exists == False:
        raise HTTPException(status_code=404, detail="등록이 안된 relation입니다.")

    q4="""
    MATCH (a)-[rel:has]->(s) 
    WHERE a.name= $album_name  AND s.name= $music_name 
    DELETE rel
        """
  
    
    session.run(q4,x)

   
    return {"response":"relation이 연결 해제되었습니다."}

@app.get("/album/music")
def readNode(q:str = None):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    x={"name":q}
  
    q1="""
    match(a:album{name:$name}) WITH COUNT(a) > 0  as node_exists
    RETURN node_exists
    """
    results1=session.run(q1,x)
   
    exists=[{"Name":row["node_exists"]}for row in results1][0]["Name"] #해당 노드가 존재하는지를 체크 -> exists:boolean: true: 존재/false:존재 안함
    if exists == False:
        raise HTTPException(status_code=404, detail="등록되지 않은 앨범입니다.")
    
       
    q2="""
    match(a:album{name:$name}) match (a) -[:has]->(s) return s as musics
    """
    results2=session.run(q2,x) # "(input album) -> (music) " 관계를 이용해서 해당 앨범의 곡 목록 추출
    datas = [{"Name":row["musics"]}for row in results2]
    if len(datas)>0:# 목록의 항목수가 0이 아니면
        response = []
        for i in range(len(datas)):
            response.append(datas[i]["Name"]["name"])

        response = list(set(response))# 목록의 값들 중복 방지
        return {"response":"해당 앨범의 곡 목록.: "+str(response)}
    else:
        return {"response":"해당 앨범에 곡이 존재하지 않습니다. "} 
        

@app.get("/album/musician")
def readNode(q:str = None):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    x={"name":q}
  
    q1=""" 
    match(a:album{name:$name}) WITH COUNT(a) > 0  as node_exists
    RETURN node_exists
    """ 
    results1=session.run(q1,x)
   
    exists=[{"Name":row["node_exists"]}for row in results1][0]["Name"] #해당 노드가 존재하는지를 체크 -> exists:boolean: true: 존재/false:존재 안함
    if exists == False: 
        raise HTTPException(status_code=404, detail="등록되지 않은 앨범입니다.")
    
       
    q2="""
    match(a:album{name:$name}) match (a) -[:has]->(s) -[:sings] -> (m) return m as musicians
    """
    results2=session.run(q2,x) # "(input album) -> (music) -> (musician)" 관계를 이용해서 해당 앨범을 쓴 뮤지션 목록 추출
    datas = [{"Name":row["musicians"]}for row in results2]
    if len(datas)>0: # 목록의 항목수가 0이 아니면
        response = []
        for i in range(len(datas)):
            response.append(datas[i]["Name"]["name"])
        response = list(set(response)) # 목록의 값들 중복 방지
        return {"response":"해당 앨범을 쓴 뮤지션 목록.: "+str(response)}
    else:
        return {"response":"해당 앨범을 쓴 뮤지션이 존재하지 않습니다. "}    



# MATCH (n) DETACH DELETE n

# MATCH (n) RETURN (n)