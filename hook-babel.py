# Runtime hook to minimize babel locales - keep only English
import os
import sys

def minimize_babel_locales():
    """Keep only English locale data to reduce executable size"""
    try:
        import babel.localedata
        
        # Keep only English locale data
        original_load = babel.localedata.load
        
        def filtered_load(name, merge_inherited=True):
            # Only allow English locales
            if name in ['en', 'en_US', 'en_GB'] or name.startswith('en_'):
                return original_load(name, merge_inherited)
            else:
                # Return minimal data for other locales
                return {}
        
        babel.localedata.load = filtered_load
        
        # Clear existing cache except English
        if hasattr(babel.localedata, '_cache'):
            cache = babel.localedata._cache
            en_data = {k: v for k, v in cache.items() if k.startswith('en')}
            cache.clear()
            cache.update(en_data)
            
    except ImportError:
        pass  # babel not installed
    except Exception:
        pass  # Any other error, continue normally

# Execute the minimization
minimize_babel_locales()
