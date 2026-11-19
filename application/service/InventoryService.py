#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List
import datetime

class InventoryService(object):
	def __init__(self, inventoryRepository):
		self._inventoryRepository = inventoryRepository

	def receiveShipment(self, variantId: int, supplierId: int, receiverStaffId: int,
	                    supplierBatchRef: str, receivedQty: int, arrivalDate: str):
		from domain.InventoryBatch import InventoryBatch
		from domain.InspectionRecord import InspectionRecord

		if receivedQty <= 0:
			raise ValueError('Received quantity must be positive.')

		batch = InventoryBatch()
		batch._supplierBatchRef = supplierBatchRef
		batch._arrivalDate = arrivalDate
		batch._receivedQty = receivedQty
		batch._readyQty = 0
		batch._reservedQty = 0
		batch._allocatedQty = 0
		batch._underCareQty = receivedQty
		batch._removedQty = 0
		batch._dispatchedQty = 0
		batch._postedAt = datetime.datetime.utcnow().isoformat()

		self._inventoryRepository.saveBatch(batch)

		inspection = InspectionRecord()
		inspection._recordType = 'receipt'
		inspection._recordedAt = datetime.datetime.utcnow().isoformat()
		inspection._conditionSummary = 'Initial receipt — awaiting inspection.'
		inspection._readyQty = 0
		inspection._underCareQty = receivedQty
		inspection._removedQty = 0
		inspection._batch = batch

		self._inventoryRepository.saveInspection(inspection)
		return batch

	def reclassify(self, batchId: int, inspectorStaffId: int, readyQty: int,
	               underCareQty: int, removedQty: int, conditionSummary: str,
	               careNote: str = None, reinspectionDate: str = None):
		from domain.InspectionRecord import InspectionRecord

		batch = self._inventoryRepository.findBatch(batchId)
		if batch is None:
			raise ValueError('Batch not found.')
		if readyQty + underCareQty + removedQty > batch._receivedQty:
			raise ValueError('Reclassified quantities exceed received quantity.')

		batch._readyQty = readyQty
		batch._underCareQty = underCareQty
		batch._removedQty = removedQty
		self._inventoryRepository.saveBatch(batch)

		inspection = InspectionRecord()
		inspection._recordType = 'reclassification'
		inspection._recordedAt = datetime.datetime.utcnow().isoformat()
		inspection._conditionSummary = conditionSummary
		inspection._careNote = careNote
		inspection._readyQty = readyQty
		inspection._underCareQty = underCareQty
		inspection._removedQty = removedQty
		inspection._reinspectionDate = reinspectionDate
		inspection._batch = batch
		self._inventoryRepository.saveInspection(inspection)
		return inspection
