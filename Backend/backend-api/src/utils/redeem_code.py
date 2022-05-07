import uuid

def generate_redeem_code():
    return str(uuid.uuid4()).replace('-', '')[:24]