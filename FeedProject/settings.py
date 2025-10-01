from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------
# Local defaults (Heroku code kept below but COMMENTED OUT)
# --------------------------------------------------------

# # Heroku detection (COMMENTED OUT)
# IS_HEROKU = bool(os.environ.get("DYNO") or os.environ.get("HEROKU_APP_NAME"))
# FORCE_HTTPS = os.environ.get("FORCE_HTTPS", "0") == "1"
# HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-unsafe-secret-key-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1" 

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# # CSRF trusted origins for Heroku (COMMENTED OUT)
# CSRF_TRUSTED_ORIGINS = []
# if HEROKU_APP_NAME:
#     CSRF_TRUSTED_ORIGINS.append(f"https://{HEROKU_APP_NAME}.herokuapp.com")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "feed",
    "crispy_forms",
    "crispy_bootstrap5",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # # Whitenoise for prod (COMMENTED OUT for local-only)
    # "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "FeedProject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "FeedProject.wsgi.application"
ASGI_APPLICATION = "FeedProject.asgi.application"

# ---------- Database (LOCAL: SQLite only) ----------
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
}

# # Heroku DATABASE_URL override (COMMENTED OUT)
# if os.environ.get("DATABASE_URL"):
#     import dj_database_url
#     DATABASES["default"] = dj_database_url.config(
#         conn_max_age=600,
#         ssl_require=True,
#         default=os.environ["DATABASE_URL"],
#     )

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = os.environ.get("TIME_ZONE", "America/Chicago")
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # harmless locally
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# # Whitenoise storages (COMMENTED OUT)
# STORAGES = {
#     "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
#     "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
# }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# ---------- HTTPS settings (LOCAL: always HTTP) ----------
SECURE_PROXY_SSL_HEADER = None
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# # Heroku proxy/header & conditional HTTPS (COMMENTED OUT)
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# if not DEBUG:
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
# else:
#     SECURE_SSL_REDIRECT = False
#     SESSION_COOKIE_SECURE = False
#     CSRF_COOKIE_SECURE = False
