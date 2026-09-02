# Color `[F]`

> 출처 — Figma **Primitve Color Palette** `1:160` (팔레트 리스트 `113:2114`), **Semantic Color Token** `144:419` (표 `148:1242`)
> 값은 `get_variable_defs`로 읽은 변수 실제값이며, 변수에 바인딩되지 않은 칸은 팔레트 스크린샷으로 확인했습니다.

NDS의 색은 2층 구조입니다.

```
primitive  color/<hue>/<step>      ← 원색 팔레트. 화면에서 직접 쓰지 않는다.
    ↓
semantic   color.<role>.<variant>  ← 역할 기반. 화면/컴포넌트는 이쪽만 쓴다.
```

---

## 1. Primitive 팔레트

### gray — 12단계 (유일하게 `150`을 가짐)

| 토큰 | HEX |
|---|---|
| `color/gray/50` | `#fcfdff` |
| `color/gray/100` | `#f9fafd` |
| `color/gray/150` | `#f4f6fb` |
| `color/gray/200` | `#edf0f5` |
| `color/gray/300` | `#e3e6ee` |
| `color/gray/400` | `#c5c9d3` |
| `color/gray/500` | `#a6acb7` |
| `color/gray/600` | `#888e9c` |
| `color/gray/700` | `#697180` |
| `color/gray/800` | `#4b5465` |
| `color/gray/900` | `#2f3744` |
| `color/gray/950` | `#171c24` |

> Change Log `251224`: **`gray 150` 추가 (기존 50→100, 100→150)**, 이후 `gray 50,100,200 hex 변경`.
> 이 리넘버링이 Semantic 표의 라벨에는 아직 반영되지 않은 곳이 있습니다(아래 §3).

### 유채색 — 각 11단계 (50 · 100 · 200 … 950)

| step | pink | red | yellow | green | cyan | blue | indigo |
|---|---|---|---|---|---|---|---|
| 50 | `#fef5fc` | `#fff7f8` | `#fffdf7` | `#f7fcf9` | `#f5fdff` | `#f9fbff` | `#f5f3ff` |
| 100 | `#fde6f7` | `#ffeef1` | `#fffaee` | `#f1fcf4` | `#ebfcff` | `#eef3ff` | `#e4e4ff` |
| 200 | `#fbccef` | `#ffc5cd` | `#ffedb8` | `#c0eed0` | `#b3f2ff` | `#cedbff` | `#cacdff` |
| 300 | `#f8ade5` | `#ffa2af` | `#ffe291` | `#96e1b4` | `#80eaff` | `#aec3ff` | `#a8b0ff` |
| 400 | `#f58ada` | `#ff7a8c` | `#ffd363` | `#68d093` | `#3ddfff` | `#8facff` | `#8a93ff` |
| 500 | `#f159cb` | `#f9556e` | `#ffc439` | `#3fbe75` | `#00d4ff` | `#6f94ff` | `#6c73ff` |
| 600 | `#e900af` | `#e6374f` | `#ffb020` | `#1fa45c` | `#00b3d6` | `#4f7cff` | `#524fe2` |
| 700 | `#c60095` | `#c8263d` | `#cc8a18` | `#17824a` | `#008ca8` | `#355fea` | `#3c37c2` |
| 800 | `#a3007a` | `#9e1d31` | `#996713` | `#10613a` | `#00667a` | `#2747be` | `#330099` |
| 900 | `#800060` | `#751524` | `#66430c` | `#0a3f27` | `#004452` | `#1a318b` | `#260070` |
| 950 | `#5d0046` | `#4d0d18` | `#3d2707` | `#051f15` | `#00262e` | `#111f5c` | `#19004a` |

> Change Log `251224`: `red, green, yellow` 의 `50, 100` HEX 변경.
> `blue/500` `#6F94FF` · `blue/600` `#4F7CFF` 은 변수 바인딩이 없어 팔레트 프레임(`132:256`) 스크린샷에서 읽었습니다.

### base · alpha

| 토큰 | 값 | | 토큰 | 값 |
|---|---|---|---|---|
| `color/base/black` | `#000000` | | `color/base/white` | `#ffffff` |
| `color/alpha/black8` | `#00000014` | | `color/alpha/white8` | `#ffffff14` |
| `color/alpha/black16` | `#00000029` | | `color/alpha/white16` | `#ffffff29` |
| `color/alpha/black24` | `#0000003d` | | `color/alpha/white24` | `#ffffff3d` |
| `color/alpha/black40` | `#00000066` | | `color/alpha/white40` | `#ffffff66` |
| `color/alpha/black64` | `#000000a3` | | `color/alpha/white64` | `#ffffffa3` |
| `color/alpha/black80` | `#000000cc` | | `color/alpha/white80` | `#ffffffcc` |

alpha 단계 이름의 숫자는 **불투명도(%)** 입니다. `black8` = 8% → `14` (hex).

---

## 2. Semantic 토큰

Semantic Color Token 페이지(`144:419`)의 표 원문입니다.
**Role** 열은 시안에 적힌 설명, **문서 매핑**은 표에 인쇄된 primitive 이름,
**변수 실제값**은 `get_variable_defs`가 돌려준 값입니다. 둘이 다르면 ⚠️ 로 표시했습니다.

### text

| 토큰 (표기) | Role (시안 원문) | 문서 매핑 | 변수 | 변수 실제값 |
|---|---|---|---|---|
| `color.text.priamry` ※오타 | 페이지/섹션 제목, 가장 중요한 텍스트 | `color/gray/900` | `color/text/primary` | `#171c24` ⚠️ = gray/**950** |
| `color.text.secondary` | 일반 본문 텍스트 기본 값 | `color/gray/800` | `color/text/secondary` | `#4b5465` ✓ |
| `color.text.tertiary` | 보조 설명, 서브 타이틀, 메타 정보(시간, 서브 라벨 등) | `color/gray/600` | `color/text/tertiary` | `#888e9c` ✓ |
| `color.text.muted` | 플레이스홀더, 덜 중요한 설명 텍스트 (캡션) | `color/gray/500` | `color/text/muted` | `#a6acb7` ✓ |
| `color.text.disabled` | 비활성 상태 텍스트 | `color/gray/400` | `color/text/disabled` | `#c5c9d3` ✓ |
| `color.text.inverse` | 어두운 배경 위에 쓰는 반전 텍스트 | `color/base/white` | `color/text/inverse` | `#ffffff` ✓ |
| `color.text.link` | 링크 텍스트 | `color/blue/700` | `color/text/status/link` | `#355fea` ✓ (변수 경로에 `status/`가 들어감) |

표에는 없지만 변수로 존재: **`color/text/brand`** = `#4f7cff` (= blue/600).

### border

| 토큰 | Role | 문서 매핑 | 변수 실제값 |
|---|---|---|---|
| `color.border.default` | 대부분의 요소(카드, 인풋, 컨테이너)에 사용하는 기본 테두리. | `color/gray/200` | `#edf0f5` ✓ |
| `color.border.strong` | 섹션 구분, 강조 상태(선택됨, 포커스된 블록 등)에 사용하는 더 진한 테두리. | `color/gray/300` | `#c5c9d3` ⚠️ = gray/**400** |
| `color.border.disabled` | *(표에 설명 없음)* | `color/gray/400` | `#e3e6ee` ⚠️ = gray/**300** |
| `color.border.inverse` | 어두운 배경, 브랜드 컬러 위에서 쓰는 반전 테두리. | `color/base/white` | `#ffffff` ✓ |
| `color.border.thumbnail` | *(표에 설명 없음)* | `color/alpha/black8` | `#00000014` ✓ |

표에는 없지만 변수로 존재: **`color/border/neutral`** = `#e3e6ee` (= gray/300).

> ⚠️ **`strong`과 `disabled`의 매핑이 서로 뒤바뀐 상태**입니다. 표대로면 `strong`(gray/300)이
> `disabled`(gray/400)보다 옅어 "더 진한 테두리"라는 설명과도 어긋납니다. 변수 실제값이 설명과 맞습니다.

### divider

| 토큰 | Role | 문서 매핑 | 변수 실제값 |
|---|---|---|---|
| `color.divider.soft` | *(표에 설명 없음)* | `color/gray/100` | `#f4f6fb` ⚠️ = gray/**150** |
| `color.divider.defualt` ※오타 | *(표에 설명 없음)* | `color/gray/200` | `#edf0f5` ✓ |
| `color.divider.strong` | 섹션 경계, 카드 그룹 사이처럼 구획을 더 명확하게 나눌 때 사용하는 진한 디바이더. | `color/gray/300` | `#e3e6ee` ✓ |
| `color.divider.inverse` | 어두운 배경(surface.inverse, brand 영역) 위에서 사용하는 반전 디바이더. | `color/base/white` | `#ffffff` ✓ |

### bg

| 토큰 | Role | 문서 매핑 | 변수 | 변수 실제값 |
|---|---|---|---|---|
| `color.bg.default` | *(표에 설명 없음)* | `color/base/white` | `color/bg/surface/default` | `#ffffff` ✓ |
| `color.bg.subtle` | 섹션을 살짝 분리하거나, 카드/레이아웃 뒤에 까는 보조 배경. | `color/gray/50` | `color/bg/surface/subtle` | `#f9fafd` ⚠️ = gray/**100** |
| `color.bg.muted` | *(표에 설명 없음)* | `color/gray/100` | `color/bg/surface/muted` | `#f4f6fb` ⚠️ = gray/**150** |
| `color.bg.disabled` | *(표에 설명 없음)* | `color/gray/200` | `color/bg/surface/disabled` | `#edf0f5` ✓ |
| `color.bg.dim` | *(표에 설명 없음)* | `color/alpha/black64` | `color/bg/overlay/dim` | `#000000a3` ✓ |
| `color.bg.inverse` | *(표에 설명 없음)* | `color/gray/900` | `color/bg/inverse` | `#2f3744` ✓ |

> 변수 경로에 표에는 없는 중간 그룹(`surface/`, `overlay/`)이 들어갑니다.
> 표기: `color.bg.default` ↔ 변수: `color/bg/surface/default`.

### icon

| 토큰 | Role |
|---|---|
| `color.icon.primary` | 기본 아이콘 색. 주요 기능, 네비게이션, 리스트 안 정보 아이콘 등 가장 자주 쓰는 아이콘에 사용한다. (`color/gray/800`) |
| `color.icon.secondary` | 우선순위가 primary보다 한 단계 낮은 아이콘. 서브 액션, 보조 정보, 리스트 보조 아이콘 등에 사용한다. (`color/gray/600`) |
| `color.icon.muted` | 강조가 필요 없는 아이콘. 설명용, 메타 정보, 비활성에 가깝지만 인터랙션은 유지되는 아이콘에 사용한다. (`color/gray/500`) |
| `color.icon.disabled` | 클릭/탭이 불가능한 비활성 상태 아이콘. disabled 버튼·인풋 옆 아이콘 등에 사용한다. (`color/gray/400`) |
| `color.icon.primary-bg` | *(표에 설명 없음)* (`color/gray/100`) |
| `color.icon.inverse` | *(표에 설명 없음)* (`color/base/white`) |

표에는 없지만 변수로 존재:
**`color/icon/status/primary`** = `#4f7cff`, **`color/icon/brand-bg`** = `#eef3ff` (= blue/100).

### brand

표 형태로 문서화된 절은 없고, 변수로만 확인됩니다.

| 변수 | 값 |
|---|---|
| `brand/default` | `#4f7cff` (= `color/blue/600`) |
| `brand/strongest` | `#1a318b` (= `color/blue/900`) |

---

## 3. 확인 필요 `[?]`

| # | 항목 | 상태 |
|---|---|---|
| 1 | `color.border.strong` ↔ `color.border.disabled` 매핑이 표와 변수에서 뒤바뀜 | 어느 쪽이 정답인지 확정 필요 (설명문은 변수 쪽과 일치) |
| 2 | `text.primary` / `bg.subtle` / `bg.muted` / `divider.soft` 의 표 라벨이 gray 리넘버링 이전 번호 | 표 라벨 갱신 필요로 보임. 변수값은 일관됨 |
| 3 | `color.icon.*` 의 변수 실제값 | 아이콘 그룹 변수는 조사 프레임에서 사용되지 않아 값 미확인. 표의 매핑만 기록함 |
| 4 | `brand/*` 스케일 전체 | `default`, `strongest` 두 개만 확인. 중간 단계 존재 여부 미확인 |
| 5 | `sementic/background/default` `#ffffff` · `sementic/background/inverse` `#0b0b0f` | 컬렉션 이름 오타(`sementic`). `color/bg/*` 와 중복되는 레거시로 보임 |
| 6 | 오타 토큰 `color.text.priamry`, `color.divider.defualt` | Figma 원문 그대로. 코드로 옮기기 전 정정 여부 결정 필요 |

---

AI 제안(코드 export 형태, 다크 모드, 대비 기준) → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#color)
