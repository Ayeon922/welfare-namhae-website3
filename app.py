from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import openai
import json
import uuid
import re
from werkzeug.utils import secure_filename
import logging
from functools import wraps
import sqlite3

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///welfare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# OpenAI API 설정
openai.api_key = os.getenv('OPENAI_API_KEY')

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 데이터베이스 모델
class WelfareProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    target_age = db.Column(db.String(50))
    target_condition = db.Column(db.String(200))
    benefit_amount = db.Column(db.String(100))
    application_method = db.Column(db.Text)
    contact_info = db.Column(db.String(200))
    category = db.Column(db.String(100))
    region = db.Column(db.String(100))
    priority = db.Column(db.Integer, default=1)
    deadline = db.Column(db.String(100))
    website_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'target_age': self.target_age,
            'target_condition': self.target_condition,
            'benefit_amount': self.benefit_amount,
            'application_method': self.application_method,
            'contact_info': self.contact_info,
            'category': self.category,
            'region': self.region,
            'priority': self.priority,
            'deadline': self.deadline,
            'website_url': self.website_url
        }

class UserResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    birth_date = db.Column(db.String(20))
    region = db.Column(db.String(100))
    sub_region = db.Column(db.String(100))
    medical_conditions = db.Column(db.Text)
    living_situation = db.Column(db.Text)
    income_level = db.Column(db.String(50))
    disability_status = db.Column(db.String(50))
    family_size = db.Column(db.Integer)
    employment_status = db.Column(db.String(50))
    housing_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WelfareCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300))
    phone = db.Column(db.String(50))
    region = db.Column(db.String(100))
    sub_region = db.Column(db.String(100))
    services = db.Column(db.Text)
    operating_hours = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

def init_sample_data():
    """확장된 샘플 복지 프로그램 데이터 초기화"""
    sample_programs = [
        {
            'name': '기초연금',
            'description': '65세 이상 노인에게 매월 지급하는 기초연금으로 노후생활 안정을 도모',
            'target_age': '65세 이상',
            'target_condition': '소득 하위 70%',
            'benefit_amount': '월 최대 334,810원 (2024년 기준)',
            'application_method': '국민연금공단 또는 주민센터 방문 신청, 온라인 신청 가능',
            'contact_info': '국민연금공단 1355',
            'category': '생활비 지원',
            'region': '전국',
            'priority': 1,
            'deadline': '상시 접수',
            'website_url': 'https://www.nps.or.kr'
        },
        {
            'name': '노인 장기요양보험',
            'description': '일상생활이 어려운 노인에게 요양 서비스를 제공하여 독립적인 생활 지원',
            'target_age': '65세 이상',
            'target_condition': '장기요양 등급 판정 필요',
            'benefit_amount': '본인부담금 15-20%',
            'application_method': '국민건강보험공단 신청, 등급 판정 후 서비스 이용',
            'contact_info': '국민건강보험공단 1577-1000',
            'category': '의료/돌봄 지원',
            'region': '전국',
            'priority': 2,
            'deadline': '상시 접수',
            'website_url': 'https://www.longtermcare.or.kr'
        },
        {
            'name': '노인 의료비 지원',
            'description': '저소득 노인의 의료비 부담을 덜어주는 지원 프로그램',
            'target_age': '65세 이상',
            'target_condition': '기초생활수급자, 차상위계층',
            'benefit_amount': '의료비 80-100% 지원',
            'application_method': '보건소 또는 주민센터 신청',
            'contact_info': '보건복지부 129',
            'category': '의료/돌봄 지원',
            'region': '전국',
            'priority': 1,
            'deadline': '상시 접수',
            'website_url': 'https://www.mohw.go.kr'
        },
        {
            'name': '독거노인 생활관리사 파견',
            'description': '독거노인의 안전 확인과 생활 지원을 위한 생활관리사 파견 서비스',
            'target_age': '65세 이상',
            'target_condition': '독거노인, 기초생활수급자 우선',
            'benefit_amount': '무료 서비스',
            'application_method': '주민센터 또는 노인복지관 신청',
            'contact_info': '지역 노인복지관',
            'category': '생활 지원',
            'region': '전국',
            'priority': 2,
            'deadline': '상시 접수',
            'website_url': 'https://www.mohw.go.kr'
        },
        {
            'name': '노인 일자리 사업',
            'description': '노인 대상 일자리 제공으로 활기찬 노후생활과 소득 보장',
            'target_age': '65세 이상',
            'target_condition': '건강상태 양호, 근로 의지가 있는 노인',
            'benefit_amount': '월 27만원 내외',
            'application_method': '노인일자리 전담기관 신청',
            'contact_info': '보건복지부 129',
            'category': '고용 지원',
            'region': '전국',
            'priority': 3,
            'deadline': '연중 수시 모집',
            'website_url': 'https://www.seniorswork.or.kr'
        },
        {
            'name': '치매 전담형 장기요양기관',
            'description': '치매 어르신을 위한 전문적인 돌봄 서비스',
            'target_age': '65세 이상',
            'target_condition': '치매 진단, 장기요양 등급 보유',
            'benefit_amount': '본인부담금 10-20%',
            'application_method': '국민건강보험공단 신청',
            'contact_info': '국민건강보험공단 1577-1000',
            'category': '의료/돌봄 지원',
            'region': '전국',
            'priority': 1,
            'deadline': '상시 접수',
            'website_url': 'https://www.longtermcare.or.kr'
        },
        {
            'name': '노인 건강관리 서비스',
            'description': '맞춤형 건강관리 서비스로 건강한 노후생활 지원',
            'target_age': '65세 이상',
            'target_condition': '건강위험요인 보유자',
            'benefit_amount': '무료 또는 저렴한 비용',
            'application_method': '보건소 신청',
            'contact_info': '지역 보건소',
            'category': '의료/돌봄 지원',
            'region': '전국',
            'priority': 3,
            'deadline': '상시 접수',
            'website_url': 'https://www.mohw.go.kr'
        },
        {
            'name': '노인 교통비 지원',
            'description': '대중교통 이용 시 요금 할인 혜택',
            'target_age': '65세 이상',
            'target_condition': '거주지 기준',
            'benefit_amount': '지역별 차등 지원',
            'application_method': '지자체 또는 교통카드 회사 신청',
            'contact_info': '지역 교통공단',
            'category': '생활 지원',
            'region': '전국',
            'priority': 3,
            'deadline': '상시 접수',
            'website_url': 'https://www.sisul.or.kr'
        },
        {
            'name': '주거급여',
            'description': '저소득층 노인의 주거비 부담 완화를 위한 지원',
            'target_age': '제한 없음',
            'target_condition': '기준 중위소득 47% 이하',
            'benefit_amount': '월 최대 32만원',
            'application_method': '주민센터 신청',
            'contact_info': '보건복지부 129',
            'category': '주거 지원',
            'region': '전국',
            'priority': 2,
            'deadline': '상시 접수',
            'website_url': 'https://www.mohw.go.kr'
        },
        {
            'name': '노인 무료 급식 서비스',
            'description': '저소득 노인을 위한 무료 급식 서비스',
            'target_age': '65세 이상',
            'target_condition': '기초생활수급자, 차상위계층',
            'benefit_amount': '무료 급식 제공',
            'application_method': '복지관 또는 급식소 신청',
            'contact_info': '지역 노인복지관',
            'category': '생활 지원',
            'region': '전국',
            'priority': 2,
            'deadline': '상시 접수',
            'website_url': 'https://www.mohw.go.kr'
        }
    ]
    
    # 복지센터 데이터
    sample_centers = [
        {
            'name': '서울시 노인복지관',
            'address': '서울시 중구 을지로 100',
            'phone': '02-1234-5678',
            'region': '서울',
            'sub_region': '중구',
            'services': '상담, 급식, 건강관리, 여가활동',
            'operating_hours': '평일 09:00-18:00'
        },
        {
            'name': '부산시 노인복지관',
            'address': '부산시 해운대구 센텀로 200',
            'phone': '051-1234-5678',
            'region': '부산',
            'sub_region': '해운대구',
            'services': '상담, 급식, 건강관리, 여가활동',
            'operating_hours': '평일 09:00-18:00'
        }
    ]
    
    # 데이터베이스에 샘플 데이터 추가
    for program_data in sample_programs:
        existing = WelfareProgram.query.filter_by(name=program_data['name']).first()
        if not existing:
            program = WelfareProgram(**program_data)
            db.session.add(program)
    
    for center_data in sample_centers:
        existing = WelfareCenter.query.filter_by(name=center_data['name']).first()
        if not existing:
            center = WelfareCenter(**center_data)
            db.session.add(center)
    
    db.session.commit()
    logger.info("샘플 데이터 초기화 완료")

def validate_user_input(data):
    """사용자 입력 데이터 검증"""
    errors = []
    
    # 나이 검증
    try:
        age = int(data.get('age', 0))
        if age < 0 or age > 120:
            errors.append('나이는 0-120 사이여야 합니다.')
    except ValueError:
        errors.append('나이는 숫자여야 합니다.')
    
    # 이름 검증
    name = data.get('name', '').strip()
    if not name or len(name) < 2:
        errors.append('이름은 2자 이상이어야 합니다.')
    
    # 생년월일 검증
    birth_date = data.get('birth_date', '')
    if birth_date:
        try:
            datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError:
            errors.append('생년월일 형식이 올바르지 않습니다.')
    
    return errors

def get_ai_recommendations(user_data):
    """개선된 AI 추천 시스템"""
    try:
        # 사용자 데이터 검증
        validation_errors = validate_user_input(user_data)
        if validation_errors:
            logger.warning(f"사용자 데이터 검증 오류: {validation_errors}")
        
        # OpenAI API를 사용한 추천
        ai_recommendation = "기본 추천 시스템을 사용합니다."
        
        if openai.api_key:
            try:
                prompt = f"""
                다음 사용자 정보를 바탕으로 가장 적합한 복지 프로그램을 추천해주세요:
                
                기본 정보:
                - 나이: {user_data.get('age')}세
                - 거주지역: {user_data.get('region')} {user_data.get('sub_region', '')}
                - 가족구성: {user_data.get('family_size', 1)}명
                
                상태 정보:
                - 의료상태: {user_data.get('medical_conditions')}
                - 생활상황: {user_data.get('living_situation')}
                - 소득수준: {user_data.get('income_level')}
                - 장애여부: {user_data.get('disability_status')}
                - 고용상태: {user_data.get('employment_status')}
                - 주거형태: {user_data.get('housing_type')}
                
                추천 시 고려사항:
                1. 긴급성과 우선순위
                2. 신청 가능성
                3. 혜택 규모
                4. 접근성
                
                간단하고 이해하기 쉽게 설명해주세요.
                """
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "당신은 노인 복지 전문가입니다. 사용자의 상황에 맞는 복지 프로그램을 추천하고 친절하게 설명해주세요."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                
                ai_recommendation = response.choices[0].message.content
                logger.info("AI 추천 완료")
                
            except Exception as e:
                logger.error(f"OpenAI API 오류: {str(e)}")
                ai_recommendation = "AI 추천 서비스가 일시적으로 이용 불가합니다. 기본 추천을 제공합니다."
        
        # 향상된 매칭 로직
        programs = WelfareProgram.query.all()
        matched_programs = []
        
        for program in programs:
            score = calculate_matching_score(user_data, program)
            
            if score > 0:
                matched_programs.append({
                    'program': program,
                    'score': score,
                    'recommendation_reason': ai_recommendation,
                    'match_details': get_match_details(user_data, program)
                })
        
        # 점수순으로 정렬
        matched_programs.sort(key=lambda x: x['score'], reverse=True)
        
        return matched_programs[:8]  # 상위 8개 프로그램 반환
        
    except Exception as e:
        logger.error(f"추천 시스템 오류: {str(e)}")
        return []

def calculate_matching_score(user_data, program):
    """정교한 매칭 점수 계산"""
    score = 0
    
    # 나이 기준 매칭
    age = user_data.get('age', 0)
    if age >= 65:
        score += 10
    
    # 카테고리별 가중치
    category_weights = {
        '생활비 지원': 15,
        '의료/돌봄 지원': 20,
        '주거 지원': 10,
        '고용 지원': 8,
        '생활 지원': 12
    }
    
    score += category_weights.get(program.category, 5)
    
    # 의료상태 매칭
    medical_conditions = str(user_data.get('medical_conditions', '')).lower()
    if medical_conditions:
        medical_keywords = ['당뇨', '고혈압', '관절염', '치매', '뇌졸중']
        for keyword in medical_keywords:
            if keyword in medical_conditions:
                if keyword in program.description.lower() or keyword in program.name.lower():
                    score += 15
                if '의료' in program.category:
                    score += 10
    
    # 생활상황 매칭
    living_situation = str(user_data.get('living_situation', '')).lower()
    if '독거' in living_situation and '독거' in program.name.lower():
        score += 25
    if '부부' in living_situation and '생활' in program.category:
        score += 8
    
    # 소득수준 매칭
    income_level = str(user_data.get('income_level', '')).lower()
    if '낮음' in income_level or '기초' in income_level:
        if '기초' in program.name.lower() or '의료비' in program.name.lower():
            score += 20
        if '급식' in program.name.lower():
            score += 15
    
    # 장애상태 매칭
    disability_status = str(user_data.get('disability_status', '')).lower()
    if '있음' in disability_status:
        if '장애' in program.description.lower() or '돌봄' in program.name.lower():
            score += 18
    
    # 고용상태 매칭
    employment_status = str(user_data.get('employment_status', '')).lower()
    if '무직' in employment_status or '구직' in employment_status:
        if '일자리' in program.name.lower() or '고용' in program.category:
            score += 12
    
    # 주거형태 매칭
    housing_type = str(user_data.get('housing_type', '')).lower()
    if '임대' in housing_type or '월세' in housing_type:
        if '주거' in program.category:
            score += 15
    
    # 우선순위 반영
    score += program.priority * 3
    
    # 지역 매칭
    user_region = user_data.get('region', '')
    if program.region == '전국' or program.region == user_region:
        score += 5
    
    return score

def get_match_details(user_data, program):
    """매칭 세부 사항 설명"""
    details = []
    
    age = user_data.get('age', 0)
    if age >= 65:
        details.append("연령 조건 충족")
    
    medical_conditions = str(user_data.get('medical_conditions', '')).lower()
    if medical_conditions and ('의료' in program.category or any(cond in program.description.lower() for cond in ['당뇨', '고혈압', '관절염'])):
        details.append("건강 상태 고려")
    
    living_situation = str(user_data.get('living_situation', '')).lower()
    if '독거' in living_situation and '독거' in program.name.lower():
        details.append("생활 상황 맞춤")
    
    income_level = str(user_data.get('income_level', '')).lower()
    if '낮음' in income_level and ('기초' in program.name.lower() or '지원' in program.category):
        details.append("소득 수준 고려")
    
    return details

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/survey')
def survey():
    """설문 시작 페이지"""
    # 세션 ID 생성
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    return render_template('survey.html')

@app.route('/survey/step1')
def survey_step1():
    """1단계: 기본 정보 입력"""
    return render_template('survey_step1.html', 
                         show_progress=True, 
                         current_step=1)

@app.route('/survey/step2')
def survey_step2():
    """2단계: 의료 상태 문진"""
    return render_template('survey_step2.html', 
                         show_progress=True, 
                         current_step=2)

@app.route('/survey/step3')
def survey_step3():
    """3단계: 생활 상태 문진"""
    return render_template('survey_step3.html', 
                         show_progress=True, 
                         current_step=3)

@app.route('/submit_survey', methods=['POST'])
def submit_survey():
    """설문 결과 제출 및 추천"""
    try:
        data = request.json
        
        # 입력 데이터 검증
        validation_errors = validate_user_input(data)
        if validation_errors:
            return jsonify({
                'success': False,
                'errors': validation_errors
            }), 400
        
        # 세션에 사용자 데이터 저장
        session['user_data'] = data
        
        # 데이터베이스에 저장
        user_response = UserResponse(
            session_id=session.get('session_id', 'anonymous'),
            name=data.get('name'),
            age=int(data.get('age', 0)),
            birth_date=data.get('birth_date'),
            region=data.get('region'),
            sub_region=data.get('sub_region'),
            medical_conditions=json.dumps(data.get('medical_conditions', [])),
            living_situation=data.get('living_situation'),
            income_level=data.get('income_level'),
            disability_status=data.get('disability_status'),
            family_size=int(data.get('family_size', 1)),
            employment_status=data.get('employment_status'),
            housing_type=data.get('housing_type')
        )
        
        db.session.add(user_response)
        db.session.commit()
        
        # AI 추천 실행
        recommendations = get_ai_recommendations(data)
        
        logger.info(f"사용자 {data.get('name')}에 대한 추천 완료: {len(recommendations)}개")
        
        return jsonify({
            'success': True,
            'recommendations': [{
                'program': rec['program'].to_dict(),
                'score': rec['score'],
                'recommendation_reason': rec['recommendation_reason'],
                'match_details': rec['match_details']
            } for rec in recommendations]
        })
        
    except Exception as e:
        logger.error(f"설문 제출 오류: {str(e)}")
        return jsonify({
            'success': False,
            'error': '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
        }), 500

@app.route('/results')
def results():
    """결과 페이지"""
    user_data = session.get('user_data')
    if not user_data:
        return redirect(url_for('index'))
    
    recommendations = get_ai_recommendations(user_data)
    
    return render_template('results.html', 
                         user_data=user_data, 
                         recommendations=recommendations,
                         current_time=datetime.now())

@app.route('/print_results')
def print_results():
    """인쇄용 결과 페이지"""
    user_data = session.get('user_data')
    if not user_data:
        return redirect(url_for('index'))
    
    recommendations = get_ai_recommendations(user_data)
    
    return render_template('print_results.html', 
                         user_data=user_data, 
                         recommendations=recommendations,
                         current_time=datetime.now())

@app.route('/welfare_centers')
def welfare_centers():
    """복지센터 찾기"""
    user_region = request.args.get('region', '')
    
    centers = WelfareCenter.query.all()
    if user_region:
        centers = WelfareCenter.query.filter(
            WelfareCenter.region.contains(user_region)
        ).all()
    
    return jsonify([{
        'id': center.id,
        'name': center.name,
        'address': center.address,
        'phone': center.phone,
        'region': center.region,
        'sub_region': center.sub_region,
        'services': center.services,
        'operating_hours': center.operating_hours
    } for center in centers])

@app.route('/api/search_welfare')
def search_welfare():
    """복지 프로그램 검색 API"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    region = request.args.get('region', '')
    
    programs = WelfareProgram.query
    
    if query:
        programs = programs.filter(
            WelfareProgram.name.contains(query) | 
            WelfareProgram.description.contains(query)
        )
    
    if category:
        programs = programs.filter(WelfareProgram.category == category)
    
    if region:
        programs = programs.filter(
            (WelfareProgram.region == region) | 
            (WelfareProgram.region == '전국')
        )
    
    programs = programs.order_by(WelfareProgram.priority.desc()).all()
    
    return jsonify([program.to_dict() for program in programs])

@app.route('/api/voice_search', methods=['POST'])
def voice_search():
    """음성 검색 API"""
    try:
        data = request.json
        voice_text = data.get('text', '')
        
        # 음성 텍스트에서 키워드 추출
        keywords = extract_keywords_from_voice(voice_text)
        
        # 키워드 기반 검색
        programs = search_programs_by_keywords(keywords)
        
        return jsonify({
            'success': True,
            'keywords': keywords,
            'programs': [program.to_dict() for program in programs[:5]]
        })
        
    except Exception as e:
        logger.error(f"음성 검색 오류: {str(e)}")
        return jsonify({
            'success': False,
            'error': '음성 검색 중 오류가 발생했습니다.'
        }), 500

def extract_keywords_from_voice(voice_text):
    """음성 텍스트에서 키워드 추출"""
    welfare_keywords = [
        '기초연금', '의료비', '장기요양', '독거노인', '일자리',
        '생활비', '주거', '급식', '건강', '돌봄', '교통비'
    ]
    
    found_keywords = []
    for keyword in welfare_keywords:
        if keyword in voice_text:
            found_keywords.append(keyword)
    
    return found_keywords

def search_programs_by_keywords(keywords):
    """키워드 기반 프로그램 검색"""
    if not keywords:
        return WelfareProgram.query.order_by(WelfareProgram.priority.desc()).limit(5).all()
    
    programs = WelfareProgram.query
    
    for keyword in keywords:
        programs = programs.filter(
            WelfareProgram.name.contains(keyword) | 
            WelfareProgram.description.contains(keyword)
        )
    
    return programs.order_by(WelfareProgram.priority.desc()).all()

@app.route('/health')
def health_check():
    """애플리케이션 상태 확인"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected' if db.session.execute('SELECT 1').scalar() else 'disconnected'
    })

@app.errorhandler(404)
def not_found(error):
    """404 에러 핸들러"""
    return render_template('error.html', 
                         error_code=404,
                         error_message='페이지를 찾을 수 없습니다.'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 에러 핸들러"""
    logger.error(f"서버 오류: {str(error)}")
    return render_template('error.html', 
                         error_code=500,
                         error_message='서버 오류가 발생했습니다.'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_sample_data()
        logger.info("애플리케이션 시작됨")
    
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 