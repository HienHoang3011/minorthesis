#!/usr/bin/python
# -*- coding: UTF-8 -*-
from application.service.ReservationRepository import ReservationRepository
from typing import List

class SQLiteReservationRepository(ReservationRepository):
	def __init__(self, transactionManager):
		self._tm = transactionManager

	def _rowToReservation(self, row):
		from domain.StockReservation import StockReservation
		r = StockReservation()
		r._reservationId = row['reservationId']
		r._checkoutRef = row['checkoutRef']
		r._receiverName = row['receiverName']
		r._receiverPhone = row['receiverPhone']
		r._deliveryAddress = row['deliveryAddress']
		r._deliveryOption = row['deliveryOption']
		r._shippingFeeCents = row['shippingFeeCents']
		r._totalCents = row['totalCents']
		r._currency = row['currency']
		r._status = row['status']
		r._createdAt = row['createdAt']
		r._expiresAt = row['expiresAt']
		return r

	def findById(self, reservationId: int):
		with self._tm.transaction() as conn:
			row = conn.execute(
				'SELECT * FROM StockReservation WHERE reservationId = ?',
				(reservationId,)
			).fetchone()
		if row is None:
			return None
		return self._rowToReservation(row)

	def findByCheckoutRef(self, checkoutRef: str):
		with self._tm.transaction() as conn:
			row = conn.execute(
				'SELECT * FROM StockReservation WHERE checkoutRef = ? LIMIT 1',
				(checkoutRef,)
			).fetchone()
		if row is None:
			return None
		return self._rowToReservation(row)

	def save(self, reservation) -> None:
		with self._tm.transaction() as conn:
			conn.execute(
				'''INSERT OR REPLACE INTO StockReservation
				   (reservationId, checkoutRef, receiverName, receiverPhone,
				    deliveryAddress, deliveryOption, shippingFeeCents,
				    totalCents, currency, status, createdAt, expiresAt,
				    cartId, customerId)
				   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
				(reservation._reservationId, reservation._checkoutRef,
				 reservation._receiverName, reservation._receiverPhone,
				 reservation._deliveryAddress, reservation._deliveryOption,
				 reservation._shippingFeeCents or 0, reservation._totalCents,
				 reservation._currency, reservation._status,
				 reservation._createdAt, reservation._expiresAt,
				 reservation._sourceCart._cartId if reservation._sourceCart else None,
				 reservation._customer._customerId if reservation._customer else None)
			)
