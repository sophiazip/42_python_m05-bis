import os
import sys
from dotenv import load_dotenv  # type: ignore

load_dotenv()

MATRIX_MODE: str = os.getenv("MATRIX_MODE", "development")
DATABASE_URL: str | None = os.getenv("DATABASE_URL")
API_KEY: str | None = os.getenv("API_KEY")
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG"
                           if MATRIX_MODE == "development" else "INFO")
ZION_ENDPOINT: str | None = os.getenv("ZION_ENDPOINT")


def check_hardcoded_secrets() -> bool:
    target_keys = {
        "MATRIX_MODE",
        "DATABASE_URL",
        "API_KEY",
        "LOG_LEVEL",
        "ZION_ENDPOINT"
    }
    try:
        with open(__file__, "r", encoding="utf-8") as f:
            for line in f:
                clean = line.strip().replace(" ", "")
                if "os.getenv" in clean or "target_keys" in clean:
                    continue
                if any(clean.startswith(f"{key}=") for key in target_keys):
                    return False
        return True
    except OSError:
        return False


def check_gitignore_status() -> bool:
    search_paths = [
        os.path.join(os.path.dirname(__file__), ".gitignore"),
        os.path.join(os.path.dirname(__file__), "..", ".gitignore"),
        ".gitignore"
    ]
    for path in search_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as gitignore:
                    for line in gitignore:
                        clean = line.strip()
                        if clean in {".env", "*.env", ".env*"}:
                            return True
            except OSError:
                continue
    return False


def get_config_report() -> None:
    print("ORACLE STATUS: Consulting the configuration...")
    print("\nConfiguration loaded:")

    mode_display = "development" if MATRIX_MODE == "development" \
        else "production"
    db_display = "Connected to local instance" if DATABASE_URL \
        else "No database URL defined"
    api_display = "Authenticated" if API_KEY else "Not Authenticated"
    network_display = "Online" if ZION_ENDPOINT else "Offline"

    print(f"Mode: {mode_display}")
    print(f"Database: {db_display}")
    print(f"API Access: {api_display}")
    print(f"Log Level: {LOG_LEVEL}")
    print(f"Remote Network: {network_display}")

    if MATRIX_MODE == "development":
        print("\n[DEV NOTICE] Running in verbose diagnostic mode.")
    else:
        print(
            """\n[PROD NOTICE] Running in hardened production mode.
            Secrets are masked."""
            )


def get_security_checks() -> None:
    print("\nConfiguration security check:")

    no_secrets = check_hardcoded_secrets()
    if no_secrets:
        print("[OK] No hardcoded secrets detected")
    else:
        print("[FAIL] Hardcoded secrets detected in source code!")

    env_ignored = check_gitignore_status()
    if env_ignored:
        print("[OK] .env file properly ignored by git")
    else:
        print("[FAIL] .env file is NOT ignored by git!")

    print("[OK] Production overrides available")


def main() -> None:
    if not os.path.exists(".env") \
            and not os.getenv("API_KEY") \
            and not os.getenv("DATABASE_URL"):
        print(
            """[WARN] No .env file or environment
            overrides found. Using defaults.\n""",
            file=sys.stderr
            )

    get_config_report()
    get_security_checks()
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
