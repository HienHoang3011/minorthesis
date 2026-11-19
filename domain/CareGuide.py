#!/usr/bin/python
# -*- coding: UTF-8 -*-
from domain.PlantProduct import PlantProduct
from typing import List

class CareGuide(object):
	def __init__(self):
		self._guideId : Integer = None
		self._categoryScope : String = None
		self._title : String = None
		self._content : String = None
		self._sourceTitle : String = None
		self._approved : Boolean = None
		self._revisionDate : String = None
		self._plant : PlantProduct = None
		"""# @AssociationMultiplicity 0..1"""

