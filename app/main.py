from auth import get_user
from fastapi import Depends, FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from routers import public, secure

app = FastAPI()
Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "/metrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="inprogress",
    inprogress_labels=True,
).instrument(app, metric_namespace="mobidrom_routing_services", metric_subsystem="geopy_rest_proxy").expose(app)

app.include_router(public.router, prefix="/public")
app.include_router(secure.router, prefix="", dependencies=[Depends(get_user)])
