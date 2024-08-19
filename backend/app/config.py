from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres.ccpighleiemxslknuvyh:fazin1980dxb@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
    secret_key: str = "a86cbc50849b00a86240caf7ab1c5be964fcdc485b78263c64b516cb93db2fa0"
    jwt_secret_key: str = "a86cbc50849b00a86240caf7ab1c5be964fcdc485b78263c64b516cb93db2fa0"
    websocket_port: int = 8001

    class Config:
        env_file = ".env"
