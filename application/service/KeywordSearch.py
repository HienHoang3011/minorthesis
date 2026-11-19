#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
from typing import List

class KeywordSearch(object):
	"""@Interface"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def search(self, query: str, limit: int = 20) -> list:
		pass
