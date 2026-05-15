# ChainPlay

![Feature Graphic](https://raw.githubusercontent.com/hyunseokyu1-netizen/chainplay/main/store/feature_graphic_en.png)

**Your playlist. Your order. Not the algorithm's.**

A simple Android app that lets you build your own YouTube playlist and auto-play videos in sequence — no algorithm, no clutter, no account login required.

[![Platform](https://img.shields.io/badge/platform-Android-green)](https://developer.android.com)
[![Expo](https://img.shields.io/badge/Expo-SDK%2054-blue)](https://expo.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6)](https://www.typescriptlang.org)
[![Version](https://img.shields.io/badge/version-2.0-brightgreen)](#version-history)

---

## Screenshots

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/hyunseokyu1-netizen/chainplay/main/store/screenshot_store_en_1.png" width="220" alt="Main Screen"/><br/>
      <sub>Main Screen</sub>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/hyunseokyu1-netizen/chainplay/main/store/screenshot_store_en_2.png" width="220" alt="Add URL Modal"/><br/>
      <sub>Add URL</sub>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/hyunseokyu1-netizen/chainplay/main/store/screenshot_store_ko_1.png" width="220" alt="메인 화면"/><br/>
      <sub>메인 화면 (한국어)</sub>
    </td>
  </tr>
</table>

---

## Features

- **Paste any YouTube URL** — supports `youtube.com/watch`, `youtu.be`, `Shorts`, and `embed` formats
- **Auto-play next** — when one video ends, the next one starts automatically
- **Prev / Next buttons** — overlaid on the player for quick navigation
- **Reorder freely** — move items up or down with ▲▼ buttons
- **Remove items** — tap ✕ to delete from the list
- **Persistent playlist** — list is saved locally and survives app restarts (AsyncStorage)
- **Auto language** — switches between Korean and English based on system language

---

## Supported URL Formats

```
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
https://www.youtube.com/embed/VIDEO_ID
https://www.youtube.com/shorts/VIDEO_ID
```

---

## Tech Stack

| | |
|---|---|
| Framework | Expo SDK 54 (React Native 0.81) |
| Language | TypeScript 5.9 |
| YouTube Player | react-native-youtube-iframe (IFrame API via WebView) |
| Video Metadata | YouTube oEmbed API (no API key needed) |
| Storage | @react-native-async-storage/async-storage |
| Safe Area | react-native-safe-area-context |
| i18n | Hermes built-in `Intl` API (no external library) |
| Target | Android (New Architecture enabled) |

---

## Getting Started

### Quick Test with Expo Go

```bash
npm install
npx expo start
```

Install **Expo Go** (SDK 54) on your phone and scan the QR code. Requires the same Wi-Fi network.

### Build APK & Install via ADB

```bash
# Generate native project (first time only)
npx expo prebuild --platform android

# Build APK
cd android && ANDROID_HOME=~/Library/Android/sdk ./gradlew assembleRelease

# Install on device (USB debugging required)
~/Library/Android/sdk/platform-tools/adb install -r \
  app/build/outputs/apk/release/app-release.apk
```

One-liner build + install:

```bash
cd android && \
ANDROID_HOME=~/Library/Android/sdk ./gradlew assembleRelease && \
~/Library/Android/sdk/platform-tools/adb install -r \
  app/build/outputs/apk/release/app-release.apk
```

### Check connected device

```bash
~/Library/Android/sdk/platform-tools/adb devices
```

---

## Limitations

- No background playback (YouTube policy)
- Screen must stay on for playback to continue
- Ads may appear per YouTube's policy
- Paid content and region-restricted videos are not playable

---

## Version History

| Version | Changes |
|---|---|
| v2.0 | Korean / English auto language switching |
| v1.0 | Initial release — playlist, auto-play, reorder, local save |

---

## About

This app was built for personal use. It uses YouTube's official IFrame Player API through `react-native-youtube-iframe` — no unauthorized access, no scraping.

**Privacy Policy:** https://hyunseokyu1-netizen.github.io/chain-play-privacy/

---

## Why "ChainPlay"?

This project started as **yt-player** — a purely functional name I gave it while building the first prototype. The idea was simple: chain YouTube videos together and play them in sequence, like links in a chain.

As the app grew into something worth publishing on the Play Store, I needed a proper name. "ChainPlay" stuck because:

- **Chain** — videos are linked one after another, playing in your defined order
- **Play** — straightforward, it's a player
- The name captures the core idea: *you* define the chain, not the algorithm

The original repository was named `yt-player` and has since been renamed to `chainplay` to match the app name.

---

---

## 한국어 소개

**알고리즘이 아닌, 내가 만든 순서대로.**

유튜브 URL을 붙여넣어 나만의 플레이리스트를 만들고, 영상을 순서대로 자동 재생하는 안드로이드 앱입니다.

### 주요 기능

- URL 붙여넣기만으로 영상 추가 (youtube.com, youtu.be, Shorts 모두 지원)
- 한 영상이 끝나면 다음 영상 자동 재생
- 플레이어 위 오버레이 이전/다음 버튼
- ▲▼ 버튼으로 플레이리스트 순서 변경
- 앱 재시작 후에도 플레이리스트 유지
- 시스템 언어에 따라 한국어/영어 자동 전환

### 이름 변경: yt-player → ChainPlay

처음엔 그냥 `yt-player`라고 이름 붙였습니다. 기능 중심의 임시 이름이었죠.

Play Store 출시를 준비하면서 제대로 된 앱 이름이 필요해졌고, **ChainPlay**로 결정했습니다.

- **Chain** — 내가 정한 순서대로 영상들이 이어지는 모습
- **Play** — 플레이어
- 핵심 가치를 담은 이름: *알고리즘이 아닌 내가 만든 체인*

원래 `yt-player`였던 GitHub 저장소 이름도 앱 이름에 맞춰 `chainplay`로 변경했습니다.

### 기술 스택

| 항목 | 내용 |
|---|---|
| 프레임워크 | Expo SDK 54 (React Native 0.81) |
| 언어 | TypeScript 5.9 |
| 플레이어 | react-native-youtube-iframe |
| 영상 정보 | YouTube oEmbed API |
| 저장 | AsyncStorage |
| 다국어 | Hermes 내장 Intl API |
