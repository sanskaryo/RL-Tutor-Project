"""API Router Configuration"""
from fastapi import APIRouter
from . import mindmap

# Single router aggregator; main.py will mount with settings.API_V1_STR
api_router = APIRouter()

# Include available routers
api_router.include_router(mindmap.router, tags=["Mind Map"])
