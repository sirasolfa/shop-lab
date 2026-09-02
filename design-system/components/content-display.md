# Content Display `[F]`

> 출처 — Figma 페이지 **• Content Display** `1595:11126`, Overview 표 `1192:7647`
> 베리언트 이름은 Figma 컴포넌트 세트의 프로퍼티 조합 그대로입니다.

## Overview 상태표

| 컴포넌트 | Status | Last Update |
|---|---|---|
| Accordion | In-progress | N/A |
| Avatar | Before | N/A |
| Draggable list | Before | N/A |
| List | In-progress | 1/26/26 |
| Thumbnail | Done | N/A |
| Image grid | Before | N/A |
| Cards | Done | 2/2/26 |
| Video player | Before | N/A |
| Data table | Before | N/A |

> 상세 페이지의 실제 구성은 이 표와 다릅니다 → [README.md](README.md#overview-표와-상세-페이지의-목록이-다릅니다-)

---

## 상세 페이지의 컴포넌트 11종

### Accordion `1621:13143`

| 프로퍼티 | 값 |
|---|---|
| `type` | `info` · `contents` |
| `size` | `lg` · `md` · `sm` |
| `expand` | `true` · `false` |

베리언트 12개 (2 × 3 × 2).

### Avatar `1621:13663`

| 프로퍼티 | 값 |
|---|---|
| `size` | `xs` · `sm` · `md` · `lg` · `xl` |
| `type` | `empty` · `text` · `image` |
| `state` | `default` · `overlay` |

베리언트 30개 (5 × 3 × 2).

### Carousel `1621:19606`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `Carousel` | `type=horizontal \| vertical` |
| `└ Swiper` (atomic) | `arrow=left \| right \| up \| down`, `state=default \| hover \| disabled` |

### OptionRow `3445:9254`

| 프로퍼티 | 값 |
|---|---|
| `viewport` | `desktop` · `mobile` |
| `showOption` | `true` · `false` |
| `isDisabled` | `true` · `false` |

### Price `3432:15991`

| 프로퍼티 | 값 |
|---|---|
| `type` | `info` · `product` · `cart` |
| `size` | `lg` · `md` |
| `currency` | `KRW` · `USD` · `JPY` |
| `discout` ※오타 | `true` · `false` |

베리언트 36개 (3 × 2 × 3 × 2). 프로퍼티 이름 `discout` 는 **Figma 원문 그대로의 오타**입니다(`discount`).

**다중 통화(KRW / USD / JPY)를 토큰 레벨이 아니라 컴포넌트 베리언트로 다룹니다.**

### Label `1621:17834`

| 프로퍼티 | 값 |
|---|---|
| `size` | `xs` · `sm` · `md` · `lg` |
| `textAlign` | `left` · `center` · `right` |

프레임 안에 `Default Label` / `Hover Label` / `Disabled Label` 상태 예시와 `Tertiary Sizes` 블록,
그리고 `Label(Usage)` 프레임이 있습니다.

> Change Log `260204`: **"required" 필수 입력/선택 표시 추가.**

### List `1621:15994`

여러 하위 컴포넌트를 묶은 프레임입니다.

| 하위 컴포넌트 | 프로퍼티 |
|---|---|
| `TextList` | `type=default` |
| `└ TextList-atomic` | `type=up \| down \| none \| new`, `active=true \| false` |
| `LogoList` | `direction=vertical \| horizontal` |
| `└ LogoList-atomic` | `type=기본` |
| `List/menu` | `Type=Features` |
| `List Item/menu` | `type=feature item \| category menu item` |
| `List/category` | `Type=대분류 \| 중분류`, `Screen=mobile \| desktop` (`대분류` 는 mobile만) |
| `List Item/category` | `type=대분류, selected=True\|False` · `type=중분류, selected=default` |

> 베리언트 값에 한글(`기본`, `대분류`, `중분류`)이 쓰이고, boolean 표기가 `True/False`(대문자)와
> `true/false`(소문자)로 섞여 있습니다. → [naming.md](../guidelines/naming.md)

### Thumbnail `1621:13882`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `Ratio` | `ratio=1:1 \| 1.618:1 \| 16:9`, `color=brand \| gray` |
| `ImageGallery` | `color=brand \| gray`, `state=default \| hover \| selected` |

`Thumbnail(Usage)` 프레임(`2980:8714`)에서 `ratio` · `color` · `showDimmer=true|false` 조합을 예시로 보여줍니다.

> `[?]` 이 프레임 안에 `sfhsfh`, `eryetyeyh`, `Stateㅁ파ㅜ미ㅏㅣㅏㅁ이ㅏㅠs Header` 같은
> **키보드 입력 실수로 보이는 레이어 이름**이 남아 있습니다. 정리 필요.

### Table `1621:13945`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `Table` | `viewport=desktop, type=horizontal, columns=1\|2` · `viewport=desktop, type=vertical, columns=3\|4` · `viewport=mobile, type=horizontal, columns=1\|2` |
| `└ Table-row` | `viewport=desktop, columns=1~4` · `viewport=mobile, columns=1~2` |
| `└ Table-atomic` | `type=head \| body`, `size=lg \| md \| sm` |

`type=horizontal` 은 columns 1–2, `type=vertical` 은 columns 3–4 조합만 존재합니다.
모바일은 columns 1–2 (horizontal)만 있습니다.

### Text List `1621:13964`

| 컴포넌트 | 프로퍼티 |
|---|---|
| `└ List-atomic` | `level=1 \| 2` |
| `└ Bullet` | `type=circle \| hypen` ※오타(`hyphen`) |
| `TextList` | `level=level2` |

### Card `1621:19898` — 가장 큰 컴포넌트 군

`7872 × 14428` 크기의 프레임으로, 5종 카드 + 원자 컴포넌트들로 구성됩니다.

#### ProductCard
| 컴포넌트 | 프로퍼티 |
|---|---|
| `ProductCard` | `viewport=desktop \| mobile` |
| `└ ProductWish-atomic` | `size=lg \| sm`, `selected=true \| false` |
| `└ ProductTitle-atomic` | `size=lg \| md`, `textLines=1 \| 2` |

#### InfoCard
| 컴포넌트 | 프로퍼티 |
|---|---|
| `InfoCard` | `viewport=desktop \| mobile`, `isDiscount=true \| false`, `isOverseas=true \| false` |
| `└ InfoBenefit-atomic` | `viewport`, `type=default \| benefit`, `expanded=true \| false` (`default` 는 `expanded=false` 만) |
| `└ InfoOption-atomic` | `size=md \| sm`, `state=default \| hover \| disabled`, `selected=True \| False` |
| `└ InfoCoupon-atomic` | *(베리언트 없음)* |

`isOverseas` — 해외 배송 상품 표시. 관련 UI로 `Import Duty`(관세) · `Shipping Fee` · `Weight Info` 블록이 있습니다.

#### ProfileCard
| 컴포넌트 | 프로퍼티 |
|---|---|
| `ProfileCard` | `size=lg \| md`, `state=default \| hover \| pressed \| disabled` |
| `└ ProfileWish-atomic` | `size=lg \| sm`, `pressed=true \| false` |

#### EventCard
| 프로퍼티 | 값 |
|---|---|
| `viewport` | `desktop` · `mobile` |
| `status` | `upcoming` · `ongoing` · `ended` |

#### CartItem
| 프로퍼티 | 값 |
|---|---|
| `viewport` | `desktop` · `mobile` |
| `state` | `default` · `selected` · `disabled` |

`Card(Usage)` (`2582:8855`) 안에 `Event Card(Usage)`, `Cart Item(Usage)` 하위 예시가 있습니다.
→ [../patterns/commerce.md](../patterns/commerce.md)

---

## 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | Overview 표와 상세 페이지의 컴포넌트 목록 불일치 (`Draggable list`, `Image grid`, `Video player` 는 상세 없음 / `Carousel`, `Price`, `OptionRow`, `Label`, `Text List` 는 Overview 표에 없음) |
| 2 | `Price` 의 프로퍼티 오타 `discout` |
| 3 | `Bullet` 의 값 오타 `hypen` |
| 4 | 베리언트 boolean 표기 혼용 — `true/false` vs `True/False` |
| 5 | 베리언트 값에 한글 사용 (`type=기본`, `Type=대분류`) — 코드 매핑 규칙 필요 |
| 6 | Thumbnail 프레임의 무의미한 레이어 이름 잔재 |
| 7 | 각 컴포넌트의 `Description` · `Version Info` · `Develop Info` 본문은 이번 조사에서 읽지 않음(스크린샷 필요) |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#components)
