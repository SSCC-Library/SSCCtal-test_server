# SSCC 라이브러리 Mock API
동아리 FE/BE 개발, API 연동 테스트를 위한 FastAPI 기반 Mock API 서버입니다.
- 실제 DB 대신 파이썬 메모리 객체로 동작합니다.
- 관리자/일반 사용자 토큰이 분리되어 있습니다.

## 💡 시작 전 안내
- 모든 보호 API는 토큰 인증(`mock-jwt-token` 또는 `mock-admin-token`)이 필요합니다.
- 토큰은 `/api/v1/auth/login`에서 발급받아 Authorization 헤더에 사용합니다.
- 서버 기본 주소: `http://localhost:8000`
- API 정의는 실제 운영 DB와 다를 수 있으며, FE 개발 및 시연/테스트 용도로 사용해주세요.

## 📂 프로젝트 구조
```bash
├── main.py           # FastAPI 앱 실행, 라우터 포함
├── item.py           # 물품 관련 모델/더미 데이터/엔드포인트
├── rental_db.py      # 대여 기록 더미 데이터
├── admin.py          # 관리자용 엔드포인트/더미 데이터
```
## 🛠️ API 목록

- ### [1. 로그인 (POST /api/v1/auth/login)](#1-로그인)
- ### [2. 물품 목록 조회 (GET /api/v1/items)](#2-물품-목록-조회)
- ### [3. 내 대여 기록 조회 (GET /api/v1/users/me/rentals)](#3-내-대여-기록-조회)
- ### [4. 관리자용 엔드포인트 예시](#4-관리자용-api)


## 1. 로그인
### POST `/api/v1/auth/login`
| 필드          | 타입     | 필수 | 설명   |
| ----------- | ------ | -- | ---- |
| student\_id | int    | ✅  | 학번   |
| password    | string | ✅  | 비밀번호 |

#### ✅ 요청 예시
```json
{ "student_id": 19830302, "password": "test1234" }
```
- 관리자 로그인: `{ "student_id": 19830302, "password": "1234test" }`

#### ⬇️ 응답 예시 (일반 사용자)
```json
{
  "success": true,
  "code": 200,
  "token": "mock-jwt-token",
  "name": "관리자",
  "student_id": 19830302
}
```
#### ⬇️ 응답 예시 (관리자)
```json
{
  "success": true,
  "code": 200,
  "token": "mock-admin-token",
  "name": "관리자",
  "student_id": 19830302,
  "is_admin": true
}
```

## 2. 물품 목록 조회
### GET `/api/v1/items`
- 인증 필요: `Authorization: Bearer mock-jwt-token`
- 쿼리 파라미터:
  - `page` (int, 기본 1)
  - `search_text` (string, optional)
- size(페이지 당 개수): 12 고정

#### ✅ 요청 예시
```bash
GET /api/v1/items?page=1&search_text=파이썬
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
    // ...최대 12개
  ],
  "page": 1,
  "size": 12
}
```

## 3. 내 대여 기록 조회
### GET `/api/v1/users/me/rentals`
- 인증 필요: `Authorization: Bearer mock-jwt-token`
- 쿼리 파라미터:
  - `page` (int, 기본 1)
- size: 12 고정

#### ✅ 요청 예시
```vbnet
GET /api/v1/users/me/rentals?page=1
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
    // ...최대 12개
  ],
  "page": 1,
  "size": 12
}
```

## 4. 관리자용 API
### 주요 엔드포인트

> **모든 관리자 API는**
> `Authorization: Bearer mock-admin-token`
> 필요합니다.

#### [GET] `/admin/items`
- 물품 목록(관리자용, 페이징/검색)

#### [GET] `/admin/items/{item_id}`
- 물품 상세 정보

#### [GET] `/admin/rentals`
- 전체 대여 기록(검색/페이징)

#### [PATCH] `/admin/rentals/{rental_id}`
- 대여 기록 정보 수정 (실제 데이터는 메모리에서만 변경, DB X)

#### [GET] `/admin/overdue`
- 연체 기록

#### [GET] `/admin/users`
- 회원 목록

#### [POST] `/admin/users`
- 회원 추가

#### [PATCH] `/admin/users/{student_id}`
- 회원 정보 수정

#### [DELETE] `/admin/users`
- 회원 삭제

## 📝 테스트/주의사항
- Authorization 헤더에 반드시 "Bearer [토큰값]" 입력 (띄어쓰기 포함)
- mock-jwt-token: 일반 사용자용, mock-admin-token: 관리자 전용
- 모든 데이터는 임시/테스트용, 서버 재시작시 초기화됨
- 페이징 size는 고정(12 또는 10)
- 실제 운영/보안 적용 전에는 반드시 코드 리뷰 및 데이터 검증 필요

## 👨‍💻 실행 방법
```sh
uvicorn main:app --reload
```
- 서버 기본 포트: 8000
- 엔드포인트 문서는 `/docs`에서 자동 확인 가능

## ❓ 문의 및 피드백
- SSCC PM 또는 개발자에게 직접 문의
- 또는 GitHub Issue에 남겨주세요