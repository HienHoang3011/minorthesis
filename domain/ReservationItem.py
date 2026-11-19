#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.StockReservation import StockReservation
from domain.InventoryBatch import InventoryBatch
from typing import List

class ReservationItem(object):
	def __init__(self):
		self._reservationItemId : Integer = None
		self._quantity : Integer = None
		self._unitPriceCents : Integer = None
		self._reservation : StockReservation = None
		"""# @AssociationMultiplicity 1"""
		self._batch : InventoryBatch = None
		"""# @AssociationMultiplicity 1"""

