#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
from typing import List

class SpeechTranscriber(object):
	"""@Interface"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def transcribe(self, audioBytes: bytes) -> str:
		pass
