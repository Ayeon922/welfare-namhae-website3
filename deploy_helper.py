#!/usr/bin/env python3
"""
복지길잡이 Render 배포 도우미 스크립트
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """명령어 실행 및 결과 확인"""
    print(f"✅ {description}")
    print(f"실행 중: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 성공!")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ 오류 발생:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 명령어 실행 실패: {e}")
        return False
    
    print("-" * 50)
    return True

def check_git_installed():
    """Git 설치 확인"""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        return True
    except:
        return False

def main():
    print("🚀 복지길잡이 Render 배포 도우미")
    print("=" * 50)
    
    # 현재 디렉토리 확인
    current_dir = Path.cwd()
    print(f"현재 디렉토리: {current_dir}")
    
    # 필수 파일 확인
    required_files = ['app.py', 'requirements.txt', 'Procfile', 'render.yaml']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 필수 파일이 없습니다: {', '.join(missing_files)}")
        return
    
    print("✅ 모든 필수 파일이 준비되었습니다!")
    print()
    
    # Git 설치 확인
    if not check_git_installed():
        print("❌ Git이 설치되지 않았습니다.")
        print("Git을 설치한 후 다시 시도해주세요: https://git-scm.com/download")
        return
    
    print("✅ Git이 설치되어 있습니다!")
    print()
    
    # 사용자로부터 GitHub 정보 받기
    print("📝 GitHub 저장소 정보를 입력해주세요:")
    github_username = input("GitHub 사용자명: ").strip()
    repo_name = input("저장소 이름 (기본값: welfare-platform): ").strip() or "welfare-platform"
    
    if not github_username:
        print("❌ GitHub 사용자명은 필수입니다!")
        return
    
    github_url = f"https://github.com/{github_username}/{repo_name}.git"
    print(f"GitHub URL: {github_url}")
    print()
    
    # Git 저장소 초기화 및 설정
    commands = [
        ("git init", "Git 저장소 초기화"),
        ("git add .", "파일들을 스테이징 영역에 추가"),
        ('git commit -m "Initial commit: 복지길잡이 웹앱"', "첫 번째 커밋 생성"),
        ("git branch -M main", "메인 브랜치 설정"),
        (f"git remote add origin {github_url}", "GitHub 저장소 연결"),
    ]
    
    print("🔄 Git 설정 및 파일 업로드 중...")
    for command, description in commands:
        if not run_command(command, description):
            print("❌ 배포 과정에서 오류가 발생했습니다.")
            return
    
    # GitHub에 푸시
    print("📤 GitHub에 업로드 중...")
    print("⚠️  GitHub 인증이 필요할 수 있습니다.")
    print("   브라우저에서 로그인하거나 개인 액세스 토큰을 사용하세요.")
    input("준비되면 Enter를 눌러주세요...")
    
    if not run_command("git push -u origin main", "GitHub에 코드 업로드"):
        print("❌ GitHub 업로드에 실패했습니다.")
        print("💡 해결 방법:")
        print("1. GitHub에서 저장소를 미리 생성했는지 확인")
        print("2. GitHub 인증 정보가 올바른지 확인")
        print("3. 개인 액세스 토큰 사용 고려")
        return
    
    print()
    print("🎉 성공적으로 GitHub에 업로드되었습니다!")
    print()
    print("📋 다음 단계 - Render에서 배포:")
    print("1. https://render.com 에 접속")
    print("2. GitHub 계정으로 로그인")
    print("3. 'New +' → 'Web Service' 선택")
    print(f"4. '{repo_name}' 저장소 선택")
    print("5. 다음 설정 사용:")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: gunicorn app:app")
    print("6. 환경 변수 설정 (선택사항):")
    print("   - SECRET_KEY: (자동 생성)")
    print("   - OPENAI_API_KEY: (OpenAI API 키)")
    print("7. 'Create Web Service' 클릭")
    print()
    print("🌐 배포 완료 후 제공되는 URL로 접속하시면 됩니다!")
    print()
    print("📖 자세한 가이드는 'RENDER_DEPLOY.md' 파일을 참조하세요.")

if __name__ == "__main__":
    main() 