# NDS — NOVERA Design System

NOVERA의 디자인 시스템(NDS)을 코드/개발 관점에서 정리한 문서 세트의 **진입점**입니다.

| | |
|---|---|
| 원본 | Figma [NDS - NOVERA Design System](https://www.figma.com/design/OJqTwQ8gHDGcvOOkOfYRgM/NDS---NOVERA-Design-System?node-id=0-1) |
| File key | `OJqTwQ8gHDGcvOOkOfYRgM` |
| 라이브러리명 | `NDS - NOVERA Design System` (Figma 라이브러리) |
| 변수 컬렉션 | `primitive` (예: `number/unit/*`, `color/*`) |
| 조사 방법 | Figma MCP — `get_metadata` / `get_variable_defs` / `get_screenshot` / `search_design_system` |
| 조사일 | 2026-09-02 |

---

## 이 문서 세트를 읽는 법 — 사실과 제안의 구분

이 저장소의 디자인 시스템 문서는 **두 종류의 내용을 물리적으로 분리**합니다.

| 구분 | 표기 | 위치 | 의미 |
|---|---|---|---|
| **Figma 사실** | `[F]` | `design-system/foundations/`, `components/`, `patterns/`, `guidelines/naming.md`, `guidelines/changelog.md` | Figma 파일에서 **직접 읽은 값**. 토큰 값, 컴포넌트/베리언트 이름, 시안에 적힌 문구. 노드 ID를 함께 표기합니다. |
| **미확인** | `[?]` | 위 문서들의 "확인 필요" 절 | Figma에 존재는 하지만 MCP로 값을 끝까지 읽지 못했거나, 시안 내부에서 값이 서로 어긋나는 항목. |
| **AI 제안** | `[A]` | **`design-system/guidelines/ai-guidelines.md` 한 곳에만** | Figma에 근거가 없는, AI가 관례·일반론에 기대어 제안한 내용. 채택 전까지는 규범이 아닙니다. |

> **원칙** — `foundations/`, `components/`, `patterns/` 아래 본문에는 `[A]` 항목을 섞어 쓰지 않습니다.
> 제안이 필요한 자리에는 각 문서 끝의 "AI 제안" 링크로만 연결합니다.

---

## 문서 지도

```
DESIGN_SYSTEM.md                    ← 지금 이 문서 (진입점)
        ↓
design-system/
├── README.md                       인덱스 · 문서 규약 · 원본 갱신 방법
├── foundations/                    [F] 토큰
│   ├── README.md
│   ├── color.md                    primitive 팔레트 · semantic 토큰
│   ├── typography.md               폰트 · 텍스트 스타일 22종
│   ├── layout.md                   gap · spacing · grid · breakpoint
│   ├── shape.md                    rounded · border-width
│   ├── elevation.md                shadow 4단계
│   ├── iconography.md              아이콘 그리드 · 사이즈 · 네이밍 · 목록
│   └── brand.md                    로고 · 파비콘 · OG 이미지
├── components/                     [F] 컴포넌트 인벤토리와 베리언트
│   ├── README.md                   6개 카테고리 · 상태(Done/In-progress/Before)
│   ├── content-display.md
│   ├── overlay.md
│   ├── inputs.md
│   ├── button.md
│   ├── navigation.md
│   └── indicator-status.md
├── patterns/                       [F] Figma의 "(Usage)" 프레임 = 조합 패턴
│   ├── README.md
│   └── commerce.md
└── guidelines/
    ├── README.md
    ├── naming.md                   [F] 네이밍 규칙 (Change Log 원문)
    ├── changelog.md                [F] Change Log 전문
    └── ai-guidelines.md            [A] AI 제안 — 이 파일만 제안입니다
```

---

## 파운데이션 한눈에 `[F]`

| 축 | 값 |
|---|---|
| 폰트 | `Pretendard Variable` — Regular 400 / SemiBold 600 / Bold 700 |
| 텍스트 스타일 | Display 2 · Title 5 · Subtitle 3 · Body 4 · Action 3(+underline 3) · Label 3 · Caption 3(+semibold 3) |
| 색 (primitive) | gray 12단계 + pink·red·yellow·green·cyan·blue·indigo 각 11단계 + base 2 + alpha black/white 각 6 |
| 색 (semantic) | `text` 6 · `border` 5 · `divider` 4 · `bg` 6 · `icon` 6 |
| 브랜드 | `brand/default` `#4f7cff` (= `color/blue/600`) |
| 간격 | `layout.gap.*` (px 이름) 15단계 / `layout.spacing.*` (3xs~3xl) 8단계 |
| 라운드 | `none 0 · xxs 4 · xs 6 · sm 8 · md 12 · lg 16 · xl 24 · full 999` |
| 보더 | `1px` / `2px` |
| 그림자 | `subtle · default · raised · overlay` |
| 아이콘 | 24×24 기준 그리드, 사이즈 `12·16·20·24·28·32·40` |
| 브레이크포인트 | Desktop `1440×960` (≥1200) · Tablet `768×960` (768–1199) · Mobile `375×812` |

자세한 값은 [`design-system/foundations/`](design-system/foundations/README.md).

---

## 컴포넌트 현황 한눈에 `[F]`

Overview 페이지(`1183:7436`)에 적힌 상태 그대로입니다.

| 카테고리 | Done | In-progress | Before | 계 |
|---|---|---|---|---|
| [Navigation](design-system/components/navigation.md) | 5 | 2 | 2 | 9 |
| [Button](design-system/components/button.md) | 0 | 1 | 1 | 2 |
| [Content display](design-system/components/content-display.md) | 2 | 2 | 5 | 9 |
| [Indicator & Status](design-system/components/indicator-status.md) | 2 | 0 | 6 | 8 |
| [Inputs](design-system/components/inputs.md) | 3 | 2 | 8 | 13 |
| [Overlays](design-system/components/overlay.md) | 5 | 2 | 2 | 9 |
| **합계** | **17** | **9** | **24** | **50** |

---

## 지금 바로 알아야 할 불일치 `[F]` `[?]`

문서를 그대로 코드로 옮기면 어긋나는 지점입니다. 상세는 각 파운데이션 문서의 "확인 필요" 절.

1. **`layout.spacing` 상위 3단계** — 시안에 인쇄된 라벨은 `xl 32 / 2xl 40 / 3xl 48`이지만,
   변수 실제값과 시안의 막대 길이는 **`xl 28 / 2xl 32 / 3xl 40`**. → [layout.md](design-system/foundations/layout.md)
2. **`color.border.strong` / `color.border.disabled`** — Semantic 표의 매핑(`gray/300` / `gray/400`)과
   변수 실제값(`#c5c9d3` = gray/400 / `#e3e6ee` = gray/300)이 **서로 뒤바뀐 상태**. → [color.md](design-system/foundations/color.md)
3. **gray 리넘버링 잔여** — Change Log `251224`의 `gray 50→100, 100→150` 반영 이후, Semantic 표의
   `bg.subtle`·`bg.muted`·`divider.soft`·`text.primary` 매핑 라벨이 옛 번호로 남아 있음. → [color.md](design-system/foundations/color.md)
4. **오타 토큰** — `color.text.priamry`, `color.divider.defualt`, `sementic/background/*`,
   Price 베리언트 프로퍼티 `discout`. → [naming.md](design-system/guidelines/naming.md)

---

## AI 제안은 여기 한 곳

[`design-system/guidelines/ai-guidelines.md`](design-system/guidelines/ai-guidelines.md) —
Figma에 근거가 없는 내용(코드 토큰 export 전략, 다크 모드, 접근성 기준, 컴포넌트 API 형태,
문서 운영 규칙 등)은 전부 이 파일에 모아 두었고, 각 항목에 "왜 제안인지 / 무엇을 확인해야 사실이 되는지"를 함께 적었습니다.
