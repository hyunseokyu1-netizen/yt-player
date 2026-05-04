import React, { useRef, useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Dimensions } from 'react-native';
import YoutubePlayer, { YoutubeIframeRef } from 'react-native-youtube-iframe';
import { PlaylistItem } from '../types';

const { width } = Dimensions.get('window');
const PLAYER_HEIGHT = Math.round(width * 9 / 16);

interface Props {
  item: PlaylistItem | null;
  onEnded: () => void;
  onPrev: () => void;
  onNext: () => void;
  hasPrev: boolean;
  hasNext: boolean;
}

export default function Player({ item, onEnded, onPrev, onNext, hasPrev, hasNext }: Props) {
  const playerRef = useRef<YoutubeIframeRef>(null);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    if (item) setPlaying(true);
    else setPlaying(false);
  }, [item?.videoId]);

  const handleStateChange = (state: string) => {
    if (state === 'ended') {
      if (!hasNext) setPlaying(false);
      onEnded();
    } else if (state === 'playing') {
      setPlaying(true);
    } else if (state === 'paused') {
      setPlaying(false);
    }
  };

  if (!item) {
    return (
      <View style={[styles.placeholder, { height: PLAYER_HEIGHT }]}>
        <Text style={styles.placeholderText}>플레이리스트에 영상을 추가해주세요</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* 플레이어 + 이전/다음 버튼 오버레이 */}
      <View style={{ height: PLAYER_HEIGHT }}>
        <YoutubePlayer
          ref={playerRef}
          height={PLAYER_HEIGHT}
          videoId={item.videoId}
          play={playing}
          onChangeState={handleStateChange}
          forceAndroidAutoplay
          initialPlayerParams={{
            preventFullScreen: false,
            modestbranding: true,
            rel: false,
          }}
          webViewProps={{
            allowsInlineMediaPlayback: true,
            mediaPlaybackRequiresUserAction: false,
          }}
        />

        {/* 이전 버튼 — 플레이어 좌측 하단 */}
        <TouchableOpacity
          style={[styles.overlayBtn, styles.overlayLeft, !hasPrev && styles.disabled]}
          onPress={onPrev}
          disabled={!hasPrev}
        >
          <View style={styles.btnBg}>
            <View style={styles.skipRow}>
              <View style={styles.skipBar} />
              <View style={styles.triLeft} />
            </View>
          </View>
        </TouchableOpacity>

        {/* 다음 버튼 — 플레이어 우측 하단 */}
        <TouchableOpacity
          style={[styles.overlayBtn, styles.overlayRight, !hasNext && styles.disabled]}
          onPress={onNext}
          disabled={!hasNext}
        >
          <View style={styles.btnBg}>
            <View style={styles.skipRow}>
              <View style={styles.triRight} />
              <View style={styles.skipBar} />
            </View>
          </View>
        </TouchableOpacity>
      </View>

      <View style={styles.info}>
        <Text style={styles.title} numberOfLines={1}>{item.title}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { backgroundColor: '#0f0f1a' },
  placeholder: {
    backgroundColor: '#0f0f1a',
    justifyContent: 'center',
    alignItems: 'center',
  },
  placeholderText: { color: '#555', fontSize: 15 },

  overlayBtn: {
    position: 'absolute',
    bottom: 10,
  },
  overlayLeft: { left: 10 },
  overlayRight: { right: 10 },
  disabled: { opacity: 0.3 },

  btnBg: {
    backgroundColor: 'rgba(0,0,0,0.45)',
    borderRadius: 24,
    padding: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },

  triRight: {
    width: 0, height: 0,
    borderTopWidth: 11, borderBottomWidth: 11, borderLeftWidth: 18,
    borderTopColor: 'transparent', borderBottomColor: 'transparent', borderLeftColor: '#fff',
    marginLeft: 3,
  },
  triLeft: {
    width: 0, height: 0,
    borderTopWidth: 11, borderBottomWidth: 11, borderRightWidth: 18,
    borderTopColor: 'transparent', borderBottomColor: 'transparent', borderRightColor: '#fff',
  },
  skipRow: { flexDirection: 'row', alignItems: 'center', gap: 3 },
  skipBar: { width: 4, height: 18, backgroundColor: '#fff', borderRadius: 2 },

  info: { paddingHorizontal: 16, paddingTop: 8, paddingBottom: 6 },
  title: { color: '#fff', fontSize: 14, fontWeight: '600', lineHeight: 20 },
});
