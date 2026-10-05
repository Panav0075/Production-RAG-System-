Title: API Rate Limits
URL: https://docs.example.local/rate-limits

# API Rate Limits

API requests are limited per workspace. The Free plan allows 60 requests per minute, the Pro plan allows 600 requests per minute, and Enterprise limits are configured with the account team.

When a workspace exceeds its limit, the API returns HTTP 429 Too Many Requests. The response includes a Retry-After header containing the number of seconds the client should wait before trying again.

Clients should use exponential backoff for repeated rate-limit responses. Retrying immediately in a tight loop can extend recovery time and create unnecessary load. Rate-limit headers are returned with authenticated API responses so applications can monitor remaining capacity.
