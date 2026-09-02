# Navigation `[F]`

> 출처 — Figma Overview `1183:7464`
> **이 파일에 Navigation 상세 프레임은 없습니다.** 아래는 Overview 상태표 전부입니다.

## Overview 상태표

| 컴포넌트 | Status | Last Update |
|---|---|---|
| Breadcrumb | In-progress | N/A |
| Bottom navigation | Done | 1/21/26 |
| Link (링크버튼!) | Done | N/A |
| Top navigation_mobile | Done | 1/23/25 |
| Top navigation_desktop | Done | 1/26/26 |
| Page Indicator | Done | 2/05/26 |
| Pagination | In-progress | N/A |
| Tabs | Before | N/A |
| Footer | Before | N/A |

Done 5 · In-progress 2 · Before 2. **카테고리 중 완료 비율이 가장 높습니다.**

### 표기 그대로 기록한 것

- `Link (링크버튼!)` — 괄호와 느낌표까지 시안 원문입니다.
- `Top navigation_mobile` / `Top navigation_desktop` — 뷰포트를 **베리언트가 아니라 별도 컴포넌트 이름**으로
  분리한 유일한 사례입니다. 다른 컴포넌트는 `viewport=desktop|mobile` 프로퍼티를 씁니다.
- `Top navigation_mobile` 의 Last Update가 **`1/23/25`** 로 다른 항목(`/26`)과 연도가 다릅니다.
  `Badge`(Indicator & Status)의 `1/22/25` 와 같은 패턴이라 오기일 가능성이 있습니다. `[?]`

---

## 다른 페이지에서 실제로 쓰이는 인스턴스 `[F]`

| 컴포넌트 | 사용처 |
|---|---|
| `BottomNavigation` | Toast(Usage) `1368:9769` 안 |
| `home_indicator__atomic` | Toast(Usage) 안 (모바일 홈 인디케이터) |
| `List/menu`, `List/category` | • Content Display > List `1621:15994` — 메뉴/카테고리 내비 리스트 |
| `direction/chevron` | Snack Bar 등 다수 |

`List/category` 는 `Type=대분류 | 중분류`, `Screen=mobile | desktop` 을 가져 **카테고리 내비게이션**을 담당합니다.
→ [content-display.md](content-display.md#list-162115994)

---

## 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | Navigation 상세 프레임이 이 파일에 없음. Overview에서 대부분 항목에 링크가 걸려 있으나 대상 미확인 |
| 2 | Top navigation 을 mobile/desktop 별도 컴포넌트로 둔 이유(다른 컴포넌트와 규칙이 다름) |
| 3 | `Tabs`, `Footer` 미착수 |
| 4 | `Page Indicator` 와 `Pagination` 의 역할 구분 |
| 5 | `Top navigation_mobile` Last Update `1/23/25` 연도 |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#components)
