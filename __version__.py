"""
Version information for CMS Application
Generated at build time: 2025-07-31 10:11:00
"""

# Version information
__version__ = "1.0.0"
__build_timestamp__ = "2025-07-31 10:11:00"
__build_date__ = "20250731"

# Combined version string for display
VERSION_STRING = f"{__version__}.{__build_date__}"
FULL_VERSION_INFO = f"CMS v{__version__} (Build: {__build_timestamp__})"

def get_version():
    """Return the version string"""
    return VERSION_STRING

def get_full_version():
    """Return the full version info with timestamp"""
    return FULL_VERSION_INFO

def get_build_info():
    """Return build information"""
    return {
        'version': __version__,
        'build_timestamp': __build_timestamp__,
        'build_date': __build_date__,
        'version_string': VERSION_STRING
    }
