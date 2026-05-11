import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StatusBar, StyleSheet } from 'react-native';
import { SafeAreaProvider, SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context';
import { usePlaylist } from './src/hooks/usePlaylist';
import Player from './src/components/Player';
import Playlist from './src/components/Playlist';
import AddUrlModal from './src/components/AddUrlModal';

function AppContent() {
  const [modalVisible, setModalVisible] = useState(false);
  const { bottom: bottomInset } = useSafeAreaInsets();
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
    <>
      <StatusBar barStyle="light-content" backgroundColor="#0f0f1a" />
      <SafeAreaView style={styles.safe} edges={['top', 'left', 'right']}>
        <View style={styles.header}>
          <View style={styles.logoRow}>
            <View style={styles.logoIcon}>
              <View style={styles.logoTriangle} />
            </View>
            <Text style={styles.headerTitle}>ChainPlay</Text>
          </View>
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
          <Text style={styles.listTitle}>재생 목록</Text>
          <Text style={styles.listCount}>{playlist.length}개</Text>
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
          <TouchableOpacity
            style={[styles.addUrlBtn, { bottom: 16 + bottomInset }]}
            onPress={() => setModalVisible(true)}
          >
            <Text style={styles.addUrlBtnText}>+ URL 추가</Text>
          </TouchableOpacity>
        </View>

        <AddUrlModal
          visible={modalVisible}
          isLoading={isLoading}
          onAdd={addUrl}
          onClose={() => setModalVisible(false)}
          bottomInset={bottomInset}
        />
      </SafeAreaView>
    </>
  );
}

export default function App() {
  return (
    <SafeAreaProvider>
      <AppContent />
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
  logoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  logoIcon: {
    width: 36,
    height: 36,
    borderRadius: 8,
    backgroundColor: '#03030a',
    borderWidth: 1.5,
    borderColor: '#00f0ff',
    justifyContent: 'center',
    alignItems: 'center',
  },
  logoTriangle: {
    width: 0,
    height: 0,
    borderTopWidth: 7,
    borderBottomWidth: 7,
    borderLeftWidth: 12,
    borderTopColor: 'transparent',
    borderBottomColor: 'transparent',
    borderLeftColor: '#00d8f0',
    marginLeft: 2,
  },
  headerTitle: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '800',
    letterSpacing: 0.5,
  },
  addUrlBtn: {
    position: 'absolute',
    right: 16,
    backgroundColor: '#8b1a1a',
    paddingHorizontal: 18,
    paddingVertical: 10,
    borderRadius: 24,
    elevation: 6,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.4,
    shadowRadius: 6,
  },
  addUrlBtnText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '700',
  },
  listHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 7,
    borderBottomWidth: 1,
    borderBottomColor: '#2a2a3e',
  },
  listTitle: {
    color: '#fff',
    fontSize: 15,
    fontWeight: '700',
  },
  listCount: {
    color: '#888',
    fontSize: 13,
  },
  listContainer: {
    flex: 1,
  },
});
