import React, { useRef, useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Dimensions } from 'react-native';
import { WebView } from 'react-native-webview';
import { PlaylistItem } from '../types';

const { width } = Dimensions.get('window');
const PLAYER_HEIGHT = (width * 9) / 16;

// YT IFrame API state codes
const YT_ENDED = 0;
const YT_PLAYING = 1;
const YT_PAUSED = 2;

function buildHTML(videoId: string) {
  return `
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
  <style>
    *{margin:0;padding:0;box-sizing:border-box}
    html,body{width:100%;height:100%;background:#000;overflow:hidden}
    #p{width:100%;height:100%}
  </style>
</head>
<body>
  <div id="p"></div>
  <script>
    var player;
    var tag=document.createElement('script');
    tag.src='https://www.youtube.com/iframe_api';
    document.head.appendChild(tag);
    function onYouTubeIframeAPIReady(){
      player=new YT.Player('p',{
        videoId:'${videoId}',
        playerVars:{autoplay:1,controls:1,playsinline:1,rel:0,modestbranding:1},
        events:{
          onReady:function(e){e.target.playVideo();},
          onStateChange:function(e){
            window.ReactNativeWebView.postMessage(JSON.stringify({state:e.data}));
          }
        }
      });
    }
    function rn_play(){player&&player.playVideo();}
    function rn_pause(){player&&player.pauseVideo();}
  </script>
</body>
</html>`;
}

interface Props {
  item: PlaylistItem | null;
  onEnded: () => void;
  onPrev: () => void;
  onNext: () => void;
  hasPrev: boolean;
  hasNext: boolean;
}

export default function Player({ item, onEnded, onPrev, onNext, hasPrev, hasNext }: Props) {
  const webRef = useRef<WebView>(null);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    setPlaying(false);
  }, [item?.videoId]);

  const handleMessage = (event: { nativeEvent: { data: string } }) => {
    try {
      const { state } = JSON.parse(event.nativeEvent.data);
      if (state === YT_PLAYING) setPlaying(true);
      else if (state === YT_PAUSED) setPlaying(false);
      else if (state === YT_ENDED) { setPlaying(false); onEnded(); }
    } catch {}
  };

  const togglePlay = () => {
    if (playing) {
      webRef.current?.injectJavaScript('rn_pause(); true;');
      setPlaying(false);
    } else {
      webRef.current?.injectJavaScript('rn_play(); true;');
      setPlaying(true);
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
      <WebView
        ref={webRef}
        style={{ width, height: PLAYER_HEIGHT }}
        source={{ html: buildHTML(item.videoId) }}
        onMessage={handleMessage}
        allowsInlineMediaPlayback
        mediaPlaybackRequiresUserAction={false}
        javaScriptEnabled
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
          <View style={styles.skipPrevIcon}>
            <View style={styles.skipBar} />
            <View style={styles.skipTriangleLeft} />
          </View>
        </TouchableOpacity>

        <TouchableOpacity style={styles.playBtn} onPress={togglePlay} activeOpacity={0.8}>
          {playing ? (
            <View style={styles.pauseIcon}>
              <View style={styles.pauseBar} />
              <View style={styles.pauseBar} />
            </View>
          ) : (
            <View style={styles.playIcon} />
          )}
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.sideBtn, !hasNext && styles.disabled]}
          onPress={onNext}
          disabled={!hasNext}
        >
          <View style={styles.skipNextIcon}>
            <View style={styles.skipTriangleRight} />
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
    gap: 32,
  },
  sideBtn: { padding: 10 },
  disabled: { opacity: 0.25 },

  // 재생 버튼 (삼각형)
  playBtn: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: '#ff0000',
    justifyContent: 'center',
    alignItems: 'center',
  },
  playIcon: {
    width: 0,
    height: 0,
    borderTopWidth: 11,
    borderBottomWidth: 11,
    borderLeftWidth: 18,
    borderTopColor: 'transparent',
    borderBottomColor: 'transparent',
    borderLeftColor: '#fff',
    marginLeft: 4,
  },

  // 정지 버튼 (두 막대)
  pauseIcon: { flexDirection: 'row', gap: 6 },
  pauseBar: { width: 5, height: 22, backgroundColor: '#fff', borderRadius: 2 },

  // 이전/다음 skip 아이콘
  skipPrevIcon: { flexDirection: 'row', alignItems: 'center', gap: 2 },
  skipNextIcon: { flexDirection: 'row', alignItems: 'center', gap: 2 },
  skipBar: { width: 4, height: 20, backgroundColor: '#fff', borderRadius: 2 },
  skipTriangleLeft: {
    width: 0,
    height: 0,
    borderTopWidth: 10,
    borderBottomWidth: 10,
    borderRightWidth: 16,
    borderTopColor: 'transparent',
    borderBottomColor: 'transparent',
    borderRightColor: '#fff',
  },
  skipTriangleRight: {
    width: 0,
    height: 0,
    borderTopWidth: 10,
    borderBottomWidth: 10,
    borderLeftWidth: 16,
    borderTopColor: 'transparent',
    borderBottomColor: 'transparent',
    borderLeftColor: '#fff',
  },
});
