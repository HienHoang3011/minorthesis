#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.CustomerOrder import CustomerOrder
from typing import List

class Shipment(object):
	def __init__(self):
		self._shipmentId : Integer = None
		self._trackingRef : String = None
		self._carrierName : String = None
		self._handlingInstructions : String = None
		self._dispatchChecklistCompleted : Boolean = None
		self._dispatchCheckNote : String = None
		self._status : String = None
		self._dispatchedAt : String = None
		self._order : CustomerOrder = None
		"""# @AssociationMultiplicity 1"""
		self._events = []
		"""# @AssociationMultiplicity 0..*
		# @AssociationKind Composition"""

