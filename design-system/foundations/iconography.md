# Iconography `[F]`

> 출처 — Figma **Icon Grid** `2442:11467`, **Iconography** `1209:12283`, 네이밍 메모 `610:4742`

---

## 1. 아이콘 그리드

Icon Grid 프레임은 **24 × 24** 셀 기준의 base grid를 정의합니다.
프레임 안에 `base` / `cell` / `grid`(1–24 눈금) / `line`(`24px` 라벨) / `space` 영역이 그려져 있습니다.

| 항목 | 값 |
|---|---|
| 기본 캔버스 | `24 × 24` |
| 눈금 | 1 ~ 24 (가로·세로) |
| 구성 요소 | `line`(획 영역), `space`(여백 영역) 사각형 가이드 |

> `[?]` 획 두께(stroke width), safe area 여백의 **수치**는 도형으로만 그려져 있고 텍스트 수치가 없어
> MCP로 확정하지 못했습니다.

## 2. 아이콘 사이즈

Iconography 프레임의 `icon` 컴포넌트가 갖는 `size` 베리언트입니다.

`12` · `16` · `20` · `24` · `28` · `32` · `40`

24가 기준 그리드이며, 나머지는 그 배율/축소입니다.

## 3. 네이밍

아이콘 컴포넌트는 **`카테고리/이름`** 경로에 베리언트 프로퍼티를 붙이는 형태입니다.

```
direction/chevron   ·  type=right|left|up|down, size=lg|sm
suggested/info      ·  fill=true|false
editor/eye          ·  view=true|false, fill=true|false
application/bag     ·  name=bag
company/KakaoTalk   ·  mode=white|black
```

### 미확정 메모 (`610:4742`)

시안 옆에 붙은 **"[개발] 아이콘 네이밍 고민.."** 메모의 원문입니다. 결론이 아니라 검토 중인 안입니다.

> 규칙안: **`[의미]-[형태]-[스타일]`**
> - 의미: `heart, check, error, success, info, edit, user, chevron, bag, menu`
> - 형태: `small, tight, left, right, up, down`
> - 스타일: `outline`(기본 — 명시 X) / `filled` / `duotone`
>
> 메모에 함께 적힌 코멘트
> - "정렬 순서를 고려하면 **크기가 방향보다 먼저**"
> - "`outline` 명시 X"
> - "닫기로 쓸 수도 삭제로 쓸 수도 있으니" (= `close`/`delete` 의미 중복 고민)
> - "그룹핑 필요... 고민"

현재 라이브러리에 실재하는 이름은 이 메모안이 아니라 아래 §4의 `카테고리/이름` 형태입니다.

## 4. 아이콘 목록

`사용X/` 접두는 **Figma에서 그렇게 이름 붙여 둔 것**이며, 현재 미사용 표시로 보입니다.

### `direction/` — 방향

| 이름 | 베리언트 |
|---|---|
| `direction/chevron` | `type=right\|left\|up\|down`, `size=lg\|sm` |
| `direction/arrow` | `type=right\|left\|up\|down` |
| `direction/caret` | `type=right\|left\|up\|down` |
| `direction/circle` | `type=right\|left\|up\|down`, `fill=true\|false` |
| `direction/expand` | `horizontal=right\|left`, `vertical=up\|down` |

### `suggested/` — 상태·알림

`info` (`fill`) · `warning` (`fill`) · `help` · `success` · `delete` · `close` (`name=x`) · `check` (`name=check`)

### `editor/` — 편집

`counter` (`type=plus\|minus`) · `circle` (`type=plus\|minus`, `fill`) · `square` · `eye` (`view`, `fill`) ·
`copy` · `edit` · `write` · `link` · `trash` · `handle` · `calendar` · `image` · `sort` · `swap` · `repeat` ·
`more` (`type=vertical\|horizontal`)

### `application/` — 서비스 기능

`home` · `bell` · `user` · `profile` · `heart` · `settings` · `category` · `hamburger` · `globe` · `search` ·
`reset` · `notice` · `forward` · `external-link` · `share` · `export` · `verified-check` · `bookmark` ·
`gift` · `bag` · `box` · `delivery`

### `company/` — 외부 서비스 로고

`KakaoTalk` (`mode=white\|black`) · `X` · `Google` (`mode=color`) · `Instagram` · `Facebook` · `Meta` ·
`YouTube` · `YouTubeMusic` · `AppleMusic` · `Naver` (`mode=primary`) · `NaverBlog` · `Spotify` · `TikTok`

### `사용X/` — 현재 미사용 표시

| 그룹 | 아이콘 |
|---|---|
| `place` | `location` · `pin` · `clock` (모두 `fill=true\|false`) |
| `commerce` | `coupon` · `store` · `ticket` · `package` · `money` (모두 `fill`) |
| `comms` | `faq` · `send` · `mail` · `inquiry` (`fill`) / `reply` · `headphone` |
| `account` | `login` · `logout` (`fill`) |
| `content` | `music-video` · `document` (`fill`) / `play` (`fill=true`) · `pause` |
| `nav` | `filter` · `dot` · `list` |
| `etc` | `download` · `upload` (`fill`) / `help` (`fill`) |

기타: `sample/blank` (`name=blank`) — 자리표시용.

---

## 5. 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | 24px 그리드의 획 두께 · safe area 수치 (도형만 존재, 텍스트 수치 없음) |
| 2 | `direction/chevron` 만 `size=lg\|sm` 을 갖는 이유. 다른 direction 아이콘과의 관계 |
| 3 | `suggested/help` 와 `사용X/etc/help` 처럼 **같은 이름이 사용/미사용 양쪽에** 존재 |
| 4 | `사용X/` 접두 아이콘의 처리 방침(삭제 예정인지, 보관인지) |
| 5 | 네이밍 메모(`[의미]-[형태]-[스타일]`)를 실제로 채택할지 |
| 6 | 아이콘 색은 `color.icon.*` 을 쓰는 것으로 보이나, 시안에 매핑 규칙 명시 없음 |

---

AI 제안(아이콘 export/코드 컴포넌트 전략) → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#iconography)
