# Overlays `[F]`

> 출처 — Figma 페이지 **• Overlay** `1595:11129` (섹션 `1600:13981`), Overview 표 `1635:14884`

## Overview 상태표

| 컴포넌트 | Status | Last Update |
|---|---|---|
| Popup | In-progress | N/A |
| Dialog | Done | N/A |
| Drawer | Done | 1/27/26 |
| Bottom sheet | Done | 1/21/26 |
| Toast | Done | 1/27/26 |
| Tooltip | In-progress | N/A |
| Snackbar | Done | 1/27/26 |
| System message | Before | N/A |
| Pulldown menu | Before | N/A |

상세 프레임이 있는 것은 6종(Dialog, Drawer, Bottom Sheet, Toast, Tooltip, Snack Bar)이며,
`Popup` · `System message` · `Pulldown menu` 는 상세 프레임이 없습니다.

---

## Dialog `1049:3492`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `Modal` | `viewport=desktop, size=lg \| md \| sm` · `viewport=mobile, size=sm` |
| `Alert` | *(베리언트 없음)* |
| `Overlay` | `type=modal \| alert` |

모바일은 `size=sm` 만 존재합니다.

### 시안에 적힌 규칙 (원문)

> **다이얼로그의 최대 높이는 화면 높이 기준 20% 여백을 가져야 합니다.**

프레임에 `예시-높이 1080` 블록으로 검증 예시가 그려져 있습니다. `Dim` 레이어가 별도로 존재합니다.

## Drawer `1065:18140`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `Side Drawer` | `Open drawer on=right`, `Size=default` |

프로퍼티 이름이 문장형(`Open drawer on`)이고 첫 글자가 대문자(`Size`)라 다른 컴포넌트와 표기가 다릅니다.
현재 값이 각각 하나뿐이라 좌측 오픈/다른 사이즈는 미정의입니다.

`Drawer(Usage)` 프레임에 실제 화면 예시가 있고, 그 안에 `Badge/Solid` 인스턴스가 쓰입니다.

## Bottom Sheet `1065:18681`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `BottomSheet` | `type=default` |
| `Overlay` | `type=bottom` |

`Action Area(Usage)` 프레임을 포함하며, 그 안에서 다음 컴포넌트를 조합해 장바구니 시트를 구성합니다:
`CartItem`, `└ Checkbox-atomic`, `Ratio`, `Price`, `addOptionRow`, `└ OptionRow`, `IconOnly`, `ActionArea`, `ButtonPair`.
→ [../patterns/commerce.md](../patterns/commerce.md)

## Toast `1368:9769`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `Toast` | `type=success \| error \| info` |
| `Toast/Text` | `Icon=True \| False`, `Line=Single \| Multi` |
| `Toast/Icon` | `Option=Check mark \| Loading \| Exclamation Mark \| Custom` |

`Toast(Usage)` 프레임에 `BottomNavigation` · `home_indicator__atomic` 과 함께 배치한 예시,
그리고 `Toast Case Icons` / `Toast Case Labels` 대응표가 있습니다.
로딩 표현용 `Loading Cirlce` 레이어가 있습니다 (오타 — `Circle`).

## Tooltip `1600:13434` — 베리언트가 가장 많음

| 컴포넌트 | 프로퍼티 | 조합 수 |
|---|---|---|
| `CompactTooltip` | `size=xs \| sm \| md`, `theme=light \| dark`, `type=default \| bold`, `showTrailingIcon=true \| false` | 24 |
| `Tooltip` | `size=sm \| md`, `direction=top \| bottom \| left \| right`, `align=start \| center \| end`, `theme=light \| dark` | 48 |

- `CompactTooltip` 만 `size=xs` 를 가집니다.
- `Tooltip` 은 꼬리 방향(`direction`) × 정렬(`align`) 12조합을 사이즈·테마와 곱합니다.
- **`theme=light | dark` 를 가진 유일한 컴포넌트 군**입니다(Snack Bar 포함 오버레이 계열 특징).

> Change Log(Input Field) `260202` 의 `showTrailingIn 추가` 와 이름이 유사한 `showTrailingIcon` 을 씁니다.

## Snack Bar `1384:7161`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `Snack bar` | `Name=Snack bar` |
| `Snack bar/leading item` | `Type=Icon \| Slot` |

`Link` · `Item` · `Lable`(오타 — `Label`) · `direction/chevron` 아이콘으로 구성됩니다.

## Search(Usage) `1170:5163`

이 페이지에 함께 놓인 `1440 × 9388` 크기의 검색 사용례 프레임입니다.
Overview 상 **Inputs > Search (Done)** 항목의 사용 흐름을 다룹니다. → [../patterns/README.md](../patterns/README.md)

---

## 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | `Popup` · `System message` · `Pulldown menu` 상세 프레임 없음 |
| 2 | `Drawer` 의 `Open drawer on` 이 `right` 만, `Size` 가 `default` 만 존재 — 좌측/다른 사이즈 계획 |
| 3 | 프로퍼티 이름 표기 혼용 — `size`(소문자) vs `Size`/`Type`/`Name`(대문자), 문장형 `Open drawer on` |
| 4 | 오타 레이어: `Loading Cirlce`, `Lable` |
| 5 | `theme=light\|dark` 가 Tooltip 계열에만 존재. 다크 테마 정책 전반은 미정의 |
| 6 | Dialog "화면 높이 20% 여백" 규칙이 모바일에도 동일 적용되는지 |
| 7 | 각 컴포넌트의 `Description` · `Version Info` 본문 미조사 |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#components)
