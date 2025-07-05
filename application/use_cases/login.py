from flask_jwt_extended import create_access_token
from domain.services.authentication_service import AuthenticationService

class LoginUseCase:
    def __init__(self, authentication_service: AuthenticationService):
        self.authentication_service = authentication_service

    def execute(self, email: str, password: str) -> dict:
        user = self.authentication_service.authenticate(email, password)
        if user:
            token = create_access_token(identity=user.email, additional_claims={"rol": user.role})
            return {"token": token, "status":200}
        return {"error": "Credenciales incorrectas", "status":401}