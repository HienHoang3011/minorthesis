#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.Cart import Cart
from domain.Customer import Customer
from domain.CustomerOrder import CustomerOrder
from typing import List

class StockReservation(object):
	def __init__(self):
		self._reservationId : Integer = None
		self._checkoutRef : String = None
		self._receiverName : String = None
		self._receiverPhone : String = None
		self._deliveryAddress : String = None
		self._deliveryOption : String = None
		self._shippingFeeCents : Integer = None
		self._totalCents : Integer = None
		self._currency : String = None
		self._status : String = None
		self._createdAt : String = None
		self._expiresAt : String = None
		self._sourceCart : Cart = None
		"""# @AssociationMultiplicity 1"""
		self._customer : Customer = None
		"""# @AssociationMultiplicity 1"""
		self._items = []
		"""# @AssociationMultiplicity 0..*
		# @AssociationKind Composition"""
		self._order : CustomerOrder = None
		"""# @AssociationMultiplicity 0..1"""
		self._paymentAttempts = []
		"""# @AssociationMultiplicity 0..*"""

