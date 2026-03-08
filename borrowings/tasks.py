import datetime
from celery import shared_task
from borrowings.models import Borrowing
from notifications import send_telegram_message


@shared_task()
def check_overdue_borrowings():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=tomorrow, actual_return_date__isnull=True
    )

    if not overdue_borrowings.exists():
        send_telegram_message("✅ No borrowings overdue today!")
        return

    message = "⚠️ <b>ATTENTION! List of overdue borrowings:</b>\n\n"

    for borrowing in overdue_borrowings:
        message += (
            f"<b>User:</b> {borrowing.user.email}\n"
            f"<b>Book:</b> {borrowing.book.title}\n"
            f"<b>Due date:</b> {borrowing.expected_return_date}\n"
            f"----------------------------\n"
        )

    send_telegram_message(message)
