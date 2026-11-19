#!/usr/bin/python
# -*- coding: UTF-8 -*-
from application.service.SearchRequest import SearchRequest
from application.service.SearchResult import SearchResult
from typing import List

class SearchService(object):
	def __init__(self, productRepository, keywordSearch, imageSearch=None,
	             speechTranscriber=None):
		self._productRepository = productRepository
		self._keywordSearch = keywordSearch
		self._imageSearch = imageSearch
		self._speechTranscriber = speechTranscriber

	def searchByText(self, request: SearchRequest) -> SearchResult:
		query = request.query or ''
		candidateIds = self._keywordSearch.search(query, limit=request.limit * 3)
		products = []
		if candidateIds:
			products = self._productRepository.findByIds(candidateIds)
		else:
			products = self._productRepository.findSearchable()
		filtered = [p for p in products if p.isSearchable()]
		if request.category:
			filtered = [p for p in filtered if p._category == request.category]
		if request.minPriceCents is not None:
			filtered = [p for p in filtered
			            if any((v._priceCents or 0) >= request.minPriceCents
			                   for v in p._variants)]
		if request.maxPriceCents is not None:
			filtered = [p for p in filtered
			            if any((v._priceCents or 0) <= request.maxPriceCents
			                   for v in p._variants)]
		return SearchResult(items=filtered[:request.limit],
		                    keywordFallback=bool(candidateIds))

	def searchByImage(self, request: SearchRequest) -> SearchResult:
		if self._imageSearch is None:
			return SearchResult(items=[], keywordFallback=False)
		candidateIds = self._imageSearch.searchByImage(
			request.imageBytes, limit=request.limit * 3)
		products = self._productRepository.findByIds(candidateIds) if candidateIds else []
		filtered = [p for p in products if p.isSearchable()]
		return SearchResult(items=filtered[:request.limit])

	def transcribe(self, audioBytes: bytes) -> str:
		if self._speechTranscriber is None:
			return ''
		return self._speechTranscriber.transcribe(audioBytes)
