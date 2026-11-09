translations = {
    'en': {
        'welcome': 'Welcome to AgroZen',
        'dashboard': 'Dashboard',
    },
    'hi': {
        'welcome': 'AgroZen me svagat hai',
        'dashboard': 'Dashboard',
    }
}

def get_translation(lang, key):
    return translations.get(lang, {}).get(key, translations['en'].get(key, key))

