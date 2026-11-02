"""
Service Package Initialization
Configures Flask app with Talisman security headers and CORS policies.
"""
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)

# Configure Talisman for security headers
talisman = Talisman(
    app,
    force_https=False,  # Set True in production
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,
    content_security_policy={
        "default-src": "'self'",
        "style-src": "'self'",
        "script-src": "'self'",
    },
    referrer_policy="strict-origin-when-cross-origin",
    feature_policy={
        "geolocation": "'none'",
        "microphone": "'none'",
        "camera": "'none'",
    },
    x_content_type_options=True,
    x_xss_protection=True,
    x_frame_options="SAMEORIGIN",
)

# Configure CORS
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
)

# Import routes after app is created to avoid circular imports
from service import routes, models  # noqa: F401, E402
