"""
Presentation Layer: Flask Routes
Demonstrates API endpoint definitions in Domain-Driven Design.
"""

from flask import Blueprint, request, jsonify, session
from modules.karma_cafe.application.services.chat_service import ChatService
from modules.karma_cafe.domain.services.avatar_service import AvatarService

# Create blueprint
karma_blueprint = Blueprint('karma', __name__)

# Initialize services
chat_service = ChatService()
avatar_service = AvatarService()

@karma_blueprint.route('/avatars', methods=['GET'])
def get_avatars():
    """Get all available avatars."""
    try:
        avatars = avatar_service.get_all_avatars()
        return jsonify({
            'success': True,
            'avatars': avatars
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@karma_blueprint.route('/avatar/<avatar_id>', methods=['GET'])
def get_avatar(avatar_id):
    """Get details for a specific avatar."""
    try:
        avatar = avatar_service.get_avatar(avatar_id)
        if avatar:
            return jsonify({
                'success': True,
                'avatar': avatar
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Avatar not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@karma_blueprint.route('/send_message', methods=['POST'])
def send_message():
    """Send a message to an avatar and get a response."""
    try:
        data = request.get_json()
        avatar_id = data.get('avatar_id')
        message = data.get('message')
        
        if not avatar_id or not message:
            return jsonify({
                'success': False,
                'error': 'avatar_id and message are required'
            }), 400
        
        # Get conversation history from session
        conversation_key = f'karma_conversation_{avatar_id}'
        conversation_history = session.get(conversation_key, [])
        
        # Generate response
        response = chat_service.generate_response(
            avatar_id=avatar_id,
            user_message=message,
            conversation_history=conversation_history
        )
        
        # Update conversation history
        conversation_history.append({'role': 'user', 'content': message})
        conversation_history.append({'role': 'assistant', 'content': response})
        session[conversation_key] = conversation_history
        
        return jsonify({
            'success': True,
            'response': response,
            'conversation_history': conversation_history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@karma_blueprint.route('/new_conversation', methods=['POST'])
def new_conversation():
    """Start a new conversation with an avatar."""
    try:
        data = request.get_json()
        avatar_id = data.get('avatar_id')
        
        if not avatar_id:
            return jsonify({
                'success': False,
                'error': 'avatar_id is required'
            }), 400
        
        # Clear conversation history
        conversation_key = f'karma_conversation_{avatar_id}'
        session[conversation_key] = []
        
        return jsonify({
            'success': True,
            'message': 'New conversation started'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
