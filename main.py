import os

from fastapi  import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv   import load_dotenv
from neo4j    import GraphDatabase

load_dotenv()
uri  = os.getenv("uri")
user = os.getenv("user")
pwd  = os.getenv("pwd")


class nodeModel(BaseModel):
    name : str

class musicianSongRelationModel(BaseModel):
    musician_name : str
    music_name    : str

class albumSongRelationModel(BaseModel):
    album_name : str
    music_name : str

def connection():
    driver=GraphDatabase.driver(uri=uri,auth=(user,pwd))
    return driver

class musicResponse200Model(BaseModel):
    message: str = "해당 음악이 등록되었습니다."
class musicResponse404Model(BaseModel):
    message: str = "이미 등록된 음악입니다."

class albumResponse200Model(BaseModel):
    message: str = "해당 앨범이 등록되었습니다."
class abumResponse404Model(BaseModel):
    message: str = "이미 등록된 앨범입니다."

class musicianResponse200Model(BaseModel):
    message: str = "해당 음악가는 이미 등록되었습니다."
class musicianResponse404Model(BaseModel):
    message: str = "이미 등록된 음악가입니다."

class relationConnectedResponse200Model(BaseModel):
    message: str ="response:relation이 등록되었습니다."
class relationResponse404Model(BaseModel):
    message: str ="등록되지 않은 음악입니다."
class musicia_songResponse405Model(BaseModel):
    message: str ="등록되지 않은  음악가입니다."
class relationResponse406Model(BaseModel):
    message: str ="이미 등록된 relation입니다.."

class DisconnectedRelationResponse200Model(BaseModel):
    message: str ="response:relation이 연결 해제되었습니다."




class album_songResponse404Model(BaseModel):
    message: str = "등록되지 않은 앨범입니다."
class albumMusicResponse200Model(BaseModel):
    message: str = "response:해당 앨범의 곡 목록.: "
class albumMusicianResponse200Model(BaseModel):
    message: str = "response:해당 앨범을 쓴 뮤지션 목록.: "


class song_albumResponse404Model(BaseModel):
    message: str = "등록되지 않은 곡입니다."
class songAlbumResponse200Model(BaseModel):
    message: str = "response:해당 곡이 속한 앨범 목록.: "
class songMusicianResponse200Model(BaseModel):
    messsage: str = "response:해당 곡을 작곡한 뮤지션 목록.: "

class musician_albumResponse404Model(BaseModel):
    message: str = "등록되지 않은 뮤지션입니다."
class musicianAlbumResponse200Model(BaseModel):
    message: str = "response:해당 뮤지션의 앨범 목록.: "
class musicianMusicResponse200Model(BaseModel):
    message: str = "response:해당 뮤지션의 곡 목록.: "

class relationResponse403Model(BaseModel):
    message: str = "해당 곡은 이미 다른 앨범에 등록이 되있습니다."




app=FastAPI()
@app.post("/create/music", description="곡 name을 입력으로 받고 곡을 생성하는 api입니다.", 
responses={
        200: {
            "model": musicResponse200Model,
        },
        404: {
            "model": musicResponse404Model,
        },
    },)
def createMusicNode(node:nodeModel):
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

@app.post("/create/album", description="앨범 name을 입력으로 받고 앨범을 생성하는 api입니다.",
responses={
        200: {
            "model": albumResponse200Model,
        },
        404: {
            "model": abumResponse404Model,
        },
    },)
def createAlbumNode(node:nodeModel):
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

@app.post("/create/musician", description="뮤지션 name을 입력으로 받고 뮤지션을 생성하는 api입니다.",
responses={
        200: {
            "model": musicianResponse200Model,
        },
        404: {
            "model": musicianResponse404Model,
        },
    },)
def createMusicianNode(node:nodeModel):
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

@app.post("/connect/musician-song", description="뮤지션 name과 곡 name을 입력으로 받고 뮤지션 - 곡 연결하는 api입니다.",
responses={
        200: {
            "model": relationConnectedResponse200Model,
        },
        404: {
            "model": relationResponse404Model,
            "description": "error1"
        },
            405: {
            "model": musicia_songResponse405Model,
            "description": "error2"
        },
        406: {
            "model": relationResponse406Model,
            "description": "error3: 이미 연결이 된 상태일때"
        },
    },)
def createMusicianMusicRelationship(node:musicianSongRelationModel):
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
        raise HTTPException(status_code=405, detail="등록되지 않은  음악가입니다.")
    
    q3="""
    MATCH  (m:musician {name:$musician_name}),(s:music {name: $music_name}) 
    RETURN exists( (s)-[:sings]->(m) ) as relation_exists
    """
    results3=session.run(q3,x)
    
    exists=[{"Name":row["relation_exists"]}for row in results3][0]["Name"]
    if exists == True:
        raise HTTPException(status_code=406, detail="이미 등록된 relation입니다..")
    
    q4="""
    MATCH (m:musician{name:$musician_name}),(s:music{name:$music_name})
    MERGE (s)-[:sings]->(m)
    """
    
    session.run(q4,x)
    return {"response":"relation이 등록되었습니다."}

@app.delete("/disconnect/musician-song", description="뮤지션 name과 곡 name을 입력으로 받고 뮤지션 - 곡 연결을 해제하는 api입니다.",
responses={
        200: {
            "model": DisconnectedRelationResponse200Model,
        },
        404: {
            "model": relationResponse404Model,
            "description": "error1"
        },
        405: {
            "model": musicia_songResponse405Model,
            "description": "error2"
        },
        406: {
            "model": relationResponse406Model,
            "description": "error3: 이미 연결이 된 상태일때"
        },
    },)
def deleteMusicianMusicRelationship(node:musicianSongRelationModel):
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
        raise HTTPException(status_code=405, detail="등록되지 않은  음악가입니다.")
    
    q3="""
    MATCH  (m:musician {name:$musician_name}),(s:music {name: $music_name}) 
    RETURN exists( (s)-[:sings]->(m) ) as relation_exists
    """
    results3=session.run(q3,x)
    
    exists=[{"Name":row["relation_exists"]}for row in results3][0]["Name"]
    if exists == False:
        raise HTTPException(status_code=406, detail="등록이 안된 relation입니다.")
    
    q4="""
    MATCH (s)-[rel:sings]->(m) 
    WHERE s.name= $music_name  AND m.name= $musician_name 
    DELETE rel
    """
    
    session.run(q4,x)
    return {"response":"relation이 연결 해제되었습니다."}

@app.post("/connect/album-song", description="앨범 name과 곡 name을 입력으로 받고 곡 - 앨범 연결하는 api입니다.",
responses={
        200: {
            "model": relationConnectedResponse200Model,
        },
        404: {
            "model": album_songResponse404Model,
            "description": "error1"
        },
        405: {
            "model": relationResponse404Model,
            "description": "error2"
        },
        406: {
            "model": relationResponse406Model,
            "description": "error3: 이미 연결이 된 상태일때"
        },
         403: {
            "model": relationResponse403Model,
            "description": "error4: 해당 곡이 이미 다른 앨범에 등록이 되있을떄."
        },
    },)
def createAlbumMusicRelationship(node:albumSongRelationModel):
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
        raise HTTPException(status_code=405, detail="등록되지 않은 음악입니다.")
    
    q3="""
    MATCH  (a:album {name:$album_name}),(s:music {name: $music_name}) 
    RETURN exists( (a)-[:has]->(s) ) as relation_exists
    """
    results3=session.run(q3,x)
    
    exists=[{"Name":row["relation_exists"]}for row in results3][0]["Name"]
    if exists == True:
        raise HTTPException(status_code=406, detail="이미 등록된 relation입니다.")

    q4="""
    match(a:album{name:$album_name}) match(s:music{name:$music_name}) where s.album_name is null set s.album_name = a.name
    """
    q5="""
     match(a:album{name:$album_name}) match(s:music{name:$music_name})  return s.album_name = a.name as matched
    """
    q6="""
    match(a:album{name:$album_name}) match(s:music{name:$music_name}) merge (a) -[:has]->(s) 
    """
    session.run(q4,x)
    results4 = session.run(q5,x)
    matchs=[{"Name":row["matched"]}for row in results4][0]["Name"]
    if matchs == False:
        raise HTTPException(status_code=403, detail="해당 곡은 이미 다른 앨범에 등록이 되있습니다.")

    session.run(q6,x)

    return {"response":"relation이 등록되었습니다."}



@app.delete("/disconnect/album-song", description="앨범 name과 곡 name을 입력으로 받고 곡 - 앨범 연결을 해제하는 api입니다.",
responses={
        200: {
            "model": DisconnectedRelationResponse200Model,
        },
        404: {
            "model": album_songResponse404Model,
            "description": "error1"
        },
        405: {
            "model": relationResponse404Model,
            "description": "error2"
        },
        406: {
            "model": relationResponse406Model,
            "description": "error3: 이미 연결이 된 상태일때"
        },
    },)
def deleteAlbumMusicRelationship(node:albumSongRelationModel):
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



# 해당 앨범의 곡 목록을 가져오는 API 
@app.get("/album/music", description="입력으로 앨범 name을 받고 해당 앨범의 곡 목록을 가져오는 api입니다.",
responses={
        200: {
            "model": albumMusicResponse200Model,
            "description": "만약 곡이 존재 안하면 ->'response :해당 앨범에 곡이 존재하지 않습니다. ' "
        },
        404: {
            "model": album_songResponse404Model,
            "description": "error1"
        }
    },)
def readAlbumMusicNode(q:str = None):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    x={"name":q} #get 쿼리 입력 데이터 -> 앨범 name

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
        

# 해당 앨범을 쓴 뮤지션 목록 가져오는 API  
@app.get("/album/musician", description="입력으로 앨범 name을 받고 해당 앨범을 쓴 뮤지션 목록을 가져오는 api입니다.",
responses={
        200: {
            "model": albumMusicianResponse200Model,
            "description": "만약 뮤지션이 존재 안하면 ->'response :해당 앨범을 쓴 뮤지션이 존재하지 않습니다. ' "
        },
        404: {
            "model": album_songResponse404Model,
            "description": "error1"
        }
    },
)
def readAlbumMusicianNode(q:str = None):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    x={"name":q} #get 쿼리 입력 데이터 -> 앨범 name

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



# 해당 곡이 속한 앨범 목록을 가져오는 API
@app.get("/music/album", description="입력으로 곡 name을 받고 해당 곡이 속한 앨범 목록을 가져오는 api입니다.",
responses={
        200: {
            "model": songAlbumResponse200Model,
            "description": "만약 앨범이 존재 안하면 ->'response :해당 곡이 속한 앨범이 존재하지 않습니다. ' "
        },
        404: {
            "model": song_albumResponse404Model,
            "description": "error1"
        }
    },
)
def readMusicAlbumNode(q:str = None):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    x={"name":q} #get 쿼리 입력 데이터 -> 곡 name

    q1=""" 
    match(s:music{name:$name}) WITH COUNT(s) > 0  as node_exists
    RETURN node_exists
    """ 
    results1=session.run(q1,x)
    exists=[{"Name":row["node_exists"]}for row in results1][0]["Name"] #해당 노드가 존재하는지를 체크 -> exists:boolean: true: 존재/false:존재 안함
    if exists == False: 
        raise HTTPException(status_code=404, detail="등록되지 않은 곡입니다.")
    
    q2="""
    match(s:music{name:$name}) match (a) -[:has] -> (s) -[:sings] -> (m) return a as albums
    """
    results2=session.run(q2,x) # "(input music) -> (musician)" 관계를 이용해서 해당 곡이 속한 앨범 목록 추출
    datas = [{"Name":row["albums"]}for row in results2]
    if len(datas)>0: # 목록의 항목수가 0이 아니면
        response = []
        for i in range(len(datas)):
            response.append(datas[i]["Name"]["name"])
        response = list(set(response)) # 목록의 값들 중복 방지
        return {"response":"해당 곡이 속한 앨범 목록.: "+str(response)}
    else:
        return {"response":"해당 곡이 속한 앨범이 존재하지 않습니다. "}  

# 해당 곡을 쓴 뮤지션 목록을 가져오는 API
@app.get("/music/musician", description="입력으로 곡 name을 받고 해당 곡을 쓴 뮤지션 목록을 가져오는 api입니다.",
responses={
        200: {
            "model": songMusicianResponse200Model,
            "description": "만약 뮤지션이 존재 안하면 ->'response :해당 곡을 쓴 뮤지션이 존재하지 않습니다. ' "
        },
        404: {
            "model": song_albumResponse404Model,
            "description": "error1"
        }
    },
)
def readMusicMusicianNode(q:str = None):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    x={"name":q} #get 쿼리 입력 데이터 -> 곡 name

    q1=""" 
    match(s:music{name:$name}) WITH COUNT(s) > 0  as node_exists
    RETURN node_exists
    """ 
    results1=session.run(q1,x)
    exists=[{"Name":row["node_exists"]}for row in results1][0]["Name"] #해당 노드가 존재하는지를 체크 -> exists:boolean: true: 존재/false:존재 안함
    if exists == False: 
        raise HTTPException(status_code=404, detail="등록되지 않은 곡입니다.")
    
    q2="""
    match(s:music{name:$name}) match (s) -[:sings] -> (m) return m as musicians
    """
    results2=session.run(q2,x) # "(input music) -> (musician)" 관계를 이용해서 해당 곡을 쓴 뮤지션 목록 추출
    datas = [{"Name":row["musicians"]}for row in results2]
    if len(datas)>0: # 목록의 항목수가 0이 아니면
        response = []
        for i in range(len(datas)):
            response.append(datas[i]["Name"]["name"])
        response = list(set(response)) # 목록의 값들 중복 방지
        return {"response":"해당 곡을 쓴 뮤지션 목록.: "+str(response)}
    else:
        return {"response":"해당 곡을 쓴 뮤지션이 존재하지 않습니다. "}   



# 해당 뮤지션의 모든 앨범 API
@app.get("/musician/album", description="입력으로 뮤지션 name을 받고 해당 뮤지선의 앨범 목록을 가져오는 api입니다.",
responses={
        200: {
            "model": musicianAlbumResponse200Model,
            "description": "만약 앨범이 존재 안하면 ->'response :해당 뮤지션의 앨범이 존재하지 않습니다. ' "
        },
        404: {
            "model": musician_albumResponse404Model,
            "description": "error1"
        }
    },
)
def readMusicianAlbumNode(q:str = None):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    x={"name":q} #get 쿼리 입력 데이터 -> 뮤지션 name

    q1=""" 
    match(m:musician{name:$name}) WITH COUNT(m) > 0  as node_exists
    RETURN node_exists
    """ 
    results1=session.run(q1,x)
    exists=[{"Name":row["node_exists"]}for row in results1][0]["Name"] #해당 노드가 존재하는지를 체크 -> exists:boolean: true: 존재/false:존재 안함
    if exists == False: 
        raise HTTPException(status_code=404, detail="등록되지 않은 뮤지션입니다.")
    
    q2="""
    match(m:musician{name:$name}) match (a) -[:has] -> (s) -[:sings] -> (m) return a as albums
    """
    results2=session.run(q2,x) # "(album) -> (music) -> (input musician)" 관계를 이용해서 해당 뮤지션의 앨범 목록 추출
    datas = [{"Name":row["albums"]}for row in results2]
    if len(datas)>0: # 목록의 항목수가 0이 아니면
        response = []
        for i in range(len(datas)):
            response.append(datas[i]["Name"]["name"])
        response = list(set(response)) # 목록의 값들 중복 방지
        return {"response":"해당 뮤지션의 앨범 목록.: "+str(response)}
    else:
        return {"response":"해당 뮤지션의 앨범이 존재하지 않습니다. "}  

# 해당 뮤지션의 곡 목록 API
@app.get("/musician/music", description="입력으로 뮤지션 name을 받고 해당 뮤지선의 곡 목록을 가져오는 api입니다.",
responses={
        200: {
            "model": musicianMusicResponse200Model,
            "description": "만약 곡이 존재 안하면 ->'response :해당 뮤지션의 곡이 존재하지 않습니다. ' "
        },
        404: {
            "model": musician_albumResponse404Model,
            "description": "error1"
        }
    },
)
def readMusicianAlbumNode(q:str = None):
    driver_neo4j=connection()
    session=driver_neo4j.session()
    x={"name":q} #get 쿼리 입력 데이터 -> 뮤지션 name

    q1=""" 
    match(m:musician{name:$name}) WITH COUNT(m) > 0  as node_exists
    RETURN node_exists
    """ 
    results1=session.run(q1,x)
    exists=[{"Name":row["node_exists"]}for row in results1][0]["Name"] #해당 노드가 존재하는지를 체크 -> exists:boolean: true: 존재/false:존재 안함
    if exists == False: 
        raise HTTPException(status_code=404, detail="등록되지 않은 뮤지션입니다.")
    
    q2="""
    match(m:musician{name:$name}) match (a) -[:has] -> (s) -[:sings] -> (m) return s as musics
    """
    results2=session.run(q2,x) # "(music) -> (input musician)" 관계를 이용해서 해당 뮤지션의 곡 목록 추출
    datas = [{"Name":row["musics"]}for row in results2]
    if len(datas)>0: # 목록의 항목수가 0이 아니면
        response = []
        for i in range(len(datas)):
            response.append(datas[i]["Name"]["name"])
        response = list(set(response)) # 목록의 값들 중복 방지
        return {"response":"해당 뮤지션의 곡 목록.: "+str(response)}
    else:
        return {"response":"해당 뮤지션의 곡이 존재하지 않습니다. "} 