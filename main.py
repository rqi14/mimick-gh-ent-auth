import logging
from flask import Flask, request, jsonify

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# In-memory store for tokens and user info
tokens = {
    "mock_access_token": {
        "user": {
            "login": "mock_user",
            "id": 123456,
            "node_id": "MDQ6VXNlcjE=",
            "avatar_url": "https://example.com/avatar.png",
            "gravatar_id": "",
            "url": "https://api.example.com/users/mock_user",
            "html_url": "https://example.com/mock_user",
            "followers_url": "https://api.example.com/users/mock_user/followers",
            "following_url": "https://api.example.com/users/mock_user/following{/other_user}",
            "gists_url": "https://api.example.com/users/mock_user/gists{/gist_id}",
            "starred_url": "https://api.example.com/users/mock_user/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.example.com/users/mock_user/subscriptions",
            "organizations_url": "https://api.example.com/users/mock_user/orgs",
            "repos_url": "https://api.example.com/users/mock_user/repos",
            "events_url": "https://api.example.com/users/mock_user/events{/privacy}",
            "received_events_url": "https://api.example.com/users/mock_user/received_events",
            "type": "User",
            "site_admin": False,
            "name": "Mock User",
            "company": "Example",
            "blog": "https://example.com/blog",
            "location": "Earth",
            "email": "mock_user@example.com",
            "hireable": True,
            "bio": "This is a mock user.",
            "twitter_username": "mockuser",
            "public_repos": 2,
            "public_gists": 1,
            "followers": 0,
            "following": 0,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    }
}

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

# Mock Device Authorization Endpoint
@app.route('/login/device/code', methods=['POST'])
def device_authorization():
    response = {
        "device_code": "mock_device_code",
        "user_code": "mock_user_code",
        "verification_uri": "http://localhost:5201/device",
        "verification_uri_complete": "http://localhost:5201/device?user_code=mock_user_code",
        "expires_in": 900,
        "interval": 5
    }
    return jsonify(response)

# Mock Verification URI Endpoint
@app.route('/device', methods=['GET'])
def device_verification():
    user_code = request.args.get('user_code', 'mock_user_code')
    return jsonify({"message": f"Enter the user code: {user_code}. Verification successful."})

# Mock Token Endpoint for POST requests
@app.route('/login/oauth/access_token', methods=['POST'])
def token():
    client_id = request.form.get('client_id')
    device_code = request.form.get('device_code')
    grant_type = request.form.get('grant_type')

    app.logger.debug(f'Client ID: {client_id}')
    app.logger.debug(f'Device Code: {device_code}')
    app.logger.debug(f'Grant Type: {grant_type}')

    if not client_id or not device_code or not grant_type:
        return jsonify({"error": "invalid_request"}), 400

    if device_code == "mock_device_code":
        return jsonify({
            "access_token": "mock_access_token",
            "token_type": "bearer",
            "expires_in": 3600,
            "refresh_token": "mock_refresh_token"
        }), 200
    else:
        return jsonify({"error": "invalid_grant"}), 400

# Mock GitHub User Endpoint
@app.route('/user', methods=['GET'])
def get_user():
    return jsonify({
        "id": 123456,
        "login": "mock_user"
    })


# Mock User Info Endpoint for GitHub Enterprise
@app.route('/api/v3/user', methods=['GET'])
def github_enterprise_user_info():
    auth_header = request.headers.get('Authorization')
    app.logger.debug(f'Authorization Header: {auth_header}')
    if not auth_header:
        return jsonify({"error": "missing_authorization_header"}), 401

    token = auth_header.split(' ')[1]
    user_info = tokens.get(token, {}).get("user", None)
    if user_info:
        return jsonify(user_info)
    else:
        return jsonify({"error": "User not authorized"}), 401

# Mock getaddrinfo Endpoint
@app.route('/getaddrinfo', methods=['GET'])
def getaddrinfo():
    hostname = request.args.get('hostname', 'localhost')
    response = {
        "hostname": hostname,
        "address": "127.0.0.1"
    }
    return jsonify(response)

# Mock Copilot Token Endpoint for GET requests
@app.route('/copilot_internal/v2/token', methods=['GET'])
def copilot_internal_token_get():
    response = {
        "token": "access_token=mock_access_token;token_type=bearer;expires_in=3600;refresh_token=mock_refresh_token",
        "user": {
            "id": "123456",
            "login": "mock_user",
            "name": "Mock User"
        },
        "expires_at": 3600,  # Add this field if it is required
        "refresh_in": 1800  # Add this field if it is required
    }
    return jsonify(response)

# Mock Copilot Token Endpoint for POST requests
@app.route('/copilot_internal/v2/token', methods=['POST'])
def copilot_internal_token_post():
    client_id = request.form.get('client_id')
    device_code = request.form.get('device_code')
    grant_type = request.form.get('grant_type')

    if not client_id or not device_code or not grant_type:
        return jsonify({"error": "invalid_request"}), 400

    if device_code == "mock_device_code":
        return jsonify({
            "token": "access_token=mock_access_token;token_type=bearer;expires_in=3600;refresh_token=mock_refresh_token",
            "user": {
                "id": "123456",
                "login": "mock_user",
                "name": "Mock User"
            },
            "expires_at": 3600,  # Add this field if it is required
            "refresh_in": 1800  # Add this field if it is required
        }), 200
    else:
        return jsonify({"error": "invalid_grant"}), 400
    
    
# Mock GitHub Enterprise Meta Endpoint
@app.route('/api/v3/meta', methods=['GET'])
def github_enterprise_meta():
    response = {
        "verifiable_password_authentication": False,
        "github_services_sha": "mock_sha",
        "installed_version": "mock_version"
    }
    return jsonify(response)

# Mock Telemetry Endpoint for POST requests
@app.route('/telemetry', methods=['POST'])
def telemetry_post():
    telemetry_data = request.get_json()
    print("Received telemetry data:", telemetry_data)
    return '', 200

if __name__ == '__main__':
    app.run(host='localhost', port=5201)
