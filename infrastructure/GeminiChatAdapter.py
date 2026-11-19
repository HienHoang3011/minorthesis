#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
GeminiChatAdapter — calls Gemini REST API for care guide Q&A.
Falls back to rule-based answer when GEMINI_API_KEY is not set.
"""
import os
import json
import urllib.request
import urllib.error

_GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent?key={key}"
)

_SYSTEM_PROMPT = (
    "Bạn là chuyên gia chăm sóc cây cảnh của cửa hàng Northfield Plant Shop. "
    "Trả lời ngắn gọn, thực tế, bằng tiếng Việt. "
    "Chỉ dùng thông tin từ hướng dẫn chăm sóc được cung cấp. "
    "Nếu không có thông tin liên quan, nói thẳng là chưa có hướng dẫn cụ thể."
)


class GeminiChatAdapter:
    def __init__(self):
        self._api_key = os.environ.get("GEMINI_API_KEY", "")

    def chat(self, question: str, context: str) -> str:
        if not self._api_key:
            return self._rule_based(question, context)
        try:
            return self._call_gemini(question, context)
        except Exception:
            return self._rule_based(question, context)

    def _call_gemini(self, question: str, context: str) -> str:
        prompt = (
            f"{_SYSTEM_PROMPT}\n\n"
            f"Hướng dẫn chăm sóc:\n{context}\n\n"
            f"Câu hỏi: {question}"
        )
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}]
        }).encode()
        url = _GEMINI_URL.format(key=self._api_key)
        req = urllib.request.Request(
            url, data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        return (
            data["candidates"][0]["content"]["parts"][0]["text"].strip()
        )

    def _rule_based(self, question: str, context: str) -> str:
        q = question.lower()
        lines = [l.strip() for l in context.splitlines() if l.strip()]
        for line in lines:
            ll = line.lower()
            if any(w in ll for w in q.split() if len(w) > 3):
                return line
        return context[:300] if context else "Chưa có hướng dẫn cụ thể cho câu hỏi này."
