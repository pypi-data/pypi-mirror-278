import time
from datetime import datetime
from datetime import timedelta

from .client import request_post
from .client import request_get

JOBS = "jobs"
FIVE_MINUES = timedelta(minutes=5)


def create_search_job(query, start: datetime = None, end: datetime = None, limit=100, timeout_ms=1000):
    if start is None:
        start = datetime.now() - FIVE_MINUES
    if end is None:
        end = datetime.now()
    data = {
        "query": query,
        "startTime": int(start.timestamp() * 1000),
        "endTime": int(end.timestamp() * 1000),
        "collectSize": limit,
        "timeout": timeout_ms,

        "app": "search",
        "preview": False,
        "mode": "smart",
    }
    return request_post(JOBS, data=data, custom_headers={"Content-Type": "application/json"}).json()


def get_search_job_status(jobid):
    return request_get(f"{JOBS}/{jobid}", custom_headers={"Content-Type": "application/json"}).json()


def get_search_job_result(jobid):
    return request_get(f"{JOBS}/{jobid}/results", custom_headers={"Content-Type": "application/json"}).json()


def search_spl(spl, start=None, end=None, limit=100, req_timeout=3000):
    resp = create_search_job(query=spl, start=start, end=end, limit=limit, timeout_ms=req_timeout)
    jobid = ""
    if ("meta" in resp) and resp["meta"]["process"] == 1:
        return resp["result"]
    else:
        jobid = resp["id"]

    while True:
        status = get_search_job_status(jobid)
        if ("process" in status) and status["process"] == 1:
            break
        time.sleep(0.2)
    return get_search_job_result(jobid)


if __name__ == "__main__":
    print(search_spl('search2 repo="*"', limit=1, req_timeout=1000))
