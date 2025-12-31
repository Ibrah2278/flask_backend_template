from .auth_routes import admin_auth

def register_blueprints(app):
    app.register_blueprint(admin_auth)
