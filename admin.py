from pydantic import BaseModel
from typing import Optional
from item import item_db
from rental_db import rental_db
from datetime import datetime
from enum import Enum
from pydantic import EmailStr


class AdminItem(BaseModel):
    item_id: str
    name: str
    type: str
    copy_status: str
    identifier_code: str
    hashtag: str

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

class AdminRentalRecord(BaseModel):
    rental_id: str
    name: str
    type: str
    user_name: str
    student_id: str
    item_borrow_date: str
    item_return_date: Optional[str]
    rental_status: str  # "대여중" or "반납 완료"

class AdminRentalRecordUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    user_name: Optional[str] = None
    student_id: Optional[str] = None
    item_borrow_date: Optional[str] = None
    item_return_date: Optional[str] = None
    rental_status: Optional[str] = None

class AdminOverdueRecord(BaseModel):
    rental_id: str
    name: str
    type: str
    user_name: str
    student_id: str
    item_borrow_date: str
    overdue: int

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

class AdminUserDeleteRequest(BaseModel):
    student_id: str


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