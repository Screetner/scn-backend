import os
from typing import Dict, Any
from authlib.jose import jwt, JoseError


def accessTokenValidation(token: str) -> Dict[str, Any]:
    secret = os.getenv("JWT_ACCESS_SECRET")

    try:
        # Decode the token
        claims = jwt.decode(token, secret)

        # Verify the token, including expiration
        # claims.validate()

        # If valid and not expired
        return {"status": "valid", "claims": claims}
    except JoseError as e:
        print(e)
        # Handle different JoseErrors for more specific feedback
        if isinstance(e, jwt.ExpiredTokenError):
            return {"status": "expired"}
        elif isinstance(e, jwt.InvalidClaimError):
            return {"status": "invalid_claim", "message": str(e)}
        else:
            return {"status": "invalid", "message": str(e)}
