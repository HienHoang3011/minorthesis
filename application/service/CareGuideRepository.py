#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
from typing import List

class CareGuideRepository(object):
	"""@Interface"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def findByPlant(self, plantProductId: int) -> list:
		pass

	@abstractmethod
	def findByCategory(self, categoryScope: str) -> list:
		pass

	@abstractmethod
	def findById(self, guideId: int):
		pass
