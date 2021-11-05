# 🔴 [위코드 x 원티드] 마피아 컴퍼니 기업 협업 과제

<br>

## 🟡 구현 기술 스택
- Language
  - Python
- Framework
  - FAST API
  - Open API (Swagger)
- DB
  - Neo4j

<br>

## 🟡 Contributors

|이름   |담당 기능                 |GitHub 주소|
|-------|-------------------------|--------------------|
|이정우 | [PM] 모델링, 화면별 UPDATE, DELETE API, 서버 배포  | [acdacd66](https://github.com/acdacd66)    |
|성우진 | 모델링, `곡`/`앨범`/`뮤지션` CREATE, READ API | [jinatra](https://github.com/jinatra)   |

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

## 🟡 구현 기능
#### 🔵 `곡`, `앨범`, `뮤지션` Create API
- `곡` 생성의 경우, 곡 제목과 뮤지션 정보를 전달받습니다.
- `앨범` 생성의 경우, 앨범 제목과 곡, 뮤지션 정보를 전달받습니다.
- `뮤지션` 생성의 경우, 뮤지선 이름으 전달받습니다.

#### 🔵 `곡`, `앨범`, `뮤지션` Read API
- `곡` 이름을 전달받게 되면 해당 곡이 속한 앨범이 출력되도록 하였습니다.
- `곡` 이름을 전달받게 되면 해당 곡을 쓴 뮤지션 목록이 출력되도록 하였습니다.
- `앨범` 이름을 전달받게 되면 해당 앨범을 쓴 뮤지션 목록이 출력되도록 하였습니다.
- `앨범` 이름을 전달받게 되면 해당 앨범의 곡 목록이 출력되도록 하였습니다.
- `뮤지션` 이름을 전달받게 되면 해당 뮤지션의 앨범 목록이 출력되도록 하였습니다.
- `뮤지션` 이름을 전달받게 되면 해당 뮤지션의 곡 목록이 출력되도록 하였습니다.

#### 🔵 `곡`, `앨범`, `뮤지션` 연결/연결해제 API
- `뮤지션` 이름과 `곡` 이름을 전달받게 되면 각 노드가 연결 또는 연결 해제 될 수 있도록 하였습니다.
- `곡` 이름과 `앨범` 이름을 전달받게 되면 각 노드가 연결 또는 연겨 해제 될 수 있도록 하였습니다.

<br>

## 🟡 API TEST 방법

아래 OPEN API 링크를 통해 엔드포인트 및 API TEST를 진행할 수 있습니다.

[OPEN API Link](http://15.165.205.37/docs#/)

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
| DELETE | /disconnect/album-song | `query` | 해당 앨범의 뮤지션 목록 호출    |
| GET    | /album/music | `query` | 해당 앨범의 수록곡 이름 호출    |
| GET    | /album/musician | `query` | 해당 앨범의 뮤지션 이름 호출     |
| GET    | /music/album | `query` | 해당 곡의 앨범 이름 호출     |
| GET    | /music/musician | `query` | 해당 곡의 뮤지션 이름 호출     |
| GET    | /musician/album | `query` | 해당 뮤지션의 앨범 이름 호출    |
| GET    | /musician/music | `query` | 해당 뮤지션의 곡 이름 호출    |


  
  
  
