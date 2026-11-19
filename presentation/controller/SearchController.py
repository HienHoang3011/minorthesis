#!/usr/bin/python
# -*- coding: UTF-8 -*-
from application.service.SearchService import SearchService
from application.service.SearchRequest import SearchRequest

class SearchController(object):
	def __init__(self, searchService: SearchService):
		self._searchService = searchService

	def search(self, query: str = '', imageBytes: bytes = None,
	           category: str = None, minPriceCents: int = None,
	           maxPriceCents: int = None, limit: int = 20) -> dict:
		request = SearchRequest(
			query=query,
			imageBytes=imageBytes,
			category=category,
			minPriceCents=minPriceCents,
			maxPriceCents=maxPriceCents,
			limit=limit,
		)
		if imageBytes:
			result = self._searchService.searchByImage(request)
		else:
			result = self._searchService.searchByText(request)
		return {
			'items': [self._productToDict(p) for p in result.items],
			'keywordFallback': result.keywordFallback,
			'priceRelaxed': result.priceRelaxed,
		}

	def _productToDict(self, p) -> dict:
		return {
			'productId': getattr(p, '_productId', None),
			'name': getattr(p, '_name', None),
			'category': getattr(p, '_category', None),
			'description': getattr(p, '_description', None),
			'careLevel': getattr(p, '_careLevel', None),
			'sku': getattr(p, '_sku', None),
			'priceCents': getattr(p, '_priceCents', None),
		}

	def transcribeAudio(self, audioBytes: bytes) -> str:
		return self._searchService.transcribe(audioBytes)
