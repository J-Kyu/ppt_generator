# Export & Result View 상세 설계 명세

> 참조: `md/spec/ui/views_spec.md` - Section 4. Export & Result View

---

## 1. 화면 개요

| 항목 | 내용 |
|------|------|
| 파일 경로 | `src/ui/views/export.py` |
| 라우트 | `/export` |
| 클래스명 | `ExportView(ft.View)` |
| 진입 조건 | `LayoutPickerView` 또는 `SlideBuilderView`에서 "Build & Export" 버튼을 클릭했을 때 |
| 다음 화면 | `/` (Onboarding View, "새 문서 시작하기" 클릭 시 초기화 후 이동) |
| 핵심 역할 | 사용자가 누적한 슬라이드 대기열(Deck) 데이터를 실제 `.pptx` 파일로 생성(굽기)하고, 완료 상태 및 후속 액션(파일 열기, 초기화)을 제공하는 최종 단계 화면 |

---

## 2. 화면 레이아웃 구조

이 화면은 '생성 진행 중(Loading)' 상태와 '생성 완료(Success)' 상태로 나뉘어 동적으로 렌더링됩니다.

### 2-1. 초기 진입 & 진행 중 (Loading State)

```text
┌─────────────────────────────────────────────────┐
│ [← Back to Builder]                             │
├─────────────────────────────────────────────────┤
│                                                  │
│                                                  │
│             [ 진행 스피너 / 아이콘 ]                 │
│                                                  │
│         [타이틀] Generating Presentation...         │
│         [서브] N개의 슬라이드를 조립하는 중입니다.        │
│                                                  │
│         [ Progress Bar (무한 반복) ]               │
│                                                  │
│                                                  │
└─────────────────────────────────────────────────┘
```

### 2-2. 생성 완료 (Success State)

```text
┌─────────────────────────────────────────────────┐
│                                                 │
├─────────────────────────────────────────────────┤
│                                                  │
│                                                  │
│               [ ✅ 성공 아이콘 ]                   │
│                                                  │
│         [타이틀] Export Successful!               │
│         [서브] 프레젠테이션 생성이 완료되었습니다.        │
│                                                  │
│         [ 생성된 파일 경로 텍스트 표기 ]               │
│                                                  │
│         [ 📂 완성된 폴더 열기 ]                     │
│         [ 🔄 새 문서 시작하기 ]                     │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 3. Flet 컴포넌트 상세 명세

### 3-1. `ft.ProgressBar` / `ft.ProgressRing` (진행 상태)

PPT 생성 작업은 I/O 및 파싱 로직으로 인해 수 초 이상 소요될 수 있으므로, 사용자에게 시각적 대기 상태를 제공합니다.

| 속성 / 동작 | 설명 |
|---|---|
| `visible` | 작업 중에는 `True`, 작업 완료 또는 실패 시 `False` |
| `value` | 명확한 퍼센트 계산이 어려울 경우 `None`(Indeterminate, 무한 로딩 바)으로 설정하여 "작업 중"임을 강조합니다. |

### 3-2. 성공 피드백 영역 (`ft.Icon` 및 `ft.Text`)

작업이 완료되었을 때 화면 중앙에 표시되는 축하 메시지 및 시각 요소입니다.

| 컴포넌트 | 설명 |
|---|---|
| `ft.Icon(ft.Icons.CHECK_CIRCLE)` | 크고 명확한 녹색 아이콘으로 성공을 직관적으로 알립니다. |
| `ft.Text` (타이틀/서브) | 완료 안내 메시지 및 생성된 총 슬라이드 수를 출력합니다. |
| `ft.Text` (경로) | 사용자가 결과물이 어디에 저장되었는지 확인할 수 있도록 절대 경로를 보여줍니다. |

### 3-3. 후속 액션 버튼 (`ft.ElevatedButton` / `ft.TextButton`)

| 버튼 | 기능 | 동작 방식 |
|---|---|---|
| `Open Folder` 버튼 | 생성된 파일이 위치한 폴더를 엽니다. | Mac의 경우 `subprocess.run(['open', '-R', path])`, Windows의 경우 `os.startfile(dir)` 사용 |
| `Start Over` 버튼 | 모든 작업을 마치고 초기 상태로 돌아갑니다. | 전역 `app_state.reset()` 호출 후 `page.push_route("/", clear=True)`로 이동 |

---

## 4. 상태 제어 흐름 (State Flow)

```text
[화면 진입 (/export)]
   │
   ▼
[app_state.user_deck 비어있는지 확인]
   │ (비어있으면 에러 텍스트 표기 후 중단)
   ▼
[Loading 상태 렌더링 (ProgressBar 노출)]
[page.update()]
   │
   ▼
[await asyncio.to_thread(generate_ppt, ...)]  ← 백그라운드 스레드에서 PPT 생성 (UI 블로킹 방지)
   │
   ├─── (실패) ──► 에러 아이콘 및 에러 메시지 렌더링 (Red Text)
   │
   └─── (성공)
           │
           ▼
        [Loading 컴포넌트들을 Success 컴포넌트(아이콘, 파일 경로, 버튼 2개)로 갱신]
        [page.update()]
           │
           ├─── "Open Folder" 클릭 시 OS 명령어 호출
           │
           └─── "Start Over" 클릭 시 app_state 초기화 후 OnboardingView로 라우팅
```

---

## 5. 코드 설계 가이드

### 5-1. 클래스 스켈레톤

```python
import os
import sys
import asyncio
import subprocess
import flet as ft
from src.state.app_state import app_state
from src.core.engine import generate_ppt

class ExportView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/export")
        self._page = page
        
        # 저장될 기본 경로 설정 (예: 바탕화면)
        self.output_path = os.path.join(os.path.expanduser("~"), "Desktop", "output_presentation.pptx")
        
        self._build_components()
        self._build_layout()
        
        # 화면 진입 시 자동으로 생성 로직 시작 (Event Loop에 예약)
        # Flet에서는 did_mount() 훅을 지원하지 않는 경우가 많으므로,
        # 생성자 끝에서 바로 비동기 태스크를 트리거하는 패턴을 사용합니다.
        if len(app_state.user_deck) > 0:
            asyncio.create_task(self.run_generation_task())

    def _build_components(self):
        # 1. Loading Components
        self.loading_spinner = ft.ProgressRing(width=40, height=40, stroke_width=4)
        self.loading_text = ft.Text("Generating Presentation...", size=20, weight=ft.FontWeight.BOLD)
        self.loading_subtext = ft.Text("이 작업은 수 초 정도 걸릴 수 있습니다.", color=ft.Colors.GREY_600)
        
        self.loading_container = ft.Column(
            [self.loading_spinner, self.loading_text, self.loading_subtext],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            visible=True
        )
        
        # 2. Success Components
        self.success_icon = ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500, size=60)
        self.success_text = ft.Text("Export Successful!", size=24, weight=ft.FontWeight.BOLD)
        self.path_text = ft.Text(self.output_path, size=14, color=ft.Colors.GREY_700, selectable=True)
        
        self.open_btn = ft.ElevatedButton("Open Folder", icon=ft.Icons.FOLDER, on_click=self.on_open_folder)
        self.restart_btn = ft.TextButton("Start Over (New Document)", icon=ft.Icons.REFRESH, on_click=self.on_start_over)
        
        self.success_container = ft.Column(
            [self.success_icon, self.success_text, self.path_text, ft.Divider(), self.open_btn, self.restart_btn],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            visible=False
        )

    def _build_layout(self):
        # 메인 컨테이너 조립 (가운데 정렬)
        main_content = ft.Container(
            content=ft.Column(
                [self.loading_container, self.success_container],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            expand=True,
            alignment=ft.alignment.Alignment(0, 0) # 중앙 정렬
        )
        
        self.controls.extend([
            ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: self._page.push_route("/slide_builder"))]),
            main_content
        ])

    async def run_generation_task(self):
        """PPT 생성 엔진 비동기 호출"""
        try:
            # 엔진 실행 (블로킹 함수이므로 to_thread 사용)
            await asyncio.to_thread(
                generate_ppt,
                app_state.template_path,
                app_state.user_deck,
                self.output_path
            )
            
            # 성공 시 컴포넌트 전환
            self.loading_container.visible = False
            self.success_container.visible = True
            
        except Exception as e:
            # 실패 시 에러 처리
            self.loading_spinner.visible = False
            self.loading_icon = ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED_500, size=60)
            self.loading_text.value = "Generation Failed!"
            self.loading_text.color = ft.Colors.RED_500
            self.loading_subtext.value = str(e)
            
        finally:
            self._page.update()

    def on_open_folder(self, e):
        """저장된 경로 열기 (크로스 플랫폼 지원)"""
        path = self.output_path
        if sys.platform == "darwin":  # macOS
            subprocess.run(["open", "-R", path])
        elif sys.platform == "win32": # Windows
            os.startfile(os.path.dirname(path))
        else:                         # Linux
            subprocess.run(["xdg-open", os.path.dirname(path)])

    def on_start_over(self, e):
        """전체 데이터 초기화 및 Onboarding으로 회귀"""
        app_state.reset() # 앱 상태를 초기화하는 메서드를 AppState 클래스에 구현 필요
        self._page.push_route("/", clear=True)
```

### 5-2. Flet 동작 최적화 및 유의사항

- **`asyncio.create_task` 활용:** 화면에 진입하자마자 무거운 `generate_ppt` 로직을 동기적으로 호출하면, 로딩 바(`ProgressBar`)가 미처 렌더링되기도 전에 앱 화면이 멈춰버리는 현상(White Screen Freeze)이 발생합니다. 반드시 뷰가 로드된 이후 백그라운드 태스크로 구동하여 UI 반응성을 유지해야 합니다.
- **크로스 플랫폼 파일 열기:** Python의 `os.startfile()`은 Windows 전용이므로, Mac 환경을 지원하기 위해 `sys.platform == "darwin"` 조건분기와 `subprocess.run(["open"])` 시스템 콜 처리를 추가했습니다.
- **State Clear:** "새 문서 시작하기" 버튼을 눌렀을 때, 이전 작업 이력이 남아있으면 치명적인 버그가 발생할 수 있습니다. `app_state` 내부에 `reset()` 같은 메서드를 미리 구성하여 `template_path`, `available_layouts`, `user_deck`을 완전히 비우는 로직이 필수입니다.
