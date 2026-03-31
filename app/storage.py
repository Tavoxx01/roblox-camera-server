"""
In-memory storage for camera frames and commands
"""

import threading
from datetime import datetime


class FrameStorage:
    """Thread-safe storage for camera frames"""
    
    def __init__(self):
        self._frame = None
        self._lock = threading.Lock()
    
    def set_frame(self, frame_data):
        """Store frame data"""
        with self._lock:
            self._frame = {
                'data': frame_data.get('frame'),
                'timestamp': frame_data.get('timestamp', datetime.now().isoformat()),
                'camera_position': frame_data.get('camera_position', {}),
                'camera_rotation': frame_data.get('camera_rotation', {})
            }
    
    def get_frame(self):
        """Get and clear frame data"""
        with self._lock:
            frame = self._frame
            self._frame = None  # Clear after retrieval
            return frame
    
    def has_frame(self):
        """Check if frame is available"""
        with self._lock:
            return self._frame is not None


class CommandStorage:
    """Thread-safe storage for camera commands"""
    
    def __init__(self):
        self._commands = {
            'pan_tilt_x': 0.0,
            'pan_tilt_y': 0.0,
            'move_x': 0.0,
            'move_z': 0.0,
        }
        self._lock = threading.Lock()
    
    def set_commands(self, commands):
        """Update command values"""
        with self._lock:
            for key in self._commands:
                if key in commands:
                    # Clamp values between -1.0 and 1.0
                    value = commands[key]
                    self._commands[key] = max(-1.0, min(1.0, float(value)))
    
    def get_commands(self):
        """Get current commands"""
        with self._lock:
            return self._commands.copy()
    
    def reset_commands(self):
        """Reset all commands to zero"""
        with self._lock:
            for key in self._commands:
                self._commands[key] = 0.0


# Global storage instances
frame_storage = FrameStorage()
command_storage = CommandStorage()
