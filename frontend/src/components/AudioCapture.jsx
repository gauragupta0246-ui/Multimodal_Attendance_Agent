import React, { useEffect, useRef, useState } from 'react';

const AudioCapture = ({ active, onMetrics }) => {
  const [isRecording, setIsRecording] = useState(false);
  const wsRef = useRef(null);
  const audioContextRef = useRef(null);
  const processorRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (active) {
      startCapture();
    } else {
      stopCapture();
    }
    return () => stopCapture();
  }, [active]);

  const startCapture = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setIsRecording(true);

      // Connect WS
      const ws = new WebSocket('ws://localhost:8000/ws/audio');
      wsRef.current = ws;

      const audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
      audioContextRef.current = audioContext;

      const input = audioContext.createMediaStreamSource(stream);
      inputRef.current = input;

      const processor = audioContext.createScriptProcessor(4096, 1, 1);
      processorRef.current = processor;

      processor.onaudioprocess = (e) => {
        if (ws.readyState === WebSocket.OPEN) {
          const inputData = e.inputBuffer.getChannelData(0);
          ws.send(inputData.buffer);
        }
      };

      input.connect(processor);
      processor.connect(audioContext.destination);

      ws.onmessage = (event) => {
        const metrics = JSON.parse(event.data);
        if (onMetrics) onMetrics(metrics);
      };
    } catch (err) {
      console.error('Error accessing microphone:', err);
    }
  };

  const stopCapture = () => {
    if (processorRef.current) processorRef.current.disconnect();
    if (inputRef.current) inputRef.current.disconnect();
    if (audioContextRef.current) audioContextRef.current.close();
    if (wsRef.current) wsRef.current.close();
    setIsRecording(false);
  };

  return (
    <div className="audio-status">
      <p>Microphone: {isRecording ? "Listening..." : "Inactive"}</p>
    </div>
  );
};

export default AudioCapture;