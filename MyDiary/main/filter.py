from main import *


@app.template_filter("formatdatetime")
def format_datetime(value):  ## utc time을 알아보기 쉬운 시간으로 변환하는 필터
    if value is None:
        return ""
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
        now_timestamp
    )
    value = datetime.fromtimestamp((int(value) / 1000)) + offset
    return value.strftime("%Y-%m-%d %H:%M:%S")
