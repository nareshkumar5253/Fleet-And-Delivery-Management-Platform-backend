from app.worker.celery_app import celery


@celery.task
def send_notification_task(
    user_id: int,
    message: str
):

    print(
        f"""
        Sending Notification

        User: {user_id}

        Message:
        {message}
        """
    )

    return {
        "status": "Notification Sent",
        "user_id": user_id
    }



@celery.task
def refresh_analytics_task():

    print(
        "Refreshing analytics cache..."
    )

    return {
        "status": "Analytics Updated"
    }