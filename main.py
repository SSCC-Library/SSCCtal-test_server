from fastapi import FastAPI, APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Union

app = FastAPI()
router = APIRouter()

MOCK_TOKEN = "mock-jwt-token"   # 임시 토큰

# --- 로그인 관련 ---
class LoginRequest(BaseModel):
    student_id: int
    password: str

async def saint_auth(student_id: int, password: str) -> str:
    if student_id == 19830302 and password == "test1234":
        return "success"
    return "fail"

@app.post("/api/v1/auth/login")
async def login(data: LoginRequest):
    result = await saint_auth(data.student_id, data.password)
    if result == "success":
        return {
            "success": True,
            "code": 200,
            "token": MOCK_TOKEN,
            "name": "관리자",
            "student_id": data.student_id
        }
    return {
        "success": False,
        "code": 401,
        "message": "존재하지 않는 학번이거나 비밀번호가 일치하지 않습니다."
    }

# --- 인증 함수 ---
def verify_token(Authorization: str = Header(None)):
    if Authorization != f"Bearer {MOCK_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

# --- 물품 목록 관련 ---
class Item(BaseModel):
    name: str
    type: str
    copy_status: str
    identifier_code: str
    hashtag: str
    image_url: str
    total_count: int
    available_count: int

item_db = [
    Item(
        name="혼자 공부하는 C언어",
        type="책",
        copy_status="대출 가능",
        identifier_code="1234567890123",
        hashtag="#c",
        image_url="https://yes24.com/",
        total_count=3,
        available_count=2,
    ),
    Item(
        name="혼자 공부하는 Python",
        type="책",
        copy_status="대출 중",
        identifier_code="1234567890124",
        hashtag="#python",
        image_url="https://yes24.com/",
        total_count=2,
        available_count=1,
    ),
    Item(
        name="Do it! C언어 입문",
        type="책",
        copy_status="대출 가능",
        identifier_code="1234567890125",
        hashtag="#c",
        image_url="https://yes24.com/",
        total_count=5,
        available_count=5,
    ),
    Item(
        name="모두의 파이썬",
        type="책",
        copy_status="대출 가능",
        identifier_code="1234567890126",
        hashtag="#python",
        image_url="https://yes24.com/",
        total_count=2,
        available_count=2,
    ),
    Item(
        name="모두의 C언어",
        type="책",
        copy_status="대출 중",
        identifier_code="1234567890127",
        hashtag="#c",
        image_url="https://yes24.com/",
        total_count=1,
        available_count=0,
    ),
    Item(
        name="아두이노 스타터 키트",
        type="기기",
        copy_status="대출 가능",
        identifier_code="2001002001001",
        hashtag="#arduino",
        image_url="https://yes24.com/",
        total_count=3,
        available_count=2,
    ),
    Item(
        name="라즈베리파이 4",
        type="기기",
        copy_status="대출 중",
        identifier_code="2001002001002",
        hashtag="#raspberrypi",
        image_url="https://yes24.com/",
        total_count=2,
        available_count=0,
    ),
    Item(
        name="STM32 개발보드",
        type="기기",
        copy_status="대출 가능",
        identifier_code="2001002001003",
        hashtag="#stm32",
        image_url="https://yes24.com/",
        total_count=1,
        available_count=1,
    ),
    Item(
        name="파이썬 코딩 도장",
        type="책",
        copy_status="대출 가능",
        identifier_code="1234567890128",
        hashtag="#python",
        image_url="https://yes24.com/",
        total_count=4,
        available_count=3,
    ),
    Item(
        name="자료구조와 C언어",
        type="책",
        copy_status="대출 가능",
        identifier_code="1234567890129",
        hashtag="#c",
        image_url="https://yes24.com/",
        total_count=2,
        available_count=2,
    ),
    Item(
        name="노트북 1번",
        type="노트북",
        copy_status="대출 가능",
        identifier_code="3003003003001",
        hashtag="#laptop",
        image_url="https://yes24.com/",
        total_count=1,
        available_count=1,
    ),
    Item(
        name="노트북 2번",
        type="노트북",
        copy_status="대출 중",
        identifier_code="3003003003002",
        hashtag="#laptop",
        image_url="https://yes24.com/",
        total_count=1,
        available_count=0,
    ),
    Item(
        name="컴퓨터 네트워크(책)",
        type="책",
        copy_status="대출 가능",
        identifier_code="1234567890130",
        hashtag="#network",
        image_url="https://yes24.com/",
        total_count=2,
        available_count=2,
    ),
    Item(
        name="운영체제(책)",
        type="책",
        copy_status="대출 중",
        identifier_code="1234567890131",
        hashtag="#os",
        image_url="https://yes24.com/",
        total_count=3,
        available_count=0,
    ),
    Item(
        name="모두의 딥러닝",
        type="책",
        copy_status="대출 가능",
        identifier_code="1234567890132",
        hashtag="#deeplearning",
        image_url="https://yes24.com/",
        total_count=3,
        available_count=2,
    ),
    Item(
        name="빅데이터를 지탱하는 기술",
        type="책",
        copy_status="대출 가능",
        identifier_code="1234567890133",
        hashtag="#bigdata",
        image_url="https://yes24.com/",
        total_count=1,
        available_count=1,
    ),
    Item(
        name="혼자 공부하는 Java",
        type="책",
        copy_status="대출 가능",
        identifier_code="1234567890134",
        hashtag="#java",
        image_url="https://yes24.com/",
        total_count=2,
        available_count=2,
    ),
]

@router.get("/api/v1/items")
async def get_items(
    page: int = Query(1, ge=1),
    search_text: Optional[str] = None,
    _: None = Depends(verify_token)  # 토큰 인증 의존성
):
    size = 12
    filtered = item_db
    if search_text:
        filtered = [item for item in item_db if search_text.lower() in item.name.lower()]
    start = (page - 1) * size
    end = start + size
    items_page = filtered[start:end]
    if not items_page:
        return {
            "success": False,
            "code": 404,
            "message": "해당 페이지에 물품이 없습니다."
        }
    return {
        "success": True,
        "code": 200,
        "items": [item.model_dump() for item in items_page],
        "page": page,
        "size": size
    }

# --- 내 대여 기록 관련 ---
class RentalRecord(BaseModel):
    name: str
    status: str  # "대여 중" or "반납 완료"
    item_borrow_date: str
    expectation_return_date: str
    item_return_date: Optional[str]
    overdue: int

# 임시 대여 기록 데이터
rental_db = [
    RentalRecord(
        name="혼자 공부하는 C언어",
        status="반납 완료",
        item_borrow_date="2025.06.06",
        expectation_return_date="2025.07.02",
        item_return_date="2025.07.07",
        overdue=5
    ),
    RentalRecord(
        name="우산",
        status="대여 중",
        item_borrow_date="2025.06.06",
        expectation_return_date="2025.07.02",
        item_return_date=None,
        overdue=6
    ),
    *[
        RentalRecord(
            name=f"노트북 {i}번",
            status="반납 완료" if i % 2 == 0 else "대여 중",
            item_borrow_date=f"2025.06.{6+i}",
            expectation_return_date=f"2025.07.{2+i}",
            item_return_date=f"2025.07.{7+i}" if i % 2 == 0 else None,
            overdue=i % 7
        )
        for i in range(1, 16)
    ]
]

@router.get("/api/v1/users/me/rentals")
async def get_my_rentals(
    page: int = Query(1, ge=1),
    _: None = Depends(verify_token)
):
    size = 12
    start = (page - 1) * size
    end = start + size
    items_page = rental_db[start:end]
    if not items_page:
        return {
            "success": False,
            "code": 404,
            "message": "대여 기록이 없습니다."
        }
    return {
        "success": True,
        "code": 200,
        "items": [item.model_dump() for item in items_page],
        "page": page,
        "size": size
    }

app.include_router(router)
