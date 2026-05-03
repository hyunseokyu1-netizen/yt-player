import React, { useState } from 'react';
import {
  Modal,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';

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
    onClose();
  };

  return (
    <Modal visible={visible} transparent animationType="slide" onRequestClose={handleClose}>
      <KeyboardAvoidingView
        style={styles.overlay}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <View style={[styles.sheet, { paddingBottom: 24 + bottomInset }]}>
          <Text style={styles.title}>유튜브 URL 추가</Text>
          <TextInput
            style={styles.input}
            placeholder="https://www.youtube.com/watch?v=..."
            placeholderTextColor="#666"
            value={url}
            onChangeText={setUrl}
            autoCapitalize="none"
            autoCorrect={false}
            editable={!isLoading}
          />
          {error ? <Text style={styles.error}>{error}</Text> : null}
          <View style={styles.row}>
            <TouchableOpacity style={styles.cancelBtn} onPress={handleClose} disabled={isLoading}>
              <Text style={styles.cancelText}>취소</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.addBtn} onPress={handleAdd} disabled={isLoading}>
              {isLoading ? (
                <ActivityIndicator color="#fff" size="small" />
              ) : (
                <Text style={styles.addText}>추가</Text>
              )}
            </TouchableOpacity>
          </View>
        </View>
      </KeyboardAvoidingView>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.6)',
    justifyContent: 'flex-end',
  },
  sheet: {
    backgroundColor: '#1e1e2e',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    padding: 24,
    gap: 12,
  },
  title: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 4,
  },
  input: {
    backgroundColor: '#2a2a3e',
    color: '#fff',
    borderRadius: 10,
    padding: 14,
    fontSize: 14,
  },
  error: {
    color: '#ff6b6b',
    fontSize: 13,
  },
  row: {
    flexDirection: 'row',
    gap: 10,
    marginTop: 4,
  },
  cancelBtn: {
    flex: 1,
    padding: 14,
    borderRadius: 10,
    backgroundColor: '#2a2a3e',
    alignItems: 'center',
  },
  cancelText: {
    color: '#aaa',
    fontSize: 15,
    fontWeight: '600',
  },
  addBtn: {
    flex: 1,
    padding: 14,
    borderRadius: 10,
    backgroundColor: '#ff0000',
    alignItems: 'center',
  },
  addText: {
    color: '#fff',
    fontSize: 15,
    fontWeight: '700',
  },
});
