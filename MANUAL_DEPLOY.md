# 🚀 복지길잡이 수동 배포 가이드 (Git 없이)

## 📋 준비된 파일들
현재 폴더에는 배포에 필요한 모든 파일이 준비되어 있습니다:
- ✅ app.py (메인 애플리케이션)
- ✅ requirements.txt (의존성 패키지)
- ✅ Procfile (Render 실행 설정)
- ✅ render.yaml (Render 배포 설정)
- ✅ templates/ (HTML 템플릿)
- ✅ static/ (CSS, JS 파일)

## 🌐 단계별 배포 방법

### 1. GitHub에 코드 업로드

#### 방법 A: GitHub 웹사이트 이용
1. **GitHub 계정 생성/로그인**
   - [github.com](https://github.com) 접속
   - 계정이 없다면 "Sign up" 클릭하여 가입

2. **새 저장소 생성**
   - 로그인 후 "+" → "New repository" 클릭
   - Repository name: `welfare-platform`
   - Public 선택
   - "Create repository" 클릭

3. **파일 업로드**
   - "uploading an existing file" 링크 클릭
   - 현재 폴더의 모든 파일을 선택해서 드래그 앤 드롭
   - Commit message: "Initial commit: 복지길잡이 웹앱"
   - "Commit changes" 클릭

#### 방법 B: GitHub Desktop 이용
1. **GitHub Desktop 설치**
   - [desktop.github.com](https://desktop.github.com) 에서 다운로드
   - 설치 후 GitHub 계정으로 로그인

2. **저장소 생성**
   - "Create a New Repository on your hard drive" 선택
   - Name: welfare-platform
   - Local path: 현재 폴더 선택
   - "Create repository" 클릭

3. **GitHub에 업로드**
   - "Publish repository" 클릭
   - "Keep this code private" 체크 해제 (Public으로 설정)
   - "Publish repository" 클릭

### 2. Render에서 배포

1. **Render 계정 생성**
   - [render.com](https://render.com) 접속
   - "Get Started for Free" 클릭
   - GitHub 계정으로 로그인

2. **새 Web Service 생성**
   - 대시보드에서 "New +" 클릭
   - "Web Service" 선택

3. **GitHub 저장소 연결**
   - "Connect a repository" 섹션에서
   - "Connect GitHub" 클릭 (필요시)
   - `welfare-platform` 저장소 선택
   - "Connect" 클릭

4. **서비스 설정**
   ```
   Name: welfare-platform
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

5. **고급 설정 (선택사항)**
   - "Advanced" 클릭
   - Environment Variables 섹션에서:
     - SECRET_KEY: (자동 생성 또는 랜덤 문자열)
     - OPENAI_API_KEY: (OpenAI API 키 - 선택사항)

6. **배포 시작**
   - "Create Web Service" 클릭
   - 빌드 로그를 확인하며 진행 상황 모니터링
   - 5-10분 후 배포 완료

### 3. 배포 완료 확인

✅ **성공 시 확인 사항:**
- Render에서 "Live" 상태 표시
- 제공된 URL 클릭 시 웹사이트 접속
- 설문조사 기능 정상 작동
- 추천 결과 생성 테스트

🌐 **최종 URL 예시:**
`https://welfare-platform.onrender.com`

## 📝 주요 특징

- ✅ **무료 배포**: Render 무료 플랜
- ✅ **자동 SSL**: HTTPS 자동 적용  
- ✅ **글로벌 접근**: 인터넷 어디서나 접속 가능
- ✅ **자동 재시작**: 서버 문제 시 자동 복구

## 🔧 문제 해결

### 배포 실패 시
1. **Build 로그 확인**
   - Render 대시보드에서 "Events" 탭 확인
   - 오류 메시지 분석

2. **일반적인 문제**
   - requirements.txt 파일 누락 → 다시 업로드
   - Start Command 오타 → `gunicorn app:app` 확인
   - Python 버전 호환성 → Python 3.8+ 사용

### 접속 안 될 시
1. 배포 상태가 "Live"인지 확인
2. URL이 정확한지 확인 (.onrender.com 포함)
3. 브라우저 캐시 삭제 후 재시도
4. 다른 브라우저나 기기에서 테스트

## 🎉 배포 완료!

배포가 성공적으로 완료되면:
1. 제공된 URL을 북마크에 저장
2. 가족, 친구들과 링크 공유
3. 노인분들께 사용법 안내
4. 피드백 수집 및 개선

## 📞 지원

배포 과정에서 도움이 필요하시면:
- Render 공식 문서: [render.com/docs](https://render.com/docs)
- GitHub 도움말: [docs.github.com](https://docs.github.com)
- 이 가이드를 다시 참조하여 단계별 확인 