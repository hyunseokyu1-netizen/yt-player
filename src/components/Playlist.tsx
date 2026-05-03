import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import DraggableFlatList, { RenderItemParams } from 'react-native-draggable-flatlist';
import { PlaylistItem } from '../types';
import PlaylistItemRow from './PlaylistItem';

interface Props {
  playlist: PlaylistItem[];
  currentIndex: number;
  onReorder: (data: PlaylistItem[]) => void;
  onDelete: (id: string) => void;
  onPlay: (index: number) => void;
}

export default function Playlist({ playlist, currentIndex, onReorder, onDelete, onPlay }: Props) {
  const renderItem = ({ item, getIndex, drag, isActive }: RenderItemParams<PlaylistItem>) => {
    const index = getIndex() ?? 0;
    return (
      <PlaylistItemRow
        item={item}
        index={index}
        isActive={isActive}
        isCurrent={index === currentIndex}
        onPress={() => onPlay(index)}
        onDelete={() => onDelete(item.id)}
        drag={drag}
      />
    );
  };

  if (playlist.length === 0) {
    return (
      <View style={styles.empty}>
        <Text style={styles.emptyText}>플레이리스트가 비어있습니다</Text>
        <Text style={styles.emptyHint}>아래 + 버튼으로 유튜브 URL을 추가해보세요</Text>
      </View>
    );
  }

  return (
    <DraggableFlatList
      data={playlist}
      keyExtractor={(item) => item.id}
      renderItem={renderItem}
      onDragEnd={({ data }) => onReorder(data)}
      contentContainerStyle={styles.list}
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
