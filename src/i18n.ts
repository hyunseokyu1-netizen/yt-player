import { NativeModules, Platform } from 'react-native';

// Android: NativeModules.I18nManager.localeIdentifier (e.g. "ko_KR")
// iOS:     NativeModules.SettingsManager.settings.AppleLocale (e.g. "ko_KR")
const rawLocale: string =
  Platform.OS === 'android'
    ? NativeModules.I18nManager?.localeIdentifier ?? ''
    : NativeModules.SettingsManager?.settings?.AppleLocale ??
      NativeModules.SettingsManager?.settings?.AppleLanguages?.[0] ??
      '';

const isKorean = rawLocale.startsWith('ko');

export const t = {
  // App.tsx
  playlistHeader: isKorean ? '재생 목록' : 'Playlist',
  itemCount: (n: number) => isKorean ? `${n}개` : `${n}`,
  addUrlBtn: isKorean ? '+ URL 추가' : '+ Add URL',

  // Player.tsx
  playerEmpty: isKorean ? '플레이리스트에 영상을 추가해주세요' : 'Add videos to get started',

  // Playlist.tsx
  listEmpty: isKorean ? '플레이리스트가 비어있습니다' : 'Your playlist is empty',
  listEmptyHint: isKorean ? '아래 + 버튼으로 유튜브 URL을 추가해보세요' : 'Tap + below to add a YouTube URL',

  // AddUrlModal.tsx
  modalTitle: isKorean ? 'YouTube URL 추가' : 'Add YouTube URL',
  inputPlaceholder: isKorean ? 'YouTube URL을 붙여넣기 하세요' : 'Paste YouTube URL here',
  addButton: isKorean ? '+ 플레이리스트에 추가' : '+ Add to Playlist',
  urlHint: isKorean
    ? 'youtube.com/watch?v=... 또는 youtu.be/... 형식 지원'
    : 'Supports youtube.com/watch?v=... or youtu.be/...',

  // 에러 메시지 (usePlaylist.ts)
  invalidUrl: isKorean ? '유효한 유튜브 URL이 아닙니다.' : 'Invalid YouTube URL.',
  alreadyExists: isKorean ? '이미 플레이리스트에 있습니다.' : 'Already in your playlist.',
};
