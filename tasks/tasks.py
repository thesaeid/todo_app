from django.utils import timezone
from django.core.mail import send_mass_mail, BadHeaderError
from celery import shared_task
from .models import Task, Profile


@shared_task
def tasks_reminder():
    tasks = (
        Task.objects.select_related("profile")
        .filter(notify=True, status="todo")
        .exclude(end_time__gte=timezone.now())
        .values("title", "profile_id")
    )

    messages = {}
    ids = []
    for task in tasks:
        p_id = str(task["profile_id"])
        title = task["title"]
        if messages.get(p_id, None):
            messages[p_id].append(title)
        else:
            messages.setdefault(
                p_id,
                [
                    title,
                ],
            )

    ids = list({str(task["profile_id"]) for task in tasks})

    profiles = Profile.objects.select_related("user").filter(pk__in=ids)
    for profile in profiles:
        messages[profile.user.email] = messages.pop(str(profile.id))

    messages_list = []
    for username, titles in messages.items():
        messages_list.append(
            (
                "Task Reminder",
                f"""HI {username}, You have {len(titles)} task to do
            Here they are:
                {titles}
                """,
                "info@wtodo.online",
                [username],
            )
        )

    print("start sending emails.")

    try:
        send_mass_mail(
            messages_list,
            fail_silently=False,
        )
    except BadHeaderError:
        print("Bad Header Error!")

    print("emails were sent succusfully.")
