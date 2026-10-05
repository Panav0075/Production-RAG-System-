Title: Authentication
URL: https://docs.example.local/authentication

# Authentication

The API supports personal access tokens and OAuth 2.0. Personal access tokens are intended for scripts, command-line tools, and internal automation. A token must be sent in the Authorization header using the Bearer scheme.

Personal access tokens can be created from Settings > Developer > API Tokens. The full token is displayed only once when it is created. Store it in a secret manager or another protected location rather than committing it to source control.

OAuth 2.0 should be used when an application needs to act on behalf of multiple users. Authorization codes expire after ten minutes. Access tokens are valid for one hour, and refresh tokens can be exchanged for a new access token without asking the user to sign in again.

API tokens can be revoked immediately from the Developer settings page. Requests made with a revoked token return HTTP 401.
