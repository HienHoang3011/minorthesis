#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List

class SearchRequest(object):
	def __init__(self, query: str = None, imageBytes: bytes = None,
	             category: str = None, minPriceCents: int = None,
	             maxPriceCents: int = None, limit: int = 20):
		self._query : str = query
		self._imageBytes : bytes = imageBytes
		self._category : str = category
		self._minPriceCents : int = minPriceCents
		self._maxPriceCents : int = maxPriceCents
		self._limit : int = limit

	@property
	def query(self):
		return self._query

	@property
	def imageBytes(self):
		return self._imageBytes

	@property
	def category(self):
		return self._category

	@property
	def minPriceCents(self):
		return self._minPriceCents

	@property
	def maxPriceCents(self):
		return self._maxPriceCents

	@property
	def limit(self):
		return self._limit
