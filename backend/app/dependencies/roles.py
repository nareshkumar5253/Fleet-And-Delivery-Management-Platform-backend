from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.models.user import UserRole



def require_role(required_role: UserRole):

    def role_checker(
        current_user = Depends(get_current_user)
    ):

        if current_user.role != required_role:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource"
            )


        return current_user


    return role_checker
def require_admin():

    return require_role(
        UserRole.ADMIN
    )

from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.models.user import UserRole


def require_admin_or_dispatcher():

    def role_checker(
        current_user=Depends(get_current_user)
    ):

        if current_user.role not in [
            UserRole.ADMIN,
            UserRole.DISPATCHER
        ]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return current_user

    return role_checker

from app.models.user import UserRole


def require_driver():

    def role_checker(
        current_user=Depends(get_current_user)
    ):

        if current_user.role != UserRole.DRIVER:
            raise HTTPException(
                status_code=403,
                detail="Driver access required"
            )

        return current_user

    return role_checker
def require_delivery_user():

    def role_checker(
        current_user=Depends(get_current_user)
    ):

        if current_user.role not in [
            UserRole.ADMIN,
            UserRole.DISPATCHER,
            UserRole.DRIVER
        ]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return current_user

    return role_checker