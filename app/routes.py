"""
API routes for Roblox Camera Server
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from app.auth import require_roblox_token, require_frontend_token
from app.storage import frame_storage, command_storage

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200


@api_bp.route('/status', methods=['GET'])
@require_roblox_token
def status():
    """Get system status"""
    return jsonify({
        'has_frame': frame_storage.has_frame(),
        'commands': command_storage.get_commands(),
        'timestamp': datetime.now().isoformat()
    }), 200


@api_bp.route('/frame/upload', methods=['POST'])
@require_roblox_token
def upload_frame():
    """
    Receive frame from Roblox
    
    Expected JSON:
    {
        "frame": "base64_encoded_image",
        "timestamp": "2024-01-01T12:00:00Z",
        "camera_position": {"x": 0, "y": 5, "z": 0},
        "camera_rotation": {"x": 0, "y": 0, "z": 0}
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'frame' not in data:
            return jsonify({'error': 'Missing frame data'}), 400
        
        # Check frame size
        frame_size = len(data['frame'])
        if frame_size > current_app.config['MAX_FRAME_SIZE']:
            return jsonify({'error': 'Frame too large'}), 413
        
        # Store frame
        frame_storage.set_frame(data)
        
        # Return current commands
        return jsonify({
            'status': 'received',
            'commands': command_storage.get_commands()
        }), 200
    
    except Exception as e:
        current_app.logger.error(f'Error uploading frame: {e}')
        return jsonify({'error': 'Internal server error'}), 500


@api_bp.route('/frame/get', methods=['GET'])
@require_frontend_token
def get_frame():
    """
    Get current frame (Frontend)
    Frame is deleted after retrieval
    """
    try:
        frame = frame_storage.get_frame()
        
        if frame is None:
            return jsonify({'frame': None}), 200
        
        return jsonify(frame), 200
    
    except Exception as e:
        current_app.logger.error(f'Error getting frame: {e}')
        return jsonify({'error': 'Internal server error'}), 500


@api_bp.route('/commands/set', methods=['POST'])
@require_frontend_token
def set_commands():
    """
    Set camera control commands (Frontend)
    
    Expected JSON:
    {
        "pan_tilt_x": -1.0 to 1.0,
        "pan_tilt_y": -1.0 to 1.0,
        "move_x": -1.0 to 1.0,
        "move_z": -1.0 to 1.0
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Missing command data'}), 400
        
        # Update commands
        command_storage.set_commands(data)
        
        return jsonify({'status': 'ok'}), 200
    
    except Exception as e:
        current_app.logger.error(f'Error setting commands: {e}')
        return jsonify({'error': 'Internal server error'}), 500


@api_bp.route('/commands/get', methods=['GET'])
@require_roblox_token
def get_commands():
    """
    Get current camera control commands (Roblox)
    """
    try:
        commands = command_storage.get_commands()
        return jsonify(commands), 200
    
    except Exception as e:
        current_app.logger.error(f'Error getting commands: {e}')
        return jsonify({'error': 'Internal server error'}), 500


@api_bp.route('/commands/reset', methods=['POST'])
@require_frontend_token
def reset_commands():
    """
    Reset all commands to zero
    """
    try:
        command_storage.reset_commands()
        return jsonify({'status': 'ok'}), 200
    
    except Exception as e:
        current_app.logger.error(f'Error resetting commands: {e}')
        return jsonify({'error': 'Internal server error'}), 500
