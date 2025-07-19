// 메인 JavaScript 파일

(function() {
    'use strict';

    // 전역 유틸리티
    const Utils = {
        // 로컬 스토리지 관리
        storage: {
            get: function(key) {
                try {
                    const item = localStorage.getItem(key);
                    return item ? JSON.parse(item) : null;
                } catch (e) {
                    console.error('Storage get error:', e);
                    return null;
                }
            },
            
            set: function(key, value) {
                try {
                    localStorage.setItem(key, JSON.stringify(value));
                    return true;
                } catch (e) {
                    console.error('Storage set error:', e);
                    return false;
                }
            },
            
            remove: function(key) {
                try {
                    localStorage.removeItem(key);
                    return true;
                } catch (e) {
                    console.error('Storage remove error:', e);
                    return false;
                }
            }
        },

        // 폼 유효성 검사
        validation: {
            required: function(value) {
                return value && value.trim() !== '';
            },
            
            email: function(value) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                return emailRegex.test(value);
            },
            
            phone: function(value) {
                const phoneRegex = /^01[0-9]-\d{3,4}-\d{4}$/;
                return phoneRegex.test(value);
            },
            
            age: function(value) {
                const num = parseInt(value);
                return !isNaN(num) && num >= 60 && num <= 120;
            },
            
            birthDate: function(value) {
                const date = new Date(value);
                const today = new Date();
                const minDate = new Date(today.getFullYear() - 120, today.getMonth(), today.getDate());
                return date >= minDate && date <= today;
            }
        },

        // 음성 안내
        speak: function(text, options = {}) {
            if ('speechSynthesis' in window && text) {
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = options.lang || 'ko-KR';
                utterance.rate = options.rate || 0.8;
                utterance.volume = options.volume || 0.7;
                
                speechSynthesis.speak(utterance);
            }
        },

        // 로딩 표시
        loading: {
            show: function(message = '처리 중...') {
                const existing = document.querySelector('.loading-overlay');
                if (existing) existing.remove();
                
                const overlay = document.createElement('div');
                overlay.className = 'loading-overlay';
                overlay.innerHTML = `
                    <div class="loading-content">
                        <div class="loading-spinner"></div>
                        <p>${message}</p>
                    </div>
                `;
                document.body.appendChild(overlay);
            },
            
            hide: function() {
                const overlay = document.querySelector('.loading-overlay');
                if (overlay) {
                    overlay.remove();
                }
            }
        },

        // 알림 표시
        notify: function(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `notification notification-${type}`;
            notification.innerHTML = `
                <div class="notification-content">
                    <span class="notification-icon">${this.getNotificationIcon(type)}</span>
                    <span class="notification-message">${message}</span>
                    <button class="notification-close" aria-label="알림 닫기">×</button>
                </div>
            `;
            
            document.body.appendChild(notification);
            
            // 자동 제거
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 5000);
            
            // 닫기 버튼 이벤트
            notification.querySelector('.notification-close').addEventListener('click', () => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            });
            
            // 음성 알림
            this.speak(message);
        },

        getNotificationIcon: function(type) {
            const icons = {
                'info': 'ℹ️',
                'success': '✅',
                'warning': '⚠️',
                'error': '❌'
            };
            return icons[type] || icons['info'];
        },

        // 날짜 포맷팅
        formatDate: function(date) {
            if (!date) return '';
            const d = new Date(date);
            return d.toLocaleDateString('ko-KR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        },

        // 나이 계산
        calculateAge: function(birthDate) {
            if (!birthDate) return 0;
            
            const birth = new Date(birthDate);
            const today = new Date();
            let age = today.getFullYear() - birth.getFullYear();
            const monthDiff = today.getMonth() - birth.getMonth();
            
            if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
                age--;
            }
            
            return age;
        }
    };

    // 설문 관리
    const SurveyManager = {
        init: function() {
            this.loadSurveyData();
            this.setupAutoSave();
        },

        loadSurveyData: function() {
            // 저장된 설문 데이터 불러오기
            const step1Data = Utils.storage.get('step1_data') || {};
            const step2Data = Utils.storage.get('step2_data') || {};
            const step3Data = Utils.storage.get('step3_data') || {};
            
            return {
                step1: step1Data,
                step2: step2Data,
                step3: step3Data
            };
        },

        saveStepData: function(step, data) {
            Utils.storage.set(`step${step}_data`, data);
        },

        getAllData: function() {
            return this.loadSurveyData();
        },

        clearData: function() {
            Utils.storage.remove('step1_data');
            Utils.storage.remove('step2_data');
            Utils.storage.remove('step3_data');
        },

        formatMedicalConditions: function(step2Data) {
            // 2단계 의료 상태 데이터를 문자열로 변환
            const conditions = [];
            
            if (step2Data.chronic_diseases) {
                conditions.push(`만성질환: ${step2Data.chronic_diseases}`);
            }
            if (step2Data.medications) {
                conditions.push(`복용약물: ${step2Data.medications}`);
            }
            if (step2Data.physical_limitations) {
                conditions.push(`신체제한: ${step2Data.physical_limitations}`);
            }
            if (step2Data.medical_history) {
                conditions.push(`의료이력: ${step2Data.medical_history}`);
            }
            
            return conditions.join(', ') || '없음';
        },

        setupAutoSave: function() {
            // 폼 변경 시 자동 저장
            document.addEventListener('input', (e) => {
                if (e.target.closest('form')) {
                    this.autoSave(e.target.closest('form'));
                }
            });

            document.addEventListener('change', (e) => {
                if (e.target.closest('form')) {
                    this.autoSave(e.target.closest('form'));
                }
            });
        },

        autoSave: function(form) {
            if (!form) return;
            
            const formData = new FormData(form);
            const data = {};
            
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            
            // 어느 단계인지 확인
            const formId = form.id;
            if (formId.includes('step1')) {
                this.saveStepData(1, data);
            } else if (formId.includes('step2')) {
                this.saveStepData(2, data);
            } else if (formId.includes('step3')) {
                this.saveStepData(3, data);
            }
        },

        submitSurvey: function() {
            const allData = this.getAllData();
            
            // 필수 데이터 확인
            if (!allData.step1.name || !allData.step1.age || !allData.step1.region) {
                Utils.notify('기본 정보를 모두 입력해주세요.', 'error');
                return false;
            }
            
            // 서버로 데이터 전송
            Utils.loading.show('AI가 맞춤 복지 프로그램을 찾고 있습니다...');
            
            // 통합 데이터 생성
            const surveyData = {
                name: allData.step1.name,
                age: parseInt(allData.step1.age),
                birth_date: allData.step1.birth_date,
                region: allData.step1.region,
                detailed_address: allData.step1.detailed_address,
                phone: allData.step1.phone,
                medical_conditions: this.formatMedicalConditions(allData.step2),
                living_situation: allData.step3.living_situation,
                income_level: allData.step3.income_level,
                family_composition: allData.step3.family_composition,
                housing_type: allData.step3.housing_type
            };
            
            // API 호출
            fetch('/submit_survey', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(surveyData)
            })
            .then(response => response.json())
            .then(data => {
                Utils.loading.hide();
                
                if (data.success) {
                    Utils.notify('복지 프로그램 추천이 완료되었습니다!', 'success');
                    
                    // 결과 페이지로 이동
                    setTimeout(() => {
                        window.location.href = '/results';
                    }, 1500);
                } else {
                    Utils.notify('오류가 발생했습니다. 다시 시도해주세요.', 'error');
                }
            })
            .catch(error => {
                Utils.loading.hide();
                console.error('Error:', error);
                Utils.notify('서버 연결에 실패했습니다. 다시 시도해주세요.', 'error');
            });
            
            return true;
        },

        formatMedicalConditions: function(step2Data) {
            const conditions = [];
            
            if (step2Data.diabetes) conditions.push('당뇨병');
            if (step2Data.hypertension) conditions.push('고혈압');
            if (step2Data.arthritis) conditions.push('관절염');
            if (step2Data.heart_disease) conditions.push('심장병');
            if (step2Data.stroke) conditions.push('뇌졸중');
            if (step2Data.dementia) conditions.push('치매');
            if (step2Data.disability) conditions.push('장애');
            if (step2Data.other_conditions) conditions.push(step2Data.other_conditions);
            
            return conditions.join(', ');
        }
    };

    // 페이지별 초기화
    const PageManager = {
        init: function() {
            const currentPage = this.getCurrentPage();
            
            switch(currentPage) {
                case 'index':
                    this.initIndexPage();
                    break;
                case 'survey':
                    this.initSurveyPage();
                    break;
                case 'survey_step1':
                    this.initStep1Page();
                    break;
                case 'survey_step2':
                    this.initStep2Page();
                    break;
                case 'survey_step3':
                    this.initStep3Page();
                    break;
                case 'results':
                    this.initResultsPage();
                    break;
            }
        },

        getCurrentPage: function() {
            const path = window.location.pathname;
            if (path === '/') return 'index';
            if (path === '/survey') return 'survey';
            if (path === '/survey/step1') return 'survey_step1';
            if (path === '/survey/step2') return 'survey_step2';
            if (path === '/survey/step3') return 'survey_step3';
            if (path === '/results') return 'results';
            return 'unknown';
        },

        initIndexPage: function() {
            // 메인 페이지 초기화
            this.setupSmoothScroll();
            this.setupCTAButtons();
        },

        initSurveyPage: function() {
            // 설문 소개 페이지 초기화
            this.setupConsentForm();
        },

        initStep1Page: function() {
            // 1단계 페이지 초기화
            this.setupFormValidation();
            this.loadSavedData(1);
        },

        initStep2Page: function() {
            // 2단계 페이지 초기화
            this.setupFormValidation();
            this.loadSavedData(2);
        },

        initStep3Page: function() {
            // 3단계 페이지 초기화
            this.setupFormValidation();
            this.loadSavedData(3);
            this.setupFinalSubmit();
        },

        initResultsPage: function() {
            // 결과 페이지 초기화
            this.setupPrintButton();
            this.setupShareButtons();
        },

        setupSmoothScroll: function() {
            const links = document.querySelectorAll('a[href^="#"]');
            links.forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    const target = document.querySelector(link.getAttribute('href'));
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });
        },

        setupCTAButtons: function() {
            const ctaButtons = document.querySelectorAll('.cta-button');
            ctaButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    // 버튼 클릭 효과
                    button.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        button.style.transform = '';
                    }, 100);
                });
            });
        },

        setupConsentForm: function() {
            // 동의 폼 관련 로직은 이미 survey.html에 있음
        },

        setupFormValidation: function() {
            // 폼 유효성 검사는 각 단계별 템플릿에서 처리
        },

        loadSavedData: function(step) {
            const savedData = Utils.storage.get(`step${step}_data`);
            if (savedData) {
                Object.keys(savedData).forEach(key => {
                    const input = document.querySelector(`[name="${key}"]`);
                    if (input) {
                        if (input.type === 'checkbox') {
                            input.checked = savedData[key];
                        } else {
                            input.value = savedData[key];
                        }
                    }
                });
            }
        },

        setupFinalSubmit: function() {
            const finalSubmitBtn = document.querySelector('#final-submit-btn');
            if (finalSubmitBtn) {
                finalSubmitBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    SurveyManager.submitSurvey();
                });
            }
        },

        setupPrintButton: function() {
            const printBtn = document.querySelector('#print-results');
            if (printBtn) {
                printBtn.addEventListener('click', () => {
                    window.open('/print_results', '_blank');
                });
            }
        },

        setupShareButtons: function() {
            // 공유 기능 (필요시 추가)
        }
    };

    // 전역 초기화
    document.addEventListener('DOMContentLoaded', function() {
        SurveyManager.init();
        PageManager.init();
        
        // 전역 에러 처리
        window.addEventListener('error', (e) => {
            console.error('Global error:', e.error);
            Utils.notify('예상치 못한 오류가 발생했습니다. 페이지를 새로고침하거나 관리자에게 문의해주세요.', 'error');
        });
        
        // 네트워크 상태 확인
        window.addEventListener('online', () => {
            Utils.notify('인터넷 연결이 복구되었습니다.', 'success');
        });
        
        window.addEventListener('offline', () => {
            Utils.notify('인터넷 연결이 끊어졌습니다. 연결을 확인해주세요.', 'warning');
        });
    });

    // 전역 함수로 노출
    window.WelfareApp = {
        Utils,
        SurveyManager,
        PageManager
    };

})(); 