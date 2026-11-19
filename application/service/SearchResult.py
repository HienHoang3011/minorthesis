#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List

class SearchResult(object):
	def __init__(self, items: list = None, keywordFallback: bool = False,
	             priceRelaxed: bool = False):
		self._items : list = items if items is not None else []
		self._keywordFallback : bool = keywordFallback
		self._priceRelaxed : bool = priceRelaxed

	@property
	def items(self):
		return self._items

	@property
	def keywordFallback(self):
		return self._keywordFallback

	@property
	def priceRelaxed(self):
		return self._priceRelaxed
