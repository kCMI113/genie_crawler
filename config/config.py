from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):
    db_host: str
    db_name: str
    db_username: str
    db_password: str

    class Config:
        env_file = ".env"
