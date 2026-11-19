#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.Cart import Cart
from typing import List

class Customer(object):
	def isActive(self) -> bool:
		return self._status == 'active'

	def updatePreferences(self, lightLevel: str, spaceCm: int, careEffort: str) -> 'Customer':
		self._lightLevel = lightLevel
		self._spaceCm = spaceCm
		self._careEffort = careEffort
		return self

	def __init__(self):
		self._customerId : Integer = None
		self._email : String = None
		self._passwordHash : String = None
		self._status : String = None
		self._fullName : String = None
		self._phone : String = None
		self._defaultAddress : String = None
		self._lightLevel : String = None
		self._spaceCm : Integer = None
		self._careEffort : String = None
		self._cart : Cart = None
		"""# @AssociationMultiplicity 0..1"""
		self._reservations = []
		"""# @AssociationMultiplicity 0..*"""
		self._orders = []
		"""# @AssociationMultiplicity 0..*"""

