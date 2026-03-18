import hmac

def normalize_user_id(user_id):
    return str(user_id)


def timing_safe_compare(a, b):
    """
    Perform a timing-safe comparison between two strings.

    This function helps prevent timing attacks by ensuring that the
    comparison takes a constant amount of time regardless of how
    similar the inputs are.

    Args:
        a (str): First string to compare.
        b (str): Second string to compare.

    Returns:
        bool: True if both strings are equal, False otherwise.
    """

    # Ensure both inputs are strings
    if not isinstance(a, str) or not isinstance(b, str):
        return False

    # Convert strings to bytes for comparison
    buf_a = a.encode()
    buf_b = b.encode()

    # If lengths differ, still perform a dummy comparison
    # to avoid leaking timing information
    if len(buf_a) != len(buf_b):
        hmac.compare_digest(buf_a, buf_a)
        return False

    # Perform constant-time comparison
    return hmac.compare_digest(buf_a, buf_b)