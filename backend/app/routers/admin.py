from fastapi import APIRouter, Depends

from app.dependencies.roles import require_admin


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)



@router.get("/test")
def admin_test(
    current_user = Depends(require_admin())
):

    return {
        "message": "Welcome Admin",
        "user": current_user.email
    }