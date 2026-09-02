# Inputs `[F]`

> 출처 — Figma Overview `1192:7929`, Change Log 섹션 `20:138`
> **이 파일에 Inputs 상세 프레임은 없습니다**(Search 사용례만 • Overlay 페이지에 존재).

## Overview 상태표

13개 컴포넌트로 카테고리 중 가장 큽니다.

| 컴포넌트 | Status | Last Update |
|---|---|---|
| Checkbox | In-progress | N/A |
| Chip | Before | N/A |
| Radio button | Before | N/A |
| Slider | Before | N/A |
| Stepper | Before | N/A |
| Switch | Before | N/A |
| Text area | Done | N/A |
| Text input | Done | N/A |
| File upload | Before | N/A |
| Date picker | Before | N/A |
| Pulldown | Before | N/A |
| Search | Done | N/A |
| Segment control | In-progress | 2/06/26 |

---

## Change Log에 기록된 스펙

### Input Field `251224` — 버튼과 높이 일치

> button과 높이값 일치
> H — **56(lg), 44(md), 32(sm)**

| size | height |
|---|---|
| `lg` | 56px |
| `md` | 44px |
| `sm` | 32px |

버튼의 `xl`(64) · `xs`(26) 에 해당하는 입력 필드 사이즈는 없습니다.

### Input Field `260202` — 프로퍼티 변경

> Property
> - state 명칭 **`completed` → `filled`** 로 변경
> - **`showTrailingIn` 추가**

> `[?]` `showTrailingIn` 은 `showTrailingIcon` 의 축약/오기로 보입니다.
> Tooltip 컴포넌트는 실제로 `showTrailingIcon` 프로퍼티를 씁니다.

### Label `260204`

> **"required" 필수 입력/선택 표시 추가**

Label 컴포넌트 자체는 • Content Display 페이지에 있습니다 → [content-display.md](content-display.md#label-162117834)

---

## 다른 페이지에 있는 관련 자산 `[F]`

| 자산 | 위치 | 비고 |
|---|---|---|
| `Search(Usage)` | • Overlay 페이지 `1170:5163` | `1440 × 9388`. 검색 사용 흐름 |
| `└ OptionRow` | • Content Display 페이지 `3445:9254` | `viewport`, `showOption`, `isDisabled` |
| `└ Checkbox-atomic` | Card / Bottom Sheet 프레임 안 인스턴스 | Checkbox 원자 컴포넌트가 이미 조합에 쓰이는 중 |
| `SelectField` | Card(Usage) 안 | 상품 옵션 선택 |

즉 **Checkbox 는 Overview 상 In-progress 이지만, 다른 컴포넌트(CartItem 등) 안에서 이미 인스턴스로 사용 중**입니다.

---

## 관련 토큰 `[F]`

- 입력 필드 기본 라운드: `shape.rounded.sm`(8px) — Role에 "입력 필드" 명시
- 기본 보더: `shape.border-width.1`(1px) — Role에 "입력필드" 명시
- 강조 보더(선택/활성): `shape.border-width.2`(2px)
- 플레이스홀더 색: `color.text.muted` — Role "플레이스홀더, 덜 중요한 설명 텍스트"
- 비활성 텍스트: `color.text.disabled` / 비활성 배경: `color.bg.disabled`
- 라벨 텍스트: `Label/1~3`

---

## 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | Inputs 상세 프레임이 이 파일에 없음 |
| 2 | Text input 의 state 전체 목록 (`filled` 외 default/focus/error/disabled 등) |
| 3 | `showTrailingIn` 의 정확한 이름과 의미 |
| 4 | 에러 메시지·헬퍼 텍스트의 스타일/색 토큰 |
| 5 | `required` 표시의 시각 규칙(별표 색·위치) |
| 6 | Checkbox / Radio / Switch 의 사이즈 스케일 |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#components)
