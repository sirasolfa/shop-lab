# AI 제안 가이드라인 `[A]`

> ⚠️ **이 문서의 모든 내용은 Figma에 근거가 없습니다.**
> AI가 일반적 관례와 이 시스템의 관측된 패턴에 기대어 만든 **초안**이며, 팀이 채택하기 전까지 규범이 아닙니다.
> 대비되는 사실 문서는 [`../foundations/`](../foundations/README.md), [`../components/`](../components/README.md),
> [`../patterns/`](../patterns/README.md), [`naming.md`](naming.md), [`changelog.md`](changelog.md).

각 제안에는 **근거**(무엇에 기댔는지)와 **확정 조건**(무엇을 확인하면 사실이 되는지)을 붙였습니다.

---

## 0. 가장 먼저 결정해야 할 것

사실 문서에서 발견된 불일치는 AI가 임의로 고를 수 없습니다. 아래 5개는 **사람이 정해야** 합니다.

| # | 결정 사항 | AI가 권하는 쪽 | 이유 |
|---|---|---|---|
| 1 | `layout.spacing.xl/2xl/3xl` = 32/40/48 인가 **28/32/40** 인가 | **28/32/40** (변수값) | 시안의 막대 길이와 변수가 일치. 인쇄된 텍스트만 어긋남 |
| 2 | `color.border.strong` / `.disabled` 매핑 | **변수값** (strong=gray/400, disabled=gray/300) | 표의 설명문("더 진한 테두리")과 변수값이 일치 |
| 3 | 오타 토큰(`priamry`, `defualt`, `discout`, `sementic`) 정정 시점 | **코드 export 시점에 정정 + Figma도 함께 수정** | 코드에만 고치면 영구 불일치 |
| 4 | 토큰 표기 정본 — 점 표기 vs 슬래시 경로 | **Figma 변수 경로를 정본**, 문서 표는 별칭 | 변수는 도구가 읽는 실체, 표는 사람이 읽는 라벨 |
| 5 | Grid 컬럼/거터 | Figma에서 직접 확인 필요 | MCP로 읽을 수 없음. 추정하지 않음 |

---

## Color

### C-1. 코드 토큰 2층 구조를 그대로 유지

**제안** — CSS 변수도 primitive / semantic 두 층으로 내보내고, 컴포넌트 CSS는 semantic만 참조합니다.

```css
:root {
  /* primitive — 직접 쓰지 않는다 */
  --color-gray-950: #171c24;
  --color-blue-600: #4f7cff;

  /* semantic — 컴포넌트는 이쪽만 */
  --color-text-primary:   var(--color-gray-950);
  --color-bg-surface-default: var(--color-base-white);
}
```

**근거** — Figma가 이미 이 구조(`primitive` 컬렉션 → semantic 변수)를 갖고 있음.
**확정 조건** — 팀이 CSS 변수 / Tailwind theme / TS 상수 중 무엇을 산출물로 삼을지 정하면 확정.

### C-2. 이름은 슬래시 → 케밥 하이픈으로 기계 변환

`color/bg/surface/default` → `--color-bg-surface-default` / `colorBgSurfaceDefault`.

**근거** — 경로 깊이를 잃지 않는 가장 단순한 변환.
**확정 조건** — 문서 표의 점 표기(`color.bg.default`)와 어긋나므로 [0-4] 결정이 선행돼야 함.

### C-3. 다크 모드는 아직 만들지 않기를 권함

**제안** — 지금은 `color.*.inverse` / `alpha/white*` / `bg.inverse` 로 **부분 반전만** 처리하고,
전체 다크 테마는 별도 과제로 미룹니다.

**근거** — 시안에서 `theme=light|dark` 를 가진 것은 Tooltip 계열과 로고뿐입니다.
semantic 색에 다크 모드 값(Figma 변수 모드)이 정의된 흔적이 없습니다.
**확정 조건** — Figma 변수 컬렉션에 dark 모드가 추가되면 그 값을 그대로 옮기면 됩니다. 추정으로 만들지 않기.

### C-4. 상태 색(success/error/warning/info) 세트 보강 필요

**제안** — `suggested/` 아이콘은 `info · warning · help · success · delete` 5종을 갖는데,
대응하는 semantic 색 토큰은 `color/text/status/link` 와 `color/icon/status/primary` 만 관측됩니다.
아이콘 5종에 맞춰 `color.text.status.*` / `color.bg.status.*` / `color.icon.status.*` 를 채우기를 제안합니다.
팔레트에는 이미 `green`(success) · `red`(error) · `yellow`(warning) · `blue`(info) 가 전 단계 존재합니다.

**근거** — 아이콘과 Toast(`type=success|error|info`)는 있는데 색 토큰이 비어 있음.
**확정 조건** — Toast 컴포넌트가 실제로 어떤 색을 쓰는지 Figma에서 확인.

### C-5. 대비(contrast) 점검 대상

계산해 보면 주의가 필요한 조합이 있습니다. **AI 계산이므로 실측 검증 필요.**

| 조합 | 용도 | 비고 |
|---|---|---|
| `text.muted` `#a6acb7` on `bg.default` `#ffffff` | 플레이스홀더·캡션 | 일반 텍스트 기준(4.5:1)에 미달로 보임 |
| `text.disabled` `#c5c9d3` on `#ffffff` | 비활성 | 비활성은 대비 예외이나 명시 필요 |
| `text.tertiary` `#888e9c` on `#ffffff` | 메타 정보 | 경계선상 |

**제안** — 캡션/메타처럼 **작은 글자에는 `text.muted` 대신 `text.tertiary` 이상**을 쓰고,
`text.muted` 는 플레이스홀더 등 대비 예외가 인정되는 곳에 한정합니다.
**확정 조건** — 팀의 접근성 목표(WCAG AA / AAA) 확정 후 실측.

---

## Typography

### T-1. 사이즈를 토큰화하지 않기로 한 결정을 존중

Change Log `251215`가 "font-family와 font-weight만 토큰화"라 못 박았고, `251217`의 "폰트 사이즈 토큰화 고민"은
취소선 처리됐습니다. **코드에서도 사이즈 변수를 새로 만들지 말고, 텍스트 스타일 단위로 내보내기**를 제안합니다.

```css
.nds-title-3 { font-size: 26px; line-height: 1.3; letter-spacing: 0; font-weight: 700; }
```

**근거** — 시안의 명시적 결정.
**확정 조건** — 별도 확인 불필요. 결정이 뒤집히면 로그에 남을 것.

### T-2. 레벨 → 용도 기본 매핑 (초안)

Figma는 예시 문구만 보여줄 뿐 "언제 무엇을" 규칙이 없습니다. 아래는 AI 초안입니다.

| 레벨 | 제안 용도 |
|---|---|
| `Display/1·2` | 랜딩·프로모션 히어로 |
| `Title/1~3` | 페이지 제목, 큰 섹션 제목 |
| `Title/4·5` | 카드/모달 제목, 서브 섹션 |
| `Subtitle/1~3` | 제목 아래 보조 줄, 리스트 그룹 헤더 |
| `Body/1~4` | 본문 (**`Body` 절의 "기본값으로 사용합니다" 주석 근거**) |
| `Action/*` | 버튼·링크 (Change Log 근거) |
| `Label/*` | 폼 라벨, 입력 필드 라벨 |
| `Caption/*` | 캡션·메타·상태 문구 (스타일 description 근거) |

**근거** — `Body` 기본값 주석과 Change Log의 action/label 언급만 사실. 나머지 행은 관례 기반.
**확정 조건** — Typography(Usage) 각 섹션의 설명 문구를 스크린샷으로 정독하면 상당수 확정 가능.

### T-3. 반응형 타이포는 도입하지 않기를 권함

**제안** — 브레이크포인트별로 같은 레벨의 사이즈를 바꾸지 말고, **레벨 자체를 바꿔** 대응합니다
(desktop `Title/2` → mobile `Title/4`).

**근거** — 시안의 텍스트 스타일에 뷰포트 축이 없고, 컴포넌트는 `viewport` 베리언트로 대응합니다.
**확정 조건** — Typography(Usage)의 `Design Only/Viewport` 칩(`Mobile` 등)이 레벨별로 어떻게 붙어 있는지 확인.

### T-4. 폰트 로딩

`Pretendard Variable` 가변 폰트 1개만 쓰므로 `font-display: swap` + `woff2` 서브셋 1파일을 제안합니다.
weight 400/600/700만 쓰이므로 가변 축 범위를 400–700으로 좁힐 수 있습니다.

**근거** — 변수에 정의된 웨이트가 3종.
**확정 조건** — 라이선스/배포 방식(자체 호스팅 vs CDN) 결정.

---

## Layout & Grid

### L-1. 브레이크포인트 코드화 (초안)

시안은 3개 뷰포트만 정의하고 **376–767px 구간이 비어** 있습니다. AI 제안은 그 구간을 모바일에 포함시키는 것입니다.

```css
/* 제안 */
--bp-tablet:  768px;   /* 768 ~ 1199 : Tablet */
--bp-desktop: 1200px;  /* 1200~      : Desktop */
/*             ~767    : Mobile (375 시안 기준으로 유동) */
```

**근거** — 시안의 "1200px 이상 / 1200px 미만 768px 이상" 은 사실. "375px 이하"를 767까지 확장하는 것은 추정.
**확정 조건** — 디자이너에게 376–767 구간의 의도를 확인.

### L-2. 컴포넌트는 tablet 베리언트를 만들지 않기

**제안** — 컴포넌트 레벨에서는 `viewport=desktop | mobile` 두 축만 유지하고,
태블릿은 desktop 레이아웃을 폭만 줄여 씁니다.

**근거** — 모든 컴포넌트 베리언트가 `desktop | mobile` 2값뿐. tablet 베리언트가 하나도 없음.
**확정 조건** — Grid 페이지에 tablet 컬럼 정의가 실제로 있는지 확인(현재 MCP 미노출).

### L-3. gap / spacing 사용 구분을 린트로 강제

시안 규칙("gap은 요소 사이, spacing은 안팎 여백, 임의 숫자 금지")을 코드에서도 지키려면
`gap` 속성에는 `--layout-gap-*`, `padding`/`margin` 에는 `--layout-spacing-*` 만 허용하는
stylelint 규칙을 두기를 제안합니다.

**근거** — 시안 설명문이 명시적으로 요구.
**확정 조건** — 없음(도구 선택 문제).

### L-4. `sm` 단계 추가 여부

spacing 스케일에 `sm` 이 비어 있습니다(`xs 16` → `md 20`). 간격이 4px뿐이라 **의도적 생략으로 보이며,
비워 두기를 권합니다.** 나중에 채우면 기존 값의 의미가 흔들립니다.

**근거** — 추정.
**확정 조건** — 디자이너 확인.

---

## Shape

### S-1. 컴포넌트별 라운드 매핑 (시안 Role을 표로 정리한 것)

Role 문장에 이미 대상이 적혀 있어, 아래는 **재배열일 뿐 새 제안은 `xs` 행뿐**입니다.

| 토큰 | 대상 |
|---|---|
| `none` (0) | 리스트 헤더, 디바이더, 테이블 셀 |
| `xxs` (4) | 토글 핸들, 작은 배지, 라벨형 버튼 |
| **`xs` (6)** | **`[A]` 칩/태그처럼 xxs보다 크고 sm보다 작은 소형 요소** — 시안 Role이 비어 있어 AI가 채운 칸 |
| `sm` (8) | 기본 버튼, 입력 필드, 카드 |
| `md` (12) | 대형 카드, 강조 섹션, 주요 surface |
| `lg` (16) | 다이얼로그, 팝업 |
| `xl` (24) | 바텀시트, 드로워 |
| `full` (999) | 아바타, 아이콘 버튼, 칩/태그, 숫자 배지 |

> `xs` 제안이 `full` 의 "칩/태그"와 겹칩니다. 디자이너 확인이 필요한 자리입니다.

---

## Elevation

### E-1. 토큰 이름은 `Semantic/Shadow/*` 대신 `elevation.shadow.*` 로

**제안** — 코드에서는 `--elevation-shadow-subtle` 형태를 쓰고, Figma 스타일 이름은 별칭으로 둡니다.

**근거** — 시안 표가 `Elevation.shadow.*` 표기를 쓰고, 다른 토큰군(`color`, `layout`, `shape`)과 결이 맞음.
**확정 조건** — [0-4] 표기 정본 결정에 함께 포함.

### E-2. `raised` 는 상태 전용으로 제한

시안이 "기본 상태에 상시 적용하는 것은 지양한다"고 명시했으므로,
코드에서 `:hover` / `:focus-visible` / `[data-dragging]` 밖에서 `raised` 를 쓰면 리뷰에서 거르기를 제안합니다.

**근거** — 시안 문장은 사실. 린트로 강제하자는 것이 제안.

---

## Iconography

### I-1. 아이콘 컴포넌트 API (초안)

```tsx
<Icon name="application/bag" size={24} />
<Icon name="direction/chevron" type="right" size={16} />
```

**제안**
- `name` 은 Figma의 `카테고리/이름` 경로를 그대로 문자열로 받습니다.
- `size` 는 `12 | 16 | 20 | 24 | 28 | 32 | 40` 리터럴 유니온.
- 색은 prop이 아니라 `currentColor` 상속 → 부모에서 `color.icon.*` 지정.

**근거** — Figma의 사이즈 베리언트는 사실. API 형태는 제안.
**확정 조건** — 코드 컴포넌트 라이브러리 구조 결정.

### I-2. `사용X/` 아이콘은 export 대상에서 제외

**제안** — 빌드 시 `사용X/` 접두 아이콘은 번들에 넣지 않되, 파일에서 지우지는 않습니다.

**근거** — 접두가 미사용 표시인 것은 사실. 번들 제외는 제안.
**확정 조건** — `사용X` 가 "폐기"인지 "보류"인지 디자이너 확인.

### I-3. 네이밍 메모(`[의미]-[형태]-[스타일]`)는 채택하지 않기를 권함

**제안** — 현행 `카테고리/이름 + 베리언트` 를 유지합니다.

**근거** — 메모 자체가 "고민.."·"그룹핑 필요... 고민"으로 미결 상태이고,
이미 200개 가까운 아이콘이 현행 규칙으로 만들어져 있어 전환 비용이 큽니다.
**확정 조건** — 디자이너가 메모를 폐기 처리하면 확정.

---

## Brand

### B-1. 파비콘 산출 세트 (초안)

Figma 컴포넌트는 `type=default` 하나뿐이라 실제 파일 규격은 정의돼 있지 않습니다.

| 파일 | 크기 | 용도 |
|---|---|---|
| `favicon.svg` | 벡터 | 최신 브라우저 |
| `favicon-32.png` | 32×32 | 폴백 |
| `apple-touch-icon.png` | 180×180 | iOS 홈 화면 |
| `icon-512.png` | 512×512 | PWA manifest |

**근거** — 일반적 웹 관례.
**확정 조건** — 디자이너가 Figma에 export 규격을 추가하면 대체.

### B-2. OG 이미지

Figma가 `600*600` 과 `1200*600` 두 규격을 정의했습니다. 웹 표준 권장은 `1200×630` 이라
`1200*600` 과 30px 차이가 납니다. **`1200×630` 으로 조정 제안** — 다만 시안 값은 `1200*600` 입니다.

**근거** — Open Graph 권장 규격.
**확정 조건** — 디자이너 판단.

### B-3. 로고 clear space

시안에 여백 규정이 없습니다. **심볼 높이의 1/2 을 최소 여백**으로 두는 관례를 제안합니다.

**근거** — 일반 관례. Figma 근거 없음.
**확정 조건** — 브랜드 가이드 확인.

---

## Components

### CO-1. 코드 컴포넌트 우선순위 (초안)

Overview 상태와 실제 사용 빈도를 함께 본 제안입니다.

| 순위 | 대상 | 이유 |
|---|---|---|
| 1 | `Button`, `Text input`, `Checkbox` | 다른 컴포넌트 안에 이미 인스턴스로 박혀 있음. Button은 In-progress이나 스펙(높이·타입)이 로그에 확정돼 있음 |
| 2 | `Price`, `Thumbnail`(Ratio), `Badge` | 커머스 화면의 최소 단위. Price는 베리언트 36개로 이미 완성도 높음 |
| 3 | `ProductCard`, `CartItem` | 위 1·2를 조합. 상세 페이지가 가장 잘 정의돼 있음 |
| 4 | `BottomSheet`, `Dialog`, `Toast`, `Tooltip` | Done 비율이 높은 오버레이 군 |
| 5 | 나머지 Before 항목 | 스펙 미정의 |

**근거** — 상태표와 인스턴스 사용 관계는 사실. 순위는 제안.

### CO-2. 베리언트 → props 변환 규칙 (초안)

| Figma | 코드 |
|---|---|
| `viewport=desktop \| mobile` | **prop으로 만들지 말 것.** CSS 미디어 쿼리로 처리 |
| `size=xs\|sm\|md\|lg\|xl` | `size` prop, 리터럴 유니온 |
| `state=default\|hover\|pressed\|disabled` | **prop 아님.** CSS 의사 클래스 + `disabled` 속성 |
| `selected` / `expanded` / `active` | boolean prop (제어 컴포넌트) |
| `isDiscount` / `isOverseas` / `showOption` | boolean prop |
| `type` / `theme` / `direction` / `align` | 문자열 유니온 prop |
| `Type=대분류\|중분류` | `level="major" \| "sub"` 로 영문 매핑 |
| `True/False` (대문자) | `true/false` 로 정규화 |

**근거** — 변환 필요성은 사실(한글 값·대문자 boolean 존재). 매핑 값은 제안.
**확정 조건** — 한글 값의 영문 대응어를 디자이너와 합의.

### CO-3. `viewport` 를 prop으로 두지 말자는 근거

Figma는 데스크톱/모바일을 **다른 베리언트**로 그리지만, 웹 구현에서 같은 컴포넌트가
prop으로 레이아웃을 바꾸면 SSR/하이드레이션에서 깜빡임이 생깁니다.
`Table` 처럼 구조가 크게 달라지는 경우에만 예외적으로 분기하기를 제안합니다.

**근거** — 일반적 구현 경험. Figma 근거 없음.

### CO-4. `Top navigation_mobile / _desktop` 은 코드에서 하나로

Figma는 두 개의 별도 컴포넌트지만, 코드에서는 `<TopNavigation />` 하나로 두고 CSS로 분기하기를 제안합니다.

**근거** — 다른 모든 컴포넌트가 `viewport` 베리언트를 쓰는데 이것만 이름을 나눈 것은 파일 관리 사정으로 보임.
**확정 조건** — 두 컴포넌트의 실제 구조 차이 확인(상세 프레임이 이 파일에 없어 미확인).

### CO-5. 상태 정의가 비어 있는 컴포넌트

`Before` 24개는 스펙이 없으므로 **코드 구현을 시작하지 않기**를 권합니다.
특히 `Divider` 는 색 토큰이 이미 완비돼 있어 유혹이 있지만, 두께·여백 규정이 없습니다.

---

## Patterns

### P-1. 화면이 아니라 조합으로 문서화하는 방식을 유지

NDS는 "장바구니 화면"을 그리지 않고 `BottomSheet + CartItem + ActionArea` 조합으로 정의합니다.
코드 문서(Storybook 등)도 같은 단위로 만들기를 제안합니다.

**근거** — 시안의 구성 방식은 사실. 코드 문서 구조는 제안.

### P-2. 빠져 있는 패턴

시안에 아직 없는, 커머스에 필요한 패턴 목록입니다. 만들 때 참고용 제안입니다.

- 빈 상태 (검색 결과 없음 / 장바구니 비어 있음) — `Empty state` 는 `Before`
- 로딩 (스켈레톤) — `Skeleton` 은 `Before`
- 에러 (네트워크 실패 / 결제 실패) — `System message` 는 `Before`
- 폼 검증 오류 표시 규칙
- 무한 스크롤 vs `Pagination` 사용 기준 (`Pagination` 은 In-progress)

### P-3. 다중 통화 처리

`Price` 가 `currency=KRW|USD|JPY` 를 베리언트로 갖습니다. 코드에서는 `Intl.NumberFormat` 으로
포맷하되, **통화 기호 위치·소수점 자릿수는 Figma 베리언트의 렌더 결과를 정본으로** 맞추기를 제안합니다.

**확정 조건** — 세 통화 각각의 렌더 결과를 스크린샷으로 확인.

---

## Naming

### N-1. Figma → 코드 이름 변환 규칙 (초안)

| 대상 | Figma | 코드 |
|---|---|---|
| 컴포넌트 | `ProductCard` | `ProductCard` (그대로) |
| 종속 컴포넌트 | `Badge/Solid` | `Badge.Solid` (컴파운드) 또는 `BadgeSolid` |
| 원자 컴포넌트 | `└ ProductWish-atomic` | `ProductWish` (`└ `, `-atomic` 제거) |
| 프로퍼티 | `showTrailingIcon` | 그대로 |
| 프로퍼티(이탈 사례) | `Open drawer on` | `openOn` |
| 값 | `external-link` | 그대로 |
| 값(한글) | `대분류` | `major` |
| 토큰 | `color/text/primary` | `--color-text-primary` |

**근거** — 변환 필요성은 사실. 매핑은 제안.

### N-2. 오타는 코드에서 정정하되 매핑 표를 남길 것

`priamry → primary`, `defualt → default`, `discout → discount`, `hypen → hyphen`, `sementic → semantic`.
자동 동기화 스크립트를 쓸 경우 **예외 매핑 표**를 코드에 둬야 Figma 갱신 시 깨지지 않습니다.

### N-3. 문서 갱신 운영 (초안)

- Figma Change Log에 항목이 추가되면 [`changelog.md`](changelog.md) 에 옮기고, 영향 문서를 함께 고칩니다.
- 파운데이션 값은 분기 1회 `get_variable_defs` 재조회로 대조합니다.
- `[?]` 항목이 해소되면 사실 문서로 옮기고 `[?]` 를 지웁니다.
- 이 파일의 항목이 채택되면 해당 사실 문서로 옮기고 여기서 삭제합니다.

---

## 이 문서가 다루지 않는 것

AI가 임의로 정하면 위험한 영역이라 제안조차 넣지 않았습니다.

- Grid 컬럼/거터 수치 — 추정하면 전 화면이 어긋납니다. Figma에서 직접 확인해야 합니다.
- 미확인 텍스트 스타일(`Caption/1`, `Caption/3`, `Caption/semibold/2·3`)의 값
- `color.icon.*` 의 실제 HEX
- `Before` 상태 24개 컴포넌트의 스펙
