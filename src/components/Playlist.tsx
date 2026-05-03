import React from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { PlaylistItem } from '../types';
import PlaylistItemRow from './PlaylistItem';

interface Props {
  playlist: PlaylistItem[];
  currentIndex: number;
  onMoveUp: (index: number) => void;
  onMoveDown: (index: number) => void;
  onDelete: (id: string) => void;
  onPlay: (index: number) => void;
}

export default function Playlist({
  playlist,
  currentIndex,
  onMoveUp,
  onMoveDown,
  onDelete,
  onPlay,
}: Props) {
  if (playlist.length === 0) {
    return (
      <View style={styles.empty}>
        <Text style={styles.emptyText}>플레이리스트가 비어있습니다</Text>
        <Text style={styles.emptyHint}>아래 + 버튼으로 유튜브 URL을 추가해보세요</Text>
      </View>
    );
  }

  return (
    <FlatList
      data={playlist}
      keyExtractor={(item) => item.id}
      contentContainerStyle={styles.list}
      renderItem={({ item, index }) => (
        <PlaylistItemRow
          item={item}
          index={index}
          isCurrent={index === currentIndex}
          isFirst={index === 0}
          isLast={index === playlist.length - 1}
          onPress={() => onPlay(index)}
          onDelete={() => onDelete(item.id)}
          onMoveUp={() => onMoveUp(index)}
          onMoveDown={() => onMoveDown(index)}
        />
      )}
    />
  );
}

const styles = StyleSheet.create({
  list: {
    paddingBottom: 100,
  },
  empty: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    gap: 8,
    paddingBottom: 100,
  },
  emptyText: {
    color: '#555',
    fontSize: 16,
  },
  emptyHint: {
    color: '#444',
    fontSize: 13,
  },
});
