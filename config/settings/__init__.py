import os


settings_profile = os.environ.get("DJANGO_ENV", "").lower()
running_on_railway = bool(os.environ.get("RAILWAY_ENVIRONMENT"))

if settings_profile in {"prod", "production"} or running_on_railway:
    from .prod import *  # noqa: F401,F403
else:
    from .dev import *  # noqa: F401,F403
