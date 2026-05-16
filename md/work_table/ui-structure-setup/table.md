# UI Structure Setup Task

* purpose: 전체적인 UI 틀을 잡기 위한 라우팅 구조 및 전역 상태(Dummy) 기본 설계 설정
* range: `src/ui/app.py`, `main.py`, `src/state/app_state.py` (Dummy 구성)

## Task List
* [x] Feature 1: 기본 Flet 앱 진입점 및 라우팅 컨트롤러 구성
  * feature_purpose: 엔진 연동 전, 각 View 컴포넌트 간의 원활한 이동을 처리하는 네비게이션 뼈대 구축 및 화면 렌더링 동작 확인
  * feature_range: `src/ui/app.py`, `main.py`

* [x] Feature 2: Dummy 데이터 전역 상태 관리 클래스 작성
  * feature_purpose: 화면 전환 시 유지되어야 할 정보(더미 레이아웃 리스트, 선택된 레이아웃 인덱스, 덱 추가 리스트 등)를 관리할 상태 클래스 구성
  * feature_range: `src/state/app_state.py` (또는 ui 더미 상태 관련 모듈)
