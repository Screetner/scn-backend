from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from functions.auth.tokenValidation import accessTokenValidation


class AccessTokenValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next: RequestResponseEndpoint):
        exclude_paths = [ "/auth/signIn", "/auth/renewToken", "/docs", "/openapi.json", "/redoc", "/faker/insert",
                         "/organization"]

        if any(request.url.path.startswith(path) for path in exclude_paths):
            return await call_next(request)

        token = request.headers.get("Authorization")
        print(token)

        if not token:
            return JSONResponse(content={"detail": "Token is required"}, status_code=403)

        try:
            user_access_token = token.split("Bearer ")[-1].strip()
            print(user_access_token)
            token = accessTokenValidation(user_access_token)
            if token["status"] != "valid":
                if token["status"] == "expired":
                    raise HTTPException(status_code=401, detail="Token has expired")
                elif token["status"] == "invalid_claim":
                    raise HTTPException(status_code=403, detail=f"Invalid claim: {token['message']}")
                else:
                    raise HTTPException(status_code=403, detail="Invalid token")

            request.state.token_payload = token["claims"]

            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
        except Exception as exc:
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
