from app.worker.celery_app import celery


@celery.task(name="send_notification_task")
def send_notification_task(user_id, message):
    print(f"Notification sent to user {user_id}: {message}")

    return {
        "status": "success",
        "user_id": user_id,
        "message": message
    }