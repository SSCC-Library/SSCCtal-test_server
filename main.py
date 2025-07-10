from fastapi import FastAPI, APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Union

app = FastAPI()
router = APIRouter()

MOCK_TOKEN = "mock-jwt-token"   # 임시 토큰

# --- 관리자 인증 관련 ---
ADMIN_TOKEN = "mock-admin-token"

def verify_admin_token(Authorization: str = Header(None)):
    if Authorization != f"Bearer {ADMIN_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized (admin)")

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
    # 1. 관리자인 경우 (아이디 동일, 비밀번호만 다름)
    if data.student_id == 19830302 and data.password == "1234test":
        return {
            "success": True,
            "code": 200,
            "token": ADMIN_TOKEN,
            "name": "관리자",
            "student_id": data.student_id,
            "is_admin": True
        }
    # 2. 일반 사용자
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
# 임시 대여 기록 데이터
rental_db = [
    RentalRecord(
        name="클라우드 네이티브를 위한 쿠버네티스 실전 프로젝트",
        status="반납 완료",
        item_borrow_date="2025.06.01",
        expectation_return_date="2025.06.15",
        item_return_date="2025.06.16",
        overdue=1
    ),
    RentalRecord(
        name="쉽고 빠른 플러터 앱 개발",
        status="대여 중",
        item_borrow_date="2025.06.10",
        expectation_return_date="2025.07.01",
        item_return_date=None,
        overdue=4
    ),
    RentalRecord(
        name="라즈베리파이로 시작하는 핸드메이드 IoT",
        status="반납 완료",
        item_borrow_date="2025.05.20",
        expectation_return_date="2025.06.10",
        item_return_date="2025.06.09",
        overdue=0
    ),
    RentalRecord(
        name="파이썬 알고리즘 인터뷰",
        status="대여 중",
        item_borrow_date="2025.06.05",
        expectation_return_date="2025.06.25",
        item_return_date=None,
        overdue=10
    ),
    RentalRecord(
        name="면접을 위한 CS 전공지식 노트",
        status="반납 완료",
        item_borrow_date="2025.05.15",
        expectation_return_date="2025.06.01",
        item_return_date="2025.06.04",
        overdue=3
    ),
    RentalRecord(
        name="3D 프린터 101",
        status="대여 중",
        item_borrow_date="2025.06.12",
        expectation_return_date="2025.06.19",
        item_return_date=None,
        overdue=0
    ),
    RentalRecord(
        name="팀 개발을 위한 Git, GitHub 시작하기",
        status="반납 완료",
        item_borrow_date="2025.05.28",
        expectation_return_date="2025.06.10",
        item_return_date="2025.06.10",
        overdue=0
    ),
    RentalRecord(
        name="라이프해커",
        status="대여 중",
        item_borrow_date="2025.06.02",
        expectation_return_date="2025.06.17",
        item_return_date=None,
        overdue=2
    ),
    RentalRecord(
        name="HTML&CSS 웹 프로그래밍 입문",
        status="반납 완료",
        item_borrow_date="2025.05.30",
        expectation_return_date="2025.06.15",
        item_return_date="2025.06.14",
        overdue=0
    ),
    RentalRecord(
        name="컴퓨터 네트워킹 하향식 접근",
        status="반납 완료",
        item_borrow_date="2025.05.10",
        expectation_return_date="2025.06.01",
        item_return_date="2025.06.01",
        overdue=0
    ),
    RentalRecord(
        name="비전공자를 위한 이해할 수 있는 IT 지식",
        status="대여 중",
        item_borrow_date="2025.06.20",
        expectation_return_date="2025.07.10",
        item_return_date=None,
        overdue=0
    ),
    RentalRecord(
        name="후니의 쉽게 쓴 시스코 네트워킹",
        status="반납 완료",
        item_borrow_date="2025.05.11",
        expectation_return_date="2025.05.25",
        item_return_date="2025.05.28",
        overdue=3
    ),
    RentalRecord(
        name="클라우드 네이티브를 위한 데이터 센터 네트워크 구축",
        status="대여 중",
        item_borrow_date="2025.06.16",
        expectation_return_date="2025.07.06",
        item_return_date=None,
        overdue=0
    ),
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

class AdminItem(BaseModel):
    item_id: str
    name: str
    type: str
    copy_status: str
    identifier_code: str
    hashtag: str

admin_item_db = [
    AdminItem(
        item_id=str(idx + 1),
        name=item.name,
        type=item.type,
        copy_status=item.copy_status,
        identifier_code=item.identifier_code,
        hashtag=item.hashtag.split(" ")[0]  # 여러 해시태그 중 첫 번째만
    )
    for idx, item in enumerate(item_db)
]

@router.get("/admin/items")
async def admin_get_items(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    search_type: Optional[str] = None,
    search_text: Optional[str] = None,
    _: None = Depends(verify_admin_token)
):
    filtered = admin_item_db
    if search_type and search_text:
        if search_type == "name":
            filtered = [item for item in filtered if search_text.lower() in item.name.lower()]
        elif search_type == "hashtag":
            filtered = [item for item in filtered if search_text.lower() in item.hashtag.lower()]
        elif search_type == "item_id":
            filtered = [item for item in filtered if search_text == item.item_id]
    start = (page - 1) * size
    end = start + size
    items_page = filtered[start:end]
    if not items_page:
        return {"success": False, "code": 404}
    return {
        "success": True,
        "code": 200,
        "items": [item.model_dump() for item in items_page],
        "page": page,
        "size": size
    }

class AdminItemDetail(BaseModel):
    item_id: str
    identifier_code: str
    name: str
    type: str
    publisher: Optional[str] = None
    publish_date: Optional[str] = None
    hashtag: str
    image_url: str
    total_count: int
    available_count: int
    create_date: Optional[str] = None
    update_date: Optional[str] = None

# 임시 상세 데이터 생성
from datetime import datetime

admin_item_detail_db = [
    AdminItemDetail(
        item_id=str(idx + 1),
        identifier_code=item.identifier_code,
        name=item.name,
        type=item.type,
        publisher="예제출판사",                  # 임의값, 실제 데이터로 교체 가능
        publish_date="2022-05-01",              # 임의값, 실제 데이터로 교체 가능
        hashtag=item.hashtag.split(" ")[0],
        image_url=item.image_url,
        total_count=item.total_count,
        available_count=item.available_count,
        create_date="2024-07-10",
        update_date=datetime.now().strftime("%Y-%m-%d")
    )
    for idx, item in enumerate(item_db)
]

@router.get("/admin/items/{item_id}")
async def admin_get_item_detail(
    item_id: str,
    _: None = Depends(verify_admin_token)
):
    for item in admin_item_detail_db:
        if item.item_id == item_id:
            return {
                "success": True,
                "code": 200,
                **item.model_dump()
            }
    return {"success": False, "code": 404}

class AdminRentalRecord(BaseModel):
    rental_id: str
    name: str
    type: str
    user_name: str
    student_id: str
    item_borrow_date: str
    item_return_date: Optional[str]
    rental_status: str  # "대여중" or "반납 완료"

# 임시 Admin 대여 기록 데이터 (예시)
admin_rental_db = [
    AdminRentalRecord(
        rental_id=str(idx + 1),
        name=item.name,
        type="책",
        user_name="홍길동" if idx % 2 == 0 else "김영희",
        student_id="20231234" if idx % 2 == 0 else "20235678",
        item_borrow_date="2025.06.{:02d}".format(1 + idx),
        item_return_date=item.item_return_date if hasattr(item, 'item_return_date') else None,
        rental_status="반납 완료" if item.item_return_date else "대여중"
    )
    for idx, item in enumerate(rental_db)
]

@router.get("/admin/rentals")
async def admin_get_rentals(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    search_type: Optional[str] = None,
    search_text: Optional[str] = None,
    _: None = Depends(verify_admin_token)
):
    filtered = admin_rental_db
    # 검색 기능
    if search_type and search_text:
        if search_type == "student_id":
            filtered = [r for r in filtered if search_text in r.student_id]
        elif search_type == "name":
            filtered = [r for r in filtered if search_text in r.name]
        elif search_type == "user_name":
            filtered = [r for r in filtered if search_text in r.user_name]
    # 페이징
    start = (page - 1) * size
    end = start + size
    items_page = filtered[start:end]
    if not items_page:
        return {"success": False, "code": 404}
    return {
        "success": True,
        "code": 200,
        "items": [item.model_dump() for item in items_page],
        "page": page,
        "size": size
    }

@router.get("/admin/rentals/{rental_id}")
async def admin_get_rental_detail(
    rental_id: str,
    _: None = Depends(verify_admin_token)
):
    for rental in admin_rental_db:
        if rental.rental_id == rental_id:
            return {
                "success": True,
                "code": 200,
                **rental.model_dump()
            }
    return {"success": False, "code": 404}

from fastapi import Body

class AdminRentalRecordUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    user_name: Optional[str] = None
    student_id: Optional[str] = None
    item_borrow_date: Optional[str] = None
    item_return_date: Optional[str] = None
    rental_status: Optional[str] = None

@router.patch("/admin/rentals/{rental_id}")
async def admin_patch_rental(
    rental_id: str,
    update: AdminRentalRecordUpdate = Body(...),
    _: None = Depends(verify_admin_token)
):
    for rental in admin_rental_db:
        if rental.rental_id == rental_id:
            # 필드별로 None이 아니면 업데이트
            if update.name is not None:
                rental.name = update.name
            if update.type is not None:
                rental.type = update.type
            if update.user_name is not None:
                rental.user_name = update.user_name
            if update.student_id is not None:
                rental.student_id = update.student_id
            if update.item_borrow_date is not None:
                rental.item_borrow_date = update.item_borrow_date
            if update.item_return_date is not None:
                rental.item_return_date = update.item_return_date
            if update.rental_status is not None:
                rental.rental_status = update.rental_status
            return {"success": True, "code": 200}
    return {"success": False, "code": 503}

class AdminOverdueRecord(BaseModel):
    rental_id: str
    name: str
    type: str
    user_name: str
    student_id: str
    item_borrow_date: str
    overdue: int

# admin_rental_db 기준으로 overdue가 1 이상인 것만
admin_overdue_db = [
    AdminOverdueRecord(
        rental_id=r.rental_id,
        name=r.name,
        type=r.type,
        user_name=r.user_name,
        student_id=r.student_id,
        item_borrow_date=r.item_borrow_date,
        overdue=getattr(r, "overdue", 0)  # rental_db와 호환되도록
    )
    for r in admin_rental_db
    if getattr(r, "overdue", 0) > 0
]

@router.get("/admin/overdue")
async def admin_get_overdue(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    search_type: Optional[str] = None,
    search_text: Optional[str] = None,
    _: None = Depends(verify_admin_token)
):
    filtered = admin_overdue_db
    # 검색 조건 적용
    if search_type and search_text:
        if search_type == "student_id":
            filtered = [o for o in filtered if search_text in o.student_id]
        elif search_type == "name":
            filtered = [o for o in filtered if search_text in o.name]
        elif search_type == "user_name":
            filtered = [o for o in filtered if search_text in o.user_name]
    # 페이징
    start = (page - 1) * size
    end = start + size
    items_page = filtered[start:end]
    if not items_page:
        return {"success": False, "code": 404}
    return {
        "success": True,
        "code": 200,
        "items": [item.model_dump() for item in items_page],
        "page": page,
        "size": size
    }

@router.get("/admin/overdue/{rental_id}")
async def admin_get_overdue_detail(
    rental_id: str,
    _: None = Depends(verify_admin_token)
):
    for overdue in admin_overdue_db:
        if overdue.rental_id == rental_id:
            # rental_db에서 상세 데이터까지 합쳐주면 더 풍부
            detail = next((r for r in admin_rental_db if r.rental_id == rental_id), None)
            if detail:
                # 응답에 상세 정보까지 합쳐서 반환
                return {
                    "success": True,
                    "code": 200,
                    "rental_id": overdue.rental_id,
                    "name": overdue.name,
                    "type": overdue.type,
                    "user_name": overdue.user_name,
                    "student_id": overdue.student_id,
                    "item_borrow_date": overdue.item_borrow_date,
                    "item_return_date": getattr(detail, "item_return_date", None),
                    "expectation_return_date": getattr(detail, "expectation_return_date", None),
                    "overdue": overdue.overdue,
                    "rental_status": getattr(detail, "rental_status", None)
                }
            # 기본 정보만 반환
            return {
                "success": True,
                "code": 200,
                **overdue.model_dump()
            }
    return {"success": False, "code": 404}

class AdminUser(BaseModel):
    name: str
    major: str
    student_id: str
    email: str
    phone_number: str
    gender: str
    user_classification: str  # 학생, 조교, 교수 등
    major2: Optional[str] = ""
    minor: Optional[str] = ""

admin_user_db = [
    AdminUser(
        name="홍길동",
        major="컴퓨터학부",
        student_id="20231234",
        email="gildong@hong.com",
        phone_number="01012345678",
        gender="남",
        user_classification="학생",
        major2="",
        minor=""
    ),
    AdminUser(
        name="김영희",
        major="소프트웨어학부",
        student_id="20235678",
        email="younghee@kim.com",
        phone_number="01098765432",
        gender="여",
        user_classification="학생",
        major2="정보통신공학부",
        minor="경영학부"
    ),
    # ... 필요한 만큼 더 추가
]

@router.get("/admin/users")
async def admin_get_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    search_type: Optional[str] = None,
    search_text: Optional[str] = None,
    _: None = Depends(verify_admin_token)
):
    filtered = admin_user_db
    if search_type and search_text:
        if search_type == "student_id":
            filtered = [u for u in filtered if search_text in u.student_id]
        elif search_type == "name":
            filtered = [u for u in filtered if search_text in u.name]
        elif search_type == "major":
            filtered = [u for u in filtered if search_text in u.major]
    start = (page - 1) * size
    end = start + size
    items_page = filtered[start:end]
    if not items_page:
        return {"success": False, "code": 404}
    return {
        "success": True,
        "code": 200,
        "items": [item.model_dump() for item in items_page],
        "page": page,
        "size": size
    }

@router.get("/admin/users/{student_id}")
async def admin_get_user_detail(
    student_id: str,
    _: None = Depends(verify_admin_token)
):
    for user in admin_user_db:
        if user.student_id == student_id:
            return {
                "success": True,
                "code": 200,
                **user.model_dump()
            }
    return {
        "success": False,
        "code": 404
    }

from enum import Enum
from pydantic import EmailStr

class GenderEnum(str, Enum):
    MALE = "남"
    FEMALE = "여"
    OTHER = "기타"

class UserClassificationEnum(str, Enum):
    STUDENT = "학생"
    TA = "조교"
    PROFESSOR = "교수"
    ETC = "기타"

class UserStatusEnum(str, Enum):
    ENROLLED = "재학"
    GRADUATED = "졸업"
    LEAVE = "휴학"
    WITHDRAWN = "자퇴"

class AdminUserCreate(BaseModel):
    student_id: str
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    gender: Optional[GenderEnum] = GenderEnum.MALE
    major: Optional[str] = None
    major2: Optional[str] = None
    minor: Optional[str] = None
    user_classification: Optional[UserClassificationEnum] = UserClassificationEnum.STUDENT
    user_status: Optional[UserStatusEnum] = UserStatusEnum.ENROLLED

@router.post("/admin/users")
async def admin_create_user(
    user: AdminUserCreate,
    _: None = Depends(verify_admin_token)
):
    # 이미 존재하는 학번인지 검사 (중복 방지)
    for u in admin_user_db:
        if u.student_id == user.student_id:
            return {"success": False, "code": 503}
    # 추가 (메모리 DB에 append)
    admin_user_db.append(
        AdminUser(
            name=user.name,
            major=user.major or "",
            student_id=user.student_id,
            email=user.email,
            phone_number=user.phone_number or "",
            gender=user.gender.value if isinstance(user.gender, Enum) else user.gender,
            user_classification=user.user_classification.value if isinstance(user.user_classification, Enum) else user.user_classification,
            major2=user.major2 or "",
            minor=user.minor or ""
        )
    )
    return {"success": True, "code": 200}

class AdminUserUpdate(BaseModel):
    name: Optional[str] = None
    major: Optional[str] = None
    student_id: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    gender: Optional[GenderEnum] = None
    user_classification: Optional[UserClassificationEnum] = None
    major2: Optional[str] = None
    minor: Optional[str] = None
    user_status: Optional[UserStatusEnum] = None

@router.patch("/admin/users/{student_id}")
async def admin_patch_user(
    student_id: str,
    update: AdminUserUpdate,
    _: None = Depends(verify_admin_token)
):
    for user in admin_user_db:
        if user.student_id == student_id:
            if update.name is not None:
                user.name = update.name
            if update.major is not None:
                user.major = update.major
            if update.student_id is not None:
                user.student_id = update.student_id
            if update.email is not None:
                user.email = update.email
            if update.phone_number is not None:
                user.phone_number = update.phone_number
            if update.gender is not None:
                user.gender = update.gender.value if isinstance(update.gender, Enum) else update.gender
            if update.user_classification is not None:
                user.user_classification = update.user_classification.value if isinstance(update.user_classification, Enum) else update.user_classification
            if update.major2 is not None:
                user.major2 = update.major2
            if update.minor is not None:
                user.minor = update.minor
            if update.user_status is not None:
                user.user_status = update.user_status.value if isinstance(update.user_status, Enum) else update.user_status
            return {"success": True, "code": 200}
    return {"success": False, "code": 503}

class AdminUserDeleteRequest(BaseModel):
    student_id: str

@router.delete("/admin/users")
async def admin_delete_user(
    req: AdminUserDeleteRequest,
    _: None = Depends(verify_admin_token)
):
    for i, user in enumerate(admin_user_db):
        if user.student_id == req.student_id:
            del admin_user_db[i]
            return {"success": True, "code": 200}
    return {"success": False, "code": 503}


app.include_router(router)
