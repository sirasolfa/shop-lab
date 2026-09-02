# Brand — Logo · Favicon · OG Image `[F]`

> 출처 — Figma **Logo** `1621:20549`, **Favicon & OG Image** `2079:2181`

---

## 1. NOVERA Logo

컴포넌트 `NOVERA Logo` 는 4개 프로퍼티의 조합입니다.

| 프로퍼티 | 값 |
|---|---|
| `type` | `primary` · `secondary` · `wordmark` · `symbol` |
| `language` | `primary(EN)` · `secondary(KR)` · `none`(symbol 전용) |
| `color` | `grayscale` · `black` · `white` · `color` |
| `mode` | `none` · `light` · `dark` |

조합 규칙 (실재하는 베리언트 기준):

- `color=grayscale | black | white` → **`mode=none`** 고정. `type` 4종 × `language` 2종 (symbol은 `language=none`) = 7개씩.
- `color=color` → **`mode=light | dark`** 를 가짐. 단 `type=symbol` 만 `mode=none`.

즉 컬러 로고에만 라이트/다크 대응이 따로 있고, 흑백·화이트 로고는 모드 구분이 없습니다.

### NOVERA shop Logo

별도 컴포넌트 `NOVERA shop Logo` 가 있으며, 프로퍼티가 더 단순합니다.

| 프로퍼티 | 값 |
|---|---|
| `color` | `color` · `black` · `white` · `wordmark` |
| `mode` | `light` · `dark` |

> `[?]` `color=wordmark` 는 색이 아니라 형태를 가리키는 값이어서, 프로퍼티 축이 섞여 있습니다.

## 2. Favicon

| 컴포넌트 | 베리언트 | 시안에 포함된 프리뷰 |
|---|---|---|
| `Favicon` | `type=default` | 브라우저 탭 목업 — **light mode / dark mode** 2종 |

목업은 실제 브라우저 탭(탭 제목·URL 바) 위에 얹어 라이트/다크 배경에서의 시인성을 보여주는 구성입니다.

## 3. OG Image

| 컴포넌트 | 베리언트 |
|---|---|
| `OG Image` | `type=600*600` · `type=1200*600` |

`OpenGraph Image` 프리뷰의 구성 요소: `Brand Name` · `Brand Slogan` · `URL`.

---

## 4. 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | 로고 **최소 크기 / clear space(여백) 규정** — 시안에 수치 없음 |
| 2 | 로고 오용 예시(Do / Don't) 없음 |
| 3 | `NOVERA Logo` 와 `NOVERA shop Logo` 의 사용 경계(언제 어느 쪽) 명시 없음 |
| 4 | `NOVERA shop Logo` 의 `color=wordmark` 값이 다른 값들과 축이 다름 |
| 5 | Favicon 실제 산출 사이즈(16/32/180/512 등) 명시 없음. 컴포넌트는 `type=default` 하나 |
| 6 | OG 이미지의 텍스트 안전 영역·폰트 크기 규정 없음 |

---

AI 제안(에셋 export 규격, 파비콘 사이즈 세트) → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#brand)
