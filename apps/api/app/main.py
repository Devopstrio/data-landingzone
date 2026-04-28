import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("landingzone-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="Data Landing Zone API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/landingzones")
def get_landing_zones():
    return [
        {"id": "lz-azure-finance", "name": "Azure Finance Zone", "cloud": "Azure", "status": "ACTIVE"},
        {"id": "lz-aws-marketing", "name": "AWS Marketing Zone", "cloud": "AWS", "status": "ACTIVE"},
        {"id": "lz-gcp-ops", "name": "GCP Operations Zone", "cloud": "GCP", "status": "PROVISIONING"}
    ]

@app.get("/governance/summary")
def get_governance_summary():
    return {
        "policy_compliance_score": 98.5,
        "active_violations": 3,
        "tags_standardized": "100%",
        "orphaned_resources": 12
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_zones": 14,
        "total_domains_onboarded": 42,
        "active_provisioning_jobs": 2,
        "monthly_platform_cost": "$42,400"
    }

@app.post("/landingzones/create")
def create_landing_zone(name: str, cloud: str):
    logger.info(f"Triggering landing zone creation: {name} on {cloud}")
    return {"status": "Provisioning Started", "job_id": "job_987654"}
