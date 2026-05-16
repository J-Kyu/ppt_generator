# Slide Builder View 상세 설계 명세

> 참조: `md/spec/ui/views_spec.md` - Section 3. Slide Builder View

---

## 1. 화면 개요

| 항목 | 내용 |
|------|------|
| 파일 경로 | `src/ui/views/slide_builder.py` |
| 라우트 | `/slide_builder` |
| 클래스명 | `SlideBuilderView(ft.View)` |
| 진입 조건 | `LayoutPickerView`에서 특정 레이아웃 카드를 클릭했을 때 |
| 다음 화면 | `/layout_picker` (다른 레이아웃 선택) 또는 `/export` (최종 빌드) |
| 핵심 역할 | 선택된 레이아웃 스키마에 맞춰 동적 폼을 생성하고, 입력값을 받아 슬라이드 대기열(Deck)에 추가하는 메인 작업 공간 |

---

## 2. 화면 레이아웃 구조

본 화면은 화면을 좌우(Left / Right) 패널로 분할하여 작업 영역과 결과 확인 영역을 동시에 제공합니다.

```text
┌───────────────────────────────────────────────────────────┐
│ [← Back to Layouts]                                       │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  [ Left Panel : Form Area ]  │ [ Right Panel : Deck Area ]│
│                              │                            │
│  Build: Title and Content    │  Your Slide Deck           │
│  ────────────────────────    │  ────────────────────────  │
│                              │                            │
│  Title (Text Box)            │  1. Title and Content      │
│  ┌──────────────────────┐    │     [2 inputs]   [🗑️]      │
│  │ Enter title...       │    │                            │
│  └──────────────────────┘    │  2. Title Only             │
│                              │     [1 inputs]   [🗑️]      │
│  Content (Text Box)          │                            │
│  ┌──────────────────────┐    │                            │
│  │ Enter content...     │    │                            │
│  │                      │    │                            │
│  └──────────────────────┘    │                            │
│                              │                            │
│  [에러 메시지 표시 영역]         │                            │
│  [ ➕ Add Slide to Deck ]    │                            │
│                              │                            │
│                              │  [ 🚀 Build & Export ]     │
└───────────────────────────────────────────────────────────┘
```

---

## 3. Flet 컴포넌트 상세 명세

### 3-1. Left Panel (`ft.Column` + 동적 `ft.TextField`)

사용자가 슬라이드 내용을 입력하는 폼 영역입니다.

| 속성 / 동작 | 설명 |
|---|---|
| **동적 생성** | `app_state.available_layouts[current_index].shapes` 배열을 순회하여 각 도형(Shape) 개수만큼 `ft.TextField`를 동적으로 생성합니다. |
| `ft.TextField` | `label`속성에는 도형의 이름(예: Title 1), `multiline=True`를 적용하여 긴 텍스트 입력을 지원합니다. |
| **유효성 검사** | '추가' 버튼 클릭 시 `Schema`의 필수값 검증을 거치며, 실패 시 텍스트 필드 하단에 붉은색 경고 메시지(`ft.Text`)를 노출합니다. |
| `ft.ElevatedButton` | "Add Slide to Deck" 버튼. 클릭 시 입력된 데이터를 수집하여 덱에 누적합니다. |

### 3-2. Right Panel (`ft.ListView` + `ft.ListTile`)

지금까지 사용자가 추가한 슬라이드 목록을 실시간으로 보여주는 장바구니/대기열 영역입니다.

| 속성 / 동작 | 설명 |
|---|---|
| `ft.ListView` | 스크롤이 가능한 리스트 뷰 컨테이너 (`expand=1` 적용) |
| `ft.ListTile` | 각 슬라이드 아이템을 표현합니다. <br> - `leading`: 슬라이드 번호 (1, 2, 3...) <br> - `title`: 사용된 레이아웃 이름 <br> - `trailing`: 삭제(`ft.IconButton(ft.Icons.DELETE)`) 버튼 |
| **상태 동기화** | 슬라이드가 추가되거나 삭제될 때마다 `self._update_deck_view()`를 호출하여 리스트를 다시 그립니다. |

---

## 4. 상태 제어 흐름 (State Flow)

```text
[화면 진입]
   │
   ▼
[app_state.current_selected_layout_index 확인]
   │ (None인 경우 에러 처리 후 /layout_picker 로 반환)
   ▼
[해당 레이아웃의 Shape 목록을 기반으로 TextField 리스트 동적 생성]
[Left Panel 렌더링] & [Right Panel(Deck) 기존 데이터 렌더링]
   │
   ▼
[사용자 데이터 입력 후 'Add Slide' 클릭]
   │
   ▼
[각 TextField의 value를 수집하여 SlideSchema 객체 임시 생성]
   │
   ├─── (검증 실패) ──► 에러 메시지 노출 (Red Text)
   │
   └─── (검증 성공)
           │
           ▼
        [app_state.add_slide_to_deck(SlideSchema) 호출]
        [TextField 입력값 초기화 (비우기)]
        [Right Panel ListView 새로고침]
           │
           ▼
[사용자가 Export 버튼 클릭 시 page.push_route("/export") 로 이동]
```

---

## 5. 코드 설계 가이드

### 5-1. 클래스 스켈레톤

```python
import flet as ft
from src.state.app_state import app_state
from src.core.schema import SlideSchema
import copy

class SlideBuilderView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/slide_builder")
        self._page = page
        self.scroll = ft.ScrollMode.AUTO
        
        # 레이아웃이 선택되지 않은 상태로 강제 진입 시 방어 로직
        if app_state.current_selected_layout_index is None:
            self._page.push_route("/layout_picker")
            return
            
        self.layout_schema = app_state.available_layouts[app_state.current_selected_layout_index]
        # 입력받을 원본 shape 데이터를 훼손하지 않기 위해 깊은 복사 사용
        self.cloned_shapes = copy.deepcopy(self.layout_schema.shapes)
        
        self._build_components()
        self._build_layout()
        self._update_deck_view() # 초기 덱 상태 렌더링

    def _build_components(self):
        # 폼 필드 리스트 
        self.text_fields = []
        self.form_column = ft.Column(spacing=15, expand=1)
        
        for idx, shape in enumerate(self.cloned_shapes):
            tf = ft.TextField(
                label=shape.shape_name,
                hint_text="내용을 입력하세요...",
                multiline=True,
                min_lines=1,
                max_lines=5
            )
            self.text_fields.append((idx, tf))
            self.form_column.controls.append(tf)
            
        self.error_text = ft.Text("", color=ft.Colors.RED_600)
        self.deck_listview = ft.ListView(expand=1, spacing=10)

    def _build_layout(self):
        # Left Panel 구성
        left_panel = ft.Container(
            content=ft.Column([
                ft.Text(f"Build: {self.layout_schema.layout_name}", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                self.form_column,
                self.error_text,
                ft.ElevatedButton("Add Slide to Deck", on_click=self.on_add_slide, icon=ft.Icons.ADD)
            ], scroll=ft.ScrollMode.AUTO),
            expand=1, padding=20
        )
        
        # Right Panel 구성
        right_panel = ft.Container(
            content=ft.Column([
                ft.Text("Your Slide Deck", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                self.deck_listview,
                ft.ElevatedButton("Build & Export", on_click=lambda _: self._page.push_route("/export"), icon=ft.Icons.ROCKET_LAUNCH)
            ]),
            expand=1, padding=20,
            border=ft.border.only(left=ft.border.BorderSide(1, ft.Colors.GREY_300))
        )
        
        self.controls.extend([
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: self._page.push_route("/layout_picker")),
                ft.Text("Back to Layouts")
            ]),
            ft.Row([left_panel, right_panel], expand=True, vertical_alignment=ft.CrossAxisAlignment.START)
        ])

    def _update_deck_view(self):
        """Right Panel의 슬라이드 목록(Deck)을 최신화합니다."""
        self.deck_listview.controls.clear()
        if not app_state.user_deck:
            self.deck_listview.controls.append(ft.Text("Your deck is empty.", color=ft.Colors.GREY_500))
        else:
            for i, slide in enumerate(app_state.user_deck):
                layout_name = app_state.available_layouts[slide.target_layout_index].layout_name
                self.deck_listview.controls.append(
                    ft.ListTile(
                        leading=ft.CircleAvatar(content=ft.Text(str(i+1))),
                        title=ft.Text(f"Slide {i+1}: {layout_name}"),
                        trailing=ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=self._create_delete_handler(i))
                    )
                )
        self._page.update()

    def _create_delete_handler(self, index: int):
        """삭제 버튼 클릭 시 호출될 클로저 핸들러"""
        def on_delete(e):
            app_state.remove_slide_from_deck(index)
            self._update_deck_view()
        return on_delete

    def on_add_slide(self, e):
        """Add Slide 버튼 클릭 핸들러"""
        # 1. 입력값 수집
        for idx, tf in self.text_fields:
            if tf.value.strip():
                self.cloned_shapes[idx].user_input = tf.value
            else:
                self.cloned_shapes[idx].user_input = None

        # 2. Schema 객체 생성 및 검증
        new_slide = SlideSchema(
            target_layout_index=self.layout_schema.layout_index,
            shapes=self.cloned_shapes
        )
        
        try:
            new_slide.check_required_fields()
        except ValueError as err:
            self.error_text.value = str(err)
            self._page.update()
            return
            
        # 3. 덱에 추가 및 UI 초기화
        self.error_text.value = ""
        app_state.add_slide_to_deck(new_slide)
        
        for _, tf in self.text_fields:
            tf.value = ""
            
        # 다음 슬라이드 작성을 위해 shape 데이터 다시 복사
        self.cloned_shapes = copy.deepcopy(self.layout_schema.shapes)
        self._update_deck_view()
```

### 5-2. Flet 동작 최적화 및 유의사항

- **Deep Copy의 필요성:** `self.layout_schema.shapes` 원본을 그대로 수정하면, 동일한 레이아웃으로 두 번째 슬라이드를 만들 때 첫 번째 슬라이드의 텍스트가 그대로 남아있거나 의도치 않은 참조 공유 오류가 발생합니다. 반드시 `copy.deepcopy`를 사용하여 인스턴스를 분리해야 합니다.
- **클로저(Closure)를 활용한 동적 이벤트 할당:** `ListTile`의 삭제 버튼(`DELETE`)에 연결되는 핸들러는 `_create_delete_handler(index)` 팩토리 메서드를 사용하여 정확한 인덱스 스코프를 유지하도록 설계합니다.
- **에러 핸들링:** 입력값이 부족한 경우 에러 메시지를 텍스트 필드 하단에 즉시 표시(`self._page.update()`)하여 사용자가 어느 부분을 놓쳤는지 명확하게 피드백합니다.
