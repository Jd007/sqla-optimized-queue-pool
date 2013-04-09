from time import time
from sqlalchemy.pool import QueuePool, _ConnectionRecord

class _OptimizedConnectionRecord(_ConnectionRecord):

	'''
	A slightly revised, optimized version of the builtin _ConnectionRecord class.
	The connection start time is reset each time a connection is made (as opposed
	to the builtin one where it is set once on creation). This is in response to
	MySQL's global wait_time variable, which refreshes everytime a connection is
	made, so there is no reason for the connection to be remade.

	Only when the connection has been truly idle for over the Pool's recycle time
	will the connection be remade on next use.
	'''

	def get_connection(self):
		if self.connection is None:
			self.connection = self._ConnectionRecord__connect()
			self.info.clear()
			if self._ConnectionRecord__pool.dispatch.connect:
				self._ConnectionRecord__pool.dispatch.connect(self.connection, self)
		elif self._ConnectionRecord__pool._recycle > -1 and \
				time() - self.starttime > self._ConnectionRecord__pool._recycle:
			self._ConnectionRecord__pool.logger.info(
					"Connection %r exceeded timeout; recycling",
					self.connection)
			self._ConnectionRecord__close()
			self.connection = self._ConnectionRecord__connect()
			self.info.clear()
			if self._ConnectionRecord__pool.dispatch.connect:
				self._ConnectionRecord__pool.dispatch.connect(self.connection, self)
		else:
			# No need to reconnect, so just refresh the start time
			self.starttime = time()
		return self.connection

class OptimizedQueuePool(QueuePool):

	'''
	A copy of the builtin QueuePool class, except that it uses the revised version
	of _ConnectionRecord class, _OptimizedConnectionRecord, for connection creation.
	'''

	def _create_connection(self):
		return _OptimizedConnectionRecord(self)