# Commerce 패턴 `[F]`

> 출처 — `Card(Usage)` `2582:8855`, `Action Area(Usage)`(Bottom Sheet `1065:18681`), `Search(Usage)` `1170:5163`
> 아래는 Usage 프레임의 **레이어 구성에서 읽어낸 조합**입니다. 픽셀 수치는 조사하지 않았습니다.

NDS는 커머스(NOVERA shop) 전용 개념을 컴포넌트 레벨에 직접 담고 있습니다:
상품 · 가격 · 통화 · 할인 · 해외배송/관세 · 옵션 · 장바구니 · 아티스트 · 이벤트.

---

## 1. 상품 카드 (ProductCard)

`Card(Usage)` 의 `Product Card` 블록 구성 — desktop / mobile 뷰포트를 나란히 제시합니다.

```
ProductCard (viewport=desktop | mobile)
├ Image Area
│  ├ Ratio                     ← Thumbnail 계열. ratio=1:1 | 1.618:1 | 16:9
│  ├ Image Background
│  └ Badge                     ← 상태/프로모션 뱃지
├ └ ProductWish-atomic         ← 찜(하트). size=lg|sm, selected=true|false
├ Bottom Container
│  ├ └ ProductTitle-atomic     ← size=lg|md, textLines=1|2
│  └ Price Area
│      └ └ Price               ← type=product, currency=KRW|USD|JPY, discout=true|false
└ BadgeContainer / └ count
```

`Product List` 는 위 카드를 나열한 목록 예시이고, `Currency Switcher` 로 통화 전환 예시를 함께 보여줍니다.

**통화는 Price 컴포넌트의 베리언트**(`currency=KRW | USD | JPY`)로 처리합니다. → [../components/content-display.md](../components/content-display.md#price-343215991)

## 2. 상품 상세 (InfoCard)

```
InfoCard (viewport, isDiscount, isOverseas)
├ Top Container
│  └ Artist Container          ← Avatar + Artist Text + Chevron Icon
├ Content Container
│  ├ Product Title / Product Description
│  ├ Discount Info             ← isDiscount=true 일 때
│  └ └ Price
├ Select Area
│  ├ SelectField
│  └ └ OptionRow               ← 옵션 선택 행
├ Shipping Select Area
│  ├ Shipping Info Container   ← └ Label + application/delivery 아이콘
│  └ Shipping Select Container
├ Accordion Container
│  ├ Product Information
│  └ Additional Product Information
└ ButtonActionBar              ← 하단 고정 액션
```

### 해외 배송 (`isOverseas=true`)

`isOverseas` 가 켜지면 아래 블록이 추가로 노출됩니다.

| 블록 | 구성 |
|---|---|
| `Weight Info Container` | `Weight Label` + `Weight Value` |
| `Calculation Info Container` | `suggested/info` 아이콘 + `Shipping Calculation Info` |
| `Shipping Fee Container` | `Shipping Fee Label` + `Shipping Fee Info` |
| `Import Duty Container` | `Import Duty Label` + `Import Duty Info` (관세) |

### 혜택 / 쿠폰 / 옵션 원자 컴포넌트

| 컴포넌트 | 프로퍼티 |
|---|---|
| `└ InfoBenefit-atomic` | `viewport`, `type=default \| benefit`, `expanded=true \| false` |
| `└ InfoOption-atomic` | `size=md \| sm`, `state=default \| hover \| disabled`, `selected=True \| False` |
| `└ InfoCoupon-atomic` | 베리언트 없음 |

## 3. 장바구니 (CartItem)

`Cart Item(Usage)` 와 바텀시트의 `Action Area(Usage)` 두 곳에 같은 조합이 나옵니다.

```
CartItem (viewport=desktop|mobile, state=default|selected|disabled)
├ └ Checkbox-atomic            ← 선택
├ Product Info
│  ├ Product Container
│  │  └ Ratio                  ← 썸네일
│  └ Product Details
│      ├ Product Name
│      └ Price Container
│          ├ Price Label
│          └ Price Details → Currency + Price Amount
├ addOptionRow / └ OptionRow   ← 옵션 추가·변경
└ IconOnly                     ← 삭제 등 아이콘 버튼
```

바텀시트 버전은 여기에 `ActionArea` + `ButtonPair` 가 붙습니다
(`Bottom Sheet` `1065:18681` 안의 `Action Area(Usage)`).

**즉 장바구니는 "화면"이 아니라 `BottomSheet` + `CartItem` + `ActionArea` 조합으로 정의돼 있습니다.**

## 4. 이벤트 카드 (EventCard)

`Event Card(Usage)` — `viewport=desktop | mobile` × `status=upcoming | ongoing | ended`.
상태 3단계가 컴포넌트 베리언트로 들어가 있어, 진행 전/중/종료 표현을 컴포넌트가 직접 갖습니다.

## 5. 프로필 카드 (ProfileCard)

`size=lg | md` × `state=default | hover | pressed | disabled`.
`└ ProfileWish-atomic`(`size`, `pressed`)로 팔로우/찜 인터랙션을 분리했습니다.
아티스트 프로필 표현에 쓰이는 것으로 보입니다 `[?]`(용도 명시 문구는 미조사).

## 6. 검색

`Search(Usage)` `1170:5163` — `1440 × 9388` 의 세로로 긴 흐름 프레임.
Overview 상 `Inputs > Search` 는 **Done** 상태입니다.
`[?]` 단계별 화면(입력 전 / 자동완성 / 결과 / 결과 없음)의 구체 구성은 이번 조사에서 확인하지 않았습니다.

---

## 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | 각 Usage 프레임의 실제 치수(카드 폭, 갭, 패딩) — 레이어 구조만 조사함 |
| 2 | `Search(Usage)` 내부 단계별 화면 |
| 3 | 상품 상태(품절/재입고/한정) 표현 규칙 — `Badge` 가 Done이나 값 정의 미확인 |
| 4 | 통화 전환(`Currency Switcher`)의 동작 규칙 |
| 5 | `ProfileCard` 의 용도 |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#patterns)
