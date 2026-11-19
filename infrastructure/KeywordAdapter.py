#!/usr/bin/python
# -*- coding: UTF-8 -*-
from application.service.KeywordSearch import KeywordSearch
class KeywordAdapter(KeywordSearch):
	def __init__(self):
		self._index = {}

	def buildIndex(self, products: list) -> None:
		self._index = {}
		for product in products:
			doc = ''
			if hasattr(product, 'searchDocument'):
				doc = product.searchDocument() or ''
			else:
				parts = [product._name or '', product._description or '',
				         product._category or '']
				doc = ' '.join(parts)
			self._index[product._productId] = doc.lower()

	def search(self, query: str, limit: int = 20) -> list:
		if not query or not self._index:
			return []
		terms = query.lower().split()
		scores = {}
		for productId, doc in self._index.items():
			score = sum(doc.count(term) for term in terms)
			if score > 0:
				scores[productId] = score
		ranked = sorted(scores.keys(), key=lambda pid: scores[pid], reverse=True)
		return ranked[:limit]
