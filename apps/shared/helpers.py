"""
Helpers
"""
import uuid


def get_unique_code(size=10):
    code = str(uuid.uuid4()).replace('-', '')
    return code.upper()[:size].upper()
