#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.Customer import Customer
from typing import List

class Cart(object):
	def estimateTotalCents(self) -> int:
		total = 0
		for item in self._items:
			if item._variant is not None and item._quantity:
				total += item._quantity * (item._variant._priceCents or 0)
		return total

	def __init__(self):
		self._cartId : Integer = None
		self._sessionKey : String = None
		self._createdAt : String = None
		self._updatedAt : String = None
		self._owner : Customer = None
		"""# @AssociationMultiplicity 0..1"""
		self._items = []
		"""# @AssociationMultiplicity 0..*
		# @AssociationKind Composition"""
		self._checkouts = []
		"""# @AssociationMultiplicity 0..*"""

