import time
import logging
import socket
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from src.database import IDatabase
from src.utils import IUtils
from src.dependencies import get_database, get_utils


logger = logging.getLogger(__name__)
router = APIRouter()


class RootResponse(BaseModel):
    version: str
    date: int
    kubernetes: bool


class LookupRequest(BaseModel):
    domain: str


class ValidateRequest(BaseModel):
    ip: str


@router.get("/", response_model=RootResponse)
async def root(utils: IUtils = Depends(get_utils)):
    return {
        "version": "0.1.0",
        "date": int(time.time()),
        "kubernetes": utils.is_running_in_kubernetes()
    }


@router.post("/v1/tools/lookup")
async def lookup(
    request: LookupRequest,
    db: IDatabase = Depends(get_database),
    utils: IUtils = Depends(get_utils)
):
    try:
        ip_addresses = utils.get_ip_addresses(request.domain)
        await db.save_query(request.domain, ip_addresses)
        return {"ip_addresses": ip_addresses}
    except socket.gaierror:
        raise HTTPException(status_code=404, detail="Domain not found")


@router.post("/v1/tools/validate")
async def validate(
    request: ValidateRequest,
    utils: IUtils = Depends(get_utils)
):
    return {"is_valid": utils.is_valid_ip(request.ip)}


@router.get("/v1/history")
async def history(db: IDatabase = Depends(get_database)):
    return await db.get_latest_queries(20)
