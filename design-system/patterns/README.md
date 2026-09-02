# Patterns `[F]`

NDS는 "패턴"이라는 이름의 별도 페이지를 두지 않습니다. 대신 컴포넌트 프레임 안에
**`<이름>(Usage)`** 프레임을 만들어 **여러 컴포넌트를 조합한 실제 화면**을 보여줍니다.
이 디렉터리는 그 `(Usage)` 프레임들을 패턴으로 정리한 것입니다.

## 파일 안의 `(Usage)` 프레임 전체

| Usage 프레임 | 위치 | 크기 | 다루는 것 |
|---|---|---|---|
| `Typography(Usage)` | Foundation `163:998` | 1600×7380 | 각 텍스트 레벨의 실제 문구 예시 |
| `Card(Usage)` | Content Display, Card `2582:8855` | 7712×9511 | 상품 상세/목록 화면 구성 |
| ├ `Event Card(Usage)` | Card(Usage) 하위 | | 이벤트 카드 배치 |
| └ `Cart Item(Usage)` | Card(Usage) 하위 | | 장바구니 아이템 |
| `Thumbnail(Usage)` | Content Display, Thumbnail `2980:8714` | 1440×2020 | 비율·컬러·딤 조합 |
| `Label(Usage)` | Content Display, Label `1621:17816` | 1440×1213 | 라벨 배치 |
| `Drawer(Usage)` | Overlay, Drawer `1065:18140` | | 사이드 드로어 화면 |
| `Toast(Usage)` | Overlay, Toast `1368:9769` | | 바텀 내비 위 토스트 배치 |
| `Action Area(Usage)` | Overlay, Bottom Sheet `1065:18681` | | 바텀시트 액션 영역 |
| `Search(Usage)` | Overlay 페이지 `1170:5163` | 1440×9388 | 검색 화면 흐름 |

## Usage 프레임의 공통 구성 `[F]`

```
<이름>(Usage)
├ Guide / Subtitle / Section Title    ← 설명 블록
├ Design Only/Viewport                ← desktop / mobile 표시 칩
├ Design Only/Value                   ← 해당 예시의 프로퍼티 값 표시
└ Preview                             ← 실제 조합 화면
```

`Design Only/*` 는 Foundation 페이지의 `System Conponent` 섹션(`260:1443`)에 정의된 **문서 전용 부품**이며,
제품 UI가 아닙니다. 코드로 옮기지 않습니다.

## 문서

- [commerce.md](commerce.md) — 상품 카드 · 상품 상세 · 장바구니 · 이벤트 카드 · 검색

---

## 확인 필요 `[?]`

| # | 항목 |
|---|---|
| 1 | `Search(Usage)` (1440×9388) 의 내부 흐름은 이번 조사에서 구조만 확인. 단계별 화면 미조사 |
| 2 | 패턴 레벨의 문서(빈 상태·에러·로딩 처리 규칙)는 시안에 없음 |
| 3 | `Typography(Usage)` 의 각 레벨별 "언제 쓰는가" 설명은 예시 문구로만 제시되고 규칙 문장은 없음 |

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md#patterns)
