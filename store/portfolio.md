# ChainPlay — 포트폴리오

<!--
  블로그 포트폴리오 페이지 작성용 원본 문서.
  이미지 링크는 GitHub raw URL 기준.
  repo: https://github.com/hyunseokyu1-netizen/yt-player
-->

---

## 메타 정보

| 항목 | 내용 |
|---|---|
| 프로젝트명 | ChainPlay |
| 유형 | 개인 프로젝트 (사이드 프로젝트) |
| 플랫폼 | Android |
| 기간 | 2026년 4월 ~ 2026년 5월 |
| 상태 | Play Store 출시 준비 중 |
| GitHub | https://github.com/hyunseokyu1-netizen/yt-player |
| 개인정보처리방침 | https://hyunseokyu1-netizen.github.io/chain-play-privacy/ |

---

## 대표 이미지 (Feature Graphic)

![ChainPlay Feature Graphic](https://raw.githubusercontent.com/hyunseokyu1-netizen/yt-player/main/store/feature_graphic.png)

---

## 한 줄 소개

> 알고리즘이 아닌, 내가 만든 순서대로 유튜브 영상을 자동 재생하는 플레이리스트 앱

---

## 프로젝트 소개

유튜브에는 플레이리스트 기능이 있지만, 원하는 영상만 골라 내 순서대로 이어 보기가 생각보다 불편하다. 특히 알고리즘 추천 영상이 중간에 끼거나, 재생 목록 관리가 복잡해지는 경우가 많다.

ChainPlay는 이 문제를 해결하기 위해 만든 간단한 안드로이드 앱이다. 유튜브 URL만 붙여넣으면 내 플레이리스트에 추가되고, 한 영상이 끝나면 다음 영상으로 자동으로 넘어간다. 별도 로그인 없이 YouTube 공식 플레이어를 그대로 사용한다.

---

## 주요 기능

- **URL 붙여넣기로 즉시 추가** — youtube.com/watch, youtu.be, Shorts, embed 형식 모두 지원
- **자동 연속 재생** — 한 영상 종료 시 다음 영상으로 자동 이동
- **이전 / 다음 버튼** — 영상 간 빠른 이동
- **순서 변경** — ▲▼ 버튼으로 플레이리스트 순서 자유롭게 조정
- **영상 삭제** — 목록에서 개별 제거
- **로컬 저장** — 앱 종료 후에도 플레이리스트 유지 (AsyncStorage)
- **한 / 영 자동 전환** — 시스템 언어가 한국어면 한국어, 나머지는 영어

---

## 기술 스택

| 분류 | 기술 |
|---|---|
| 프레임워크 | React Native (Expo SDK 54) |
| 언어 | TypeScript |
| YouTube 재생 | react-native-youtube-iframe |
| 로컬 저장 | @react-native-async-storage/async-storage |
| Safe Area | react-native-safe-area-context |
| 다국어 | Intl API (Hermes 내장, 외부 라이브러리 없음) |
| 빌드 타겟 | Android (New Architecture 활성화) |

---

## 스크린샷

### 메인 화면

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/hyunseokyu1-netizen/yt-player/main/store/screenshot_store_ko_1.png" width="260" alt="메인 화면 (한국어)"/><br/>
      <sub>메인 화면 — 한국어</sub>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/hyunseokyu1-netizen/yt-player/main/store/screenshot_store_en_1.png" width="260" alt="Main Screen (English)"/><br/>
      <sub>Main Screen — English</sub>
    </td>
  </tr>
</table>

### URL 추가 모달

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/hyunseokyu1-netizen/yt-player/main/store/screenshot_store_ko_2.png" width="260" alt="URL 추가 모달 (한국어)"/><br/>
      <sub>URL 추가 — 한국어</sub>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/hyunseokyu1-netizen/yt-player/main/store/screenshot_store_en_2.png" width="260" alt="Add URL Modal (English)"/><br/>
      <sub>Add URL — English</sub>
    </td>
  </tr>
</table>

---

## 앱 아이콘

![ChainPlay Icon](https://raw.githubusercontent.com/hyunseokyu1-netizen/yt-player/main/store/icon_512.png)

---

## 개발 과정에서 해결한 문제들

### 1. YouTube WebView 직접 접근 차단
YouTube가 User-Agent 기반으로 안드로이드 WebView 직접 접근을 막는다. 커스텀 WebView embed 방식은 동작하지 않아 `react-native-youtube-iframe`(공식 IFrame Player API 기반)으로 전환했다.

### 2. 안드로이드 이모지 렌더링 깨짐
재생/정지/이전/다음 버튼에 이모지(⏸ 등)를 쓰면 안드로이드에서 □로 표시된다. View + border 트릭으로 삼각형·사각형을 직접 그려서 해결했다.

### 3. 다국어 감지 삽질
- `expo-localization` → 네이티브 빌드에서 링킹 누락으로 undefined
- `NativeModules.I18nManager.localeIdentifier` → Android에서 해당 속성 없음
- **최종 해결**: Hermes 내장 `Intl.DateTimeFormat().resolvedOptions().locale` 사용

### 4. New Architecture + reanimated 충돌
`newArchEnabled: true` + reanimated v4 조합이 TurboModule 에러를 일으켜 reanimated를 완전히 제거하고, 드래그 정렬 대신 ▲▼ 버튼 방식으로 대체했다.

---

## 버전 이력

| 버전 | 주요 변경 |
|---|---|
| v1.0 | 최초 출시 — 플레이리스트 재생, URL 추가, 순서 변경, 로컬 저장 |
| v2.0 | 한/영 다국어 지원 추가 (시스템 언어 자동 감지) |
