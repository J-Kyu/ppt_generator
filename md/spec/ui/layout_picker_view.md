# Layout Picker View 상세 설계 명세

> 참조: `md/spec/ui/views_spec.md` - Section 2. Layout Picker View

---

## 1. 화면 개요

| 항목 | 내용 |
|------|------|
| 파일 경로 | `src/ui/views/layout_picker.py` |
| 라우트 | `/layout_picker` |
| 클래스명 | `LayoutPickerView(ft.View)` |
| 진입 조건 | `OnboardingView`에서 PPT 템플릿 분석 성공 후 자동 진입 또는 `SlideBuilderView`에서 "다른 레이아웃 추가하기" 클릭 시 |
| 다음 화면 | `/slide_builder` (레이아웃 선택 시) 또는 `/export` (완료 및 빌드하기 클릭 시) |

---

## 2. 화면 레이아웃 구조

```text
┌─────────────────────────────────────────────────┐
│ [← 뒤로가기 버튼]                                 │
├─────────────────────────────────────────────────┤
│                                                  │
│         [타이틀] Available Layouts                │
│         [서브 텍스트] 원하시는 슬라이드 레이아웃을 선택하세요. │
│                                                  │
│   ┌─────────────────────────────────────────┐   │
│   │                                         │   │
│   │  [Layout Card 1]      [Layout Card 2]   │   │
│   │  ┌────────────┐       ┌────────────┐    │   │
│   │  │ Title      │       │ Title      │    │   │
│   │  │ 3 text box │       │ 1 text box │    │   │
│   │  └────────────┘       └────────────┘    │   │
│   │                                         │   │
│   │  [Layout Card 3]      [Layout Card 4]   │   │
│   │  ┌────────────┐       ┌────────────┐    │   │
│   │  │ Title      │       │ Title      │    │   │
│   │  │ 2 text box │       │ 4 text box │    │   │
│   │  └────────────┘       └────────────┘    │   │
│   │                                         │   │
│   └─────────────────────────────────────────┘   │
│                                                  │
│   [Deck 요약 텍스트] 현재 대기열: N개 슬라이드          │
│   [버튼] View Deck / Export                      │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 3. Flet 컴포넌트 상세 명세

### 3-1. `ft.GridView` (레이아웃 갤러리)

가용 레이아웃 목록을 격자 형태로 표시하는 메인 컨테이너입니다.

| 속성 | 값 |
|---|---|
| `expand` | `1` (남은 공간 모두 차지) |
| `runs_count` | 3 (또는 4, 화면 너비에 따라 조절) |
| `max_extent` | 250 (각 카드의 최대 너비 제한) |
| `child_aspect_ratio` | 1.0 (정사각형 비율) |
| `spacing` / `run_spacing` | 15 |

### 3-2. `ft.Card` (개별 레이아웃 카드)

각 레이아웃의 정보를 시각적으로 분리하고 클릭 이벤트를 받습니다.

| 속성 | 값 |
|---|---|
| `elevation` | 2 |
| 내부 컨텐츠 | `ft.Container(ink=True, on_click=...)` 를 사용하여 클릭 리플 효과 적용 |
| 내용 구성 | `ft.Column` ➔ `ft.Icon(ft.Icons.DASHBOARD)`, `ft.Text(layout_name)`, `ft.Text(f"{shapes_count} text boxes")` |

> **설계 포인트:** 
> 사용자가 레이아웃의 구성을 대략적으로 알 수 있도록 Placeholder 아이콘이나 도형 개수(shapes count) 등의 메타데이터를 함께 표시합니다.

### 3-3. `ft.ElevatedButton` (Export 이동)

지금까지 작성된 슬라이드 덱을 모아 실제 PPT로 내보내는 화면으로 이동합니다.

| 속성 | 값 |
|---|---|
| `text` | `"View Deck ({N} slides) / Export"` |
| `icon` | `ft.Icons.SAVE` |
| `on_click` | `/export` 라우트로 이동 |

### 3-4. `ft.IconButton` (뒤로 가기)

이전 화면(Onboarding)으로 돌아가는 기능입니다. (경고: 기존 덱 내용이 유실될 수 있음을 안내하는 것이 좋습니다)

| 속성 | 값 |
|---|---|
| `icon` | `ft.Icons.ARROW_BACK` |
| `on_click` | `/` 라우트로 이동 (`app_state` 초기화 필요 여부 검토) |

---

## 4. 상태 제어 흐름 (State Flow)

```text
[화면 진입]
   │
   ▼
[app_state.available_layouts 배열 순회]
   │
   ▼
[각 LayoutSchema에 대해 ft.Card 동적 생성]
   │
   ▼
[GridView 렌더링 및 하단 Deck 요약 업데이트]
   │
   ├─── (이벤트) 특정 레이아웃 카드 클릭 시
   │       │
   │       ▼
   │    [app_state.current_selected_layout_index = index]
   │    [page.push_route("/slide_builder")]
   │
   └─── (이벤트) Export 버튼 클릭 시
           │
           ▼
        [page.push_route("/export")]
```

---

## 5. 코드 설계 가이드

### 5-1. 클래스 스켈레톤

```python
import flet as ft
from src.state.app_state import app_state

class LayoutPickerView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/layout_picker")
        self._page = page
        self.scroll = ft.ScrollMode.AUTO
        
        self._build_layout()

    def _build_layout(self):
        """전체 UI 레이아웃 조립"""
        title = ft.Text("Available Layouts", size=28, weight=ft.FontWeight.BOLD)
        desc = ft.Text("사용할 슬라이드 레이아웃을 선택하여 내용을 채워보세요.", size=16, color=ft.Colors.GREY_700)
        
        # GridView 생성
        grid = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=250,
            child_aspect_ratio=1.0,
            spacing=15,
            run_spacing=15,
        )
        
        # app_state에서 레이아웃 데이터를 읽어와 카드 생성
        for idx, layout in enumerate(app_state.available_layouts):
            card = self._create_layout_card(idx, layout)
            grid.controls.append(card)
            
        # 하단 내비게이션 바 (덱 확인 및 추출)
        bottom_nav = ft.Row(
            [
                ft.ElevatedButton(
                    f"View Deck ({len(app_state.user_deck)} slides) / Export", 
                    on_click=lambda _: self._page.push_route("/export"), 
                    icon=ft.Icons.SAVE
                ),
            ],
            alignment=ft.MainAxisAlignment.END
        )

        self.controls.extend([
            ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=self.on_back_clicked)]),
            title,
            desc,
            ft.Container(content=grid, expand=True),
            bottom_nav
        ])

    def _create_layout_card(self, index: int, layout_schema) -> ft.Card:
        """개별 레이아웃 카드 UI 컴포넌트 생성"""
        
        shapes_count = len(layout_schema.shapes)
        
        # 카드 클릭 이벤트 핸들러 생성용 클로저
        def on_card_click(e):
            app_state.current_selected_layout_index = index
            self._page.push_route("/slide_builder")
            
        content = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.DASHBOARD, size=40, color=ft.Colors.BLUE_400),
                    ft.Text(layout_schema.layout_name, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Text(f"{shapes_count} text boxes", size=12, color=ft.Colors.GREY_600),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            ink=True,
            on_click=on_card_click,
            alignment=ft.alignment.Alignment(0, 0)
        )
        
        return ft.Card(content=content, elevation=2)

    def on_back_clicked(self, e):
        """뒤로 가기 처리 로직"""
        # (선택) app_state 초기화 여부 등 확인 로직 추가 가능
        self._page.push_route("/", clear=True)
```

### 5-2. Flet 동작 최적화 포인트

- **GridView 사용:** 레이아웃 종류가 많을 경우 `ListView` 보다 `GridView`를 사용하여 화면 공간을 효율적으로 활용합니다. `max_extent` 속성을 활용하면 반응형(Responsive) 그리드를 쉽게 구현할 수 있습니다.
- **클로저(Closure) 활용:** 루프 안에서 이벤트 핸들러(`on_click`)를 바인딩할 때, Python의 지연 바인딩(Late binding) 문제를 피하기 위해 팩토리 메서드(`_create_layout_card`)를 사용하여 각 카드가 올바른 `index` 값을 캡처하도록 합니다.
- **`push_route` 권장:** Flet 0.80 이상에서는 `go()` 대신 `push_route()` 사용이 권장됩니다.
