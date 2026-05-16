# UI Slide Builder View Task

* purpose: `md/spec/ui/slide_builder_viewer.md` 명세에 따른 동적 폼 생성 및 슬라이드 누적 분할 화면 구축 (Dummy 연동)
* range: `src/ui/views/slide_builder.py` 및 관련 컴포넌트

## Task List
* [ ] Feature 1: 좌측 동적 텍스트 입력 폼(Left Panel) 렌더링
  * feature_purpose: Dummy Layout Schema를 읽어들여 텍스트 속성에 맞는 입력 필드(`ft.TextField`)를 동적으로 렌더링하고 유효성 검사 경고를 표시하는 UI 구축
  * feature_range: `src/ui/views/slide_builder.py` 좌측 패널

* [ ] Feature 2: 우측 슬라이드 대기열(Deck Area) 누적 및 갱신 로직 구현
  * feature_purpose: '추가' 클릭 시 Dummy 덱 리스트에 슬라이드를 누적하고, 우측 ListView에 실시간으로 반영/삭제가 정상 작동하는지 확인
  * feature_range: `src/ui/views/slide_builder.py` 우측 패널 및 상태 이벤트
