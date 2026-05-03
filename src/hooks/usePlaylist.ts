import { useState, useEffect, useCallback } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { PlaylistItem } from '../types';
import { extractVideoId, fetchVideoInfo } from '../utils/youtube';

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
      if (!videoId) return '유효한 유튜브 URL이 아닙니다.';

      const already = playlist.some((p) => p.videoId === videoId);
      if (already) return '이미 플레이리스트에 있습니다.';

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
    playNext,
    playPrev,
    playAt,
  };
}
