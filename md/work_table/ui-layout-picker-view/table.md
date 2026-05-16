# UI Layout Picker View Task

* purpose: `md/spec/ui/layout_picker_view.md` 명세에 따른 가용 레이아웃 선택 화면 구축 (Dummy 연동)
* range: `src/ui/views/layout_picker.py` 및 관련 컴포넌트

## Task List
* [ ] Feature 1: Dummy 레이아웃 목록 GridView 갤러리 렌더링
  * feature_purpose: 더미 상태에서 가져온 레이아웃 정보들을 카드로 시각화하여 `ft.GridView` 기반 갤러리 뷰로 배치
  * feature_range: `src/ui/views/layout_picker.py` 메인 레이아웃

* [ ] Feature 2: 카드 선택 이벤트 및 뷰 전환 연동
  * feature_purpose: 카드를 선택했을 때 선택된 인덱스 상태값을 기록하고 `Slide Builder View`로 정상적으로 진입하는 라우팅 검증
  * feature_range: `src/ui/views/layout_picker.py` 이벤트 로직
