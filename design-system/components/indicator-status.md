# Indicator & Status `[F]`

> 출처 — Figma Overview `1192:7796`
> **이 파일에 상세 프레임은 없습니다.** 아래는 Overview 상태표 전부입니다.

## Overview 상태표

| 컴포넌트 | Status | Last Update |
|---|---|---|
| Badge | Done | 1/22/25 |
| Empty state | Before | N/A |
| Skeleton | Before | N/A |
| Progress bar | Before | N/A |
| Progress circle | Before | N/A |
| Progress steps | Before | N/A |
| Push badge | Done | 1/26/26 |
| Divider | Before | N/A |

Done 2 · Before 6. **In-progress가 하나도 없는 유일한 카테고리**로, 진행이 가장 덜 된 영역입니다.

> `Badge` 의 Last Update `1/22/25` 는 연도가 다른 항목과 다릅니다(오기 가능성). `[?]`

---

## 다른 페이지에서 실제로 쓰이는 인스턴스 `[F]`

| 컴포넌트 | 사용처 |
|---|---|
| `Badge/Solid` | Drawer(Usage) `1065:18140` 안 |
| `Badge` | Card(Usage) `2582:8855` — 상품 이미지 영역 위 |
| `BadgeContainer`, `└ count` | Card(Usage) — 개수 표시 |

`Badge` 는 `Badge/Solid` 처럼 슬래시 하위 종속 형태를 갖습니다(네이밍 규칙상 `/` = 종속).
→ [../guidelines/naming.md](../guidelines/naming.md)

---

## 관련 토큰 `[F]`

- Divider 색: `color.divider.soft` / `.defualt` / `.strong` / `.inverse` → [../foundations/color.md](../foundations/color.md#divider)
- Divider 라운드: `shape.rounded.none`(0) Role에 "디바이더" 명시
- 작은 배지 라운드: `shape.rounded.xxs`(4) Role에 "작은 배지" 명시
- 숫자 배지 라운드: `shape.rounded.full`(999) Role에 "숫자 배지" 명시
- 배지 텍스트: `Caption/semibold/1`(12/SemiBold) 또는 `Label/3`(13/SemiBold) 계열 `[?]` 매핑 규칙은 미정의

---

## 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | 상세 프레임 없음. Overview 표에도 이 카테고리는 링크(밑줄) 표시가 없음 |
| 2 | `Badge` 의 타입(Solid 외), 사이즈, 색 베리언트 정의 |
| 3 | `Divider` 가 `Before` 인데 `color.divider.*` 토큰은 이미 완비돼 있음 — 컴포넌트화만 남은 상태로 보임 |
| 4 | 상태 색(success/error/warning/info)이 `color.text.status.*` / `color.icon.status.*` 로 일부만 존재. 전체 세트 미확인 |
| 5 | `Badge` Last Update `1/22/25` 연도 |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#components)
