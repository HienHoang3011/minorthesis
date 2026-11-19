#!/usr/bin/python
# -*- coding: UTF-8 -*-
from application.service.PaymentGateway import PaymentGateway
from typing import List
import uuid
import datetime

class LocalPaymentGateway(PaymentGateway):
	def charge(self, checkoutRef: str, amountCents: int, currency: str) -> dict:
		return {
			'status': 'approved',
			'providerTransactionId': str(uuid.uuid4()),
			'checkoutRef': checkoutRef,
			'amountCents': amountCents,
			'currency': currency,
			'timestamp': datetime.datetime.utcnow().isoformat(),
		}

	def refund(self, providerTransactionId: str, amountCents: int) -> dict:
		return {
			'status': 'refunded',
			'providerTransactionId': providerTransactionId,
			'amountCents': amountCents,
			'timestamp': datetime.datetime.utcnow().isoformat(),
		}
