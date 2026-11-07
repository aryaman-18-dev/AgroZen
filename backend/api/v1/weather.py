from flask import Blueprint, request, jsonify, current_app
from backend.services.weather_service import WeatherService
from auth_utils import token_required
import requests

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/banner', methods=['GET'])
def get_weather_banner():
    """Return current WeatherAPI data for the public homepage banner."""
    api_key = current_app.config.get('WEATHER_API_KEY')
    if not api_key:
        return jsonify({
            'status': 'error',
            'message': 'Weather service is not configured. Set WEATHER_API_KEY in .env.'
        }), 503

    location = (request.args.get('location') or 'Punjab, India').strip()
    if not location:
        return jsonify({'status': 'error', 'message': 'Location is required.'}), 400

    base_url = (current_app.config.get('WEATHER_API_URL') or 'https://api.weatherapi.com/v1').rstrip('/')
    try:
        response = requests.get(
            f'{base_url}/current.json',
            params={'key': api_key, 'q': location},
            timeout=10,
        )
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.Timeout:
        current_app.logger.warning('WeatherAPI request timed out for location %s', location)
        return jsonify({'status': 'error', 'message': 'Weather provider timed out. Please try again.'}), 504
    except requests.RequestException as exc:
        status_code = getattr(getattr(exc, 'response', None), 'status_code', None)
        current_app.logger.warning(
            'WeatherAPI request failed for location %s (status %s)', location, status_code
        )
        if status_code == 401:
            message = 'WeatherAPI rejected the key. Check WEATHER_API_KEY in .env.'
        elif status_code == 400:
            message = 'WeatherAPI could not find that location.'
        else:
            message = 'Weather provider is unavailable. Please try again later.'
        return jsonify({'status': 'error', 'message': message}), 502

@weather_bp.route('/current', methods=['GET'])
def get_weather():
    location = request.args.get('location')
    if not location:
        return jsonify({'status': 'error', 'message': 'Location required'}), 400
        
    weather = WeatherService.get_latest_weather(location)
    if not weather:
        return jsonify({'status': 'error', 'message': 'Could not fetch weather'}), 500
        
    return jsonify({
        'status': 'success',
        'data': weather.to_dict()
    }), 200

@weather_bp.route('/subscribe', methods=['POST'])
@token_required
def subscribe(current_user):
    data = request.get_json()
    if not data or 'crop_name' not in data or 'location' not in data:
        return jsonify({'status': 'error', 'message': 'Missing fields'}), 400
        
    sub = WeatherService.subscribe_user(
        user_id=current_user.id,
        crop_name=data['crop_name'],
        location=data['location'],
        soil_type=data.get('soil_type'),
        sowing_date=data.get('sowing_date')
    )
    
    return jsonify({
        'status': 'success',
        'message': 'Subscribed to automated advisories'
    }), 201
