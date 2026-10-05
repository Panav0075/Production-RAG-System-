Title: Webhooks
URL: https://docs.example.local/webhooks

# Webhooks

Webhooks notify an application when selected events occur. A webhook endpoint must use HTTPS and return a successful 2xx response within five seconds.

Every webhook request includes an X-Webhook-Signature header. The signature is an HMAC-SHA256 digest created from the raw request body using the webhook signing secret. Applications should compute the HMAC using the raw body and compare it with the header using a constant-time comparison before processing the event.

If delivery fails, the service retries the webhook with exponential backoff for up to 24 hours. Event payloads include a unique event_id. Consumers should store processed event IDs so repeated deliveries do not cause the same action to run twice.
