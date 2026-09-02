# 네이밍 규칙 `[F]`

> 출처 — Figma Change Log 섹션 `20:138` 의 **"네이밍 규칙"** 프레임 `742:1604`

## 원문

> - 컴포넌트 이름(ComponentName) → **PascalCase**
>   - 컴포넌트 종속 시 → **`/`(Slash)** 사용
>     - 종속 정의가 애매한 컴포넌트는 **`-`(Hyphen)** 사용
> - 컴포넌트 프로퍼티(Property / Props) → **camelCase**
> - 프로퍼티 상세값(Value) → **kebab-case**

## 실제 적용 예 `[F]`

| 규칙 | 지켜진 예 |
|---|---|
| PascalCase | `ProductCard`, `InfoCard`, `BottomSheet`, `CompactTooltip`, `TextList`, `LogoList` |
| 종속 = `/` | `Badge/Solid`, `Toast/Text`, `Toast/Icon`, `List/menu`, `List/category`, `Snack bar/leading item` |
| 애매 = `-` | `ProductWish-atomic`, `InfoOption-atomic`, `Table-row`, `Table-atomic`, `TextList-atomic`, `home_indicator__atomic` |
| camelCase 프로퍼티 | `showTrailingIcon`, `isDiscount`, `isOverseas`, `showOption`, `isDisabled`, `textLines`, `textAlign` |
| kebab-case 값 | `external-link`, `music-video`, `verified-check`, `feature item` `[?]`(공백), `category menu item` `[?]`(공백) |

원자 컴포넌트는 이름 앞에 **`└ `** 를 붙여 트리 구조를 시각화합니다 (`└ OptionRow`, `└ Swiper`).

---

## 규칙에서 벗어난 사례 `[?]`

정정 대상 후보입니다. 코드로 옮기기 전에 정본을 정해야 합니다.

### 대소문자 / 표기 혼용

| 위치 | 현재 | 규칙대로면 |
|---|---|---|
| Drawer | `Open drawer on=right` | 문장형 프로퍼티. camelCase (`openOn`) |
| Drawer | `Size=default` | `size` |
| Snack Bar | `Name=Snack bar` | `name` |
| Snack bar/leading item | `Type=Icon \| Slot` | `type=icon \| slot` |
| Table | `viewport` / `columns` (소문자) ↔ List `Type` / `Screen` (대문자) | 소문자 통일 |
| InfoOption / List Item | `selected=True \| False` | `selected=true \| false` |
| Snack bar | 컴포넌트명 `Snack bar` (공백 + 소문자) | `SnackBar` |
| Bottom Sheet 프레임 | `Bottom Sheet` ↔ 컴포넌트 `BottomSheet` | 프레임/컴포넌트 표기 분리 확인 |
| Toast | `Icon=True \| False`, `Line=Single \| Multi` | `icon` / `line`, 값은 소문자 |

### 한글 값

| 위치 | 값 |
|---|---|
| `LogoList-atomic` | `type=기본` |
| `List/category` | `Type=대분류 \| 중분류` |
| `List Item/category` | `type=대분류 \| 중분류` |
| Iconography | `사용X/...` 카테고리 접두 |

코드 매핑 규칙이 필요합니다(예: `대분류` → `major`).

### 오타

| 위치 | 현재 | 올바른 표기 |
|---|---|---|
| Semantic Color 표 | `color.text.priamry` | `primary` |
| Semantic Color 표 | `color.divider.defualt` | `default` |
| 변수 컬렉션 | `sementic/background/*` | `semantic` |
| Price | `discout` | `discount` |
| Text List | `Bullet type=hypen` | `hyphen` |
| Toast(Usage) | `Loading Cirlce` | `Circle` |
| Snack Bar | `Lable` | `Label` |
| Foundation 프레임 | `Primitve Color Palette` | `Primitive` |
| Foundation 섹션 | `System Conponent` | `Component` |
| Elevation 설명 | "기복적인 방법" | "기본적인 방법"으로 추정 |
| Change Log (Input) | `showTrailingIn` | `showTrailingIcon` 으로 추정 |

### 토큰 표기 두 갈래

문서 표는 점 표기(`color.text.secondary`), Figma 변수는 슬래시 경로(`color/text/secondary`)를 씁니다.
게다가 일부는 **경로 구조 자체가 다릅니다.**

| 문서 표 | 변수 경로 |
|---|---|
| `color.bg.default` | `color/bg/surface/default` |
| `color.bg.dim` | `color/bg/overlay/dim` |
| `color.text.link` | `color/text/status/link` |
| `Elevation.shadow.subtle` | `Semantic/Shadow/Subtle` |

---

AI 제안(코드 네이밍 변환 규칙) → [ai-guidelines.md](ai-guidelines.md#naming)
