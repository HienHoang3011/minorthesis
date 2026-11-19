#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
from typing import List

class PaymentGateway(object):
	"""@Interface"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def charge(self, checkoutRef: str, amountCents: int, currency: str) -> dict:
		pass

	@abstractmethod
	def refund(self, providerTransactionId: str, amountCents: int) -> dict:
		pass
