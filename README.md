# 🔴 [위코드 x 원티드] 마피아 컴퍼니 기업 협업 과제

## 🟡 구현 기술 스택
- Language
  - Python
- Framework
  - FAST API
  - Open API (Swagger)
- DB
  - Neo4j

## 🟡 Contributors

|이름   |담당 기능                 |GitHub 주소|
|-------|-------------------------|--------------------|
|이정우 | [PM] 모델링, 화면별 READ API, UPDATE, DELETE API  | [acdacd66](https://github.com/acdacd66)    |
|성우진 | 모델링, `곡`/`앨범`/`뮤지션` CREATE API, 섭 배포  | [jinatra](https://github.com/jinatra)   |


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

## 🟡 구현 방법
#### 🔵 `곡`, `앨범`, `뮤지션` Create API
- `곡` 생성의 경우, 곡 제목과 뮤지션 정보를 전달받습니다.
- `앨범` 생성의 경우, 앨범 제목과 곡, 뮤지션 정보를 전달받습니다.
- `뮤지션` 생성의 경우, 뮤지선 이름으 전달받습니다.

#### 🔵 `곡`, `앨범`, `뮤지션` Read API
- Pleas Fill in

#### 🔵 `곡`, `앨범`, `뮤지션` 연결/연결해제 API
- Please Fill in


## 🟡 ENDPOINT 
| **METHOD** | **ENDPOINT**   | **body**   | **수행 목적** |
|:------|:-------------|:-----------------------:|:------------|
| POST   | /create_music | title, musician | 곡 생성    |
| POST   | /create_album  | title, song, musician       | 앨범 생성        |
| POST    | /create_musician | name      | 뮤지션 생성 |
| GET   | /boards/list      |                   |  해당 곡이 속한 앨범 호출  |
| GET    | /boards/read/board_id>|                        | 해당 곡을 쓴 뮤지션 호출 |
| GET  | /boards/update/<board_id> | title, content | 해당 앨범을 쓴 뮤지션 호출     |
| GET | /boards/delete/<board_id> |               | 해당 앨범의 곡 목록 호출 |
| GET | /boards/delete/<board_id> |               | 해당 뮤지션의 모든 앨범 호출 |
| GET | /boards/delete/<board_id> |               | 해당 뮤지션의 곡 목로 호출 |
| PUT | /boards/delete/<board_id> |               | 뮤지션-곡 연결 |
| PUT | /boards/delete/<board_id> |               | 뮤지션-곡 연결 해제 |
| PUT | /boards/delete/<board_id> |               | 곡-앨범 연결 |
| PUT | /boards/delete/<board_id> |               | 곡-앨범 연결 해제 |

## 🟡 API 명세
**🟣 1. 회원가입**

| **이름**       | **data type**  | **body input**                          | **처리**|
|:----------|--------|----------------------------|------------------------|
| email    | string | "email" : "test2@test2.com"            | "@" 앞과 "@", "." 사이에 특정 문자가 포함되어햐 하며 "." 뒤 2글자 이상 |
| password    | string | "password" : "TESTtest1234!!" | 영문 소문자, 영문 대문자, 특수문자가 모두 포함된 10자 이상 |
| nickname | string | "nickname" : "testman2"   | 영문/한글 1글자 이상 |
 
<br>

**SUCCESS EXAMPLE**
```
{
"MESSAGE": "user created"
}
```
**ERROR EXAMPLE**
```
# body의 일부 미입력 시
{
  'MESSAGE':'KEY_ERROR'
}
```
```
# body 자체가 없을 시
{
  'MESSAGE':'VALUE_ERROR'
}
``` 
```
# email 양식이 잘못되었을 시
{
  'MESSAGE': 'wrong e-mail form'
}
``` 
```
# 비밀번호 양식이 잘못되었을 시
{
  'MESSAGE': 'wrong password form'
}
``` 
```
# 입력 이메일이 이미 존재할 시
{
  'MESSAGE': 'existing e-mail'
}
``` 
```
# 입력 닉네임이 이미 존재할 시
{
  'MESSAGE': 'existing nickname'
}
``` 

---

**🟣 2. 로그인**

| **이름**       | **data type**  | **body input**                          | **처리**|
|:----------|--------|----------------------------|------------------------|
| email    | string | "email" : "test1@test1.com" |  "@" 앞과 "@", "." 사이에 특정 문자가 포함되어햐 하며 "." 뒤 2글자 이상|
| password | string | "password" : "TESTtest1234!!"   | 영문 소문자, 영문 대문자, 특수문자가 모두 포함된 10자 이상 |

**SUCCESS EXAMPLE**
```
# 로그인 성공(200)
{
    "MESSAGE": "sign in success",
    "TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.1iP-Si6crrqq0Pofw3LcpHA4iVfYym5cs0TZzIUO3hY",
    "USER_NICKNAME": "testman1"
}
```

**ERROR EXAMPLE**
```
# body 일부 미입력 시(400)
{
  "MESSAGE": "KEY_ERROR"
}
```
```
# body 없을 시(400)
{
  "MESSAGE": "VALUE_ERROR"
}
```
```
# 가입된 이메일 존재하지 않을 시(409)
{
  "MESSAGE": "non-existing e-mail"
}
```
```
# 비밀번호가 일치하지 않을 시(401)
{
  "message": "wrong password"
}
```
---
**🟣 3. 게시글 작성**
| **이름**       | **data type**  | **body input**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| title    | string | "title" : "test title 1" | 글자를 하나 이상 포함해야 한다(공백 불가) |
| content | string | "content" : "test content 1"   | 글자를 하나 이상 포함해야 한다(공백 불가)|

**SUCCESS EXAMPLE**
```
# 생성 성공 시(201)
{
    "MESSAGE": {
        "title": "test title 1",
        "content": "test content 1!",
        "user_id": 1,
        "user_nickname": "testman1"
    }
}
```
**ERROR EXAMPLE**
```
# body 일부 미입력 시(400)
{
  'MESSAGE':'KEY_ERROR'
}
```
```
# title 혹은 content에 공백에 존재할 시(404)
{
  "MESSAGE": "please fill in both title and content"
}
```

---
**🟣 4. 게시판 리스트 조회**
| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| page    | string |  posts/main?page=1 | page 위치와 pageint형으로 입력받는다. 미입력시 각각 자동으로 0, 3 할당 |
  
 
**SUCCESS EXAMPLE**
```
{
    "MESSAGE": {
        "count": 3,
        "data": [
            {
                "title": "test title 1",
                "content": "test content 1!",
                "user_id": 1,
                "user_nickname": "testman1",
                "created_at": "2021-10-23 06:23:45"
            },
            {
                "title": "test title 2",
                "content": "test content 2",
                "user_id": 1,
                "user_nickname": "testman1",
                "created_at": "2021-10-23 06:26:21"
            },
            {
                "title": "test title 3",
                "content": "test content 3",
                "user_id": 1,
                "user_nickname": "testman1",
                "created_at": "2021-10-23 06:26:25"
            }
        ]
    }
}
```
**ERROR EXAMPLE**
```
# query parameter가 음수가 전달되었을 시(404)
{
    "MESSAGE": "please request positive number"
}
```
---

**🟣 5. 게시글 상세 조회**
| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| board_id    | string |  boards/read/1 | path parameter로 board_id을 전달받아서 게시글이 존재하는 지 파악한 후 있으면 반환 |
  
**SUCCESS EXAMPLE**
```
{
    "MESSAGE": {
        "title": "test title 1",
        "content": "test content 1!",
        "user_id": 1,
        "user_nickname": "testman1",
        "created_at": "2021-10-23 06:23:45"
    }
}
```
**ERROR EXAMPLE**
```
# 게시글이 존재하지 않을 시(404)
{
  "MESSAGE": "non-existing board"
}
```
---

**🟣 6. 게시글 수정**
| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| board_id   | string |  boards/update/1 | path parameter로 board_id을 전달받아서 게시글이 존재하는 지 파악한 후 있으면 수정  |
| new_title | string | "new_title": "new test title 1"| 타이틀을 수정할 경우 공백을 제외한 글자가 존재하여야 한다 |
| new_content | string |"new_ content": "new test content 1"| 본문을 수정할 경우 공백을 제외한 글자가 존재하여야 한다|

- POST METHOD 사용

**SUCCESS EXAMPLE**
```
# 성공적으로 수정 시(201)
{
    "MESSAGE": "board edited",
    "UPDATE_TIME": "2021-10-23 06:46:39"
}
```

**ERROR EXAMPLE**

```
# 해당 게시글이 존재하지 않을 시(404)
{
  "MESSAGE": "non-existing board"
}
```
```
# 권한이 없는 사용자가 수정하려 할 시(404)
{
  "MESSAGE": "wrong user"
}
```
```
# title 또는 content에 공백이 존재할 시(400)
{
  "MESSAGE": "please fill in both title and content"
}
```

---
 
**🟣7. 게시글 삭제**
| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| board_id    | string |  boards/delete/1 | path parameter로 board_id을 전달받아서 게시글이 존재하는 지 파악한 후 있으면 삭제 |

- delete METHOD 사용

**SUCCESS EXAMPLE**
```
# 성공 시(200)
{
  "MESSAGE": "board deleted"
}
```
**ERROR EXAMPLE**
```
# 해당 게시글이 없을 시(404)
{
  "MESSAGE": "board-not-exists"
}
```
```
# 권한없는 사용자가 삭제하려 할 시(404)
{
  "MESSAGE": "wrong user"
}
```
  
  
  
