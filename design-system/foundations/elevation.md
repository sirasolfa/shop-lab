# Elevation — shadow `[F]`

> 출처 — Figma **Elevation** `749:4126`

설명(원문): **요소의 깊이감을 표현하는 기복적인 방법** *(원문 그대로. "기본적인"의 오타로 보임)*

4단계이며, 모두 `#171C24`(= `color/gray/950`) 기반의 다중 드롭섀도우입니다.

---

## `Elevation.shadow.*`

### `subtle`

```css
box-shadow:
  0 1px 2px 0 rgba(23, 28, 36, 0.12),   /* #171C241F */
  0 0   1px 0 rgba(23, 28, 36, 0.08);   /* #171C2414 */
```

> 배경과 요소를 최소한으로 분리하기 위한 기본 섀도우. 리스트 아이템, 섹션 컨테이너, 헤더·툴바 등
> 경계 인지가 필요한 영역에 사용한다. 시각적 강조 없이 레이아웃 구조를 구분할 때 적합하다.

### `default`

```css
box-shadow:
  0 2px 8px 0 rgba(23, 28, 36, 0.12),
  0 1px 4px 0 rgba(23, 28, 36, 0.08),
  0 0   1px 0 rgba(23, 28, 36, 0.08);
```

> 서비스 전반에서 가장 많이 사용하는 기본 깊이 섀도우. card, input field, button 등 일반적인
> 인터랙션 컴포넌트의 기본 상태에 사용한다. 과하지 않으면서 요소가 배경 위에 떠 있음을 명확히 인지시킨다.

### `raised`

```css
box-shadow:
  0 6px 12px 0 rgba(23, 28, 36, 0.12),
  0 4px  8px 0 rgba(23, 28, 36, 0.08),
  0 0    4px 0 rgba(23, 28, 36, 0.08);
```

> 인터랙션에 따른 떠오름을 강조하는 섀도우. hover, focus, drag 상태의 카드나 선택된 요소 등
> 사용자 액션에 반응하는 UI에 사용한다. **기본 상태에 상시 적용하는 것은 지양한다.**

### `overlay`

```css
box-shadow:
  0 6px 12px 0 rgba(23, 28, 36, 0.12),
  0 4px  8px 0 rgba(23, 28, 36, 0.08),
  0 0   24px 0 rgba(23, 28, 36, 0.12);
```

> 최상위 레이어를 명확히 구분하기 위한 강한 섀도우. 모달, 팝오버, 드롭다운, 바텀시트 등
> 오버레이 컴포넌트에 사용한다. **일반 버튼이나 리스트 요소 등 일반적 요소에는 사용하지 않는다.**

---

## 원본 값 (Figma effect 정의 그대로)

| 토큰 | offset / radius / spread · color |
|---|---|
| `Semantic/Shadow/Subtle` | `(0,1) r2 s0 #171C241F` · `(0,0) r1 s0 #171C2414` |
| `Semantic/Shadow/Default` | `(0,2) r8 s0 #171C241F` · `(0,1) r4 s0 #171C2414` · `(0,0) r1 s0 #171C2414` |
| `Semantic/Shadow/Raised` | `(0,6) r12 s0 #171C241F` · `(0,4) r8 s0 #171C2414` · `(0,0) r4 s0 #171C2414` |
| `Semantic/Shadow/Overlay` | `(0,6) r12 s0 #171C241F` · `(0,4) r8 s0 #171C2414` · `(0,0) r24 s0 #171C241F` |

> 시안 표에 쓰인 토큰 표기는 `Elevation.shadow.subtle` 형태이고,
> Figma 스타일 이름은 `Semantic/Shadow/Subtle` 입니다. 같은 대상의 두 표기입니다.

`raised` 와 `overlay` 는 앞 두 레이어가 동일하고, 세 번째 레이어의 blur(4 → 24)와 alpha(0.08 → 0.12)만 다릅니다.

---

## 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | 표기가 `Elevation.shadow.*` 와 `Semantic/Shadow/*` 로 갈림. 코드 토큰 이름을 어느 쪽으로 할지 |
| 2 | 다크 배경에서의 shadow 대체 규칙(시안에 없음) |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#elevation)
