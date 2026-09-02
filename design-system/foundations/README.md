# Foundations `[F]`

Figma **Foundation** 페이지(`0:1`)에서 읽은 토큰입니다. 이 디렉터리의 값은 전부 Figma 사실이며,
값이 확정되지 않은 항목은 각 문서의 "확인 필요" 절에 `[?]`로 모아 두었습니다.

| 문서 | 다루는 것 | Figma 프레임 |
|---|---|---|
| [color.md](color.md) | primitive 팔레트, semantic 토큰 | Primitve Color Palette `1:160` · Semantic Color Token `144:419` |
| [typography.md](typography.md) | 폰트/웨이트 변수, 텍스트 스타일 | Typography `139:1666` · Typography(Usage) `163:998` |
| [layout.md](layout.md) | `layout.gap`, `layout.spacing`, 브레이크포인트 | Layout `170:1666` · Grid `380:1802` |
| [shape.md](shape.md) | `shape.rounded`, `shape.border-width` | Shape `170:1660` |
| [elevation.md](elevation.md) | `Elevation.shadow` | Elevation `749:4126` |
| [iconography.md](iconography.md) | 아이콘 그리드·사이즈·네이밍·목록 | Icon Grid `2442:11467` · Iconography `1209:12283` |
| [brand.md](brand.md) | 로고, 파비콘, OG 이미지 | Logo `1621:20549` · Favicon & OG `2079:2181` |

## Foundation 페이지에 있는 프레임 전체

x좌표 순(왼쪽 → 오른쪽)입니다. 아래 목록이 Foundation 페이지의 전부입니다.

| 프레임 | 노드 | 크기 |
|---|---|---|
| System Conponent (섹션, 문서용 부품) | `260:1443` | 482×841 |
| Logo | `1621:20549` | 1600×6425 |
| Favicon & OG Image | `2079:2181` | 1600×3553 |
| Primitve Color Palette | `1:160` | 1714×3007 |
| Semantic Color Token | `144:419` | 1440×3145 |
| Typography (업데이트 필요) | `139:1666` | 1600×4480 |
| Typography(Usage) | `163:998` | 1600×7380 |
| Grid | `380:1802` | 1600×3710 |
| Layout | `170:1666` | 1100×2943 |
| Shape | `170:1660` | 1400×2229 |
| Elevation | `749:4126` | 1600×1148 |
| Icon Grid | `2442:11467` | 1600×1124 |
| Iconography | `1209:12283` | 1600×3595 |
| (아이콘 네이밍 메모) | `610:4742` | 455×500 |

> 프레임 이름의 오타(`Primitve`, `Conponent`)와 `Typography (업데이트 필요)` 표기는 **Figma 원문 그대로**입니다.

## 두 개의 Typography 프레임

- `139:1666` **Typography (업데이트 필요)** — 스펙(사이즈/웨이트/행간) 나열. 이름에 "업데이트 필요"가 붙어 있음.
- `163:998` **Typography(Usage)** — 실제 화면 예시로 각 레벨의 쓰임을 보여주는 프레임.

두 프레임이 참조하는 텍스트 스타일 값은 동일했습니다. 상세는 [typography.md](typography.md).

---

AI 제안 → [../guidelines/ai-guidelines.md](../guidelines/ai-guidelines.md)
