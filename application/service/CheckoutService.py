#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List
import uuid
import datetime

class CheckoutService(object):
	def __init__(self, cartRepository, productRepository, inventoryRepository,
	             reservationRepository, paymentRepository, paymentGateway,
	             inventoryService=None):
		self._cartRepository = cartRepository
		self._productRepository = productRepository
		self._inventoryRepository = inventoryRepository
		self._reservationRepository = reservationRepository
		self._paymentRepository = paymentRepository
		self._paymentGateway = paymentGateway
		self._inventoryService = inventoryService

	def beginCheckout(self, customerId: int, cartId: int, deliveryAddress: str,
	                  deliveryOption: str, quotedTotalCents: int,
	                  receiverName: str, receiverPhone: str):
		from domain.StockReservation import StockReservation
		from domain.ReservationItem import ReservationItem

		cart = self._cartRepository.findByCustomer(customerId)
		if cart is None or cart._cartId != cartId:
			raise ValueError('Cart not found or does not belong to customer.')

		if not deliveryAddress or not receiverName or not receiverPhone:
			raise ValueError('Delivery address, receiver name and phone are required.')

		totalCents = cart.estimateTotalCents()
		if totalCents != quotedTotalCents:
			raise ValueError(f'Price changed: quoted {quotedTotalCents}, current {totalCents}.')

		reservation = StockReservation()
		reservation._checkoutRef = str(uuid.uuid4())
		reservation._receiverName = receiverName
		reservation._receiverPhone = receiverPhone
		reservation._deliveryAddress = deliveryAddress
		reservation._deliveryOption = deliveryOption
		reservation._totalCents = totalCents
		reservation._currency = 'VND'
		reservation._status = 'pending'
		reservation._createdAt = datetime.datetime.utcnow().isoformat()
		reservation._expiresAt = (
			datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
		).isoformat()
		reservation._customer = None
		reservation._sourceCart = cart

		self._reservationRepository.save(reservation)
		return reservation

	def confirmPayment(self, checkoutRef: str, providerRef: str,
	                   amountCents: int, currency: str):
		from domain.CustomerOrder import CustomerOrder
		from domain.PaymentTransaction import PaymentTransaction

		reservation = self._reservationRepository.findByCheckoutRef(checkoutRef)
		if reservation is None:
			raise ValueError('Reservation not found.')
		if reservation._status != 'pending':
			return None
		if amountCents != reservation._totalCents or currency != reservation._currency:
			raise ValueError('Payment amount or currency mismatch.')

		order = CustomerOrder()
		order._orderRef = str(uuid.uuid4())
		order._receiverName = reservation._receiverName
		order._receiverPhone = reservation._receiverPhone
		order._deliveryAddress = reservation._deliveryAddress
		order._deliveryOption = reservation._deliveryOption
		order._shippingFeeCents = 0
		order._status = 'placed'
		order._totalCents = reservation._totalCents
		order._currency = reservation._currency
		order._createdAt = datetime.datetime.utcnow().isoformat()
		order._paidAt = datetime.datetime.utcnow().isoformat()
		order._reservation = reservation

		payment = PaymentTransaction()
		payment._providerTransactionId = providerRef
		payment._paymentMethod = 'online'
		payment._amountCents = amountCents
		payment._currency = currency
		payment._status = 'paid'
		payment._receivedAt = datetime.datetime.utcnow().isoformat()
		payment._reservation = reservation
		payment._order = order

		reservation._status = 'confirmed'
		self._reservationRepository.save(reservation)
		self._paymentRepository.save(payment)
		return order

	def expireHolds(self, now: str) -> int:
		return 0
