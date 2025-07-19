# 🌟 노인 복지 추천 플랫폼

65세 이상 노인을 위한 AI 기반 맞춤형 복지 혜택 추천 웹 플랫폼입니다.

## 📋 프로젝트 개요

이 플랫폼은 노인들이 자신의 상황에 맞는 복지 혜택을 쉽게 찾을 수 있도록 도와주는 서비스입니다. 간단한 3단계 문진을 통해 개인 맞춤형 복지 프로그램을 AI가 추천해드립니다.

### 🎯 주요 기능

- **3단계 간단 문진**: 기본정보 → 의료상태 → 생활상황
- **AI 맞춤 추천**: OpenAI GPT 기반 개인화 추천
- **접근성 우선 설계**: 큰 글씨, 고대비 모드, 음성 안내
- **복지센터 찾기**: 지역별 복지센터 정보 제공
- **결과 저장/인쇄**: PDF 다운로드, 인쇄 기능
- **음성 검색**: 자연어 음성 입력 지원

### 🎨 접근성 기능

- ✅ WCAG 2.2 접근성 기준 준수
- ✅ 4단계 글씨 크기 조절
- ✅ 고대비 모드 지원
- ✅ 키보드 네비게이션
- ✅ 스크린 리더 지원
- ✅ 음성 안내 (TTS)

## 🛠️ 기술 스택

### 백엔드
- **Flask**: 웹 프레임워크
- **SQLAlchemy**: ORM
- **SQLite**: 데이터베이스 (개발용)
- **OpenAI GPT**: AI 추천 엔진

### 프론트엔드
- **HTML5**: 시맨틱 마크업
- **CSS3**: 반응형 디자인
- **JavaScript**: 동적 기능
- **Web Speech API**: 음성 기능

### 주요 패키지
- `Flask==2.3.2`
- `Flask-SQLAlchemy==3.0.5`
- `openai==0.27.8`
- `python-dotenv==1.0.0`

## 🚀 설치 및 실행

### 1. 사전 요구사항

- Python 3.8 이상
- pip 패키지 관리자

### 2. Python 설치 (Windows)

#### 방법 1: Microsoft Store (추천)
1. Microsoft Store에서 "Python" 검색
2. 최신 버전 설치
3. 자동으로 PATH 설정됨

#### 방법 2: 공식 웹사이트
1. [python.org](https://www.python.org/downloads/) 방문
2. 최신 버전 다운로드
3. 설치 시 "Add Python to PATH" 체크

### 3. 프로젝트 설치

```bash
# 프로젝트 디렉터리로 이동
cd C:\Users\pc\welfare-platform

# 가상환경 생성 (선택사항)
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 4. 환경 설정

`.env` 파일 생성 (선택사항):
```bash
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here
FLASK_ENV=development
```

### 5. 실행 방법

#### 방법 1: 기본 실행
```bash
python app.py
```

#### 방법 2: 개선된 실행 스크립트 사용
```bash
# 개발 환경
python run.py

# 운영 환경
python run.py --prod

# 사용자 정의 설정
python run.py --host 0.0.0.0 --port 8080 --debug
```

### 6. 애플리케이션 접속

브라우저에서 다음 주소로 접속:
- 개발 환경: http://localhost:5000
- 또는: http://127.0.0.1:5000

## 📊 샘플 데이터

애플리케이션 실행 시 다음 복지 프로그램들이 자동으로 생성됩니다:

1. **기초연금** - 월 최대 334,810원
2. **노인 장기요양보험** - 요양 서비스 제공
3. **노인 의료비 지원** - 의료비 80-100% 지원
4. **독거노인 생활관리사 파견** - 무료 생활 지원
5. **노인 일자리 사업** - 월 27만원 내외
6. **치매 전담형 장기요양기관** - 전문 치매 돌봄
7. **노인 건강관리 서비스** - 맞춤형 건강관리
8. **노인 교통비 지원** - 대중교통 요금 할인
9. **주거급여** - 주거비 부담 완화
10. **노인 무료 급식 서비스** - 무료 급식 제공

## 🔧 문제 해결

### Python 실행 오류

PowerShell에서 `python` 명령어가 인식되지 않을 때:

```bash
# Python 설치 확인
where python

# 없다면 Microsoft Store에서 Python 설치
# 또는 python.org에서 다운로드

# Python Launcher 사용 (Windows)
py --version
py app.py
```

### 패키지 설치 오류

```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 패키지 개별 설치
pip install flask flask-sqlalchemy openai python-dotenv

# 캐시 삭제 후 재설치
pip install --no-cache-dir -r requirements.txt
```

### 포트 충돌 오류

```bash
# 다른 포트 사용
python app.py --port 8080

# 또는 run.py 사용
python run.py --port 8080
```

## 🌐 API 엔드포인트

- `GET /` - 메인 페이지
- `GET /survey` - 설문 시작
- `POST /submit_survey` - 설문 제출
- `GET /results` - 결과 페이지
- `GET /welfare_centers` - 복지센터 찾기
- `POST /api/voice_search` - 음성 검색
- `GET /api/search_welfare` - 복지 프로그램 검색
- `GET /health` - 애플리케이션 상태 확인

## 📱 사용자 가이드

### 1. 메인 페이지 접속
- 브라우저에서 `http://localhost:5000` 접속
- "복지 혜택 찾기 시작하기" 버튼 클릭

### 2. 3단계 문진 진행
- **1단계**: 이름, 나이, 거주지역 입력
- **2단계**: 건강상태, 의료상황 선택
- **3단계**: 생활상황, 소득수준 선택

### 3. 결과 확인
- AI가 추천하는 복지 프로그램 확인
- 각 프로그램의 혜택 내용, 신청 방법 확인
- 결과 저장 또는 인쇄

### 4. 접근성 기능 사용
- 상단 도구바에서 글씨 크기 조절
- 고대비 모드 활성화
- 읽어주기 기능 사용

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 지원 및 문의

- **전화**: 보건복지부 콜센터 129
- **이메일**: support@welfare-platform.kr
- **웹사이트**: https://welfare-platform.kr

## 📄 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🙏 감사의 말

이 프로젝트는 대한민국 보건복지부의 복지 정책을 기반으로 하며, 노인분들의 복지 향상을 위해 개발되었습니다.

---

**만든 사람**: 복지 플랫폼 개발팀  
**버전**: 1.0.0  
**최종 업데이트**: 2024년 7월 