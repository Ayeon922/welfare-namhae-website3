# 🚀 복지길잡이 Render 배포 가이드

## 📋 배포 단계

### 1. GitHub 저장소 생성 및 업로드

1. **GitHub에서 새 저장소 생성**
   - [GitHub](https://github.com)에 로그인
   - "New repository" 클릭
   - 저장소 이름: `welfare-platform`
   - Public으로 설정
   - Create repository 클릭

2. **프로젝트를 GitHub에 업로드**
   ```bash
   # 현재 디렉토리에서 실행
   git init
   git add .
   git commit -m "Initial commit: 복지길잡이 웹앱"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/welfare-platform.git
   git push -u origin main
   ```

### 2. Render 배포

1. **Render 계정 생성**
   - [render.com](https://render.com) 접속
   - "Get Started for Free" 클릭
   - GitHub 계정으로 로그인

2. **새 Web Service 생성**
   - 대시보드에서 "New +" 클릭
   - "Web Service" 선택
   - "Connect a repository" 섹션에서 GitHub 연결
   - `welfare-platform` 저장소 선택

3. **서비스 설정**
   ```
   Name: welfare-platform
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. **환경 변수 설정**
   - "Environment" 탭에서 다음 환경 변수 추가:
   ```
   SECRET_KEY: (자동 생성되거나 랜덤 문자열)
   OPENAI_API_KEY: your_openai_api_key_here (선택사항)
   ```

5. **배포 시작**
   - "Create Web Service" 클릭
   - 빌드 로그를 확인하며 배포 진행 상황 모니터링
   - 배포 완료 후 제공되는 URL로 접속

### 3. 배포 완료 확인

- 제공된 URL (예: `https://welfare-platform.onrender.com`)로 접속
- 웹사이트가 정상적으로 로드되는지 확인
- 설문조사 기능 테스트
- 추천 결과 생성 테스트

## 📝 주요 특징

- ✅ **무료 배포**: Render 무료 플랜 사용
- ✅ **자동 SSL**: HTTPS 자동 적용
- ✅ **GitHub 연동**: 코드 업데이트 시 자동 재배포
- ✅ **24/7 접근**: 인터넷 어디서나 접속 가능

## 🔧 문제 해결

### 배포 실패 시
1. Build 로그 확인
2. requirements.txt 의존성 점검
3. 환경 변수 설정 확인

### 접속 안 될 시
1. 배포 상태 확인 (Render 대시보드)
2. 도메인 URL 정확성 확인
3. 브라우저 캐시 삭제 후 재시도

## 📞 지원

배포 과정에서 문제가 발생하면:
1. Render 공식 문서 참조
2. GitHub Issues를 통한 문의
3. 로그 파일 확인 및 오류 메시지 분석 