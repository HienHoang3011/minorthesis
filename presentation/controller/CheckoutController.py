#!/usr/bin/python
# -*- coding: UTF-8 -*-
from application.service.CheckoutService import CheckoutService

class CheckoutController(object):
	def __init__(self, checkoutService: CheckoutService):
		self._checkoutService = checkoutService

	def beginCheckout(self, customerId: int, cartId: int,
	                  deliveryAddress: str, deliveryOption: str,
	                  quotedTotalCents: int, receiverName: str,
	                  receiverPhone: str) -> dict:
		reservation = self._checkoutService.beginCheckout(
			customerId=customerId,
			cartId=cartId,
			deliveryAddress=deliveryAddress,
			deliveryOption=deliveryOption,
			quotedTotalCents=quotedTotalCents,
			receiverName=receiverName,
			receiverPhone=receiverPhone,
		)
		return {
			'checkoutRef': reservation._checkoutRef,
			'totalCents': reservation._totalCents,
			'currency': reservation._currency,
			'expiresAt': reservation._expiresAt,
		}

	def confirmPayment(self, checkoutRef: str, providerRef: str,
	                   amountCents: int, currency: str) -> dict:
		order = self._checkoutService.confirmPayment(
			checkoutRef=checkoutRef,
			providerRef=providerRef,
			amountCents=amountCents,
			currency=currency,
		)
		if order is None:
			return {'status': 'failed'}
		return {
			'status': 'placed',
			'orderRef': order._orderRef,
			'totalCents': order._totalCents,
		}
