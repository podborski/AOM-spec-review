import urllib3
import datetime


class RateLimitRetry(urllib3.util.retry.Retry):
    def get_retry_after(self, response):
        reset_time = datetime.datetime.fromtimestamp(
            int(response.headers["X-RateLimit-Reset"])
        )
        retry_after = (reset_time - datetime.datetime.now()).total_seconds() + 1
        retry_after = max(retry_after, 0)  # In case we hit a negative total_seconds
        print(f"Rate limited, retry after: {retry_after} seconds")
        return retry_after
