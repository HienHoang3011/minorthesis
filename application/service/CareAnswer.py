#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List

class CareAnswer(object):
	def __init__(self, text: str = None, sourceTitle: str = None,
	             isRefusal: bool = False):
		self._text : str = text
		self._sourceTitle : str = sourceTitle
		self._isRefusal : bool = isRefusal

	@property
	def text(self):
		return self._text

	@property
	def sourceTitle(self):
		return self._sourceTitle

	@property
	def isRefusal(self):
		return self._isRefusal
