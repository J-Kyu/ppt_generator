# UI Onboarding View Task

* purpose: `md/spec/ui/onboarding.md` 명세에 따른 파일 업로드 및 분석 대기 화면의 UI 구성 (Dummy 엔진 연동)
* range: `src/ui/views/onboarding.py` 및 관련 컴포넌트

## Task List
* [ ] Feature 1: 파일 업로드 Drop Zone 및 상태 텍스트 레이아웃 구성
  * feature_purpose: 파일 선택 및 분석 시 표기될 텍스트, 버튼, 컴포넌트 레이아웃의 시각적 형태 구성
  * feature_range: `src/ui/views/onboarding.py` 화면 렌더링

* [ ] Feature 2: 파일 선택 이벤트 및 분석 중 (Spinner) Dummy 전환 로직 구현
  * feature_purpose: 파일을 첨부했을 때 경로가 표시되고, 일정 시간(Dummy Timer) 동안 Spinner가 표기된 후 로그 출력과 함께 다음 뷰로 라우팅되는 기능 검증
  * feature_range: `src/ui/views/onboarding.py` 이벤트 로직
