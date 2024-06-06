from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from danswer.auth.users import current_admin_user
from danswer.db.engine import get_session
from danswer.db.models import User
from danswer.db.standard_answer import fetch_standard_answer
from danswer.db.standard_answer import fetch_standard_answer_categories
from danswer.db.standard_answer import fetch_standard_answer_category
from danswer.db.standard_answer import fetch_standard_answers
from danswer.db.standard_answer import insert_standard_answer
from danswer.db.standard_answer import insert_standard_answer_category
from danswer.db.standard_answer import remove_standard_answer
from danswer.db.standard_answer import update_standard_answer
from danswer.db.standard_answer import update_standard_answer_category
from danswer.server.manage.models import StandardAnswer
from danswer.server.manage.models import StandardAnswerCategory
from danswer.server.manage.models import StandardAnswerCategoryCreationRequest
from danswer.server.manage.models import StandardAnswerCreationRequest

router = APIRouter("/manage/admin")


@router.post("/standard-answer")
def create_standard_answer(
    standard_answer_creation_request: StandardAnswerCreationRequest,
    db_session: Session = Depends(get_session),
    _: User | None = Depends(current_admin_user),
) -> StandardAnswer:
    standard_answer_model = insert_standard_answer(
        keyword=standard_answer_creation_request.keyword,
        answer=standard_answer_creation_request.answer,
        categories=standard_answer_creation_request.categories,
        db_session=db_session,
    )
    return StandardAnswer.from_model(standard_answer_model)


@router.get("/standard-answer")
def list_standard_answers(
    db_session: Session = Depends(get_session),
    _: User | None = Depends(current_admin_user),
) -> list[StandardAnswer]:
    standard_answer_models = fetch_standard_answers(db_session=db_session)
    return [
        StandardAnswer.from_model(standard_answer_model)
        for standard_answer_model in standard_answer_models
    ]


@router.patch("/standard-answer/{standard_answer_id}")
def patch_standard_answer(
    standard_answer_id: int,
    standard_answer_creation_request: StandardAnswerCreationRequest,
    db_session: Session = Depends(get_session),
    _: User | None = Depends(current_admin_user),
) -> StandardAnswer:
    existing_standard_answer = fetch_standard_answer(
        standard_answer_id=standard_answer_id,
        db_session=db_session,
    )

    if existing_standard_answer is None:
        raise HTTPException(status_code=404, detail="Standard answer not found")

    standard_answer_model = update_standard_answer(
        standard_answer_id=standard_answer_id,
        keyword=standard_answer_creation_request.keyword,
        answer=standard_answer_creation_request.answer,
        categories=standard_answer_creation_request.categories,
        db_session=db_session,
    )
    return StandardAnswer.from_model(standard_answer_model)


@router.delete("/standard-answer/{standard_answer_id}")
def delete_standard_answer(
    standard_answer_id: int,
    db_session: Session = Depends(get_session),
    _: User | None = Depends(current_admin_user),
) -> None:
    return remove_standard_answer(
        standard_answer_id=standard_answer_id,
        db_session=db_session,
    )


@router.post("/standard-answer/category")
def create_standard_answer_category(
    standard_answer_category_creation_request: StandardAnswerCategoryCreationRequest,
    db_session: Session = Depends(get_session),
    _: User | None = Depends(current_admin_user),
) -> StandardAnswerCategory:
    standard_answer_category_model = insert_standard_answer_category(
        category_name=standard_answer_category_creation_request.name,
        db_session=db_session,
    )
    return StandardAnswerCategory.from_model(standard_answer_category_model)


@router.get("/standard-answer/category")
def list_standard_answer_categories(
    db_session: Session = Depends(get_session),
    _: User | None = Depends(current_admin_user),
) -> list[StandardAnswerCategory]:
    standard_answer_category_models = fetch_standard_answer_categories(
        db_session=db_session
    )
    return [
        StandardAnswerCategory.from_model(standard_answer_category_model)
        for standard_answer_category_model in standard_answer_category_models
    ]


@router.patch("/standard-answer/category/{standard_answer_category_id}")
def patch_standard_answer_category(
    standard_answer_category_id: int,
    standard_answer_category_creation_request: StandardAnswerCategoryCreationRequest,
    db_session: Session = Depends(get_session),
    _: User | None = Depends(current_admin_user),
) -> StandardAnswerCategory:
    existing_standard_answer_category = fetch_standard_answer_category(
        standard_answer_category_id=standard_answer_category_id,
        db_session=db_session,
    )

    if existing_standard_answer_category is None:
        raise HTTPException(
            status_code=404, detail="Standard answer category not found"
        )

    standard_answer_category_model = update_standard_answer_category(
        standard_answer_category_id=standard_answer_category_id,
        category_name=standard_answer_category_creation_request.name,
        db_session=db_session,
    )
    return StandardAnswerCategory.from_model(standard_answer_category_model)
