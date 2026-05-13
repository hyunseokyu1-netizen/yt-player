import React, { useState, useEffect } from 'react';
import {
  Modal,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  StyleSheet,
  Keyboard,
} from 'react-native';
import { t } from '../i18n';

interface Props {
  visible: boolean;
  isLoading: boolean;
  onAdd: (url: string) => Promise<string | null>;
  onClose: () => void;
  bottomInset?: number;
}

export default function AddUrlModal({ visible, isLoading, onAdd, onClose, bottomInset = 0 }: Props) {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const [focused, setFocused] = useState(false);
  const [keyboardHeight, setKeyboardHeight] = useState(0);

  useEffect(() => {
    if (!visible) {
      setKeyboardHeight(0);
      return;
    }
    const show = Keyboard.addListener('keyboardDidShow', (e) => {
      setKeyboardHeight(e.endCoordinates.height);
    });
    const hide = Keyboard.addListener('keyboardDidHide', () => {
      setKeyboardHeight(0);
    });
    return () => {
      show.remove();
      hide.remove();
    };
  }, [visible]);

  const handleAdd = async () => {
    const trimmed = url.trim();
    if (!trimmed) return;
    setError('');
    const err = await onAdd(trimmed);
    if (err) {
      setError(err);
    } else {
      setUrl('');
      onClose();
    }
  };

  const handleClose = () => {
    setUrl('');
    setError('');
    Keyboard.dismiss();
    onClose();
  };

  // 키보드가 올라오면 overlay 하단에 패딩을 줘서 시트를 밀어올림
  const overlayPaddingBottom = keyboardHeight > 0 ? keyboardHeight : 0;
  const sheetPaddingBottom = keyboardHeight > 0 ? 16 : 20 + bottomInset;

  return (
    <Modal visible={visible} transparent animationType="slide" onRequestClose={handleClose}>
      <View style={[styles.overlay, { paddingBottom: overlayPaddingBottom }]}>
        <View style={[styles.sheet, { paddingBottom: sheetPaddingBottom }]}>
          <View style={styles.dragBar} />

          <View style={styles.titleRow}>
            <Text style={styles.title}>{t.modalTitle}</Text>
            <TouchableOpacity onPress={handleClose} hitSlop={12} disabled={isLoading}>
              <Text style={styles.closeIcon}>✕</Text>
            </TouchableOpacity>
          </View>

          <View style={[styles.inputWrap, focused && styles.inputFocused]}>
            <View style={styles.linkIconWrap}>
              <View style={styles.linkRing1} />
              <View style={styles.linkRing2} />
            </View>
            <TextInput
              style={styles.input}
              placeholder={t.inputPlaceholder}
              placeholderTextColor="#666"
              value={url}
              onChangeText={setUrl}
              autoCapitalize="none"
              autoCorrect={false}
              editable={!isLoading}
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
            />
          </View>

          {error ? <Text style={styles.error}>{error}</Text> : null}

          <TouchableOpacity
            style={[styles.addBtn, (!url.trim() || isLoading) && styles.addBtnDisabled]}
            onPress={handleAdd}
            disabled={isLoading || !url.trim()}
            activeOpacity={0.8}
          >
            {isLoading ? (
              <ActivityIndicator color="#fff" size="small" />
            ) : (
              <Text style={styles.addBtnText}>{t.addButton}</Text>
            )}
          </TouchableOpacity>

          <Text style={styles.hint}>{t.urlHint}</Text>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.65)',
    justifyContent: 'flex-end',
  },
  sheet: {
    backgroundColor: '#1a1a1a',
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    paddingHorizontal: 20,
    paddingTop: 12,
    gap: 14,
  },
  dragBar: {
    width: 40,
    height: 4,
    backgroundColor: '#444',
    borderRadius: 2,
    alignSelf: 'center',
    marginBottom: 4,
  },
  titleRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  title: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '700',
  },
  closeIcon: {
    color: '#888',
    fontSize: 18,
  },
  inputWrap: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#2a2a2a',
    borderRadius: 10,
    borderWidth: 1.5,
    borderColor: 'transparent',
    paddingHorizontal: 12,
    gap: 10,
  },
  inputFocused: {
    borderColor: '#3a7bd5',
  },
  linkIconWrap: {
    width: 18,
    height: 18,
    justifyContent: 'center',
    alignItems: 'center',
  },
  linkRing1: {
    position: 'absolute',
    width: 10,
    height: 6,
    borderRadius: 3,
    borderWidth: 2,
    borderColor: '#888',
    top: 2,
    left: 0,
    transform: [{ rotate: '-45deg' }],
  },
  linkRing2: {
    position: 'absolute',
    width: 10,
    height: 6,
    borderRadius: 3,
    borderWidth: 2,
    borderColor: '#888',
    bottom: 2,
    right: 0,
    transform: [{ rotate: '-45deg' }],
  },
  input: {
    flex: 1,
    color: '#fff',
    fontSize: 14,
    paddingVertical: 14,
  },
  error: {
    color: '#ff6b6b',
    fontSize: 13,
    marginTop: -6,
  },
  addBtn: {
    backgroundColor: '#8b1a1a',
    borderRadius: 10,
    paddingVertical: 16,
    alignItems: 'center',
  },
  addBtnDisabled: {
    opacity: 0.5,
  },
  addBtnText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '700',
  },
  hint: {
    color: '#555',
    fontSize: 12,
    textAlign: 'center',
    paddingBottom: 4,
  },
});
