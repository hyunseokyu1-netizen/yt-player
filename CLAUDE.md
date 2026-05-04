# YT Player — AI 컨텍스트 문서

유튜브 플레이리스트 모바일 앱. YouTube Premium 없이 유튜브 영상을 순차 재생하는 용도.  
React Native (Expo SDK 54) + TypeScript. Android 실기기 대상.

---

## 기술 스택

| 항목 | 버전 |
|---|---|
| Expo SDK | ~54.0.33 |
| React Native | ^0.81.5 |
| React | ^19.1.0 |
| TypeScript | ~5.9.2 |
| react-native-youtube-iframe | ^2.4.1 |
| @react-native-async-storage/async-storage | 2.2.0 |
| react-native-safe-area-context | ~5.6.0 |
| react-native-webview | ^13.15.0 |
| @expo/metro-runtime | ~6.1.2 |

**없는 것:** react-native-reanimated (New Architecture 충돌로 제거됨, 드래그 대신 ▲▼ 버튼으로 대체)

---

## 파일 구조

```
youtubePlayer/
├── App.tsx                          # 앱 루트. SafeAreaProvider + AppContent 분리
├── index.ts                         # registerRootComponent. 첫 줄에 @expo/metro-runtime import 필수
├── app.json                         # newArchEnabled: true, package: com.anonymous.ytplayer
├── babel.config.js                  # babel-preset-expo만. reanimated plugin 없음
├── src/
│   ├── types/index.ts               # PlaylistItem 인터페이스
│   ├── utils/youtube.ts             # extractVideoId, fetchVideoInfo (oEmbed)
│   ├── hooks/usePlaylist.ts         # 전체 플레이리스트 상태 관리
│   └── components/
│       ├── Player.tsx               # YouTube 플레이어 + 재생/이전/다음 컨트롤
│       ├── Playlist.tsx             # FlatList 래퍼
│       ├── PlaylistItem.tsx         # 플레이리스트 행 (▲▼ + 썸네일 + 제목 + ✕)
│       └── AddUrlModal.tsx          # URL 입력 바텀시트 모달
```

---

## 핵심 아키텍처 결정사항

### SafeArea 구조
`useSafeAreaInsets`는 `SafeAreaProvider` 내부에서만 호출 가능.  
`App()` → `SafeAreaProvider` → `AppContent()` 구조로 분리.  
`bottomInset`을 FAB(`bottom: 24 + bottomInset`)과 `AddUrlModal`(`paddingBottom: 24 + bottomInset`)에 내려줌.

```tsx
// App.tsx 핵심 패턴
function AppContent() {
  const { bottom: bottomInset } = useSafeAreaInsets();
  // ...
}
export default function App() {
  return <SafeAreaProvider><AppContent /></SafeAreaProvider>;
}
```

### YouTube 재생
`react-native-youtube-iframe` 사용. YouTube가 안드로이드 WebView 직접 접근을 UA로 차단하기 때문에 커스텀 WebView embed는 동작하지 않음.  
`play` prop으로 재생 상태 제어. `onChangeState`로 동기화.

```tsx
// Player.tsx 자동재생 패턴
useEffect(() => {
  if (item) setPlaying(true);
  else setPlaying(false);
}, [item?.videoId]);
```

### 아이콘 렌더링
안드로이드에서 emoji 렌더링이 깨짐 (⏸ 등). Player 재생/정지/이전/다음 버튼은 모두 View + border trick으로 그린 삼각형/사각형 사용. ▲▼ 순서 변경 버튼과 ✕ 삭제 버튼은 Text emoji 사용 (이쪽은 안드로이드에서 정상 렌더링됨).

### AsyncStorage
Storage key: `@yt_playlist`  
앱 시작 시 로드, 변경 시마다 저장.

### YouTube URL 파싱 (youtube.ts)
지원 패턴:
- `youtube.com/watch?v=ID`
- `youtu.be/ID`
- `youtube.com/embed/ID`
- `youtube.com/shorts/ID`

영상 정보는 oEmbed API로 fetch (API 키 불필요):
```
https://www.youtube.com/oembed?url=<encoded_url>&format=json
```

---

## 데이터 타입

```ts
interface PlaylistItem {
  id: string;        // `${videoId}_${Date.now()}`
  videoId: string;   // 11자 YouTube video ID
  title: string;     // oEmbed에서 가져온 제목
  thumbnail: string; // oEmbed thumbnail_url
  url: string;       // 원본 입력 URL
}
```

---

## usePlaylist 훅 API

| 반환값 | 타입 | 설명 |
|---|---|---|
| `playlist` | `PlaylistItem[]` | 전체 플레이리스트 |
| `currentIndex` | `number` | 현재 재생 인덱스 |
| `currentItem` | `PlaylistItem \| null` | 현재 아이템 |
| `isLoading` | `boolean` | oEmbed fetch 중 |
| `addUrl(url)` | `Promise<string \| null>` | null=성공, string=에러메시지 |
| `removeItem(id)` | `void` | currentIndex 자동 보정 포함 |
| `moveItem(index, 'up'\|'down')` | `void` | 배열 swap + currentIndex 추적 |
| `playNext()` | `void` | |
| `playPrev()` | `void` | |
| `playAt(index)` | `void` | |

---

## 빌드 & 설치

### Expo Go로 개발 (빠른 테스트)
```bash
npx expo start
# QR 코드 스캔 (Expo Go SDK 54 필요)
```

### APK 빌드 + ADB 설치
```bash
# 네이티브 프로젝트 생성 (최초 1회)
npx expo prebuild --platform android

# APK 빌드
cd android && ANDROID_HOME=~/Library/Android/sdk ./gradlew assembleRelease

# 기기에 설치 (USB 디버깅 연결 필요)
~/Library/Android/sdk/platform-tools/adb install -r \
  app/build/outputs/apk/release/app-release.apk
```

### 한 번에 빌드 + 설치
```bash
cd android && \
ANDROID_HOME=~/Library/Android/sdk ./gradlew assembleRelease && \
~/Library/Android/sdk/platform-tools/adb install -r \
  app/build/outputs/apk/release/app-release.apk && \
echo "설치 완료"
```

### ADB 기기 확인
```bash
~/Library/Android/sdk/platform-tools/adb devices
# 연결된 기기: R5KYA01JSXA (삼성 갤럭시)
```

---

## 알려진 이슈 & 주의사항

### react-native-reanimated 사용 금지
New Architecture(`newArchEnabled: true`) + reanimated v4 조합이 TurboModule 에러를 일으킴.  
`babel.config.js`에 reanimated plugin 추가하지 말 것. 드래그 정렬이 필요하다면 다른 방법 검토.

### index.ts 첫 줄
```ts
import '@expo/metro-runtime'; // HMR window.location 에러 방지. 반드시 첫 줄
```

### YouTube play/pause 버튼 제어
`react-native-youtube-iframe`의 `play` prop으로 제어하지만 WebView 기반이라 응답성이 완벽하지 않을 수 있음. 사용자가 YouTube 플레이어 자체를 직접 탭해도 상태가 바뀜(`onChangeState`로 동기화).

### 안드로이드 SafeAreaView
`react-native`의 기본 `SafeAreaView`는 상단만 처리함. `react-native-safe-area-context`의 것 사용 + `edges={['top', 'left', 'right']}` 명시.

---

## GitHub 저장소

```
https://github.com/hyunseokYeo/yt-player
```
