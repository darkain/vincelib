

################################################################################
# EXTERNAL DEPENDENCIES
################################################################################
from threading import Thread




class threed(Thread):
	value = None


	def set(self, value):
		self.value = value


	def get(self):
		return self.value


	def join(self):
		Thread.join(self)
		return self.value
