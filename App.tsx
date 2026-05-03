import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StatusBar, StyleSheet } from 'react-native';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import { usePlaylist } from './src/hooks/usePlaylist';
import Player from './src/components/Player';
import Playlist from './src/components/Playlist';
import AddUrlModal from './src/components/AddUrlModal';

export default function App() {
  const [modalVisible, setModalVisible] = useState(false);
  const {
    playlist,
    currentIndex,
    currentItem,
    isLoading,
    addUrl,
    removeItem,
    moveItem,
    playNext,
    playPrev,
    playAt,
  } = usePlaylist();

  return (
    <SafeAreaProvider>
      <StatusBar barStyle="light-content" backgroundColor="#0f0f1a" />
      <SafeAreaView style={styles.safe} edges={['top', 'left', 'right']}>
        <View style={styles.header}>
          <Text style={styles.headerTitle}>YT Player</Text>
          <Text style={styles.headerCount}>{playlist.length}곡</Text>
        </View>

        <Player
          item={currentItem}
          onEnded={playNext}
          onPrev={playPrev}
          onNext={playNext}
          hasPrev={currentIndex > 0}
          hasNext={currentIndex < playlist.length - 1}
        />

        <View style={styles.listHeader}>
          <Text style={styles.listTitle}>플레이리스트</Text>
          <Text style={styles.listHint}>▲▼ 버튼으로 순서 변경</Text>
        </View>

        <View style={styles.listContainer}>
          <Playlist
            playlist={playlist}
            currentIndex={currentIndex}
            onMoveUp={(i) => moveItem(i, 'up')}
            onMoveDown={(i) => moveItem(i, 'down')}
            onDelete={removeItem}
            onPlay={playAt}
          />
        </View>

        <TouchableOpacity style={styles.fab} onPress={() => setModalVisible(true)}>
          <Text style={styles.fabText}>+</Text>
        </TouchableOpacity>

        <AddUrlModal
          visible={modalVisible}
          isLoading={isLoading}
          onAdd={addUrl}
          onClose={() => setModalVisible(false)}
        />
      </SafeAreaView>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: '#0f0f1a',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#1e1e2e',
  },
  headerTitle: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '800',
    letterSpacing: 0.5,
  },
  headerCount: {
    color: '#888',
    fontSize: 13,
  },
  listHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#2a2a3e',
  },
  listTitle: {
    color: '#fff',
    fontSize: 15,
    fontWeight: '700',
  },
  listHint: {
    color: '#555',
    fontSize: 12,
  },
  listContainer: {
    flex: 1,
  },
  fab: {
    position: 'absolute',
    bottom: 32,
    right: 24,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#ff0000',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#ff0000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 8,
    elevation: 8,
  },
  fabText: {
    color: '#fff',
    fontSize: 28,
    fontWeight: '300',
    lineHeight: 32,
  },
});
