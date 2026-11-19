#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
from typing import List

class ReservationRepository(object):
	"""@Interface"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def findById(self, reservationId: int):
		pass

	@abstractmethod
	def findByCheckoutRef(self, checkoutRef: str):
		pass

	@abstractmethod
	def save(self, reservation) -> None:
		pass
