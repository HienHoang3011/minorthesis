#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.Shipment import Shipment
from typing import List

class ShipmentEvent(object):
	def __init__(self):
		self._eventId : Integer = None
		self._providerEventRef : String = None
		self._eventStatus : String = None
		self._occurredAt : String = None
		self._shipment : Shipment = None
		"""# @AssociationMultiplicity 1"""

