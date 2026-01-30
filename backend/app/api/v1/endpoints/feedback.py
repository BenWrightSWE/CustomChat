from fastapi import APIRouter, HTTPException, Depends
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.crud import feedback as crud
from app.core.security import verify_bot_ownership

router = APIRouter()


@router.post("/", response_model=FeedbackResponse, status_code=201)
def create_feedback(
    bot_id: int,
    fb_data: FeedbackCreate,
    _: dict = Depends(verify_bot_ownership)
):
    try:
        return crud.create_feedback(bot_id, fb_data)
    except Exception as e:
        print(f"Error creating feedback: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while creating feedback"
        )


@router.get("/", response_model=list[FeedbackResponse])
def get_all_feedback(bot_id: int, _: dict = Depends(verify_bot_ownership)):
    try:
        return crud.get_all_feedback(bot_id)
    except Exception as e:
        print(f"Error fetching feedback: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while getting all feedback for bot")


@router.get("/{fb_id}", response_model=FeedbackResponse)
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
        raise HTTPException(status_code=500, detail="Internal server error while getting feedback by id")
