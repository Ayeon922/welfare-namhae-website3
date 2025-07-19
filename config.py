import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class Config:
    """기본 설정"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///welfare.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # OpenAI API 설정
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # 세션 설정
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_FILE_DIR = 'instance/sessions'
    
    # 보안 설정
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # 업로드 설정
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # 로깅 설정
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or 'welfare_platform.log'
    
    # 캐시 설정
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # 레이트 리미팅 설정
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_DEFAULT = '100/hour'
    
    # 데이터베이스 연결 풀 설정
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0
    }

class DevelopmentConfig(Config):
    """개발 환경 설정"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    LOG_LEVEL = 'DEBUG'
    
    # 개발 환경에서는 더 관대한 설정
    RATELIMIT_DEFAULT = '1000/hour'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """운영 환경 설정"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # 운영 환경에서는 더 엄격한 설정
    RATELIMIT_DEFAULT = '50/hour'
    WTF_CSRF_ENABLED = True
    
    # 보안 강화
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # PostgreSQL 설정 (운영 환경)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@localhost/welfare_db'

class TestingConfig(Config):
    """테스트 환경 설정"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# 환경별 설정 매핑
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """현재 환경에 맞는 설정 반환"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default']) 