import logging
from app.core.mastodon_client import get_mastodon_client
from concurrent.futures import ThreadPoolExecutor
import asyncio

_executor = ThreadPoolExecutor(max_workers=4)

def _run_in_executor(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(_executor, lambda: func(*args, **kwargs))

def _api_request(mastodon, method, endpoint, params=None):
    # Try public 'request' method first, fallback to private '_Mastodon__api_request'
    actual_params = params or {} # Ensure params is a dict, especially for _Mastodon__api_request
    if hasattr(mastodon, 'request'):
        # The public 'request' method likely handles params=None correctly itself.
        return mastodon.request(method, endpoint, params=params)
    elif hasattr(mastodon, '_Mastodon__api_request'):
        # _Mastodon__api_request might be more sensitive to params not being a dict.
        return mastodon._Mastodon__api_request(method, endpoint, params=actual_params)
    else:
        raise RuntimeError('No suitable Mastodon API request method found')

async def get_federated_peers():
    mastodon = get_mastodon_client()
    try:
        peers = await _run_in_executor(mastodon.instance_peers)
        return peers
    except Exception as e:
        logging.error(f"Error fetching federated peers: {e}")
        raise RuntimeError(f"Error fetching federated peers: {e}")

async def get_federated_instances():
    mastodon = get_mastodon_client()
    try:
        result = await _run_in_executor(
            lambda: _api_request(mastodon, 'GET', '/api/v1/admin/instances')
        )
        instances = []
        for inst in result:
            instances.append({
                "domain": inst.get("domain"),
                "users_count": inst.get("users_count"),
                "statuses_count": inst.get("statuses_count"),
                "software": inst.get("software"),
                "version": inst.get("version"),
                "uptime": inst.get("uptime", "unknown")
            })
        return instances
    except Exception as e:
        logging.error(f"Error fetching federated instances: {e}")
        raise RuntimeError(f"Error fetching federated instances: {e}")

async def get_report_summary():
    mastodon = get_mastodon_client()
    try:
        reports = await _run_in_executor(mastodon.admin_reports)
        open_reports = sum(1 for r in reports if not r.get("resolved"))
        resolved_reports = sum(1 for r in reports if r.get("resolved"))
        spam_related = sum(1 for r in reports if "spam" in (r.get("category") or ""))
        harassment_related = sum(1 for r in reports if "harassment" in (r.get("category") or ""))
        latest_report_ts = max((r.get("created_at") for r in reports if r.get("created_at")), default=None)
        if latest_report_ts:
            latest_report_ts = str(latest_report_ts)
        return {
            "open_reports": open_reports,
            "resolved_reports": resolved_reports,
            "spam_related": spam_related,
            "harassment_related": harassment_related,
            "latest_report_ts": latest_report_ts
        }
    except Exception as e:
        logging.error(f"Error fetching report summary: {e}")
        raise RuntimeError(f"Error fetching report summary: {e}")

async def get_system_measures():
    mastodon = get_mastodon_client()
    try:
        now = datetime.utcnow()
        yesterday = now - timedelta(days=1)
        measures = await _run_in_executor(
            lambda: _api_request(
                mastodon,
                'GET',
                '/api/v1/admin/measures',
                params={
                    'start_at': yesterday.isoformat() + 'Z',
                    'end_at': now.isoformat() + 'Z'
                }
            )
        )
        return measures
    except Exception as e:
        logging.error(f"Error fetching system measures: {e}")
        raise RuntimeError(f"Error fetching system measures: {e}") 