from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import ExpiredSignatureError
from werkzeug.exceptions import Forbidden, NotFound

from StudioPulse.app import config
from StudioPulse.app.utils import permissions
from StudioPulse import __version__ as StudioPulse_version


if config.SENTRY_ENABLED:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        from sentry_sdk.integrations.rq import RqIntegration
    except ModuleNotFoundError:
        print("sentry_sdk module not found.")

if config.PROMETHEUS_METRICS_ENABLED:
    try:
        import prometheus_flask_exporter
        import prometheus_flask_exporter.multiprocess
    except ModuleNotFoundError:
        print("prometheus_flask_exporter not found.")


def init_monitoring(app):
    if config.SENTRY_ENABLED:
        sentry_sdk.init(
            dsn=config.SENTRY_DSN,
            integrations=[
                FlaskIntegration(),
                RqIntegration(),
            ],
            traces_sample_rate=config.SENTRY_SR,
            ignore_errors=[
                NoAuthorizationError,
                NotFound,
                Forbidden,
                ExpiredSignatureError,
            ],
        )

        if config.SENTRY_DEBUG_URL:

            @app.route(config.SENTRY_DEBUG_URL)
            def trigger_error():
                return 1 / 0

    if config.PROMETHEUS_METRICS_ENABLED:
        prometheus_kwargs = {
            "app": app,
            "defaults_prefix": "StudioPulse",
            "group_by": "url_rule",
        }
        try:
            metrics = prometheus_flask_exporter.multiprocess.GunicornPrometheusMetrics(
                **prometheus_kwargs
            )
        except ValueError:
            prometheus_kwargs["api"] = None
            prometheus_kwargs["metrics_decorator"] = (
                permissions.require_admin,
            )
            metrics = prometheus_flask_exporter.RESTfulPrometheusMetrics(
                **prometheus_kwargs
            )
        metrics.info("StudioPulse_info", "Application info", version=StudioPulse_version)
