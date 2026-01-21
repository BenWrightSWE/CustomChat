from fastapi import APIRouter, HTTPException, Depends
from backend.app.schemas.bots import BotCreate, BotUpdate, BotResponse
from backend.app.crud import bots as crud
from backend.app.core.security import get_current_user, verify_bot_ownership

router = APIRouter()


@router.post("/bots", response_model=BotResponse, status_code=201)
def create_bot(bot_data: BotCreate, current_user: dict = Depends(get_current_user)):
    try:
        return crud.create_bot(current_user["id"], bot_data)
    except Exception as e:
        print(f"Error creating bot: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/bots", response_model=list[BotResponse])
def get_all_bots(current_user: dict = Depends(get_current_user)):
    try:
        return crud.get_all_bots(current_user["id"])
    except Exception as e:
        print(f"Error fetching bots: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/bots/{bot_id}", response_model=BotResponse)
def get_bot_by_id(bot_id: int, current_user: dict = Depends(get_current_user)):
    try:
        response = crud.get_bot_by_id(current_user["id"], bot_id)
        if not response:
            raise HTTPException(status_code=404, detail="Bot not found")
        return response
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching bot: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/bots/{bot_id}", response_model=BotResponse)
def update_bot_by_id(
    update_data: BotUpdate,
    bot_id: int,
    current_user: dict = Depends(get_current_user),
    _: dict = Depends(verify_bot_ownership)
):
    try:
        if not update_data.model_dump(exclude_unset=True):
            raise HTTPException(status_code=400, detail="No update data provided")

        return crud.update_bot_by_id(current_user["id"], bot_id, update_data)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating bot: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/bots/{bot_id}", status_code=204)
def delete_bot_by_id(
    bot_id: int,
    current_user: dict = Depends(get_current_user),
    _: dict = Depends(verify_bot_ownership)
):
    try:
        crud.delete_bot_by_id(current_user["id"], bot_id)
        return None
    except Exception as e:
        print(f"Error updating bot: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
