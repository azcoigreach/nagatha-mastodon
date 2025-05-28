from fastapi import APIRouter, HTTPException
import logging
from app.services import admin_mastodon
from fastapi.responses import JSONResponse

router = APIRouter(tags=["admin"])

@router.get("/peers", summary="List all federated peer servers")
async def get_peers():
    try:
        peers = await admin_mastodon.get_federated_peers()
        return {"peers": peers}
    except Exception as e:
        logging.error(f"/admin/peers error: {e}")
        raise HTTPException(status_code=502, detail="Failed to fetch peers")

@router.get("/instances", summary="List known federated instances with metrics")
async def get_instances():
    try:
        instances = await admin_mastodon.get_federated_instances()
        return instances
    except Exception as e:
        logging.error(f"/admin/instances error: {e}")
        raise HTTPException(status_code=502, detail="Failed to fetch instances")

@router.get("/reports/summary", summary="Summary of pending and resolved reports")
async def get_reports_summary():
    try:
        summary = await admin_mastodon.get_report_summary()
        return summary
    except Exception as e:
        logging.error(f"/admin/reports/summary error: {e}")
        raise HTTPException(status_code=502, detail="Failed to fetch report summary")

@router.get("/measures", summary="System-wide stats (raw JSON)")
async def get_measures():
    try:
        measures = await admin_mastodon.get_system_measures()
        return JSONResponse(content=measures)
    except Exception as e:
        logging.error(f"/admin/measures error: {e}")
        raise HTTPException(status_code=502, detail="Failed to fetch system measures") 