# JWT Authentication

This project uses [Django SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) for handling JSON Web Token (JWT) authentication. Below are the endpoints provided for token management.

## Authentication Endpoints

### Obtain Token

To get a pair of access and refresh tokens, make a POST request to the following endpoint:

**URL**: `/auth/token/`

**Method**: `POST`

**Request Body**:

```json
{
    "username": "username",
    "password": "password"
}
```

**Response**:

```json
{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}
```

### Refresh Token

To refresh an expired access token, make a POST request to the following endpoint with the refresh token:

**URL**: `/auth/token/refresh/`

**Method**: `POST`

**Request Body**:

```json
{
    "refresh": "your_refresh_token"
}
```

**Response**:

```json
{
    "access": "your_access_token"
}
```

### Verify Token

To verify the validity of an access token, make a POST request to the following endpoint:

**URL**: `/auth/token/verify/`

**Method**: `POST`

**Request Body**:

```json
{
    "token": "your_access_token"
}
```

**Response**:

```json
{}
```

If the token is valid, the response will be empty. If the token is invalid, an error message will be returned.

## Example Usage

Here is an example of how you might use these endpoints in your client:

### Obtain Token Example

```bash
curl -X POST http://localhost:8000/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "password123"}'
```

### Refresh Token Example

```bash
curl -X POST http://localhost:8000/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your_refresh_token"}'
```

### Verify Token Example

```bash
curl -X POST http://localhost:8000/auth/token/verify/ \
  -H "Content-Type: application/json" \
  -d '{"token": "your_access_token"}'
```

## Settings

You can override the default `SIMPLE_JWT`configs inside `config/settings/base.py`.
