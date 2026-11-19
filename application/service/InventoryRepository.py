#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
from typing import List

class InventoryRepository(object):
	"""@Interface"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def findBatch(self, batchId: int):
		pass

	@abstractmethod
	def findByVariant(self, variantId: int) -> list:
		pass

	@abstractmethod
	def saveBatch(self, batch) -> None:
		pass

	@abstractmethod
	def saveInspection(self, record) -> None:
		pass
