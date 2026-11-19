#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.StockReservation import StockReservation
from domain.CustomerOrder import CustomerOrder
from typing import List

class PaymentTransaction(object):
	def __init__(self):
		self._paymentId : Integer = None
		self._providerTransactionId : String = None
		self._paymentMethod : String = None
		self._amountCents : Integer = None
		self._currency : String = None
		self._status : String = None
		self._receivedAt : String = None
		self._reservation : StockReservation = None
		"""# @AssociationMultiplicity 1"""
		self._order : CustomerOrder = None
		"""# @AssociationMultiplicity 0..1"""

