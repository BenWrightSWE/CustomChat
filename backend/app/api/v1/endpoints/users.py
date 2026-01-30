from fastapi import APIRouter, HTTPException, Depends
from app.schemas.users import UserUpdate, UserResponse, EmailUpdate
from app.crud import users as crud
from app.core.security import get_current_user
from app.core.supabase import supabase_admin

router = APIRouter()


@router.get("/", response_model=UserResponse)
def get_user_profile(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["id"]
        user = crud.get_user_by_user_id(user_id)
        return user
    except Exception as e:
        print(f"Error fetching user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while getting user profile")


@router.patch("/", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate, current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user["id"]

        if not user_update.model_dump(exclude_unset=True):
            raise HTTPException(status_code=400, detail="No update data provided")

        crud.update_user_by_user_id(user_id, user_update)
        user = crud.get_user_by_user_id(user_id)
        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while updating user profile")


@router.patch("/email")
def update_user_email(
    email_data: EmailUpdate,
    current_user: dict = Depends(get_current_user)
):
    try:
        supabase_admin.auth.admin.update_user_by_id(
            current_user["id"],
            {"email": str(email_data.email)}
        )
        return {"message": "Email updated successfully"}
    except Exception as e:
        print(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while updating user email")