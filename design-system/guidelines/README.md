# Guidelines

| 문서 | 성격 | 내용 |
|---|---|---|
| [naming.md](naming.md) | `[F]` Figma 사실 | Change Log의 네이밍 규칙 원문 + 실제 적용/이탈 사례 |
| [changelog.md](changelog.md) | `[F]` Figma 사실 | Change Log 전문(원문 그대로) + 시간순 정리 |
| [ai-guidelines.md](ai-guidelines.md) | **`[A]` AI 제안** | Figma에 근거가 없는 제안. **채택 전까지 규범 아님** |

## 왜 파일을 나눴는가

`naming.md` 와 `changelog.md` 는 **Figma에 적힌 문장을 옮긴 것**이라 그대로 따르면 됩니다.

`ai-guidelines.md` 는 다릅니다. Figma에는 없지만 코드로 옮기려면 결정이 필요한 자리
(토큰 export 형식, 다크 모드, 접근성 기준선, 컴포넌트 API 형태 등)를 AI가 채워 넣은 **초안**입니다.
각 항목에 다음을 함께 적어 두었습니다.

- **근거** — 무엇에 기대어 제안했는지
- **확정 조건** — 무엇을 확인하면 이 제안이 사실로 승격되는지

디자이너/개발자가 검토해 채택한 항목은 해당 파운데이션/컴포넌트 문서로 옮기고,
`ai-guidelines.md` 에서는 지우는 방식을 권합니다.
