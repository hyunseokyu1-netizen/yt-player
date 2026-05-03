import React from 'react';
import { View, Text, Image, TouchableOpacity, StyleSheet } from 'react-native';
import { PlaylistItem as Item } from '../types';

interface Props {
  item: Item;
  index: number;
  isActive: boolean;
  isCurrent: boolean;
  onPress: () => void;
  onDelete: () => void;
  drag: () => void;
}

export default function PlaylistItemRow({
  item,
  index,
  isActive,
  isCurrent,
  onPress,
  onDelete,
  drag,
}: Props) {
  return (
    <View style={[styles.container, isActive && styles.dragging, isCurrent && styles.current]}>
      <TouchableOpacity onLongPress={drag} style={styles.dragHandle}>
        <Text style={styles.dragIcon}>☰</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.info} onPress={onPress} activeOpacity={0.7}>
        <Image source={{ uri: item.thumbnail }} style={styles.thumbnail} resizeMode="cover" />
        <View style={styles.textBlock}>
          <Text style={[styles.title, isCurrent && styles.currentTitle]} numberOfLines={2}>
            {isCurrent ? '▶ ' : `${index + 1}. `}
            {item.title}
          </Text>
        </View>
      </TouchableOpacity>
      <TouchableOpacity style={styles.deleteBtn} onPress={onDelete} hitSlop={8}>
        <Text style={styles.deleteIcon}>✕</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    paddingHorizontal: 12,
    backgroundColor: '#1e1e2e',
    borderBottomWidth: 1,
    borderBottomColor: '#2a2a3e',
  },
  dragging: {
    opacity: 0.8,
    backgroundColor: '#2a2a3e',
    shadowColor: '#000',
    shadowOpacity: 0.4,
    shadowRadius: 8,
    elevation: 8,
  },
  current: {
    borderLeftWidth: 3,
    borderLeftColor: '#ff0000',
  },
  dragHandle: {
    paddingRight: 10,
    paddingVertical: 4,
  },
  dragIcon: {
    color: '#555',
    fontSize: 18,
  },
  info: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  thumbnail: {
    width: 72,
    height: 48,
    borderRadius: 6,
    backgroundColor: '#2a2a3e',
  },
  textBlock: {
    flex: 1,
  },
  title: {
    color: '#ccc',
    fontSize: 13,
    lineHeight: 18,
  },
  currentTitle: {
    color: '#fff',
    fontWeight: '700',
  },
  deleteBtn: {
    paddingLeft: 10,
    paddingVertical: 4,
  },
  deleteIcon: {
    color: '#666',
    fontSize: 16,
  },
});
