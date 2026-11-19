#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
from typing import List

class OrderRepository(object):
	"""@Interface"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def findById(self, orderId: int):
		pass

	@abstractmethod
	def findByCustomer(self, customerId: int) -> list:
		pass

	@abstractmethod
	def save(self, order) -> None:
		pass
