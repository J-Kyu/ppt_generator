# Core Layer: Schema Specification

이 문서는 `Pydantic` 모델을 기반으로 하며 서비스 내에서 돌아다니는 데이터의 뼈대(구조)와 무결성 검증 규칙을 정의합니다. 워크플로우 변경에 따라 **'제공되는 레이아웃 템플릿 정보'**와 **'사용자가 문구를 채워 조립해 낸 실제 슬라이드 데이터'**를 명확히 구분하여 설계했습니다.

---

## 1. 개별 요소 단위 모델 (최하위 노드)

### `ShapeSchema` (BaseModel)
슬라이드나 레이아웃 템플릿 내부에 위치하는 개별 텍스트 박스, 이미지 등 편집 가능한 구역을 정의하는 최소 단위입니다.
- **필드 구성:**
  - `shape_name` (str): PPT 원본에서 추출된 텍스트 상자 이름 (예: "Title 1", "Content Placeholder"). 동적 폼을 그릴 때 입력창의 라벨(Label) 역할로 직결됩니다.
  - `shape_id` (Optional[str/int]): `python-pptx`에서 내부적으로 식별하기 위한 고유 ID.
  - `shape_type` (str): "TEXT" 형태를 기본으로 지원하며 향후 확장("IMAGE" 등)에 대비.
  - `default_text` (str): 템플릿 원본 레이아웃에 써있던 더미 텍스트 구문 (UI에서 Placeholder로 활용하기 좋음).
  - `user_input` (Optional[str]): **초기에는 빈값(`None`)이지만, 사용자가 폼에 직접 타자를 쳐 입력하면 이 필드에 문자열이 저장됩니다.**
  - `is_required` (bool): 폼 유효성 검사 기준점. 향후 무조건 필수값 등으로 제어할 때 사용.

---

## 2. 템플릿 정의 모델 (Read-Only)

### `LayoutSchema` (BaseModel)
1단계 분석(`analyze_ppt()`) 직후 엔진에서 반환하는 결과물입니다. 2단계 가용 레이아웃 선택 화면을 그리기 위해 사용됩니다.
- **필드 구성:**
  - `layout_name` (str): PPT 레이아웃 이름 (예: "제목 슬라이드", "본문 슬라이드").
  - `layout_index` (int): 엔진이 PPT를 생성할 때 몇 번째 레이아웃을 복사해야 하는지 맵핑해주는 고유 슬라이드 인덱스.
  - `shapes` (List[`ShapeSchema`]): 해당 레이아웃이 보유하고 있는 입력 가능한 영역(`ShapeSchema`)의 배열. 여기서는 `ShapeSchema.user_input`이 빈 공간으로 제공됩니다.

---

## 3. 사용자 조립 슬라이드 모델 (Mutable)

### `SlideSchema` (BaseModel)
사용자가 3단계에서 위 `LayoutSchema` 뼈대 중 하나를 선택(Clone)하여, 실제로 데이터를 채워 넣음으로써 **생성을 기다리고 있는 하나의 슬라이드 장본인**입니다.
- **필드 구성:**
  - `target_layout_index` (int): 이 슬라이드를 생성할 때 기반이 될 레이아웃의 원본 인덱스. (엔진이 새 슬라이드를 추가할 때 기준이 됨)
  - `shapes` (List[`ShapeSchema`]): `user_input` 필드 값들이 빈틈없이 꽉 채워진 형태 요소들의 배열.
- **내부 무결성 검증 (Pydantic Validators):**
  - 생성하기 직전에, 내부 `shapes`를 하나씩 돌면서 `is_required == True`인 요소의 `user_input`에 데이터가 비어있지는 않은지 자체적으로 검증하며 튕겨내는 로직(메서드)을 가집니다. 

---

## 💡 종합 요약
- **UI 흐름 대응 요약:** 
  1. 엔진 분석 결과 -> `List[LayoutSchema]` 리스트가 상태(state)에 보관.
  2. 사용자가 레이아웃 중 하나를 고름 -> 해당 모델의 모양대로 폼 그림.
  3. 사용자가 입력하고 "추가" 버튼 클릭 -> 완성된 데이터를 지닌 `SlideSchema`가 하나 생성되어 장바구니(`user_deck: List[SlideSchema]`) 배열에 .append() 됨!
