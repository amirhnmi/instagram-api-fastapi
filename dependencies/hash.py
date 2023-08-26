from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(self, password):
        return password_context.hash(password)
    
    def verify(self, hashed_password, plain_password):
        return password_context.verify(plain_password, hashed_password)