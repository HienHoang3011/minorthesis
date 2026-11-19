#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
from typing import List

class PaymentRepository(object):
	"""@Interface"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def findById(self, paymentId: int):
		pass

	@abstractmethod
	def findByReservation(self, reservationId: int) -> list:
		pass

	@abstractmethod
	def save(self, payment) -> None:
		pass
