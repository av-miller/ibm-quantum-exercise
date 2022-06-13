from pydantic import BaseSettings



class Settings(BaseSettings):
    acme_load_url: str
    acme_run_url: str
    madrid_load_url: str
    madrid_run_url: str

    class Config:
        env_file = ".env"
