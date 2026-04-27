# Onboarding View 상세 설계 명세

> 참조: `md/spec/ui/views_spec.md` - Section 1. Onboarding View

---

## 1. 화면 개요

| 항목 | 내용 |
|------|------|
| 파일 경로 | `src/ui/views/onboarding.py` |
| 라우트 | `/` |
| 클래스명 | `OnboardingView(ft.View)` |
| 진입 조건 | 앱 최초 실행 또는 "새 문서 시작하기" 복귀 시 |
| 다음 화면 | `/layout_picker` (분석 성공 시 자동 전환) |

---

## 2. 화면 레이아웃 구조

```
┌─────────────────────────────────────────────────┐
│                  AppBar (없음)                   │
├─────────────────────────────────────────────────┤
│                                                  │
│         [앱 타이틀]  PPT Layout Builder           │
│         [서브 텍스트] 분석할 PPTX 템플릿 파일을    │
│                       선택해주세요                │
│                                                  │
│   ┌─────────────────────────────────────────┐   │
│   │                                         │   │
│   │      📄 Drop File Here  (Drop Zone)     │   │
│   │      or click to select a file          │   │
│   │                                         │   │
│   └─────────────────────────────────────────┘   │
│                                                  │
│          [버튼] Select Template PPTX             │
│                                                  │
│   ┌─────────────────────────────────────────┐   │
│   │ 📎 선택된 파일 (파일 선택 전: 숨김)      │   │
│   │  /Users/.../template.pptx               │   │
│   └─────────────────────────────────────────┘   │
│                                                  │
│          [ProgressRing - 기본 숨김]              │
│          [상태 텍스트 - 기본 빈 문자열]           │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 3. Flet 컴포넌트 상세 명세

### 3-1. `ft.FilePicker` (파일 선택 서비스)

| 속성 / 메서드 | 설명 |
|---|---|
| 인스턴스 생성 | `ft.FilePicker()` (on_result 콜백은 구 버전 API이므로 미사용) |
| `page.overlay.append(picker)` | FilePicker는 반드시 overlay에 등록해야 동작함 |
| `await picker.pick_files(...)` | `async` 함수 내에서 `await`로 호출하여 결과 반환 대기 |
| `file_type` | `ft.FilePickerFileType.CUSTOM` |
| `allowed_extensions` | `["pptx"]` |
| 반환 타입 | `List[ft.FilePickerFile]` 또는 `None` (취소 시) |

> **설계 포인트:** Flet 0.80+ 부터 `pick_files()`가 `async` 함수로 변경됨. 이벤트 핸들러를 `async def`로 선언하고 내부에서 `await`를 사용해야 함.

```python
async def on_select_clicked(self, e):
    files = await self._picker.pick_files(
        file_type=ft.FilePickerFileType.CUSTOM,
        allowed_extensions=["pptx"]
    )
    if files:
        await self._handle_file(files[0].path, files[0].name)
    else:
        self._set_status("파일 선택이 취소되었습니다.", is_error=False)
        self._page.update()
```

---

### 3-2. Drop Zone (`ft.Container`)

드래그 앤 드롭 영역의 시각적 구성 요소입니다. (※ Flet 데스크탑은 현재 OS 수준의 드래그 앤 드롭을 완전히 지원하지 않으므로, 초기 MVP에서는 **클릭 시 FilePicker 실행**으로 동작하되 디자인은 Drop Zone 형태로 유지합니다.)

| 속성 | 값 |
|---|---|
| `width` | 400 |
| `height` | 200 |
| `border` | `ft.border.all(2, ft.Colors.BLUE_200)` |
| `border_radius` | 12 |
| `bgcolor` | `ft.Colors.BLUE_50` |
| `on_click` | `on_select_clicked` 연결 |
| `ink` | `True` (클릭 리플 효과) |

내부 컨텐츠 (`ft.Column` → 중앙 정렬):
- `ft.Icon(ft.Icons.UPLOAD_FILE, size=48, color=ft.Colors.BLUE_300)`
- `ft.Text("파일을 여기에 드래그하거나 클릭하세요", size=14, color=ft.Colors.GREY_600)`
- `ft.Text(".pptx 파일만 지원합니다", size=12, color=ft.Colors.GREY_400)`

---

### 3-3. `ft.ElevatedButton` (파일 선택 버튼)

Drop Zone 아래에 보조 수단으로 배치하는 명시적 버튼입니다.

| 속성 | 값 |
|---|---|
| `text` | `"파일 선택하기"` |
| `icon` | `ft.Icons.FOLDER_OPEN` |
| `on_click` | `on_select_clicked` (Drop Zone과 동일 핸들러) |
| `style` | `ft.ButtonStyle(padding=16)` |

---

### 3-4. `ft.Container` + `ft.Text` (선택된 파일 경로 표시 박스)

파일이 선택된 직후에만 나타나는 경로 표시 박스입니다. 파일 선택 전에는 `visible=False`로 숨겨져 있으며, 파일이 선택되는 순간 경로 정보를 담아 표시됩니다.

| 속성 | 값 |
|---|---|
| 초기 `visible` | `False` |
| 파일 선택 후 `visible` | `True` |
| `bgcolor` | `ft.Colors.GREEN_50` |
| `border` | `ft.border.all(1, ft.Colors.GREEN_300)` |
| `border_radius` | 8 |
| `padding` | 12 |

내부 컨텐츠 (`ft.Row`):
- `ft.Icon(ft.Icons.ATTACH_FILE, size=16, color=ft.Colors.GREEN_700)`
- `ft.Column`:  
  - `ft.Text("선택된 파일", size=11, color=ft.Colors.GREEN_700, weight=BOLD)`  
  - `ft.Text(value=file_path, size=12, color=ft.Colors.GREY_800)` ← 동적으로 업데이트

> **설계 포인트:** 경로가 매우 길 수 있으므로 `ft.Text`에 `overflow=ft.TextOverflow.ELLIPSIS`와 `max_lines=1`을 적용합니다.

---


파일 분석 중(`analyze_ppt()` 호출 시)에만 표시됩니다.

| 속성 | 값 |
|---|---|
| `visible` | 초기값 `False`, 분석 시작 시 `True` |
| `width` | 32 |
| `height` | 32 |
| `stroke_width` | 3 |

---

### 3-6. `ft.Text` (상태 메시지)

성공/실패/취소 메시지를 동적으로 출력합니다.

| 상태 | `value` 예시 | `color` |
|---|---|---|
| 초기 | `""` | - |
| 분석 중 | `"분석 중입니다... filename.pptx"` | `ft.Colors.BLUE_600` |
| 성공 | `"분석 완료! 레이아웃 N개가 발견되었습니다."` | `ft.Colors.GREEN_600` |
| 오류 | `"오류: {에러 메시지}"` | `ft.Colors.RED_600` |
| 취소 | `"파일 선택이 취소되었습니다."` | `ft.Colors.GREY_600` |

---

## 4. 상태 제어 흐름 (State Flow)

```
[앱 시작]
   │
   ▼
[OnboardingView 렌더링]
   │  ProgressRing.visible = False
   │  status_text.value = ""
   │  path_box.visible = False      ← 초기 경로 박스 숨김
   ▼
[사용자: 버튼/드롭존 클릭]
   │
   ▼
[FilePicker.pick_files() await 호출]
   │
   ├─── 취소 ──► status_text 업데이트 (취소 메시지)
   │             path_box.visible 변경 없음
   │
   └─── 파일 선택됨
           │
           ▼
        [ProgressRing.visible = True]
        [status_text = "분석 중..."]
        [page.update()]
           │
           ▼
        [await asyncio.to_thread(analyze_ppt, path)]  ← 블로킹 방지
           │
           ├─── PPTAnalyzeError ──► 에러 메시지 표시
           │                        ProgressRing.visible = False
           │
           └─── 성공
                   │
                   ▼
                [app_state.initialize_session(path, layouts)]
                [ProgressRing.visible = False]
                [status_text = "완료!"]
                [page.update()]
                   │
                   ▼
                [page.go("/layout_picker")]
```

---

## 5. 코드 설계 가이드

### 5-1. 클래스 스켈레톤

```python
import asyncio
import flet as ft
from src.core.engine import analyze_ppt, PPTAnalyzeError
from src.state.app_state import app_state

class OnboardingView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/")
        self._page = page
        self._build_components()
        self._register_overlay()
        self._build_layout()

    def _build_components(self):
        """재사용 가능한 컴포넌트 초기화"""
        self._picker = ft.FilePicker()
        self._spinner = ft.ProgressRing(visible=False, width=32, height=32, stroke_width=3)
        self._status = ft.Text("", size=13)
        self._drop_zone = self._create_drop_zone()
        self._select_btn = ft.ElevatedButton(
            "파일 선택하기",
            icon=ft.Icons.FOLDER_OPEN,
            on_click=self.on_select_clicked
        )
        # 파일 경로 표시 텍스트 및 박스 초기화
        self._path_text = ft.Text(
            "",
            size=12,
            color=ft.Colors.GREY_800,
            overflow=ft.TextOverflow.ELLIPSIS,
            max_lines=1,
            expand=True
        )
        self._path_box = ft.Container(
            visible=False,
            bgcolor=ft.Colors.GREEN_50,
            border=ft.border.all(1, ft.Colors.GREEN_300),
            border_radius=8,
            padding=12,
            content=ft.Row([
                ft.Icon(ft.Icons.ATTACH_FILE, size=16, color=ft.Colors.GREEN_700),
                ft.Column([
                    ft.Text("선택된 파일", size=11, color=ft.Colors.GREEN_700,
                            weight=ft.FontWeight.BOLD),
                    self._path_text
                ], expand=True, spacing=2)
            ], spacing=8)
        )

    def _register_overlay(self):
        """FilePicker는 반드시 overlay에 등록"""
        if self._picker not in self._page.overlay:
            self._page.overlay.append(self._picker)

    def _build_layout(self):
        """레이아웃 조립 및 controls에 추가"""
        self.controls.extend([...])

    def _create_drop_zone(self) -> ft.Container:
        """Drop Zone 컴포넌트 생성 및 반환"""
        ...

    def _set_status(self, message: str, color=ft.Colors.GREY_600, is_error=False):
        """상태 텍스트와 색상을 한 번에 업데이트하는 헬퍼 메서드"""
        self._status.value = message
        self._status.color = ft.Colors.RED_600 if is_error else color

    def _show_selected_path(self, file_path: str):
        """경로 표시 박스를 업데이트하고 표시"""
        self._path_text.value = file_path
        self._path_box.visible = True

    async def on_select_clicked(self, e):
        """파일 선택 이벤트 핸들러 (async)"""
        files = await self._picker.pick_files(
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["pptx"]
        )
        if not files:
            self._set_status("파일 선택이 취소되었습니다.")
            self._page.update()
            return
        await self._handle_file(files[0].path, files[0].name)

    async def _handle_file(self, file_path: str, file_name: str):
        """선택된 파일에 대한 분석 처리"""
        self._show_selected_path(file_path)   # ← 파일 선택 즉시 경로 박스 표시
        self._spinner.visible = True
        self._set_status(f"분석 중입니다... {file_name}", ft.Colors.BLUE_600)
        self._page.update()
        try:
            # analyze_ppt는 동기 함수이므로 블로킹 방지를 위해 스레드에서 실행
            layouts = await asyncio.to_thread(analyze_ppt, file_path)
            app_state.initialize_session(file_path, layouts)
            self._set_status(
                f"분석 완료! 레이아웃 {len(layouts)}개가 발견되었습니다.",
                ft.Colors.GREEN_600
            )
        except PPTAnalyzeError as e:
            self._set_status(str(e), is_error=True)
        except Exception as e:
            self._set_status(f"예기치 못한 오류: {e}", is_error=True)
        finally:
            self._spinner.visible = False
            self._page.update()

        if app_state.available_layouts:
            self._page.go("/layout_picker")
```

### 5-2. 비동기 처리 주의사항

| 항목 | 내용 |
|---|---|
| `pick_files()` | `async def` 핸들러 안에서 `await` 필수 |
| `analyze_ppt()` | 동기 함수이므로 `await asyncio.to_thread(fn, arg)` 로 실행하여 UI 쓰레드 블로킹 방지 |
| `page.update()` | 상태 변경 후 반드시 호출해야 UI 반영됨 |
| `page.go()` | 분석 완료 후 라우팅. `go()`가 deprecated인 경우 `push_route()` 대안 검토 |

### 5-3. 컴포넌트 분리 원칙

- `_build_components()`, `_build_layout()` 로 초기화 단계를 분리하여 코드 가독성 확보
- `_set_status()` 헬퍼를 통해 상태 텍스트 변경 로직 중복 제거
- Drop Zone은 `_create_drop_zone()` 팩토리 메서드로 추출하여 독립적으로 관리

---

## 6. 에러 처리 시나리오

| 시나리오 | 처리 방법 |
|---|---|
| 파일 선택 취소 | 상태 메시지만 표시, 화면 전환 없음 |
| `.pptx`가 아닌 파일 | OS 레벨에서 필터링 (`allowed_extensions`), 추가 검증 불필요 |
| 파일 경로 없음 (웹 환경) | `files[0].path`가 `None`일 수 있으므로 `None` 체크 후 안내 메시지 |
| `PPTAnalyzeError` | 에러 내용을 빨간 상태 텍스트로 표시, 스피너 종료 |
| 예외 발생 | `except Exception`으로 포착 후 사용자 친화적 메시지 표시 |
