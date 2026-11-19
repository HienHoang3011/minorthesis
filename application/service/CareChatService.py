#!/usr/bin/python
# -*- coding: UTF-8 -*-
from application.service.CareAnswer import CareAnswer
from typing import List

class CareChatService(object):
	def __init__(self, careGuideRepository, geminiAdapter=None):
		self._careGuideRepository = careGuideRepository
		self._gemini = geminiAdapter

	def answer(self, question: str, productId: int = None) -> CareAnswer:
		guides = []
		if productId is not None:
			guides = self._careGuideRepository.findByPlant(productId)
		if not guides:
			return CareAnswer(
				text='Hiện tại không có hướng dẫn chăm sóc được phê duyệt cho câu hỏi này.',
				isRefusal=True
			)
		approved = [g for g in guides if g._approved]
		if not approved:
			return CareAnswer(
				text='Chưa có hướng dẫn chăm sóc được phê duyệt cho cây này.',
				isRefusal=True
			)
		question_lower = question.lower()
		best = None
		for guide in approved:
			content = (guide._content or '').lower()
			title = (guide._title or '').lower()
			if any(word in content or word in title
			       for word in question_lower.split()):
				best = guide
				break
		if best is None:
			best = approved[0]
		if self._gemini is not None:
			context = '\n'.join(
				g._content for g in approved if g._content
			)
			answer_text = self._gemini.chat(question, context)
		else:
			answer_text = best._content
		return CareAnswer(
			text=answer_text,
			sourceTitle=best._sourceTitle,
			isRefusal=False
		)
