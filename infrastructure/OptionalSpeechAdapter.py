#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
OptionalSpeechAdapter — transcribes audio bytes to text.

Strategy (tried in order):
  1. google-cloud-speech (if installed + GOOGLE_APPLICATION_CREDENTIALS set)
  2. SpeechRecognition library with Google's free web API (if installed)
  3. Returns empty string (graceful no-op for demo)

In the web frontend, the browser's Web Speech API (SpeechRecognition JS)
handles speech recognition client-side before the request reaches this
server, so this adapter acts as a server-side fallback for direct API calls.
"""
import io
import os

from application.service.SpeechTranscriber import SpeechTranscriber


class OptionalSpeechAdapter(SpeechTranscriber):

    def transcribe(self, audioBytes: bytes) -> str:
        if not audioBytes:
            return ''
        result = self._try_speech_recognition(audioBytes)
        if result:
            return result
        return self._try_gemini_audio(audioBytes)

    def _try_speech_recognition(self, audioBytes: bytes) -> str:
        """Use SpeechRecognition library with Google's free web service."""
        try:
            import speech_recognition as sr  # type: ignore
            recognizer = sr.Recognizer()
            audio_file = io.BytesIO(audioBytes)
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
            return recognizer.recognize_google(audio, language='vi-VN')
        except ImportError:
            return ''
        except Exception:
            return ''

    def _try_gemini_audio(self, audioBytes: bytes) -> str:
        """Fallback: send audio to Gemini multimodal (if key available)."""
        import base64, json, urllib.request
        api_key = os.environ.get('GEMINI_API_KEY', '')
        if not api_key:
            return ''
        try:
            audio_b64 = base64.b64encode(audioBytes).decode()
            payload = json.dumps({
                'contents': [{
                    'parts': [
                        {'inline_data': {'mime_type': 'audio/webm', 'data': audio_b64}},
                        {'text': 'Transcribe this audio to Vietnamese text. Output only the transcribed text.'}
                    ]
                }]
            }).encode()
            url = (
                'https://generativelanguage.googleapis.com/v1beta/models/'
                f'gemini-2.0-flash:generateContent?key={api_key}'
            )
            req = urllib.request.Request(
                url, data=payload,
                headers={'Content-Type': 'application/json'}, method='POST'
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
            return data['candidates'][0]['content']['parts'][0]['text'].strip()
        except Exception:
            return ''
