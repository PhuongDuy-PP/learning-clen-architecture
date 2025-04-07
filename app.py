from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from frameworks.container import Container
from frameworks.database.database import init_db, get_db
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from asgiref.wsgi import WsgiToAsgi
from frameworks.logging.logger import FileLogger
from application.validators.user_validator import UserValidator
from tests.mocks import MockLogger, MockValidator
import os
import logging
import signal
import socket

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            return False
        except socket.error:
            return True

async def create_app(testing=False):
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    CORS(app)
    
    logger.debug("Creating Flask application")
    container = Container()
    
    # Configure container based on environment
    if testing:
        container.logger.override(MockLogger())
        container.user_validator.override(MockValidator())
    else:
        container.logger.override(FileLogger(name="clean_architecture", log_file="app.log"))
        container.user_validator.override(UserValidator())

    # Initialize resources and get user controller
    logger.debug("Initializing resources")
    await container.init_resources()
    logger.debug("Initializing database")
    await init_db()
    logger.debug("Getting user controller")
    user_controller = await container.user_controller()
    logger.debug("Initialization complete")

    @app.route('/api/users/register', methods=['POST'])
    async def register_user():
        logger.debug("Received register user request")
        try:
            data = request.get_json()
            logger.debug(f"Request data: {data}")
            result, status_code = await user_controller.register_user(data)
            logger.debug(f"Register result: {result}")
            return jsonify(result), status_code
        except Exception as e:
            logger.error(f"Error in register_user: {str(e)}", exc_info=True)
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/users', methods=['GET'])
    async def list_users():
        logger.debug("Received list users request")
        try:
            result, status_code = await user_controller.list_users()
            logger.debug(f"List users result: {result}")
            return jsonify(result), status_code
        except Exception as e:
            logger.error(f"Error in list_users: {str(e)}", exc_info=True)
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/users/<user_id>', methods=['GET'])
    async def get_user(user_id):
        logger.debug(f"Received get user request for id: {user_id}")
        try:
            result, status_code = await user_controller.get_user(user_id)
            logger.debug(f"Get user result: {result}")
            return jsonify(result), status_code
        except Exception as e:
            logger.error(f"Error in get_user: {str(e)}", exc_info=True)
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/users/<user_id>', methods=['PUT'])
    async def update_user(user_id):
        logger.debug(f"Received update user request for id: {user_id}")
        try:
            data = request.get_json()
            logger.debug(f"Update data: {data}")
            result, status_code = await user_controller.update_user(user_id, data)
            logger.debug(f"Update result: {result}")
            return jsonify(result), status_code
        except Exception as e:
            logger.error(f"Error in update_user: {str(e)}", exc_info=True)
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/users/<user_id>', methods=['DELETE'])
    async def delete_user(user_id):
        logger.debug(f"Received delete user request for id: {user_id}")
        try:
            result, status_code = await user_controller.delete_user(user_id)
            logger.debug(f"Delete result: {result}")
            return jsonify(result), status_code
        except Exception as e:
            logger.error(f"Error in delete_user: {str(e)}", exc_info=True)
            return jsonify({"success": False, "error": str(e)}), 500

    # Register Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Clean Architecture API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    logger.debug("Swagger UI registered")

    return app

async def cleanup():
    logger.debug("Cleaning up resources")
    try:
        async for db in get_db():
            await db.close()
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
    logger.debug("Cleanup complete")

async def main():
    logger.debug("Starting application")
    app = await create_app()
    config = Config()
    
    # Find an available port starting from 5001
    port = 5001
    while is_port_in_use(port):
        port += 1
    config.bind = [f"0.0.0.0:{port}"]
    
    logger.debug(f"Server configured, starting on port {port}...")

    # Set up signal handlers
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(cleanup()))

    try:
        await serve(WsgiToAsgi(app), config)
    finally:
        await cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 