from pydantic import SecretStr
from pydantic_settings import BaseSettings


class EngineSettings(BaseSettings):

    user: str
    password: SecretStr
    host: str
    port: str
    database: str

    @property
    def url(self) -> str:
        user = self.user
        password = self.password.get_secret_value()
        host = self.host
        port = self.port
        database = self.database

        return f'postgresql+psycopg://{user}:{password}@{host}:{port}/{database}'

