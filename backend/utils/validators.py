import os
import mimetypes
from typing import List, Optional

# `python-magic` loads a native libmagic DLL. On some Windows setups that DLL
# crashes the entire Python process during import (it cannot be caught as an
# exception), so use the standard-library MIME map there.
if os.name == "nt":
    magic = None
else:
    try:
        import magic
    except (ImportError, OSError):
        magic = None

class DataIntegrityValidator:
    """
    Utility for validating file types, sizes, and structure across the platform.
    """
    
    ALLOWED_EXTENSIONS = {
        'DISEASE': ['.jpg', '.jpeg', '.png'],
        'SOIL': ['.jpg', '.jpeg', '.png', '.csv', '.json'],
        'CROP': ['.jpg', '.jpeg', '.png', '.csv'],
        'EQUIPMENT': ['.jpg', '.jpeg', '.png', '.pdf']
    }
    
    # 10 MB limit as default
    MAX_FILE_SIZE = 10 * 1024 * 1024 

    @staticmethod
    def validate_file(file_path: str, payload_type: str) -> (bool, Optional[str]):
        """
        Validates file existence, size, extension, and MIME type.
        """
        if not os.path.exists(file_path):
            return False, "File does not exist"
            
        # Size check
        size = os.path.getsize(file_path)
        if size > DataIntegrityValidator.MAX_FILE_SIZE:
            return False, f"File size ({size} bytes) exceeds limit"
            
        # Extension check
        ext = os.path.splitext(file_path)[1].lower()
        allowed = DataIntegrityValidator.ALLOWED_EXTENSIONS.get(payload_type, [])
        if ext not in allowed:
            return False, f"Extension {ext} not allowed for {payload_type}"
            
        # MIME type deep check
        try:
            mime = None
            if magic:
                try:
                    mime = magic.from_file(file_path, mime=True)
                except (ImportError, OSError):
                    # Fall back when libmagic itself is unavailable.
                    pass
            if not mime:
                mime, _ = mimetypes.guess_type(file_path)
            if not mime:
                return False, "Unable to determine MIME type"
            if payload_type in ['DISEASE', 'SOIL', 'CROP'] and 'image' in mime:
                return True, None
            if payload_type == 'EQUIPMENT' and ('image' in mime or 'pdf' in mime):
                return True, None
            if payload_type in ['SOIL', 'CROP'] and ('text' in mime or 'json' in mime or 'csv' in mime):
                return True, None
        except Exception as e:
            return False, f"MIME validation failed: {str(e)}"
            
        return False, f"MIME type {mime} mismatch for {payload_type}"

    @staticmethod
    def validate_metadata(metadata: dict, payload_type: str) -> (bool, Optional[str]):
        """
        Checks for required fields based on payload type.
        """
        required_fields = {
            'DISEASE': ['crop_name'],
            'SOIL': ['location_lat', 'location_lon'],
            'CROP': ['variety']
        }
        
        needed = required_fields.get(payload_type, [])
        for field in needed:
            if field not in metadata:
                return False, f"Missing required metadata: {field}"
                
        return True, None
