# Purpose
- This project is to understand a sample presentation file(ppt) and make a new presentation file(ppt) with same structure and content.

# Techinical Overview
## 추천 시스템 아키텍처: 파이프라인 기반 계층 구조
- 오프라인 앱의 핵심은 각 단계가 독립적으로 작동하면서도 데이터 정합성을 유지하는 것입니다.
- 파일 처리 계층 (I/O Layer): 로컬 파일 시스템에서 PPTX 파일을 읽고 저장합니다. (python-pptx 활용)
- 분석 엔진 (Analysis Engine): PPT의 XML 구조를 분석하여 레이아웃(좌표, 크기, 텍스트 상자 이름)을 추출하고 이를 내부 데이터 모델(JSON 객체)로 변환합니다.
- 데이터 스토리지 (Local State): 분석된 레이아웃과 사용자가 입력 중인 데이터를 로컬에 임시 저장합니다. (단순 JSON 파일 또는 가벼운 SQLite)
- 동적 UI 레이어 (Interaction Layer): 분석된 JSON 스키마를 바탕으로 사용자 입력 폼을 동적으로 생성합니다.
- 렌더링 엔진 (Generation Engine): 최종 입력 데이터와 원본 레이아웃 템플릿을 결합하여 새로운 PPT를 빌드합니다.

## 단계별 핵심 기술 및 설계 포인트
### PPT 레이아웃 분석 (Analysis Engine)
- PPT의 마스터 슬라이드나 특정 슬라이드의 shapes를 순회하며 속성을 추출해야 합니다.
- 핵심 로직: shape.name, shape.left, shape.top, shape.text 등의 속성을 딕셔너리 형태로 맵핑합니다.
- shape와 text 이외의 속성에 대해서는 현재 지원하지 않지만, 코드 적으로 interface를 만들어나 나중에 구현될 수 있도록 준비한다. 단, 서비스에서는 해당 속성을 사용하지 않는다.
- 팁: 사용자가 폼에서 입력하기 쉽도록 각 텍스트 박스에 'Placeholder'나 'Alt Text'를 미리 지정해두면 분석 단계에서 이를 Key값으로 쓰기 좋습니다.

### 동적 폼 생성 도구 (Form UI)
- "사용자로부터 쉽게 받기 위한 툴"은 JSON Schema 기반의 동적 폼 생성 방식을 추천합니다.
- 설계: 분석된 JSON의 구조에 따라 텍스트 박스, 이미지 업로드 버튼 등을 자동으로 화면에 배치합니다.

### 데이터 직렬화 및 검증
- 사용자가 입력한 데이터를 JSON으로 유지하되, 생성 버튼을 누르기 전 Validation(검증) 단계를 두어 데이터 누락을 방지해야 합니다.


# Recommed Technical Stack
- GUI 프레임워크: Flet (빠른 개발)
- PPT 조작: python-pptx (거의 유일하고 강력한 표준)
- 데이터 관리: Pydantic (JSON 데이터 구조 정의 및 검증용)
- 패키징: PyInstaller
- Python: uv를 통한 python 3.13 버전 사용

# Dev Environment
- Mac과 Windows에 모두 개발 가능하다.

# UI/UX
- UI/UX의 workflow는 다음과 같습니다.
    - 진입 및 파일 업로드 (Onboarding & Upload)
    - 분계 결과 확인 및 구조화
    - 동적 데이터 입력 (Data-Entry)
    - 최종 생성 및 내보내기 (Generate & Export)

# Precautious
- 폰트 및 리소스: 오프라인 앱이므로 템플릿 PPT에 사용된 특수 폰트가 사용자 PC에 없을 경우 레이아웃이 깨질 수 있습니다. 폰트를 함께 배포하거나 시스템 기본 폰트를 사용하도록 설계해야 합니다.
- 이미지 처리: 텍스트 필드뿐만 아니라 이미지 필드도 JSON에 경로(path)로 담아 처리하면 훨씬 확장성 있는 앱이 됩니다.