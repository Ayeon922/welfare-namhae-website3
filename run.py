#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
노인 복지 추천 플랫폼 실행 스크립트

사용법:
    python run.py              # 개발 환경으로 실행
    python run.py --prod       # 운영 환경으로 실행
    python run.py --test       # 테스트 환경으로 실행
"""

import os
import sys
import argparse
from app import app, db, init_sample_data, logger

def create_directories():
    """필요한 디렉터리 생성"""
    directories = [
        'instance',
        'instance/sessions',
        'uploads',
        'logs'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"디렉터리 생성: {directory}")

def setup_database():
    """데이터베이스 초기화"""
    try:
        with app.app_context():
            db.create_all()
            init_sample_data()
            logger.info("데이터베이스 초기화 완료")
    except Exception as e:
        logger.error(f"데이터베이스 초기화 오류: {str(e)}")
        sys.exit(1)

def check_dependencies():
    """필수 패키지 확인"""
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'openai',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"다음 패키지가 설치되지 않았습니다: {', '.join(missing_packages)}")
        logger.error("pip install -r requirements.txt 명령어로 패키지를 설치하세요.")
        sys.exit(1)

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='노인 복지 추천 플랫폼')
    parser.add_argument('--prod', action='store_true', help='운영 환경으로 실행')
    parser.add_argument('--test', action='store_true', help='테스트 환경으로 실행')
    parser.add_argument('--host', default='127.0.0.1', help='호스트 주소 (기본값: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='포트 번호 (기본값: 5000)')
    parser.add_argument('--debug', action='store_true', help='디버그 모드 활성화')
    
    args = parser.parse_args()
    
    # 환경 설정
    if args.prod:
        os.environ['FLASK_ENV'] = 'production'
        debug = False
    elif args.test:
        os.environ['FLASK_ENV'] = 'testing'
        debug = False
    else:
        os.environ['FLASK_ENV'] = 'development'
        debug = True
    
    if args.debug:
        debug = True
    
    # 의존성 확인
    check_dependencies()
    
    # 디렉터리 생성
    create_directories()
    
    # 데이터베이스 초기화
    setup_database()
    
    # 시작 메시지
    logger.info(f"노인 복지 추천 플랫폼 시작")
    logger.info(f"환경: {os.environ.get('FLASK_ENV', 'development')}")
    logger.info(f"주소: http://{args.host}:{args.port}")
    logger.info(f"디버그 모드: {debug}")
    
    # 애플리케이션 실행
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=debug,
            use_reloader=debug,
            threaded=True
        )
    except KeyboardInterrupt:
        logger.info("애플리케이션 종료됨")
    except Exception as e:
        logger.error(f"애플리케이션 실행 오류: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 