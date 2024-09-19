# Access Tokens
The /token endpoint generates the required access token to allow a user to access the service. When submitting other requests, the request needs to contain this authorisation bearer token.

All access tokens are valid for 30 minutes on the API. This can be adjusted by amending ACCESS_TOKEN_EXPIRE_MINUTES on the auth/security.py file. This can be authenticated via a username and password which is compared to the hashed password in the database. As long as the user is logged in, a JWT token can be generated for their user.

## Updating the Secret Key
The OAuth2 JWT encoding requires a SECRET_KEY. This can be defined in your .env file to generate unique tokens. All environments have a different secret key that defines what to be encoded against.

## Adding Auth to Routes
To add authorisation to any route, simply add the below to the route definition:
```shell
current_user: Users = Depends(get_current_active_user)
```

## Hashing and Encoding
All password information is hashed and salted per argon2 and passlib. The token is then generated and encoded via JWT which uses the secret key to sign the identity of the token. This means that the token contains a header, payload and a signature following the HS256 algorithm ensuring security.

## Default credentials
When running the app locally the script in `bin/add_users.py` will add a default user:

- **Username:** test_user

- **Password:** test_password

Users should be present in the database when not running this locally.