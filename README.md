# SSCC 라이브러리 Mock API

동아리 내부 테스트용 Mock API 서버입니다.  
**FastAPI 기반**으로, 로그인·물품 조회·내 대여기록 조회 기능이 임시 구현되어 있습니다.

---

## 💡 **시작 전 안내**

- 모든 보호 API는 임시 토큰(`mock-jwt-token`) 인증이 필요합니다.
- 토큰 발급은 `/api/v1/auth/login`으로 로그인하여 응답의 `token` 값을 사용합니다.
- 서버 기본 주소: `http://localhost:8000` (FastAPI 실행 시)

---

## 📚 **API 목록**

- [1. 로그인 (POST /api/v1/auth/login)](#1-로그인)
- [2. 물품 목록 조회 (GET /api/v1/items)](#2-물품-목록-조회)
- [3. 내 대여 기록 조회 (GET /api/v1/users/me/rentals)](#3-내-대여-기록-조회)

---

## 1. 로그인

### **POST** `/api/v1/auth/login`

| 필드        | 타입   | 필수 | 설명         |
| ----------- | ------ | ---- | ------------|
| student_id  | int    | ✅   | 학번         |
| password    | string | ✅   | 비밀번호     |

#### ✅ 요청 예시
```json
{
  "student_id": 19830302,
  "password": "test1234"
}
```

#### ⬇️ 응답 예시 (성공)
```json
{
  "success": true,
  "code": 200,
  "token": "mock-jwt-token",
  "name": "관리자",
  "student_id": 19830302
}
```
- token 값을 복사해 아래 API의 Authorization 헤더에 사용합니다.

#### ⬇️ 응답 예시 (실패)
```json
{
  "success": false,
  "code": 401,
  "message": "존재하지 않는 학번이거나 비밀번호가 일치하지 않습니다."
}
```
## 2. 물품 목록 조회
### GET `/api/v1/items`
인증
- 필수: `Authorization: Bearer mock-jwt-token`

쿼리 파라미터
| 파라미터 | 타입  | 필수 | 기본값 | 설명          |
| ---- | --- | -- | --- | ----------- |
| page | int | ❌  | 1   | 페이지 번호(1\~) |

- size(페이지당 아이템 수)는 항상 12로 고정

#### ✅ 요청 예시
```bash
GET /api/v1/items?page=1&search_text=파이썬
```
```makefile
Authorization: Bearer mock-jwt-token
```
#### ⬇️ 성공 응답 예시
```json
{
  "success": true,
  "code": 200,
  "items": [
    {
      "name": "혼자 공부하는 Python",
      "type": "책",
      "copy_status": "대출 중",
      "identifier_code": "1234567890124",
      "hashtag": "#python",
      "image_url": "https://yes24.com/",
      "total_count": 2,
      "available_count": 1
    }
    // ... 최대 12개
  ],
  "page": 1,
  "size": 12
}
```
#### ⬇️ 실패(빈페이지) 응답 예시
```json
{
  "success": false,
  "code": 404,
  "message": "해당 페이지에 물품이 없습니다."
}
```
## 3. 내 대여 기록 조회
### GET `/api/v1/users/me/rentals`
인증
- 필수: `Authorization: Bearer mock-jwt-token`

쿼리 파라미터
| 파라미터 | 타입  | 필수 | 기본값 | 설명          |
| ---- | --- | -- | --- | ----------- |
| page | int | ❌  | 1   | 페이지 번호(1\~) |


- size(페이지당 항목 수)는 항상 12로 고정

#### ✅ 요청 예시
```bash
GET /api/v1/users/me/rentals?page=1
```
```makefile
Authorization: Bearer mock-jwt-token
```
#### ⬇️ 성공 응답 예시
```json
{
  "success": true,
  "code": 200,
  "items": [
    {
      "name": "혼자 공부하는 C언어",
      "status": "반납 완료",
      "item_borrow_date": "2025.06.06",
      "expectation_return_date": "2025.07.02",
      "item_return_date": "2025.07.07",
      "overdue": 5
    }
    // ... 최대 12개
  ],
  "page": 2,
  "size": 12
}
```
#### ⬇️ 실패(빈페이지) 응답 예시
```json
{
  "success": false,
  "code": 404,
  "message": "대여 기록이 없습니다."
}
```
## 📝 테스트 시 주의사항
- Authorization 헤더는 반드시 "Bearer mock-jwt-token"로 입력
(띄어쓰기 포함)

- 실제 로그인/조회 기능은 모두 테스트/mock 데이터 기반입니다.

- 모든 페이징 size는 12로 고정입니다.

- 비밀번호, 학번 등은 임시값이므로 운영 시스템에서는 반드시 교체 필요

## 👨‍💻 실행 예시 (uvicorn)
```sh
uvicorn main:app --reload
```
## ❓ 문의 및 피드백
동아리 PM, 개발자에게 직접 문의 또는 Issues에 등록해주세요.