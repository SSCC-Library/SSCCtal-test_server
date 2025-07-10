from pydantic import BaseModel
from typing import Optional

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