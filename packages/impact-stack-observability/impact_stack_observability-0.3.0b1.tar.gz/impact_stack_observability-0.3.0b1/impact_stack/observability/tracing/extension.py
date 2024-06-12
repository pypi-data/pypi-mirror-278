"""Tracing extension for Flask.

Features

- Reads tracing related config from the app config
- Does nothing if `TRACING_ENABLED` is `False` (default: `True`)
- Creates a new tracer provider (global by default) and it's resource
  via detectors and attributes (given as argument and configured)
- Or: uses the provided tracer provider (not creating or updating a new resource)
- Finally: autoinstruments the app

Configuration keys:

- `TRACING_ENABLED` (default: `True`)
- `TRACING_INSTRUMENTORS` (default: `None`, means all instrumentors found are used)
- `TRACING_RESOURCE_ATTRIBUTES` (default: `{}`)
"""

import logging

from . import utils

logger = logging.getLogger("impact_stack.observability")


class Tracing:
    """Tracing extension."""

    # pylint: disable=too-few-public-methods

    def __init__(self, app=None):
        """Initialize the extension."""
        self.tracer_provider = None

        if app is not None:
            self.init_app(app)

    def init_app(
        self,
        app,
        resource_attributes=None,
        resource_detectors=None,
        tracer_provider=None,
        set_global_tracer_provider=True,
    ):
        """Initialize a Flask application for use with this extension instance.

        This starts the tracing.

        Resource detectors need to be already intialized.
        """
        # pylint: disable=too-many-arguments
        if "tracing" in app.extensions:
            raise RuntimeError(
                "A 'Tracing' instance has already been registered on this Flask app."
            )
        app.extensions["tracing"] = self

        if not app.config.get("TRACING_ENABLED", True):
            app.logger.info("Tracing disabled")
            return

        attributes = resource_attributes or {}
        instrumentors = app.config.get("TRACING_INSTRUMENTORS", None)
        app_attributes = app.config.get("TRACING_RESOURCE_ATTRIBUTES", {})

        self.tracer_provider = utils.init_tracing(
            resource_detectors=resource_detectors,
            attributes=attributes | app_attributes,
            tracer_provider=tracer_provider,
            set_global_tracer_provider=set_global_tracer_provider,
        )

        loaded_instrumentors = utils.autoinstrument_app(
            app, instrumentors=instrumentors, tracer_provider=self.tracer_provider
        )

        app.logger.info(
            "Tracing started",
            extra={
                "instrumentors": list(loaded_instrumentors.keys()),
                "resource_attributes": self.tracer_provider.resource.attributes,
            },
        )
