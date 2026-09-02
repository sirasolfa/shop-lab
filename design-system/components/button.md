# Button `[F]`

> 출처 — Figma Overview `1192:6212`, Change Log 섹션 `20:138`
> **이 파일에 Button 상세 프레임은 없습니다.** 아래는 Overview 상태표와 Change Log에 적힌 사실 전부입니다.

## Overview 상태표

| 컴포넌트 | Status | Last Update |
|---|---|---|
| Button | In-progress | N/A |
| Button group | Before | N/A |

---

## Change Log에 기록된 스펙

### `251217` — 사이즈 추가와 높이 고정

> button 사이즈 `xs`, `xl` 추가
> btn의 높이값은 **고정(fixed)** 으로 함
> H — **64(xl), 56(lg), 44(md), 32(sm), 26(xs)**

| size | height |
|---|---|
| `xl` | 64px |
| `lg` | 56px |
| `md` | 44px |
| `sm` | 32px |
| `xs` | 26px |

### `251224` — 타입 재정의

> Secondary → 컬러 **darkgray** 로 변경
> Tertiary → 컬러 **gray** 로 변경
> **TextOnly 추가**
> **Outlined 따로 분리**

즉 현재 타입 체계는 `Primary` · `Secondary`(darkgray) · `Tertiary`(gray) · `TextOnly` · `Outlined` 입니다.
(`Primary` 는 Change Log에 변경 기록이 없어 이름만 유추 가능 — 나머지 네 개가 명시적으로 언급됩니다.)

---

## 관련 토큰 `[F]`

- 버튼 텍스트: **`Action/*`** 텍스트 스타일. Change Log `251216` — "button에 사용될 action 텍스트 스타일 추가".
  `Action/1` 16 · `Action/2` 14 · `Action/3` 12 (모두 SemiBold 600, line-height 1.5)
- 밑줄 버튼(TextOnly 등): `Action/underline/1~3`. Change Log `251217` — "action 內 underline 텍스트 스타일 추가".
- 기본 라운드: `shape.rounded.sm`(8px) 이 "기본 버튼, 입력 필드, 카드 등 핵심 인터랙션 컴포넌트의 기본 값"으로 정의됨.
- 아이콘 버튼: `shape.rounded.full`(999px) 의 Role에 "아이콘 버튼"이 명시됨.
- 패딩: `layout.spacing.*` 스케일에서 고르도록 규정 (임의 숫자 금지). → [../foundations/layout.md](../foundations/layout.md)

---

## 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | Button 상세 프레임이 이 파일에 없음. Overview의 `Button` 항목에 링크가 걸려 있으나 대상 미확인 |
| 2 | 타입별 색 토큰 매핑 (Primary/Secondary/Tertiary/TextOnly/Outlined ↔ semantic 색) |
| 3 | 상태(hover / pressed / disabled / loading) 정의 |
| 4 | size별 좌우 padding, 아이콘 간격, 최소 너비 |
| 5 | `Button group` 의 정의 전무 (Before) |
| 6 | Change Log의 "darkgray", "gray" 가 어떤 primitive/semantic 토큰을 가리키는지 |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#components)
