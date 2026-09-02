# Typography `[F]`

> 출처 — Figma **Typography (업데이트 필요)** `139:1666`, **Typography(Usage)** `163:998`
> 값은 두 프레임에서 `get_variable_defs`로 읽은 텍스트 스타일 정의입니다.

---

## 1. 폰트 · 웨이트 변수

| 변수 | 값 |
|---|---|
| `typo/font-family/primary` | `Pretendard Variable` |
| `typo/font-family/Pretendard Variable` | `Pretendard Variable` |
| `typo/weight/regular` | `400` |
| `typo/weight/semibold` | `600` |
| `typo/weight/bold` | `700` |

> Change Log `251215`: **font-family와 font-weight만 토큰화. 나머지(font-size, height, spacing)는 토큰화하지 않음.**
> 그래서 사이즈/행간/자간은 변수가 아니라 **텍스트 스타일**에 직접 박혀 있습니다.
> `251217` 항목에는 "폰트 사이즈 토큰화 고민"이 취소선으로 적혀 있습니다(= 보류).

> 폰트 패밀리 변수가 `primary` 와 `Pretendard Variable` **두 개**로 존재하고, 스타일마다 참조가 갈립니다.
> `Display/1`, `Subtitle/*` 은 `primary` 를, 나머지는 `Pretendard Variable` 을 참조합니다. → [확인 필요](#4-확인-필요-)

---

## 2. 텍스트 스타일

행간(lineHeight)은 배수, 자간(letterSpacing)은 px입니다.
Figma가 돌려주는 `1.2000000476837158` 같은 값은 `1.2`로 반올림해 적었습니다.

### Display — 2단계

| 스타일 | Size | Weight | Line height | Letter spacing |
|---|---|---|---|---|
| `Display/1` | 56 | Bold 700 | 1.2 | −1 |
| `Display/2` | 44 | Bold 700 | 1.2 | −1 |

### Title — 5단계

Change Log `251217`: **Title, Heading → Title 하나로 카테고리 묶음 (위계 5~6으로). 명칭 `lg>md>sm` → `T1>T2>T3` 로 숫자화.**

| 스타일 | Size | Weight | Line height | Letter spacing |
|---|---|---|---|---|
| `Title/1` | 40 | Bold 700 | 1.3 | 0 |
| `Title/2` | 32 | Bold 700 | 1.3 | 0 |
| `Title/3` | 26 | Bold 700 | 1.3 | 0 |
| `Title/4` | 22 | Bold 700 | 1.3 | 0 |
| `Title/5` | 20 | Bold 700 | 1.3 | 0 |

### Subtitle — 3단계

Change Log `251216`: **subtitle 텍스트 스타일 추가.**

| 스타일 | Size | Weight | Line height | Letter spacing |
|---|---|---|---|---|
| `Subtitle/1` | 18 | SemiBold 600 | 1.4 | 0 |
| `Subtitle/2` | 16 | SemiBold 600 | 1.4 | 0 |
| `Subtitle/3` | 14 | SemiBold 600 | 1.4 | 1 |

### Body — 4단계

Typography(Usage)의 Body 절에 **"* 기본값으로 사용합니다."** 라는 주석이 붙어 있습니다.

| 스타일 | Size | Weight | Line height | Letter spacing |
|---|---|---|---|---|
| `Body/1` | 18 | Regular 400 | 1.4 | 0 |
| `Body/2` | 16 | Regular 400 | 1.4 | 0 |
| `Body/3` | 14 | Regular 400 | 1.4 | 0 |
| `Body/4` | 13 | Regular 400 | 1.4 | 0 |

### Action — 3단계 + underline 3단계

Change Log `251216`: **button에 사용될 action 텍스트 스타일 추가** / `251217`: **action 內 underline 텍스트 스타일 추가.**

| 스타일 | Size | Weight | Line height | Letter spacing |
|---|---|---|---|---|
| `Action/1` | 16 | SemiBold 600 | 1.5 | 0 |
| `Action/2` | 14 | SemiBold 600 | 1.5 | 1 |
| `Action/3` | 12 | SemiBold 600 | 1.5 | 1 |
| `Action/underline/1` | 16 | SemiBold 600 | 1.5 | 0 |
| `Action/underline/2` | 14 | SemiBold 600 | 1.5 | 1 |
| `Action/underline/3` | 12 | SemiBold 600 | 1.5 | 1 |

`underline` 계열은 사이즈/웨이트/행간/자간이 같은 번호의 `Action/*` 과 동일하고, 밑줄 장식만 다릅니다.

### Label — 3단계

Change Log `251222`: **label 1: 15px, 140% → 16px, 150%** (현재 값이 변경 후 값과 일치).

| 스타일 | Size | Weight | Line height | Letter spacing |
|---|---|---|---|---|
| `Label/1` | 16 | SemiBold 600 | 1.5 | 0 |
| `Label/2` | 14 | SemiBold 600 | 1.4 | 1 |
| `Label/3` | 13 | SemiBold 600 | 1.4 | 1 |

### Caption

Typography(Usage) Caption 절의 설명: **"보조 설명, 부가 정보, 상태 안내 등 가장 작은 텍스트로 사용"**
(라이브러리의 스타일 description도 같은 취지: "보조 설명, 부가 정보, 상태 안내 등 맥락을 보완하기 위한 작은 텍스트에 사용합니다.")

| 스타일 | Size | Weight | Line height | Letter spacing |
|---|---|---|---|---|
| `Caption/1` | *미확인* `[?]` | Regular 400 (추정 아님 — 계열 규칙) | — | — |
| `Caption/2` | 11 | Regular 400 | 1.4 | 1 |
| `Caption/3` | *미확인* `[?]` | — | — | — |
| `Caption/semibold/1` | 12 | SemiBold 600 | 1.4 | 1 |
| `Caption/semibold/2` | *미확인* `[?]` | — | — | — |
| `Caption/semibold/3` | *미확인* `[?]` | — | — | — |

`Caption/1`, `Caption/3`, `Caption/semibold/2`, `Caption/semibold/3` 은
`search_design_system` 으로 **라이브러리에 존재함은 확인**했지만, 조사한 프레임들이 사용하지 않아
사이즈/행간 값을 읽지 못했습니다. 추정값을 적지 않았습니다.

---

## 3. 스타일 개수 요약

| 카테고리 | 개수 | 값 확인 |
|---|---|---|
| Display | 2 | 2 |
| Title | 5 | 5 |
| Subtitle | 3 | 3 |
| Body | 4 | 4 |
| Action (+underline) | 3 + 3 | 6 |
| Label | 3 | 3 |
| Caption (+semibold) | 3 + 3 | 2 |
| **합계** | **29** | **25** |

---

## 4. 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | `Caption/1`, `Caption/3`, `Caption/semibold/2`, `Caption/semibold/3` 의 사이즈/행간/자간 |
| 2 | 폰트 패밀리 변수가 `typo/font-family/primary` 와 `typo/font-family/Pretendard Variable` 두 갈래. 둘 다 값은 `Pretendard Variable` 이지만 스타일마다 참조가 다름 — 하나로 정리할지 |
| 3 | `139:1666` 프레임 이름에 붙은 **"(업데이트 필요)"** — 어떤 부분이 미갱신인지 시안에 명시 없음 |
| 4 | Typography(Usage)에 `Heading` 이름의 프레임이 남아 있음(`163:1025`). Change Log 상 Title로 통합됐으므로 잔재로 보임 |
| 5 | 자간이 스타일마다 0 / 1 로 갈리는 규칙(예: `Body/*` 는 0, `Label/2·3` 은 1)이 의도인지 |

---

AI 제안(코드 매핑, 반응형 타이포, 웹폰트 로딩) → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#typography)
