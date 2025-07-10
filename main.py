from fastapi import FastAPI, APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from item import item_db
from rental_db import rental_db
from fastapi import Body
from enum import Enum
from admin import (admin_item_db, admin_item_detail_db, admin_rental_db,
                   admin_overdue_db, admin_user_db, AdminItem, AdminItemDetail,
                   AdminRentalRecord, AdminRentalRecordUpdate, AdminOverdueRecord,
                   AdminUser, AdminUserCreate, AdminUserUpdate, AdminUserDeleteRequest)

app = FastAPI()
router = APIRouter()

# Mock data for demonstration purposes
MOCK_TOKEN = "mock-jwt-token"
ADMIN_TOKEN = "mock-admin-token"

# Mock data models
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
