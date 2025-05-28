from mastodon import Mastodon
from functools import lru_cache
from app.core.config import settings

@lru_cache()
def get_mastodon_client() -> Mastodon:
    access_token = settings.MASTODON_ACCESS_TOKEN
    api_base_url = settings.MASTODON_API_BASE or "https://stranger.social"
    if not access_token:
        raise RuntimeError("MASTODON_ACCESS_TOKEN not set in environment.")
    return Mastodon(
        access_token=access_token,
        api_base_url=api_base_url,
        ratelimit_method='throw',
    ) 