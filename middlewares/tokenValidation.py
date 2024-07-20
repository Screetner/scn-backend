from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from functions.auth.tokenValidation import accessTokenValidation


class AccessTokenValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next: RequestResponseEndpoint):
        exclude_paths = ["/auth/signIn", "/auth/renewToken", "/docs", "/openapi.json", "/redoc"]

        if any(request.url.path.startswith(path) for path in exclude_paths):
            return await call_next(request)

        token = request.headers.get("Authorization")
        if not token:
            return JSONResponse(content={"detail": "Token is required"}, status_code=403)

        try:
            token_status = accessTokenValidation(token)
            if token_status["status"] != "valid":
                if token_status["status"] == "expired":
                    raise HTTPException(status_code=401, detail="Token has expired")
                elif token_status["status"] == "invalid_claim":
                    raise HTTPException(status_code=403, detail=f"Invalid claim: {token_status['message']}")
                else:
                    raise HTTPException(status_code=403, detail="Invalid token")

            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
        except Exception as exc:
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
