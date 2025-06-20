from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_fastapi_instrumentator import Instrumentator

#Auth
from app.core.auth.router import router as employees_router
#Organizations
from app.core.organizations.router import router as organizations_router
#Tenders
from app.core.tenders.router import router as tender_router
#Bids
from app.core.bids.router import router as bids_router


app = FastAPI()
app.include_router(employees_router)
app.include_router(organizations_router)
app.include_router(tender_router)
app.include_router(bids_router)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)

@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return "pong"
