#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.Customer import Customer
from domain.StockReservation import StockReservation
from domain.Shipment import Shipment
from typing import List

class CustomerOrder(object):
	def isDispatchable(self) -> bool:
		return self._status in ('placed', 'processing')

	def __init__(self):
		self._orderId : Integer = None
		self._orderRef : String = None
		self._receiverName : String = None
		self._receiverPhone : String = None
		self._deliveryAddress : String = None
		self._deliveryOption : String = None
		self._shippingFeeCents : Integer = None
		self._status : String = None
		self._totalCents : Integer = None
		self._currency : String = None
		self._createdAt : String = None
		self._paidAt : String = None
		self._cancellationReason : String = None
		self._customer : Customer = None
		"""# @AssociationMultiplicity 1"""
		self._reservation : StockReservation = None
		"""# @AssociationMultiplicity 1"""
		self._lines = []
		"""# @AssociationMultiplicity 0..*
		# @AssociationKind Composition"""
		self._transactions = []
		"""# @AssociationMultiplicity 0..*"""
		self._shipment : Shipment = None
		"""# @AssociationMultiplicity 0..1
		# @AssociationKind Composition"""

