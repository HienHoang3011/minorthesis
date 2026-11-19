#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
from typing import List

class ProductRepository(object):
	"""@Interface"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def findById(self, productId: int):
		pass

	@abstractmethod
	def findSearchable(self) -> list:
		pass

	@abstractmethod
	def findByIds(self, ids: list) -> list:
		pass

	@abstractmethod
	def save(self, product) -> None:
		pass
