import uuid


def generate_random_code():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return code
