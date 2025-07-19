// 접근성 기능 JavaScript

(function() {
    'use strict';

    // 접근성 설정 저장/불러오기
    const AccessibilitySettings = {
        load: function() {
            return {
                fontSize: localStorage.getItem('accessibility-font-size') || 'normal',
                highContrast: localStorage.getItem('accessibility-high-contrast') === 'true',
                reduceMotion: localStorage.getItem('accessibility-reduce-motion') === 'true'
            };
        },
        
        save: function(settings) {
            localStorage.setItem('accessibility-font-size', settings.fontSize);
            localStorage.setItem('accessibility-high-contrast', settings.highContrast);
            localStorage.setItem('accessibility-reduce-motion', settings.reduceMotion);
        }
    };

    // 글씨 크기 조절
    const FontSizeController = {
        init: function() {
            const normalBtn = document.getElementById('font-size-normal');
            const largeBtn = document.getElementById('font-size-large');
            const xlargeBtn = document.getElementById('font-size-xlarge');
            
            if (normalBtn) normalBtn.addEventListener('click', () => this.setFontSize('normal'));
            if (largeBtn) largeBtn.addEventListener('click', () => this.setFontSize('large'));
            if (xlargeBtn) xlargeBtn.addEventListener('click', () => this.setFontSize('xlarge'));
            
            // 저장된 설정 적용
            const settings = AccessibilitySettings.load();
            this.setFontSize(settings.fontSize);
        },
        
        setFontSize: function(size) {
            const body = document.body;
            
            // 기존 글씨 크기 클래스 제거
            body.classList.remove('font-size-large', 'font-size-xlarge');
            
            // 새로운 글씨 크기 적용
            if (size === 'large') {
                body.classList.add('font-size-large');
            } else if (size === 'xlarge') {
                body.classList.add('font-size-xlarge');
            }
            
            // 버튼 상태 업데이트
            this.updateButtonStates(size);
            
            // 설정 저장
            const settings = AccessibilitySettings.load();
            settings.fontSize = size;
            AccessibilitySettings.save(settings);
            
            // 음성 알림
            this.announceChange(`글씨 크기가 ${this.getSizeText(size)}로 변경되었습니다.`);
        },
        
        getSizeText: function(size) {
            const sizeMap = {
                'normal': '기본 크기',
                'large': '크게',
                'xlarge': '매우 크게'
            };
            return sizeMap[size] || '기본 크기';
        },
        
        updateButtonStates: function(currentSize) {
            const buttons = ['font-size-normal', 'font-size-large', 'font-size-xlarge'];
            const sizes = ['normal', 'large', 'xlarge'];
            
            buttons.forEach((btnId, index) => {
                const btn = document.getElementById(btnId);
                if (btn) {
                    btn.classList.toggle('active', sizes[index] === currentSize);
                    btn.setAttribute('aria-pressed', sizes[index] === currentSize);
                }
            });
        },
        
        announceChange: function(message) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(message);
                utterance.lang = 'ko-KR';
                utterance.rate = 0.8;
                utterance.volume = 0.5;
                speechSynthesis.speak(utterance);
            }
        }
    };

    // 고대비 모드
    const HighContrastController = {
        init: function() {
            const btn = document.getElementById('high-contrast');
            if (btn) {
                btn.addEventListener('click', () => this.toggle());
            }
            
            // 저장된 설정 적용
            const settings = AccessibilitySettings.load();
            if (settings.highContrast) {
                this.enable();
            }
        },
        
        toggle: function() {
            const body = document.body;
            const isEnabled = body.classList.contains('high-contrast');
            
            if (isEnabled) {
                this.disable();
            } else {
                this.enable();
            }
        },
        
        enable: function() {
            document.body.classList.add('high-contrast');
            
            const btn = document.getElementById('high-contrast');
            if (btn) {
                btn.classList.add('active');
                btn.setAttribute('aria-pressed', 'true');
            }
            
            // 설정 저장
            const settings = AccessibilitySettings.load();
            settings.highContrast = true;
            AccessibilitySettings.save(settings);
            
            this.announceChange('고대비 모드가 활성화되었습니다.');
        },
        
        disable: function() {
            document.body.classList.remove('high-contrast');
            
            const btn = document.getElementById('high-contrast');
            if (btn) {
                btn.classList.remove('active');
                btn.setAttribute('aria-pressed', 'false');
            }
            
            // 설정 저장
            const settings = AccessibilitySettings.load();
            settings.highContrast = false;
            AccessibilitySettings.save(settings);
            
            this.announceChange('고대비 모드가 비활성화되었습니다.');
        },
        
        announceChange: function(message) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(message);
                utterance.lang = 'ko-KR';
                utterance.rate = 0.8;
                utterance.volume = 0.5;
                speechSynthesis.speak(utterance);
            }
        }
    };

    // 읽어주기 기능
    const ReadAloudController = {
        init: function() {
            const btn = document.getElementById('read-aloud');
            if (btn) {
                btn.addEventListener('click', () => this.toggle());
            }
            
            this.isReading = false;
            this.currentUtterance = null;
        },
        
        toggle: function() {
            if (this.isReading) {
                this.stop();
            } else {
                this.start();
            }
        },
        
        start: function() {
            if (!('speechSynthesis' in window)) {
                alert('죄송합니다. 이 브라우저에서는 읽어주기 기능을 지원하지 않습니다.');
                return;
            }
            
            const content = this.getPageContent();
            if (content) {
                this.currentUtterance = new SpeechSynthesisUtterance(content);
                this.currentUtterance.lang = 'ko-KR';
                this.currentUtterance.rate = 0.8;
                this.currentUtterance.volume = 0.8;
                
                this.currentUtterance.onstart = () => {
                    this.isReading = true;
                    this.updateButton(true);
                };
                
                this.currentUtterance.onend = () => {
                    this.isReading = false;
                    this.updateButton(false);
                };
                
                this.currentUtterance.onerror = () => {
                    this.isReading = false;
                    this.updateButton(false);
                };
                
                speechSynthesis.speak(this.currentUtterance);
            }
        },
        
        stop: function() {
            if (speechSynthesis.speaking) {
                speechSynthesis.cancel();
            }
            this.isReading = false;
            this.updateButton(false);
        },
        
        getPageContent: function() {
            const main = document.querySelector('.main-content');
            if (!main) return '';
            
            const content = [];
            
            // 제목 추출
            const headings = main.querySelectorAll('h1, h2, h3, h4, h5, h6');
            headings.forEach(heading => {
                content.push(heading.textContent.trim());
            });
            
            // 단락 추출
            const paragraphs = main.querySelectorAll('p');
            paragraphs.forEach(p => {
                const text = p.textContent.trim();
                if (text && !text.match(/^\s*$/) && !text.match(/^[^\w\s가-힣]+$/)) {
                    content.push(text);
                }
            });
            
            return content.join('. ');
        },
        
        updateButton: function(isReading) {
            const btn = document.getElementById('read-aloud');
            if (btn) {
                btn.classList.toggle('active', isReading);
                btn.setAttribute('aria-pressed', isReading);
                btn.innerHTML = isReading ? '⏸️' : '🔊';
                btn.setAttribute('aria-label', isReading ? '읽기 중지' : '읽어주기');
            }
        }
    };

    // 키보드 내비게이션
    const KeyboardNavigation = {
        init: function() {
            document.addEventListener('keydown', (e) => this.handleKeydown(e));
            
            // 키보드 사용 감지
            document.addEventListener('keydown', () => {
                document.body.classList.add('keyboard-navigation');
            });
            
            document.addEventListener('mousedown', () => {
                document.body.classList.remove('keyboard-navigation');
            });
        },
        
        handleKeydown: function(e) {
            // Alt + 1: 메인 컨텐츠로 이동
            if (e.altKey && e.key === '1') {
                e.preventDefault();
                const mainContent = document.getElementById('main-content');
                if (mainContent) {
                    mainContent.focus();
                    mainContent.scrollIntoView();
                }
            }
            
            // Alt + 2: 내비게이션으로 이동
            if (e.altKey && e.key === '2') {
                e.preventDefault();
                const nav = document.querySelector('.header');
                if (nav) {
                    nav.focus();
                    nav.scrollIntoView();
                }
            }
            
            // Escape: 모든 모달/팝업 닫기
            if (e.key === 'Escape') {
                this.closeModals();
            }
        },
        
        closeModals: function() {
            // 모달이나 팝업이 있다면 닫기
            const modals = document.querySelectorAll('.modal, .popup');
            modals.forEach(modal => {
                if (modal.style.display !== 'none') {
                    modal.style.display = 'none';
                }
            });
        }
    };

    // 포커스 관리
    const FocusManager = {
        init: function() {
            this.setupFocusTraps();
            this.setupSkipLinks();
        },
        
        setupFocusTraps: function() {
            const focusableElements = 'a[href], area[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), button:not([disabled]), iframe, object, embed, [tabindex="0"], [contenteditable]';
            
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Tab') {
                    const focusable = Array.from(document.querySelectorAll(focusableElements));
                    const currentIndex = focusable.indexOf(document.activeElement);
                    
                    if (e.shiftKey) {
                        // Shift + Tab (이전 요소로)
                        if (currentIndex <= 0) {
                            e.preventDefault();
                            focusable[focusable.length - 1].focus();
                        }
                    } else {
                        // Tab (다음 요소로)
                        if (currentIndex >= focusable.length - 1) {
                            e.preventDefault();
                            focusable[0].focus();
                        }
                    }
                }
            });
        },
        
        setupSkipLinks: function() {
            const skipLinks = document.querySelectorAll('.skip-nav');
            skipLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    const targetId = link.getAttribute('href').substring(1);
                    const target = document.getElementById(targetId);
                    if (target) {
                        target.focus();
                        target.scrollIntoView();
                    }
                });
            });
        }
    };

    // 초기화
    document.addEventListener('DOMContentLoaded', function() {
        FontSizeController.init();
        HighContrastController.init();
        ReadAloudController.init();
        KeyboardNavigation.init();
        FocusManager.init();
        
        // 접근성 안내 메시지
        const announceAccessibility = function() {
            if ('speechSynthesis' in window) {
                const message = '접근성 도구가 활성화되었습니다. Alt + 1을 눌러 메인 컨텐츠로 이동하거나, 상단의 접근성 버튼을 사용하세요.';
                const utterance = new SpeechSynthesisUtterance(message);
                utterance.lang = 'ko-KR';
                utterance.rate = 0.8;
                utterance.volume = 0.5;
                
                // 페이지 로드 후 3초 뒤에 안내
                setTimeout(() => {
                    speechSynthesis.speak(utterance);
                }, 3000);
            }
        };
        
        // 첫 방문자에게만 안내
        if (!localStorage.getItem('accessibility-announced')) {
            announceAccessibility();
            localStorage.setItem('accessibility-announced', 'true');
        }
    });

    // 전역 함수로 노출
    window.AccessibilityController = {
        FontSizeController,
        HighContrastController,
        ReadAloudController,
        KeyboardNavigation,
        FocusManager
    };

})(); 