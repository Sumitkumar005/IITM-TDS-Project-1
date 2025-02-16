from tasks import handle_task

def run_task(task_description: str) -> str:
    """
    Parse the plain‑English task description, execute the necessary steps,
    and return a status message.
    """
    message = handle_task(task_description)
    return message
