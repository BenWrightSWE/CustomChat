from fastapi import APIRouter, HTTPException, Depends
from backend.app.schemas.feedback import FeedbackCreate, FeedbackResponse
from backend.app.crud import feedback as crud
from backend.app.crud import bots as bot_crud
from backend.app.core.security import get_current_user, verify_bot_ownership

router = APIRouter()


@router.post(
    "/bots/{bot_id}/feedback", response_model=FeedbackResponse, status_code=201
)
def create_feedback(
    bot_id: int, fb_data: FeedbackCreate, _: dict = Depends(verify_bot_ownership)
):
    try:
        return crud.create_feedback(bot_id, fb_data)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating feedback: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/bots/{bot_id}/feedback", response_model=list[FeedbackResponse])
def get_all_feedback(bot_id: int, _: dict = Depends(verify_bot_ownership)):
    try:
        return crud.get_all_feedback(bot_id)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching feedback: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/bots/{bot_id}/feedback/{fb_id}", response_model=FeedbackResponse)
def get_feedback_by_id(
    bot_id: int, fb_id: int, _: dict = Depends(verify_bot_ownership)
):
    try:
        feedback = crud.get_feedback_by_id(bot_id, fb_id)
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback not found")

        return feedback
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching feedback: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
