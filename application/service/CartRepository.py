#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
from typing import List

class CartRepository(object):
	"""@Interface"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def findByCustomer(self, customerId: int):
		pass

	@abstractmethod
	def findBySession(self, sessionKey: str):
		pass

	@abstractmethod
	def save(self, cart) -> None:
		pass
