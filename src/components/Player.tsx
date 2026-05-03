import React, { useRef, useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Dimensions } from 'react-native';
import YoutubePlayer from 'react-native-youtube-iframe';
import { PlaylistItem } from '../types';

const { width } = Dimensions.get('window');
const PLAYER_HEIGHT = width * (9 / 16);

interface Props {
  item: PlaylistItem | null;
  onEnded: () => void;
  onPrev: () => void;
  onNext: () => void;
  hasPrev: boolean;
  hasNext: boolean;
}

export default function Player({ item, onEnded, onPrev, onNext, hasPrev, hasNext }: Props) {
  const [playing, setPlaying] = useState(false);
  const playerRef = useRef(null);

  const handleStateChange = (state: string) => {
    if (state === 'ended') {
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
        initialPlayerParams={{ preventFullScreen: false, modestbranding: true }}
      />
      <View style={styles.info}>
        <Text style={styles.title} numberOfLines={2}>
          {item.title}
        </Text>
      </View>
      <View style={styles.controls}>
        <TouchableOpacity
          style={[styles.ctrlBtn, !hasPrev && styles.disabled]}
          onPress={onPrev}
          disabled={!hasPrev}
        >
          <Text style={styles.ctrlIcon}>⏮</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.playBtn} onPress={() => setPlaying((p) => !p)}>
          <Text style={styles.playIcon}>{playing ? '⏸' : '▶'}</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.ctrlBtn, !hasNext && styles.disabled]}
          onPress={onNext}
          disabled={!hasNext}
        >
          <Text style={styles.ctrlIcon}>⏭</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#0f0f1a',
  },
  placeholder: {
    backgroundColor: '#0f0f1a',
    justifyContent: 'center',
    alignItems: 'center',
  },
  placeholderText: {
    color: '#555',
    fontSize: 15,
  },
  info: {
    paddingHorizontal: 16,
    paddingTop: 12,
    paddingBottom: 4,
  },
  title: {
    color: '#fff',
    fontSize: 15,
    fontWeight: '600',
    lineHeight: 22,
  },
  controls: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 12,
    gap: 24,
  },
  ctrlBtn: {
    padding: 10,
  },
  ctrlIcon: {
    fontSize: 28,
    color: '#fff',
  },
  playBtn: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: '#ff0000',
    justifyContent: 'center',
    alignItems: 'center',
  },
  playIcon: {
    fontSize: 28,
    color: '#fff',
  },
  disabled: {
    opacity: 0.3,
  },
});
