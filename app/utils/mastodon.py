def normalize_mastodon_username(username: str) -> str:
    """
    Normalize a Mastodon username by removing a leading '@' if present.
    Accepts 'username', '@username', or '@username@server'.
    Returns 'username' or 'username@server'.
    """
    if username.startswith("@"):
        return username[1:]
    return username

def get_local_server_domain() -> str:
    """
    Extract the domain from the Mastodon API base URL in settings.
    Returns the domain as a string, e.g., 'stranger.social'.
    """
    from app.core.config import settings
    import re
    api_base = settings.MASTODON_API_BASE or "https://stranger.social"
    # Remove protocol
    domain = re.sub(r"^https?://", "", api_base)
    # Remove trailing slash if present
    domain = domain.rstrip("/")
    return domain

def extract_local_username(username: str) -> str:
    """
    If the username is in the form 'username@localdomain', and localdomain matches the local server,
    return just 'username'. Otherwise, return the username unchanged.
    """
    domain = get_local_server_domain()
    if "@" in username:
        parts = username.split("@")
        # Handles both '@username@domain' and 'username@domain'
        if len(parts) == 3 and parts[2] == domain:
            return parts[1]
        elif len(parts) == 2 and parts[1] == domain:
            return parts[0]
    return username 