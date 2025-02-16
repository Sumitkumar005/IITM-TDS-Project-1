import os
import re

def query_llm(prompt: str) -> str:
    """
    Simulate sending a prompt to the LLM (GPT-4o-Mini) using the AIPROXY_TOKEN.
    For demonstration, if an email is present in the prompt, return it.
    """
    token = os.environ.get("AIPROXY_TOKEN")
    if not token:
        raise Exception("AIPROXY_TOKEN not set")
    # Dummy simulation: extract an email address if one exists.
    match = re.search(r'[\w\.-]+@[\w\.-]+', prompt)
    if match:
        return match.group(0)
    return "dummy@example.com"

def query_llm_image(prompt: str, image_bytes: bytes) -> str:
    """
    Simulate sending an image and a prompt to the LLM.
    For demonstration, return a dummy credit card number.
    """
    token = os.environ.get("AIPROXY_TOKEN")
    if not token:
        raise Exception("AIPROXY_TOKEN not set")
    return "1234567812345678"
