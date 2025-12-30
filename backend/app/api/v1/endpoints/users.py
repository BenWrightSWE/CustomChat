from fastapi import APIRouter, HTTPException, Depends
from backend.app.schemas.users import UserUpdate, UserResponse
from backend.app.crud import users as crud
from backend.app.core.security import get_current_user

router = APIRouter()

# route to get a user's data
@router.get("/me", response_model=UserResponse)
def get_current_user(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["id"]
        user = crud.get_user_by_user_id(user_id)
        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# route to update a user's data
@router.patch("/me", response_model=UserResponse)
def update_current_user(user_update: UserUpdate, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]

    if not user_update.model_dump(exclude_unset=True):
        raise HTTPException(status_code=400, detail="No update data provided.")
    try:
        crud.update_user_by_user_id(user_id, user_update)
        user = crud.get_user_by_user_id(user_id)
        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
