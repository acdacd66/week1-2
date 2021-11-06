# 🔴 [위코드 x 원티드] 마피아 컴퍼니 기업 협업 과제

<br>

## 🟡 구현 기술 스택
- Language
  - Python
  - cypher
- Framework
  - FAST API
  - Open API (Swagger)
- DB
  - Neo4j
- 배포
  - AWS EC2 with Nginx,Gunicorn

<br>

## 🟡 Contributors

|이름   |담당 기능                 |GitHub 주소|
|-------|-------------------------|--------------------|
|이정우 | [PM] 모델링, 화면별 UPDATE, DELETE API, 서버 배포  | [acdacd66](https://github.com/acdacd66)    |
|성우진 | 모델링, `곡`/`앨범`/`뮤지션` CREATE, READ API | [jinatra](https://github.com/jinatra)   |

<br>

## 🟡 빌드 및 실행 방법
- 1. repo 폴더안의 requirements.text 파일을 install 한다.
  - pip install -r requirements.txt 
- 2. repo 폴더안에서 main app을 실행한다.
  - uvicorn main:app --port 8000 --reload

<br>

## 🟡 기본 설계
<img src="https://user-images.githubusercontent.com/39540606/140586110-ad70f806-6dc2-4c3f-a586-342891527730.jpg"  width="300" height="220">
-  이게 정석적인 그래프 db 스키마 설계인진 모르겠지만 자체적인 직감적인 설계를 하였다. <br>
-  우선 앨범은 여러 곡을 가질수 있으나 곡은 하나의 앨범에만 속해야 하기에 1대다의 관계라고 할 수있다. 그리고 곡과 뮤지션은 일반적인 다대다 관계이고 뮤지션과 앨범은 연결되있지 않다. 앨범과 곡의 relationship을 [:has]라는 라벨로 칭하였고 뮤지션과 곡의 관계는 [:sings]이라는 라벨로 칭하였다. 

<br>

## 🟡 구현 내용
- 화면별 READ API
  - `곡` 페이지 
    - 해당 `곡`이 속한 `앨범`을 가져오는 API
    - 해당 `곡`을 쓴 `뮤지션` 목록을 가져오는 API

  - `앨범` 페이지  
    - 해당 `앨범`을 쓴 `뮤지션` 목록 가져오는 API
    - 해당 `앨범`의 `곡` 목록을 가져오는 API
  - `뮤지션` 페이지 
    - 해당 `뮤지션`의 모든 `앨범` API
    - 해당 `뮤지션`의 `곡` 목록 가져오는 API

- Create, Update, Delete API
  - `곡` 생성 API
  - `앨범` 생성 API
  - `뮤지션` 생성 API
  - `뮤지션` - `곡` 연결/연결해제 API
  - `곡` - `앨범` 연결/연결해제 API

<br>

## 🟡 구현 기능/구현 방법
#### 🔵 `곡`, `앨범`, `뮤지션` Create API
- `곡` 생성의 경우, 곡 제목과 뮤지션 정보를 전달받습니다.
  - 추후 `앨범`과의 연결을 위해 사전에 default로 `곡` 노드의 album_name property를 null로 설정합니다.
- `앨범` 생성의 경우, 앨범 제목과 곡, 뮤지션 정보를 전달받습니다.
- `뮤지션` 생성의 경우, 뮤지선 이름으 전달받습니다.

#### 🔵 `곡`, `앨범`, `뮤지션` Read API
- `곡` 노드와 연결된 `뮤지션` 노드가 서로 찾을 경우 (music) -> (musician)" 관계를 이용해서 연결된 노드들 추출 
- `앨범` 노드와 연결된 `곡` 노드가 서로 찾을 경우 (album) -> (music)" 관계를 이용해서 연결된 노드들 추출 
- `앨범` 노드와 연결된 `뮤지션` 노드가 서로 찾을 경우 "( album) -> (music) -> (musician)" 관계를 이용해서 연결된 노드들 추출 
<br>

- `곡`  이름을 전달받게 되면 해당 곡이 속한 앨범이 출력되도록 하였습니다.
- `곡` 이름을 전달받게 되면 해당 곡을 쓴 뮤지션 목록이 출력되도록 하였습니다.
- `앨범` 이름을 전달받게 되면 해당 앨범을 쓴 뮤지션 목록이 출력되도록 하였습니다.
- `앨범` 이름을 전달받게 되면 해당 앨범의 곡 목록이 출력되도록 하였습니다.
- `뮤지션` 이름을 전달받게 되면 해당 뮤지션의 앨범 목록이 출력되도록 하였습니다.
- `뮤지션` 이름을 전달받게 되면 해당 뮤지션의 곡 목록이 출력되도록 하였습니다.

#### 🔵 `곡`, `앨범`, `뮤지션` 연결/연결해제 API

- `뮤지션` 이름과 `곡` 이름을 전달받게 되면 각 노드가 연결 또는 연결 해제 될 수 있도록 하였습니다.
- `곡` 이름과 `앨범` 이름을 전달받게 되면 각 노드가 연결 또는 연겨 해제 될 수 있도록 하였습니다.
  - 1.`곡`노드와 `앨범`노드의 1대다 연결을 위해 `곡` 노드의 album_name property가 null인지 체크하고 만약 null이면 album_name을 해당 `앨범`노드의 name으로 초기화 한다.
  - 2.만약 `곡`노드의 album_name property와 `앨범`노드의 name name이 일치하지 않으면 해당 곡은 이미 다른 앨범에 포함되있다는 의미이므로 관계가 형성되지 않는다.
<br>

## 🟡 프로젝트 연결 neo4j DB 주소

아래 링크를 통해 본 프로젝트와 연동된 neo4j DB에 접근할 수 있습니다.
ID와 비밀번호는 별돌 제공된 노션 페이지에서 확인 가능합니다.

[ner4j DB Link](http://54.180.159.203:7474/browser/)

<br>

## 🟡 API TEST 방법 

아래 OPEN API 링크를 통해 엔드포인트 및 API TEST를 진행할 수 있습니다.

[OPEN API Link](http://54.180.159.203/docs)

<br>

## 🟡 엔드포인트 설명

| **METHOD** | **ENDPOINT**   | **body**   | **수행 목적** |
|:------|:-------------|:-----------------------:|:------------|
| POST   | /create/music | name | 곡 생성    |
| POST   | /create/album  | name | 앨범 생성        |
| POST   | /create/musician | name     | 뮤지션 생성 |
| POST   | /connect/musician-song     | musician_name, music_name | 뮤지션-곡 연결   |
| POST   | /connect/album-song     | album_name, music_name | 앨범-곡 연결   |
| DELETE | /disconnect/musician-song | musician_name, music_name | 뮤지션-곡 연결 해제 |
| DELETE | /disconnect/album-song | `query` | 앨범-곡 연결 해제    |
| GET    | /album/music | `query` | 해당 앨범의 수록곡 목록 호출    |
| GET    | /album/musician | `query` | 해당 앨범의 뮤지션 목록 호출     |
| GET    | /music/album | `query` | 해당 곡의 앨범 목록 호출     |
| GET    | /music/musician | `query` | 해당 곡의 뮤지션 목록 호출     |
| GET    | /musician/album | `query` | 해당 뮤지션의 앨범 목록 호출    |
| GET    | /musician/music | `query` | 해당 뮤지션의 곡 목록 호출    |

<br>

## 🟡 프로젝트 회고

- 이정우: [블로그](https://mytech123.tistory.com/)
- 성우진: [블로그](https://velog.io/@jinatra)



  
  
  
