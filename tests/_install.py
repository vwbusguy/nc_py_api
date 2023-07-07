from os import environ

import uvicorn
from fastapi import FastAPI

from nc_py_api import NextcloudApp, set_enabled_handler, ApiScope, set_scopes, enable_heartbeat, LogLvl

APP = FastAPI()


def enabled_handler(enabled: bool, nc: NextcloudApp) -> str:
    print(f"enabled_handler: enabled={enabled}", flush=True)
    if enabled:
        nc.log(LogLvl.WARNING, f"Hello from {nc.app_cfg.app_name} :)")
    else:
        nc.log(LogLvl.WARNING, f"Bye bye from {nc.app_cfg.app_name} :(")
    return ""


@APP.on_event("startup")
def initialization():
    set_enabled_handler(APP, enabled_handler)
    set_scopes(
        APP,
        {
            "required": [
                ApiScope.SYSTEM,
                ApiScope.DAV,
                ApiScope.USER_INFO,
                ApiScope.USER_STATUS,
                ApiScope.NOTIFICATIONS,
                ApiScope.WEATHER_STATUS,
            ],
            "optional": [],
        },
    )
    enable_heartbeat(APP)


if __name__ == "__main__":
    uvicorn.run(
        "_install:APP", host=environ.get("APP_HOST", "127.0.0.1"), port=int(environ["APP_PORT"]), log_level="trace"
    )
