#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
from typing import List

class ImageSearch(object):
	"""@Interface"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def searchByImage(self, imageBytes: bytes, limit: int = 20) -> list:
		pass
