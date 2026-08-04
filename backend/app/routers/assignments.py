from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.assignment import (
    AssignmentCreate,
    AssignmentResponse
)

from app.services.assignment_service import (
    create_assignment
)



router = APIRouter(
    prefix="/assignments",
    tags=["Route Assignment"]
)



@router.post(
    "",
    response_model=AssignmentResponse
)
def assign_delivery(
    assignment: AssignmentCreate,
    db: Session = Depends(get_db)
):

    return create_assignment(
        db,
        assignment
    )