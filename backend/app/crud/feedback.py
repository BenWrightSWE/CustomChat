from backend.app.schemas.feedback import FeedbackCreate
from backend.app.core.supabase import supabase_admin


def create_feedback(bot_id: int, fb_data: FeedbackCreate):
    fb_dict = fb_data.model_dump(mode="json")
    fb_dict["bot_id"] = bot_id

    response = supabase_admin.table("feedback").insert(fb_dict).execute()
    return response.data[0]


def get_all_feedback(bot_id: int):
    response = supabase_admin.table("feedback").select("*").eq("bot_id", bot_id).execute()
    return response.data


def get_feedback_by_id(bot_id: int, fb_id: int):
    response = (
        supabase_admin.table("feedback")
        .select("*")
        .eq("bot_id", bot_id)
        .eq("fb_id", fb_id)
        .single()
        .execute()
    )
    return response.data
