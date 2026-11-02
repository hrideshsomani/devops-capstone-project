"""
REST API Routes for Customer Accounts Service
"""
import logging
from flask import jsonify, request, make_response, abort, url_for
from service.models import Account, DataValidationError
from service import app

logger = logging.getLogger("flask.app")

BASE_URL = "/accounts"


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status."""
    return jsonify({"status": "OK"}), 200


############################################################
# Home Page
############################################################
@app.route("/")
def index():
    """Root URL response."""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            paths=url_for("list_accounts", _external=True),
        ),
        200,
    )


############################################################
# CREATE an Account
############################################################
@app.route(BASE_URL, methods=["POST"])
def create_accounts():
    """Create an Account."""
    logger.info("Request to Create an Account")
    check_content_type("application/json")

    account = Account()
    account.deserialize(request.get_json())
    account.create()

    location_url = url_for("get_accounts", account_id=account.id, _external=True)
    return (
        jsonify(account.serialize()),
        201,
        {"Location": location_url},
    )


############################################################
# LIST all Accounts
############################################################
@app.route(BASE_URL, methods=["GET"])
def list_accounts():
    """Returns all Accounts."""
    logger.info("Request to list Accounts")
    accounts = Account.all()
    account_list = [account.serialize() for account in accounts]
    logger.info("Returning %d accounts", len(account_list))
    return jsonify(account_list), 200


############################################################
# READ an Account
############################################################
@app.route(f"{BASE_URL}/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """Reads an Account."""
    logger.info("Request to Read an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(404, f"Account with id [{account_id}] could not be found.")
    return jsonify(account.serialize()), 200


############################################################
# UPDATE an Account
############################################################
@app.route(f"{BASE_URL}/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """Update an Account."""
    logger.info("Request to Update an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(404, f"Account with id [{account_id}] could not be found.")

    account.deserialize(request.get_json())
    account.id = account_id
    account.update()
    return jsonify(account.serialize()), 200


############################################################
# DELETE an Account
############################################################
@app.route(f"{BASE_URL}/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """Delete an Account."""
    logger.info("Request to Delete an Account with id: %s", account_id)
    account = Account.find(account_id)
    if account:
        account.delete()
    return make_response("", 204)


############################################################
# Utility functions
############################################################
def check_content_type(media_type):
    """Checks that the media type is correct."""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    logger.error("Invalid Content-Type: %s", content_type)
    abort(
        415,
        f"Content-Type must be {media_type}",
    )


@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """Handles Value Errors from bad data."""
    return bad_request(error)


@app.errorhandler(400)
def bad_request(error):
    """Handle Bad Request (400)."""
    logger.warning(str(error))
    return (
        jsonify(
            status=400,
            error="Bad Request",
            message=str(error),
        ),
        400,
    )


@app.errorhandler(404)
def not_found(error):
    """Handle Not Found (404)."""
    logger.warning(str(error))
    return (
        jsonify(
            status=404,
            error="Not Found",
            message=str(error),
        ),
        404,
    )


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle Method Not Allowed (405)."""
    return (
        jsonify(
            status=405,
            error="Method Not Allowed",
            message=str(error),
        ),
        405,
    )


@app.errorhandler(415)
def mediatype_not_supported(error):
    """Handle Unsupported Media Type (415)."""
    logger.warning(str(error))
    return (
        jsonify(
            status=415,
            error="Unsupported media type",
            message=str(error),
        ),
        415,
    )


@app.errorhandler(500)
def internal_server_error(error):
    """Handle Internal Server Error (500)."""
    logger.error(str(error))
    return (
        jsonify(
            status=500,
            error="Internal Server Error",
            message=str(error),
        ),
        500,
    )
