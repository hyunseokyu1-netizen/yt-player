# YT Player

유튜브 URL을 플레이리스트에 추가해서 순서대로 재생하는 모바일 플레이어 앱.  
YouTube Premium 없이 음악·영상 플레이리스트를 관리하고 싶은 사람을 위해 만들었습니다.

**대상 플랫폼:** Android  
**용도:** 개인 사용 목적으로 만든 앱입니다. 앱 스토어에 등록되어 있지 않으며, APK를 직접 설치해서 사용합니다.

## 주요 기능

- **URL 추가** — 유튜브 링크를 붙여넣으면 제목·썸네일 자동 조회
- **순서 재생** — 영상이 끝나면 자동으로 다음 영상 재생
- **재생 제어** — 재생/정지, 이전/다음 버튼 (플레이어 오버레이)
- **순서 변경** — ▲▼ 버튼으로 플레이리스트 순서 조정
- **삭제** — 각 항목 우측 ✕ 버튼으로 삭제
- **로컬 저장** — 앱을 껐다 켜도 플레이리스트 유지 (AsyncStorage)

## 지원 URL 형식

```
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
https://www.youtube.com/embed/VIDEO_ID
https://www.youtube.com/shorts/VIDEO_ID
```

## 기술 스택

| 항목 | 내용 |
|---|---|
| 프레임워크 | Expo SDK 54 (React Native 0.81) |
| 언어 | TypeScript 5.9 |
| 플레이어 | react-native-youtube-iframe (WebView 기반) |
| 영상 정보 | YouTube oEmbed API (API 키 불필요) |
| 저장 | @react-native-async-storage/async-storage |
| 안전 영역 | react-native-safe-area-context |

## 실행 방법

### Expo Go로 개발 (빠른 테스트)

```bash
npm install
npx expo start
```

핸드폰에 **Expo Go** 앱(SDK 54) 설치 후 QR 코드 스캔.  
같은 Wi-Fi 환경이 필요합니다.

### APK 빌드 + 기기 설치

```bash
# 네이티브 프로젝트 생성 (최초 1회)
npx expo prebuild --platform android

# APK 빌드
cd android && ANDROID_HOME=~/Library/Android/sdk ./gradlew assembleRelease

# 기기에 설치 (USB 디버깅 연결 필요)
~/Library/Android/sdk/platform-tools/adb install -r \
  app/build/outputs/apk/release/app-release.apk
```

한 번에 빌드 + 설치:

```bash
cd android && \
ANDROID_HOME=~/Library/Android/sdk ./gradlew assembleRelease && \
~/Library/Android/sdk/platform-tools/adb install -r \
  app/build/outputs/apk/release/app-release.apk
```

## 한계

- 백그라운드 재생 불가 (YouTube 정책)
- 화면이 켜진 상태에서만 재생
- 광고는 YouTube 정책에 따라 표시될 수 있음
- 유료 콘텐츠 및 지역 제한 영상 재생 불가
