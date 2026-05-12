---
title: 'React Native + Expo로 유튜브 플레이리스트 앱 만들기 (삽질 7종 세트 포함)'
date: '2026-05-03'
description: Expo Go + react-native-youtube-iframe 조합으로 유튜브 플레이리스트 앱을 만들면서 겪은 환경 설정부터 WebView 차단까지 실전 트러블슈팅 기록
tags:
  - React Native
  - Expo
  - YouTube
  - TypeScript
  - AsyncStorage
---

## 왜 만들었냐면

유튜브 프리미엄 없이 백그라운드 재생을 하고 싶어서 이것저것 써봤는데, 결국 직접 만드는 게 낫겠다 싶었다. 어차피 React Native도 한번 제대로 써보고 싶었고.

목표는 단순했다.

- 유튜브 URL을 붙여넣으면 자동으로 제목이랑 썸네일을 가져오고
- 플레이리스트로 쌓아두고
- 끝나면 다음 곡이 자동으로 재생되는 것

결과물은 여기서 볼 수 있다: [https://github.com/hyunseokyu1-netizen/yt-player](https://github.com/hyunseokyu1-netizen/yt-player)

실제로 완성까지 가는 데 코드보다 환경 설정 싸움에 시간을 더 많이 썼다. 이 글은 그 삽질의 기록이다.

---

## 기술 스택

| 역할 | 라이브러리 |
|------|------------|
| 프레임워크 | Expo SDK 54, React Native 0.81 |
| 언어 | TypeScript |
| YouTube 재생 | react-native-youtube-iframe ^2.4.1 |
| 로컬 저장 | @react-native-async-storage/async-storage |
| 안전 영역 | react-native-safe-area-context |
| 웹뷰 | react-native-webview |

---

## 기본 구조 먼저

앱 구조는 크게 세 파트다.

```
App.tsx
├── Player         # 유튜브 플레이어 + 재생 컨트롤
├── Playlist       # 플레이리스트 목록 (FlatList)
└── AddUrlModal    # URL 입력 모달
```

상태 관리는 `usePlaylist` 훅 하나에 몰아넣었다. 플레이리스트 배열과 현재 인덱스를 같이 관리하고, AsyncStorage와의 동기화도 여기서 처리한다.

```typescript
// src/hooks/usePlaylist.ts
export function usePlaylist() {
  const [playlist, setPlaylist] = useState<PlaylistItem[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  // 앱 시작 시 저장된 플레이리스트 불러오기
  useEffect(() => {
    AsyncStorage.getItem(STORAGE_KEY).then((raw) => {
      if (raw) setPlaylist(JSON.parse(raw));
    });
  }, []);

  // 변경할 때마다 바로 저장
  const save = useCallback((items: PlaylistItem[]) => {
    AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  }, []);

  // ...
}
```

---

## 핵심 기능 구현

### 1. URL에서 제목·썸네일 자동 조회

유튜브 oEmbed API를 쓰면 API 키 없이도 제목과 썸네일을 가져올 수 있다.

```typescript
// src/utils/youtube.ts
export async function fetchVideoInfo(url: string) {
  const oembedUrl = `https://www.youtube.com/oembed?url=${encodeURIComponent(url)}&format=json`;
  const res = await fetch(oembedUrl);
  if (!res.ok) return null;
  const data = await res.json();
  return {
    title: data.title ?? 'Unknown Title',
    thumbnail: data.thumbnail_url ?? '',
  };
}
```

URL 파싱은 정규식으로 처리한다. `watch?v=`, `youtu.be/`, Shorts URL까지 커버한다.

```typescript
export function extractVideoId(url: string): string | null {
  const patterns = [
    /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})/,
    /youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})/,
  ];
  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) return match[1];
  }
  return null;
}
```

### 2. YouTube 재생

`react-native-youtube-iframe`을 쓴다. 이유는 트러블슈팅 섹션에서 자세히 설명하는데, 간단히 말하면 커스텀 WebView로는 재생이 안 된다.

```typescript
// src/components/Player.tsx
import YoutubePlayer from 'react-native-youtube-iframe';

<YoutubePlayer
  height={PLAYER_HEIGHT}
  videoId={item.videoId}
  play={playing}
  onChangeState={handleStateChange}
  webViewProps={{
    allowsInlineMediaPlayback: true,
    mediaPlaybackRequiresUserAction: false,
  }}
/>
```

영상이 끝나면 `onChangeState`에서 `'ended'` 상태를 잡아서 다음 곡으로 넘긴다.

```typescript
const handleStateChange = (state: string) => {
  if (state === 'ended') {
    setPlaying(false);
    onEnded(); // playNext() 호출
  }
};
```

곡이 바뀔 때 자동 재생은 `useEffect`로 처리한다.

```typescript
useEffect(() => {
  if (item) setPlaying(true);
}, [item?.videoId]);
```

### 3. 순서 변경 (▲▼)

드래그 정렬은 포기했다 (이유는 트러블슈팅 참고). 대신 ▲▼ 버튼으로 한 칸씩 이동한다.

```typescript
const moveItem = useCallback((index: number, direction: 'up' | 'down') => {
  setPlaylist((prev) => {
    const next = [...prev];
    const target = direction === 'up' ? index - 1 : index + 1;
    if (target < 0 || target >= next.length) return prev;
    [next[index], next[target]] = [next[target], next[index]]; // swap
    save(next);
    return next;
  });
  // 현재 재생 중인 인덱스도 같이 업데이트
  setCurrentIndex((ci) => {
    const target = direction === 'up' ? index - 1 : index + 1;
    if (ci === index) return target;
    if (ci === target) return index;
    return ci;
  });
}, [save]);
```

---

## 삽질 7종 세트

이 프로젝트에서 진짜 시간 잡아먹은 것들이다. 같은 삽질 반복하지 않길 바라면서 정리한다.

### 삽질 1: Expo SDK 버전 불일치

Expo Go 앱은 특정 SDK 버전에 묶여 있다. 핸드폰에 설치된 Expo Go가 SDK 54인데 프로젝트를 SDK 52로 내리면 이런 에러가 뜬다:

```
Project is incompatible with this version of Expo Go.
```

반대로 프로젝트가 SDK 54인데 Expo Go가 52면 또 안 된다.

**해결**: 핸드폰 Expo Go 버전을 먼저 확인하고, 프로젝트를 그에 맞춰 생성한다.

```bash
# SDK 54로 프로젝트 생성
npx create-expo-app@latest yt-player
# 기본 템플릿이 최신 SDK로 생성됨
```

### 삽질 2: react-native-reanimated v4 + Expo Go 충돌

드래그 정렬을 위해 `react-native-draggable-flatlist`를 설치했는데, 이게 내부적으로 `react-native-reanimated` v4를 쓴다. Expo Go에서 실행하면 이런 에러가 터진다:

```
installTurboModule called with 1 arguments, expected 0
```

Expo Go의 TurboModule 구현과 reanimated v4가 기대하는 인터페이스가 다른 것이 원인이다. 개발 빌드(EAS Build)를 쓰면 해결되지만, 그냥 Expo Go로 테스트하고 싶다면 reanimated v4가 필요한 라이브러리는 포기해야 한다.

**해결**: `react-native-draggable-flatlist` 제거, ▲▼ 버튼으로 대체.

### 삽질 3: HMR window.location 에러

프로젝트를 처음 실행하면 이런 에러가 뜰 수 있다:

```
TypeError: Cannot read properties of undefined (reading 'protocol')
```

Hot Module Replacement(HMR)가 `window.location`을 찾는데 React Native 환경에는 없어서 터지는 거다.

**해결**: `index.ts` 최상단에 `@expo/metro-runtime`을 명시적으로 import한다.

```typescript
// index.ts - 반드시 첫 번째 줄
import '@expo/metro-runtime';
import { registerRootComponent } from 'expo';
import App from './App';

registerRootComponent(App);
```

순서가 중요하다. `@expo/metro-runtime`이 가장 먼저 import되어야 한다.

### 삽질 4: create-expo-app 덮어쓰기 실패

기존 디렉토리에 `create-expo-app`을 실행하면 실패한다. 특히 `.claude` 같은 숨김 디렉토리가 있으면 더 꼬인다. `babel-preset-expo`가 없다는 에러가 나오기도 한다.

**해결**: 임시 위치에 새 프로젝트를 만들고 필요한 파일만 복사한다.

```bash
# 임시 폴더에 생성
npx create-expo-app@latest /tmp/yt-player-fresh

# 핵심 설정 파일만 복사
cp /tmp/yt-player-fresh/package.json ./
cp /tmp/yt-player-fresh/babel.config.js ./
cp /tmp/yt-player-fresh/tsconfig.json ./
cp /tmp/yt-player-fresh/app.json ./

npm install
```

### 삽질 5: YouTube가 Android WebView를 차단한다

이게 제일 황당했다. `react-native-webview`로 유튜브 URL을 직접 열면 "이 영상은 이 앱에서 재생할 수 없습니다"가 뜬다.

YouTube가 Android WebView의 User-Agent를 감지해서 재생을 막는 거다. 보안 정책이라고는 하는데 개발할 때는 정말 당황스럽다.

**해결**: `react-native-youtube-iframe`을 사용한다. 이 라이브러리는 YouTube IFrame Player API를 사용해서 이 제한을 우회한다. 직접 WebView에 URL을 넣는 방식은 동작하지 않는다.

```bash
npx expo install react-native-youtube-iframe
```

### 삽질 6: 이모지 버튼이 안드로이드에서 깨진다

재생 버튼으로 ▶ 이모지, 일시정지로 ⏸ 이모지를 썼는데 안드로이드에서 깨져서 나온다. 폰마다 다르게 보이기도 한다.

**해결**: View 컴포넌트로 도형을 직접 그린다. CSS border 트릭으로 삼각형을 만들 수 있다.

```typescript
// 재생 버튼 (삼각형)
<View style={styles.triRight} />

// 일시정지 버튼 (막대 두 개)
<View style={styles.pauseWrap}>
  <View style={styles.pauseBar} />
  <View style={styles.pauseBar} />
</View>

// 스타일
const styles = StyleSheet.create({
  triRight: {
    width: 0, height: 0,
    borderTopWidth: 11, borderBottomWidth: 11, borderLeftWidth: 18,
    borderTopColor: 'transparent', borderBottomColor: 'transparent',
    borderLeftColor: '#fff',
    marginLeft: 4,
  },
  pauseWrap: { flexDirection: 'row', gap: 6 },
  pauseBar: { width: 5, height: 22, backgroundColor: '#fff', borderRadius: 2 },
});
```

이렇게 하면 모든 기기에서 동일하게 보인다.

### 삽질 7: SafeAreaView가 상태바를 무시한다

`react-native`에서 기본 제공하는 `SafeAreaView`를 썼더니 안드로이드에서 상태바와 컨텐츠가 겹쳤다. iOS는 괜찮은데 안드로이드에서만 문제가 생겼다.

**해결**: `react-native-safe-area-context`의 `SafeAreaProvider` + `SafeAreaView`를 쓰고, `edges` prop으로 방향을 명시한다.

```typescript
// App.tsx
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';

export default function App() {
  return (
    <SafeAreaProvider>
      <StatusBar barStyle="light-content" backgroundColor="#0f0f1a" />
      <SafeAreaView style={styles.safe} edges={['top', 'left', 'right']}>
        {/* 컨텐츠 */}
      </SafeAreaView>
    </SafeAreaProvider>
  );
}
```

`edges={['top', 'left', 'right']}`로 하단은 제외했다. FAB 버튼이 바닥에 떠있는 구조라 하단 safe area까지 적용하면 어색해 보였다.

---

## 핵심 흐름 정리

```
URL 입력
  ↓
extractVideoId() → 비디오 ID 파싱
  ↓
fetchVideoInfo() → oEmbed API로 제목·썸네일 조회
  ↓
AsyncStorage 저장 → 앱 재시작해도 유지
  ↓
YoutubePlayer에 videoId 전달 → 재생
  ↓
onChangeState('ended') → playNext() 자동 호출
```

---

## 마무리

코드 자체는 별로 어렵지 않았다. 오히려 Expo SDK 버전 맞추고, reanimated 충돌 피하고, YouTube 재생 라이브러리 찾는 게 훨씬 오래 걸렸다.

React Native + Expo 생태계가 빠르게 변하다 보니 구글에서 찾은 해결법이 이미 구버전 기준인 경우가 많았다. 특히 Expo SDK 버전, Expo Go 버전, 각 라이브러리 버전의 삼각 관계가 생각보다 복잡하다.

Expo Go로 빠르게 테스트하고 싶다면 reanimated v4 의존성이 있는 라이브러리는 처음부터 피하는 게 낫다. 드래그 정렬이 아쉽긴 한데 ▲▼ 버튼도 실사용엔 충분하다.
