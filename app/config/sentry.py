from app.config import Config


sentry_config = {
    "dsn": Config.SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    "traces_sample_rate": 0.01,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    "profiles_sample_rate": 0.2,
    # This can either be dev, uat, staging, or production.
    # It is set by CLA_ENVIRONMENT in the helm charts.
    "environment": Config.ENVIRONMENT,
}
