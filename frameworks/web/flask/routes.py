from flask import Blueprint, request, jsonify

# Blueprint cho User API
user_bp = Blueprint("user_api", __name__, url_prefix="/api/users")


def register_routes(app, user_controller):
    """
    Register all route blueprints to Flask app

    Args:
        app: Flask application instance
        user_controller: UserController instance
    """
    # Register user routes
    register_user_routes(user_bp, user_controller)
    app.register_blueprint(user_bp)

    # Register other route blueprints here as needed
    # Example: app.register_blueprint(auth_bp)


def register_user_routes(blueprint, user_controller):
    """
    Register routes for user API

    Args:
        blueprint: Flask Blueprint instance
        user_controller: UserController instance
    """

    @blueprint.route("", methods=["POST"])
    def register_user():
        """Register a new user"""
        response, status_code = user_controller.register_user(request.json)
        return jsonify(response), status_code

    @blueprint.route("", methods=["GET"])
    def list_users():
        """List all users"""
        response, status_code = user_controller.list_users()
        return jsonify(response), status_code

    @blueprint.route("/<user_id>", methods=["GET"])
    def get_user(user_id):
        """Get a specific user by ID"""
        response, status_code = user_controller.get_user(user_id)
        return jsonify(response), status_code

    @blueprint.route("/<user_id>", methods=["PUT"])
    def update_user(user_id):
        """Update a specific user"""
        response, status_code = user_controller.update_user(user_id, request.json)
        return jsonify(response), status_code

    @blueprint.route("/<user_id>", methods=["DELETE"])
    def delete_user(user_id):
        """Delete a specific user"""
        response, status_code = user_controller.delete_user(user_id)
        return jsonify(response), status_code
