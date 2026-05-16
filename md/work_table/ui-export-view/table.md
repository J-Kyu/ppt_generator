# UI Export View Task

* purpose: `md/spec/ui/export_view.md` 명세에 따른 PPT 추출 완료 화면 및 기능 초기화 구성 (Dummy 연동)
* range: `src/ui/views/export.py` 및 관련 컴포넌트

## Task List
* [ ] Feature 1: Export 진행 중 로딩 상태(Loading UI) 구성
  * feature_purpose: PPT 생성 중 상태를 알리는 Spinner 및 로딩 메시지 화면 구성
  * feature_range: `src/ui/views/export.py` Loading State 영역

* [ ] Feature 2: Dummy 작업 완료 시나리오 전환 및 버튼 동작 확인
  * feature_purpose: 일정 시간 경과 후 성공(Success UI) 화면으로 전환하고, 더미 로그 출력, 상태 리셋(Reset) 기능이 포함된 완료 버튼 동작 검증
  * feature_range: `src/ui/views/export.py` Success State 영역 및 상태 제어 이벤트
