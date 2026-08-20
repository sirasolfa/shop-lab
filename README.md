# shop-lab

NOVERA shop에 대한 코드를 저장합니다.

## mobile-home

`shop.novera.town` 홈 화면 개편 **모바일 프로토타입**.

| | |
|---|---|
| 디자인 | Figma [\[NOVERA\] Shop / Handoff / Mobile](https://www.figma.com/design/Li8im2dMEZygQo0p7s4ea2/-NOVERA--Shop?node-id=4869-77378) (`4869:77378`) |
| 디자인 시스템 | Storybook `develop--693fcc16142e19f5d9fb6f9c.chromatic.com` — Foundation(Colors·Icon·Typo·Rounded·Spacing) + Components(Badge·Avatar·Tabs) |
| 데이터 | `shop.novera.town` 실제 상품 / `shop-api.novera.town` |

### 구조

```
mobile-home/
├── build.py                        # 빌더 — 에셋을 data URI 로 인라인해 단일 HTML 생성
├── data.json                       # 섹션별 상품 데이터 (API 스냅샷)
├── assets/
│   ├── nds_icons.json              # NDS 아이콘 (viewBox 0 0 24 24)
│   ├── artist/                     # 아티스트 아바타
│   ├── banner/                     # 메인·인라인·컬렉션 배너
│   ├── brand/                      # 로고 / SNS SVG
│   └── prod/                       # 상품 썸네일
└── NOVERA_shop_home_mobile.html    # 빌드 결과물 (단일 파일, 그대로 열면 동작)
```

### 빌드

```bash
cd mobile-home && python3 build.py
```

의존성은 표준 라이브러리만 사용합니다. 에셋을 갱신하려면 `assets/` 를 교체한 뒤 다시 빌드하세요.

### 화면 구성

TopNavigation → 카테고리 탭 → 메인 배너(자동 슬라이드) → Who's Your Bias? →
Meet Your Artist Event! → Fan's Pick!(TOP 3) → New Arrival → Now Trending →
인라인 배너 → NOVERA shop Collection(탭) → 무료배송 상품 → Footer → BottomNavigation
