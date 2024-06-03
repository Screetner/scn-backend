from pydantic import BaseModel


class SignInModel(BaseModel):
    username: str
    password: str


class SignUpModel(BaseModel):
    username: str
    password: str
    roleId: int
