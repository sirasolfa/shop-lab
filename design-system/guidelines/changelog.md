# Change Log `[F]`

> 출처 — Figma Overview 페이지의 **Change Log** 섹션 `20:138`
> 아래는 시안에 적힌 내용을 **원문 그대로** 옮긴 것입니다(취소선 포함). 날짜는 `YYMMDD` 표기입니다.

---

## 네이밍 규칙 `742:1604`

날짜 표기 없음. → [naming.md](naming.md)

- 컴포넌트 이름(ComponentName) → PascalCase
  - 컴포넌트 종속 시 → `/`(Slash) 사용
    - 종속 정의가 애매한 컴포넌트는 `-`(Hyphen) 사용
- 컴포넌트 프로퍼티(Property / Props) → camelCase
- 프로퍼티 상세값(Value) → kebab-case

## Token `742:1635`

**260106**
- rounded
  - `shape.rounded.xs` → `shape.rounded.xxs` 로 변경
  - value가 6인 `shape.rounded.xs` token 추가

## Typography `131:346`

**251215**
- font-family와 font-weight만 토큰화
  - 나머지(font-size, height, spacing)는 토큰화하지 않음

**251216**
- button에 사용될 action 텍스트 스타일 추가
- subtitle 텍스트 스타일 추가

**251217**
- action 內 underline 텍스트 스타일 추가
- Title, Heading → Title 하나로 카테고리 묶음 (위계 5~6으로)
  - 명칭 `lg>md>sm` → `T1>T2>T3` 로 숫자화
  - ~~폰트 사이즈 토큰화 고민~~ *(취소선 = 보류/폐기)*

**251222**
- label 텍스트 스타일 변경
  - label 1: 15px, 140% → **16px, 150%**

## Color `461:4962`

**251224**
- red, green, yellow `50`, `100` hex 변경
- **gray `150` 추가 (기존 50→100, 100→150)**
- gray `50`, `100`, `200` hex 변경

## Button `196:5393`

**251217**
- button 사이즈 `xs`, `xl` 추가
- btn의 높이값은 고정(fixed)으로 함
  - H — 64(xl), 56(lg), 44(md), 32(sm), 26(xs)

**251224**
- Secondary → 컬러 darkgray로 변경
- Tertiary → 컬러 gray로 변경
- TextOnly 추가
- Outlined 따로 분리

## Input Field `470:4961`

**251224**
- button과 높이값 일치
  - H — 56(lg), 44(md), 32(sm)

**260202**
- Property
  - state 명칭 `completed` → `filled` 로 변경
  - `showTrailingIn` 추가

## Label `1556:11082`

**260204**
- "required" 필수 입력/선택 표시 추가

---

## 시간 순 정리

| 날짜 | 영역 | 변경 |
|---|---|---|
| 251215 | Typography | font-family / font-weight만 토큰화 |
| 251216 | Typography | action · subtitle 스타일 추가 |
| 251217 | Typography | action underline 추가 / Title·Heading 통합, 숫자 명명 |
| 251217 | Button | xs·xl 추가, 높이 고정 |
| 251222 | Typography | label 1: 15/140% → 16/150% |
| 251224 | Color | red·green·yellow 50·100 / gray 50·100·200 hex 변경, **gray 150 추가 + 리넘버링** |
| 251224 | Button | Secondary·Tertiary 색 변경, TextOnly 추가, Outlined 분리 |
| 251224 | Input Field | 높이 버튼과 일치 |
| 260106 | Token | `rounded.xs` → `xxs`, 새 `xs`(6) 추가 |
| 260202 | Input Field | `completed` → `filled`, `showTrailingIn` 추가 |
| 260204 | Label | `required` 추가 |

## 이 로그가 설명해 주는 현재 상태의 불일치

- **251224 gray 리넘버링** → Semantic Color 표의 `bg.subtle`·`bg.muted`·`divider.soft`·`text.primary` 매핑 라벨이
  옛 번호로 남은 이유. → [../foundations/color.md](../foundations/color.md)
- **260106 rounded 재정의** → `shape.rounded.xs`(6)만 Role 설명이 `--` 로 빈 이유.
  → [../foundations/shape.md](../foundations/shape.md)
- **251217 Title/Heading 통합** → Typography(Usage)에 `Heading` 프레임이 잔재로 남은 이유.
  → [../foundations/typography.md](../foundations/typography.md)

## 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | Change Log에 **Layout / Elevation / Iconography / Logo** 영역 항목이 없음 |
| 2 | `layout.spacing` 상위 3단계 값 변경(32/40/48 → 28/32/40)이 로그에 기록되지 않음 |
| 3 | 마지막 기록이 `260204`. 이후 변경분은 로그 미반영 가능성 |
