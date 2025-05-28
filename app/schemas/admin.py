from pydantic import BaseModel
from typing import List, Optional

class PeersResponse(BaseModel):
    peers: List[str]

class InstanceInfo(BaseModel):
    domain: str
    users_count: int
    statuses_count: int
    software: str
    version: str
    uptime: str

class ReportSummary(BaseModel):
    open_reports: int
    resolved_reports: int
    spam_related: int
    harassment_related: int
    latest_report_ts: Optional[str] 