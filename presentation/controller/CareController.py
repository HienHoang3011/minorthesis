#!/usr/bin/python
# -*- coding: UTF-8 -*-
from application.service.CareChatService import CareChatService

class CareController(object):
	def __init__(self, careChatService: CareChatService):
		self._careChatService = careChatService

	def answer(self, question: str, productId: int = None) -> dict:
		result = self._careChatService.answer(question=question, productId=productId)
		return {
			'text': result.text,
			'sourceTitle': result.sourceTitle,
			'isRefusal': result.isRefusal,
		}
