import React, { useRef, useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Dimensions } from 'react-native';
import YoutubePlayer, { YoutubeIframeRef } from 'react-native-youtube-iframe';
import { PlaylistItem } from '../types';

const { width } = Dimensions.get('window');
const PLAYER_HEIGHT = (width * 9) / 16;

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

      <View style={styles.info}>
        <Text style={styles.title} numberOfLines={2}>{item.title}</Text>
      </View>

      <View style={styles.controls}>
        <TouchableOpacity
          style={[styles.sideBtn, !hasPrev && styles.disabled]}
          onPress={onPrev}
          disabled={!hasPrev}
        >
          <View style={styles.skipRow}>
            <View style={styles.skipBar} />
            <View style={styles.triLeft} />
          </View>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.sideBtn, !hasNext && styles.disabled]}
          onPress={onNext}
          disabled={!hasNext}
        >
          <View style={styles.skipRow}>
            <View style={styles.triRight} />
            <View style={styles.skipBar} />
          </View>
        </TouchableOpacity>
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
  info: { paddingHorizontal: 16, paddingTop: 12, paddingBottom: 4 },
  title: { color: '#fff', fontSize: 15, fontWeight: '600', lineHeight: 22 },
  controls: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 14,
    gap: 48,
  },
  sideBtn: { padding: 14 },
  disabled: { opacity: 0.25 },

  triRight: {
    width: 0, height: 0,
    borderTopWidth: 13, borderBottomWidth: 13, borderLeftWidth: 22,
    borderTopColor: 'transparent', borderBottomColor: 'transparent', borderLeftColor: '#fff',
    marginLeft: 4,
  },
  triLeft: {
    width: 0, height: 0,
    borderTopWidth: 13, borderBottomWidth: 13, borderRightWidth: 22,
    borderTopColor: 'transparent', borderBottomColor: 'transparent', borderRightColor: '#fff',
  },
  skipRow: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  skipBar: { width: 4, height: 22, backgroundColor: '#fff', borderRadius: 2 },
});
