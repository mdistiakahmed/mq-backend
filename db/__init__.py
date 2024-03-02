from config.config_manager import CONFIG

DB_PATH = (
    "postgresql://"
    f"{CONFIG.db_username}:{CONFIG.db_password}@"
    f"{CONFIG.db_host}:{CONFIG.db_port}/{CONFIG.db_name}"
)
