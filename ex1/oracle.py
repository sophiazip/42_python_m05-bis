import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()

matrix_mode = os.getenv("MATRIX_MODE")
db_url = os.getenv("DATABASE_URL")
api_key = os.getenv("API_KEY")
log_level = os.getenv("LOG_LEVEL")
zion_endpoint = os.getenv("ZION_ENDPOINT")

network_online = "Offline"


def get_config_report() -> None:
    config_report: dict[str, str | None] = {
        "Mode": "development"
                if matrix_mode == "development" else "production",
        "Database": "Connected to local instance"
                if db_url else "No database URL defined",
        "API Access": "Authenticated" if api_key else "Not Authenticated",
        "Log Level": log_level,
        "Remote Network": "Online" if network_online else "Offline"
    }

    print("Configuration loaded:")
    for key, value in config_report.items():
        print(f"{key}: {value}")


def get_security_checks() -> None:
    pass
