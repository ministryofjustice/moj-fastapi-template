from app.main import create_app
from app.config import Config
from app.config.sentry import sentry_config
import sentry_sdk


if Config.SENTRY_DSN:
    sentry_sdk.init(**sentry_config)


api = create_app()
