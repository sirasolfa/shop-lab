# Components — 인벤토리 `[F]`

> 출처 — Figma **Overview** 페이지 `1183:7436`
> 상태(`Done` / `In-progress` / `Before`)와 `Last Update` 는 시안에 적힌 값 그대로입니다.

Overview 페이지는 6개 카테고리, **총 50개 컴포넌트**를 나열합니다.

| 카테고리 | 노드 | Done | In-progress | Before | 계 | 문서 |
|---|---|---|---|---|---|---|
| Navigation | `1183:7464` | 5 | 2 | 2 | 9 | [navigation.md](navigation.md) |
| Button | `1192:6212` | 0 | 1 | 1 | 2 | [button.md](button.md) |
| Content display | `1192:7647` | 2 | 2 | 5 | 9 | [content-display.md](content-display.md) |
| Indicator & Status | `1192:7796` | 2 | 0 | 6 | 8 | [indicator-status.md](indicator-status.md) |
| Inputs | `1192:7929` | 3 | 2 | 8 | 13 | [inputs.md](inputs.md) |
| Overlays | `1635:14884` | 5 | 2 | 2 | 9 | [overlay.md](overlay.md) |
| **합계** | | **17** | **9** | **24** | **50** | |

---

## 상세 스펙이 이 파일에 있는 컴포넌트 / 없는 컴포넌트

이 Figma 파일에는 페이지가 **4개**뿐입니다.

| 페이지 | 노드 | 내용 |
|---|---|---|
| Overview | `1183:7436` | 인벤토리 표 + Change Log 섹션 |
| Foundation | `0:1` | 토큰 |
| • Content Display | `1595:11126` | 컴포넌트 상세 11개 |
| • Overlay | `1595:11129` | 컴포넌트 상세 6개 + Search(Usage) |

즉 **Navigation · Button · Inputs · Indicator & Status 카테고리의 상세 프레임은 이 파일에 없습니다.**
해당 문서들은 Overview의 상태표와 Change Log에서 읽어낸 사실만 담고 있습니다.
(Overview 표의 컴포넌트 이름 중 밑줄이 그어진 항목은 링크가 걸려 있어, 다른 파일 또는 미공개 페이지로
연결되는 것으로 보입니다. `[?]` 링크 대상 파일은 미확인.)

## Overview 표와 상세 페이지의 목록이 다릅니다 `[?]`

Content Display 카테고리가 특히 어긋납니다.

| Overview 표 (`1192:7647`) | • Content Display 페이지 (`1595:11126`) |
|---|---|
| Accordion, Avatar, Draggable list, List, Thumbnail, Image grid, **Cards**, Video player, Data table | Accordion, Avatar, **Carousel**, **OptionRow**, **Price**, **Label**, List, Thumbnail, **Table**, **Text List**, **Card** |

- Overview에만 있는 것: `Draggable list`, `Image grid`, `Video player`, `Data table`
- 상세 페이지에만 있는 것: `Carousel`, `OptionRow`, `Price`, `Label`, `Table`, `Text List`
- 이름 불일치: `Cards`(Overview) ↔ `Card`(상세), `Data table`(Overview) ↔ `Table`(상세)

Overlay 쪽도 비슷합니다.

| Overview 표 (`1635:14884`) | • Overlay 페이지 (`1595:11129`) |
|---|---|
| Popup, Dialog, Drawer, Bottom sheet, Toast, Tooltip, Snackbar, System message, Pulldown menu | Dialog, Drawer, Bottom Sheet, Toast, Tooltip, Snack Bar, *(+ Search(Usage))* |

- Overview에만: `Popup`, `System message`, `Pulldown menu`
- 이름 표기 차이: `Snackbar` ↔ `Snack Bar`, `Bottom sheet` ↔ `Bottom Sheet`
- 상세 페이지에 있는 `Search(Usage)`(`1170:5163`)는 Overview 상 **Inputs > Search** 항목의 사용례로 보입니다.

---

## 컴포넌트 상세 문서의 공통 템플릿 `[F]`

• Content Display / • Overlay 페이지의 컴포넌트 프레임은 모두 같은 골격을 씁니다.

```
<컴포넌트명>
├ Title Container
│  ├ Title
│  └ System Container
│      ├ Version Info
│      ├ Library Info
│      ├ Design Only/Status     ← Done / In-progress / Before 뱃지
│      └ Develop Info
├ Description                    ← 컴포넌트 설명 문장
├ Main Container / Container     ← 베리언트 전개
│   └ Atomic Container           ← 하위 원자 컴포넌트(`└ Xxx-atomic`)
└ <컴포넌트명>(Usage)             ← 실제 화면 조합 예시 (일부 컴포넌트만)
```

Foundation 페이지의 `System Conponent` 섹션(`260:1443`)에 이 템플릿용 부품이 정의돼 있습니다:
`Design Only/Text Container`, `Design Only/Viewport`, `Design Only/Status`, `Design Only/Value`.

하위 원자 컴포넌트는 이름 앞에 **`└ `** 를 붙이는 관례를 씁니다 (예: `└ ProductWish-atomic`, `└ Table-row`).

---

AI 제안(컴포넌트 API 형태, 우선순위) → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#components)
