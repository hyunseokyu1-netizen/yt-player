# YT Player

유튜브 URL을 플레이리스트에 추가해서 순서대로 재생하는 모바일 플레이어 앱입니다.
유튜브 프리미엄 없이 음악/영상 플레이리스트를 관리하고 싶은 사람을 위해 만들었습니다.

## 주요 기능

- **URL 추가** — 유튜브 링크를 붙여넣으면 제목·썸네일 자동 조회
- **순서 재생** — 플레이리스트를 위에서 아래로 순서대로 재생, 영상 끝나면 자동으로 다음 재생
- **재생 제어** — 재생/정지, 이전 곡, 다음 곡 버튼
- **순서 변경** — ▲▼ 버튼으로 플레이리스트 순서 조정
- **삭제** — 각 항목 우측 ✕ 버튼으로 삭제
- **로컬 저장** — 앱을 껐다 켜도 플레이리스트 유지 (AsyncStorage)

## 지원 URL 형식

```
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
https://www.youtube.com/shorts/VIDEO_ID
```

## 기술 스택

| 항목 | 내용 |
|---|---|
| 프레임워크 | Expo SDK 54 (React Native) |
| 언어 | TypeScript |
| 플레이어 | WebView + YouTube IFrame API |
| 영상 정보 | YouTube oEmbed API (API 키 불필요) |
| 저장 | @react-native-async-storage/async-storage |
| UI | react-native-safe-area-context |

## 실행 방법

```bash
# 의존성 설치
npm install

# 개발 서버 시작 (같은 Wi-Fi 필요)
npx expo start --lan

# 터널 모드 (다른 네트워크도 가능)
npx expo start --tunnel
```

핸드폰에 **Expo Go** 앱 설치 후 QR 코드 스캔

## 한계

- 백그라운드 재생 불가 (YouTube ToS 정책)
- 화면이 켜진 상태에서만 재생
- 광고는 유튜브 정책에 따라 표시될 수 있음
- 유료 콘텐츠 및 지역 제한 영상 재생 불가
