from .main import bp as main_bp
from .records import bp as records_bp

def register_blueprints(app):
    """將此資料夾下的所有 blueprints 註冊到 flask app 中"""
    app.register_blueprint(main_bp)
    app.register_blueprint(records_bp)
