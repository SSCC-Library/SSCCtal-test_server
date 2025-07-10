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
        name="후니의 쉽게 쓴 시스코 네트워킹",
        type="책",
        copy_status="대출 가능",
        identifier_code="9788931551167",
        hashtag="#network #cisco #book",
        image_url="	https://image.yes24.com/goods/4747319/XL",
        total_count=1,
        available_count=1,
    ),
    Item(
        name="클라우드 네이티브를 위한 데이터 센터 네트워크 구축",
        type="책",
        copy_status="일부 대여 가능",
        identifier_code="9791162244586",
        hashtag="#cloud #network #datacenter #book",
        image_url="https://image.yes24.com/goods/103223506/XL",
        total_count=2,
        available_count=1,
    ),
    Item(
        name="클라우드 네이티브를 위한 쿠버네티스 실전 프로젝트",
        type="책",
        copy_status="대출 가능",
        identifier_code="9791157687138",
        hashtag="#kubernetes #cloud #project #book",
        image_url="	https://image.yes24.com/goods/102234803/XL",
        total_count=5,
        available_count=5,
    ),
    Item(
        name="라즈베리파이로 시작하는 핸드메이드 IoT",
        type="책",
        copy_status="대출 가능",
        identifier_code="9791190014489",
        hashtag="#raspberrypi #iot #handmade #book",
        image_url="	https://image.yes24.com/goods/78869304/XL",
        total_count=2,
        available_count=2,
    ),
    Item(
        name="쉽고 빠른 플러터 앱 개발",
        type="책",
        copy_status="대출 중",
        identifier_code="9791165921514",
        hashtag="#flutter #appdevelopment #book",
        image_url="	https://image.yes24.com/goods/109020524/XL",
        total_count=1,
        available_count=0,
    ),
    Item(
        name="면접을 위한 CS 전공지식 노트",
        type="책",
        copy_status="대출 가능",
        identifier_code="9791165219529",
        hashtag="#cs #interview #book",
        image_url="https://image.yes24.com/goods/108887922/XL",
        total_count=3,
        available_count=2,
    ),
    Item(
        name="UX/UI 디자이너를 위한 실무 피그마",
        type="책",
        copy_status="대출 중",
        identifier_code="9791162244760",
        hashtag="#ux #ui #figma #book",
        image_url="https://image.yes24.com/goods/104734674/XL",
        total_count=2,
        available_count=0,
    ),
    Item(
        name="비전공자를 위한 이해할 수 있는 IT 지식",
        type="책",
        copy_status="대출 가능",
        identifier_code="2001002001003",
        hashtag="#it #nonmajor #knowledge",
        image_url="https://image.yes24.com/goods/91165789/XL",
        total_count=1,
        available_count=1,
    ),
    Item(
        name="파이썬 알고리즘 인터뷰",
        type="책",
        copy_status="대출 가능",
        identifier_code="9791189909178",
        hashtag="#python #algorithm #interview #book",
        image_url="https://image.yes24.com/goods/91084402/XL",
        total_count=4,
        available_count=3,
    ),
    Item(
        name="라이프해커",
        type="책",
        copy_status="대출 가능",
        identifier_code="9788992939096",
        hashtag="#lifehacker #productivity #book",
        image_url="https://image.yes24.com/momo/TopCate202/MidCate005/20141203(1).jpg",
        total_count=2,
        available_count=2,
    ),
    Item(
        name="3D 프린터 101",
        type="책",
        copy_status="대출 가능",
        identifier_code="9791162240793",
        hashtag="#3dprinter #book",
        image_url="https://image.yes24.com/goods/62110027/XL",
        total_count=1,
        available_count=1,
    ),
    Item(
        name="UX/UI의 10가지 심리학 법칙",
        type="책",
        copy_status="대출 중",
        identifier_code="9791189909208",
        hashtag="#ux #ui #psychology #book",
        image_url="https://image.yes24.com/goods/92426632/XL",
        total_count=1,
        available_count=0,
    ),
    Item(
        name="사용자를 사로잡는 UX/UI 실전 가이드",
        type="책",
        copy_status="대출 가능",
        identifier_code="9791186710753",
        hashtag="#ux #ui #guide #book",
        image_url="https://image.yes24.com/goods/105749858/XL",
        total_count=2,
        available_count=2,
    ),
    Item(
        name="팀 개발을 위한 Git, GitHub 시작하기",
        type="책",
        copy_status="대출 중",
        identifier_code="9791169210607",
        hashtag="#git #github #book",
        image_url="https://image.yes24.com/goods/118827280/XL",
        total_count=3,
        available_count=0,
    ),
    Item(
        name="Do it! 웹 프로그래밍을 위한 자바스크립트 기본 편",
        type="책",
        copy_status="대출 가능",
        identifier_code="9791163030645",
        hashtag="#javascript #webdevelopment #book",
        image_url="https://image.yes24.com/goods/71127080/XL",
        total_count=3,
        available_count=2,
    ),
    Item(
        name="컴퓨터 네트워킹 하향식 접근",
        type="책",
        copy_status="대출 가능",
        identifier_code="9789813350212",
        hashtag="#networking #computer #book",
        image_url="https://image.yes24.com/goods/112228953/XL",
        total_count=1,
        available_count=1,
    ),
    Item(
        name="HTML&CSS 웹 프로그래밍 입문",
        type="책",
        copy_status="대출 가능",
        identifier_code="9791193083000",
        hashtag="#html #css #webdevelopment #book",
        image_url="https://image.yes24.com/goods/118609988/XL",
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
