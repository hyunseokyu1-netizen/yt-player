import { useState, useEffect, useCallback } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { PlaylistItem } from '../types';
import { extractVideoId, fetchVideoInfo } from '../utils/youtube';
import { t } from '../i18n';

const STORAGE_KEY = '@yt_playlist';

export function usePlaylist() {
  const [playlist, setPlaylist] = useState<PlaylistItem[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    AsyncStorage.getItem(STORAGE_KEY).then((raw) => {
      if (raw) setPlaylist(JSON.parse(raw));
    });
  }, []);

  const save = useCallback((items: PlaylistItem[]) => {
    AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  }, []);

  const addUrl = useCallback(
    async (url: string): Promise<string | null> => {
      const videoId = extractVideoId(url);
      if (!videoId) return t.invalidUrl;

      const already = playlist.some((p) => p.videoId === videoId);
      if (already) return t.alreadyExists;

      setIsLoading(true);
      const info = await fetchVideoInfo(url);
      setIsLoading(false);

      const item: PlaylistItem = {
        id: `${videoId}_${Date.now()}`,
        videoId,
        title: info?.title ?? url,
        thumbnail: info?.thumbnail ?? `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`,
        url,
      };

      setPlaylist((prev) => {
        const next = [...prev, item];
        save(next);
        return next;
      });
      return null;
    },
    [playlist, save]
  );

  const removeItem = useCallback(
    (id: string) => {
      setPlaylist((prev) => {
        const idx = prev.findIndex((p) => p.id === id);
        const next = prev.filter((p) => p.id !== id);
        save(next);
        setCurrentIndex((ci) => {
          if (next.length === 0) return 0;
          if (idx < ci) return ci - 1;
          if (idx === ci) return Math.min(ci, next.length - 1);
          return ci;
        });
        return next;
      });
    },
    [save]
  );

  const reorderItems = useCallback(
    (data: PlaylistItem[]) => {
      setPlaylist(data);
      save(data);
    },
    [save]
  );

  const moveItem = useCallback(
    (index: number, direction: 'up' | 'down') => {
      setPlaylist((prev) => {
        const next = [...prev];
        const target = direction === 'up' ? index - 1 : index + 1;
        if (target < 0 || target >= next.length) return prev;
        [next[index], next[target]] = [next[target], next[index]];
        save(next);
        return next;
      });
      setCurrentIndex((ci) => {
        const target = direction === 'up' ? index - 1 : index + 1;
        if (ci === index) return target;
        if (ci === target) return index;
        return ci;
      });
    },
    [save]
  );

  const playNext = useCallback(() => {
    setCurrentIndex((ci) => (ci + 1 < playlist.length ? ci + 1 : ci));
  }, [playlist.length]);

  const playPrev = useCallback(() => {
    setCurrentIndex((ci) => (ci - 1 >= 0 ? ci - 1 : 0));
  }, []);

  const playAt = useCallback((index: number) => {
    setCurrentIndex(index);
  }, []);

  return {
    playlist,
    currentIndex,
    currentItem: playlist[currentIndex] ?? null,
    isLoading,
    addUrl,
    removeItem,
    reorderItems,
    moveItem,
    playNext,
    playPrev,
    playAt,
  };
}
