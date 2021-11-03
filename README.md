# [Assignment 1] 에이모

## 사용한 기술 스택
- python flask, mongoengine, mongodb

## 환경 구축

```bash
#윈도우
python -m venv venv

source venv/Scripts/activate

pip install -r requirements.txt
```

```bash
#맥
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

```
flask run
```

유닛테스트 실행
```shell
python -m unittest
```

## 구현 내용 
- 게시글 카테고리  
- 게시글 검색  
- 대댓글(1 depth), Pagination  
- 게시글 읽힘 수  
- Unit Test  

## 수행하지 못한 것  

### 배포  
- AWS를 이용해 배포를 시도하였고, host를 외부에서도 사용 가능하게 0.0.0.0으로 지정했으나, 내부 wi-fi ip주소로 자꾸 서버가 Open이 되는 상황이 발생하였습니다.  
- 5시간 동안 배포 방법도 바꾸고 스택오버플로우도 뒤져봤지만 마땅한 해결책이 나오지 않아 배포에 실패했습니다.  

### 문제의 ip  

![image](https://user-images.githubusercontent.com/32921115/139961256-68888b54-6aaa-4c79-b239-3c7cf4141f06.png)
- 0.0.0.0, 5000으로 지정한 코드.

![image](https://user-images.githubusercontent.com/32921115/139961333-8e23578b-d46e-400e-873e-c248eedc047a.png)
- 위와 같이 지정해도 local ip주소로 서버가 Open된 사진  

## 팀원과 맡은 역할    
- 강대훈 : 게시글 읽힘 수, 게시글 검색 
- 송빈호 : 댓글 모델 작성, 대댓글 pagination  
- 정성헌 : 회원가입, 로그인, 게시판 CRUD, 카테고리, 유닛테스트  
 

## 구현 방법
#### 회원가입
- 사용자로부터 이름, 비밀번호를 받습니다.
- 비밀번호는 bcrypt를 통해 hashing하여 저장합니다.

#### 로그인
- 사용자는 이름, 비밀번호를 통해 로그인합니다.
- 사용자의 원활한 이용을 위해 jwt 토큰을 발행하여 제공합니다.

#### 게시판
- 게시글을 작성하기 위해서는 로그인을 해야하고 jwt를 통해 확인합니다. 마찬가지로 게시글의 수정, 삭제도 동일하게 적용됩니다.  
- 단순 게시판이나 특정 게시물을 열람하는 것은 로그인을 필요로 하지 않습니다.  

#### 카테고리  
- 게시글을 표현하는 모델인 Post에 tags라는 속성 하나를 지정했습니다.   
- 리스트 형식으로 되어 있으며 최대 30개의 카테고리를 저장할 수 있습니다.

#### 게시글 검색
- 클라이언트가 파라미터로 검색 키워드를 서버에 보내면 서버는 제목과 키워드가 일치하는 데이터를 찾고 반환합니다.
- SQL의 like절을 구현하기 위해 키워드에 정규식을 이용했습니다.

#### 대댓글  
- 댓글을 표현하는 모델인 Comment에 List 형식인 reply 속성을 지정했습니다.

#### 게시글 읽힘 수
- post_id가 쿠키에 없으면 post_id를 쿠키에 추가하고 조회수를 증가시킵니다.  


## ENDPOINT 
| **METHOD** | **ENDPOINT** | **parameter**| **body**   | **수행 목적** |
|:------|:-------------|:-------------|:-----------------------:|:------------|
| POST   | /auth/signup |         | name, password | 회원가입    |
| POST   | /auth/login  |         | name, password       | 로그인        |
| POST    | /create |         | title, content      | 게시글 작성 |
| GET   | /posts        |   page   |                   | 게시글 리스트   |
| GET    | /posts/<post_id>|   post_id      |             | 게시글 보기 |
| PATCH, PUT  | /posts<post_id> |         | title, content | 게시글 수정     |
| DELETE | /posts/<post_id> |         |               | 게시글 삭제 |
| GET | /lists |  keyword  |         | 게시글 검색 |
| POST | /posts/<post_id>/comment_create |    | oid | 댓글 생성 |  
| DELETE | /posts/<post_id> |    |         | 댓글 삭제 |


## API 명세

**0. Postman Test**  
- https://documenter.getpostman.com/view/17196833/UVBznUh4 클릭 후 Postman에서 실행  

**1. 회원가입**

| **이름**       | **data type**  | **body input** | 
|:----------|--------|----------------------------|
| name     | string | "name" : "Daehoon"            | 
| password | string | "password" : "rjdeogns123!"   | 

<br>

**SUCCESS EXAMPLE**
```
{
　　'msg':'success'
　　'status_code': 201
}
```
---

**2. 로그인**

| **이름**       | **data type**  | **body input** | 
|:----------|--------|----------------------------|
| name     | string | "name" : "Daehoon"            | 
| password | string | "password" : "rjdeogns123!"   | 

**SUCCESS EXAMPLE**
```
{
　　"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNDU0MzY4MSwianRpIjoiMTE3NzcyMmUtNmQ0MS00M2Y2LTg5YTktZGI0YTBlYTZlZmEwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjM0NTQzNjgxLCJleHAiOjE2MzQ1NDQ1ODF9.-22JE3F9LySXfKdKByS-8-VB6N3NDdU2p_ZtCqC1m8Y",
　　"status_code": 200 
}
```
---

**3. 게시글 작성**  

| **이름**       | **data type**  | **body input**   | 
|:----------|:--------:|:----------------------------|
| title    | string | "title" : "this is me" | 
| content | string | "content" : "this is post"   |

**SUCCESS EXAMPLE**
```
{
　　'msg':'success'
　　'status_code': 201
}
```
---

**4. 게시글 리스트 조회**

| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| page    | string |  posts?page=1 | page 위치를 int형으로 받고 데이터를 요청을 처리합니다. |


**SUCCESS EXAMPLE**
```
{
　　["_id" : {
            "$oid": "6180e926890fb1b18adbc3d7"
            },
　　"title": "title"
　　"content": "게시글",
　　"create_date": "2021-10-18T14:26:54.177247",
　　"user": "Daehoon",
　　"modify_date": null
   ]
    .
    .
    .
}

```
---

**5. 게시글 상세 조회**  

| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| post_id    | string |  posts/6180e926890fb1b18adbc3d7 | parameter로 post_id을 전달받아서 게시글이 존재하는 지 파악한 후 있으면 반환합니다 |
  
**SUCCESS EXAMPLE**
```
{
　　"_id" : {
            "$oid": "6180e926890fb1b18adbc3d7"
            },
　　"title": "title"
　　"content": "게시글",
　　"create_date": "2021-10-18T14:26:54.177247",
　　"user": "Daehoon",
　　"modify_date": null
}
```
---

**6. 게시글 수정**

| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| post_id   | string | posts/6180e926890fb1b18adbc3d7  |  parameter로 post_id을 전달받아서 게시글이 존재하는 지 파악한 후 있으면 반환합니다 |
| title | string | "title": "rewrite posts"| 타이틀을 수정할 경우 공백을 제외한 글자가 존재하여야 합니다 |
| content | string |"content": "kkk very hungry.."| 본문을 수정할 경우 공백을 제외한 글자가 존재하여야 합니다|

- PATCH,PUT 둘다 사용
- title, content 둘 중 하나만 body에 실어보내도 된다. (title, content 중 하나 선택하여 수정하거나 모두 수정 가능)

**SUCCESS EXAMPLE**
```
{
　　"msg": "success",
　　"status_code": 200
}
```
**ERROR EXAMPLE**
```
# 해당 게시글을 작성한 사용자가 아닐 때
{
　　"msg" : "권한이 없습니다. 해당 글을 쓰신 유저가 맞는지 확인해주세요."
　　"status_code" : 401
}
```

---

**7. 게시글 삭제**  

| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| post_id   | string | posts/6180e926890fb1b18adbc3d7  |  parameter로 post_id을 전달받아서 게시글이 존재하는 지 파악한 후 있으면 반환합니다. |


**SUCCESS EXAMPLE**
```
{
   
}, 204
```
**ERROR EXAMPLE**
```
# 해당 게시글을 작성한 사용자가 아닐 때
{
　　"msg" : "권한이 없습니다. 해당 글을 쓰신 유저가 맞는지 확인해주세요."
　　"status_code" : 401
}
```
---

**8. 게시글 검색**  

| **이름**       | **data type**  | **endpoint**   | **처리**|
|:----------|:--------:|:----------------------------|:------------------------|
| keyword   | string | /lists?keyword  | 제목과 키워드가 일치하는 데이터를 찾고 반환합니다.|


**SUCCESS EXAMPLE**
```
[
    {
        "_id": {
            "$oid": "6180e926890fb1b18adbc3d7"
        },
        "title": "test123",
        "content": "밥주세용",
        "create_date": {
            "$date": 1635870646595
        },
        "user": "name",
        "hits": 0
    },
    
    {
        "_id": {
            "$oid": "6180e926890fb1b18adbc3d7"
        },
        "title": "test1234556",
        "content": "test123354",
        "create_date": {
            "$date": 1635870646597
        },
        "user": "name",
        "hits": 0
    },
    .
    .
    .
]
```
---

**9. 댓글 생성**  

**댓글**
| **이름**       | **data type**  | **body input**   | 
|:----------|:--------:|:----------------------------|
| content | string | "content" : "this is content" | 

**대댓글**
| **이름**       | **data type**  | **body input**   | 
|:----------|:--------:|:----------------------------|
| content | string | "content" : "this is nested content" |
| oid | string | "oid" : "Parent comment ID" |

**SUCCESS EXAMPLE**
 
```
 - SUCCESS MESSAGE
[
 {
     "id": "<built-in function id>",
     "msg": "create_comment_success",
     "status_code": 201
 }
]
 
 - POST DETAIL
{
    "_id": {
        "$oid": "61816fc3e74e758d257a15b7"
    },
    "title": "test1",
    "content": "test1",
    "create_date": {
        "$date": 1635905107278
    },
    "hits": 1,
    "user": "618143e4fe6f1704c4023b57",
    "tags": [
        "test"
    ],
    "reply": {
        "61816fe2e74e758d257a15b8": {
            "content": "test1",
            "create_date": {
                "$date": 1635905138303
            },
            "user_id": "618143e4fe6f1704c4023b57",
            "post_id": "61816fc3e74e758d257a15b7",
            "oid": {
                "$oid": "61816fe2e74e758d257a15b8"
            },
            "reply": [
                {
                    "content": "test1",
                    "create_date": {
                        "$date": 1635905385783
                    },
                    "user_id": "618143e4fe6f1704c4023b57",
                    "post_id": "61816fc3e74e758d257a15b7"
                },
                {
                    "content": "test1",
                    "create_date": {
                        "$date": 1635905423709
                    },
                    "user_id": "618143e4fe6f1704c4023b57",
                    "post_id": "61816fc3e74e758d257a15b7"
                }
            ]
        },
    }
}
 
```
 

**ERROR EXAMPLE**
```
# 해당 게시글을 작성한 사용자가 아닐 때
{
　　"msg" : "권한이 없습니다. 해당 글을 쓰신 유저가 맞는지 확인해주세요."
　　"status_code" : 401
}
```
