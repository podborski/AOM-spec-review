import urllib3
import datetime


class RateLimitRetry(urllib3.util.retry.Retry):
    """
    This class overrides the urllib3 retry mechanism to comply with
    GitHub's API rate limiting constraints
    Source: https://github.com/PyGithub/PyGithub/issues/1989#issuecomment-1261656811
    """
    def get_retry_after(self, response):
        reset_time = datetime.datetime.fromtimestamp(
            int(response.headers["X-RateLimit-Reset"])
        )
        retry_after = (reset_time - datetime.datetime.now()).total_seconds() + 1
        retry_after = max(retry_after, 0)
        print(f"Rate limited, retry after: {retry_after} seconds")
        return retry_after
