"""
	Code sourced from here, added error handling to it.
	https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
"""
import threading
import traceback
import queue


# wrap function in @threaded decorator
def threaded(f, daemon=False):
	def wrapped_f(q, *args, **kwargs):
		"""this function calls the decorated function and puts the
		result in a queue"""
		try:
			ret = f(*args, **kwargs)
			q.put(ret)
		except:
			return q.put(None, traceback.format_exc())

	def wrap(*args, **kwargs):
		"""this is the function returned from the decorator. It fires off
		wrapped_f in a new thread and returns the thread object with
		the result queue attached"""

		q = queue.Queue()

		t = threading.Thread(target=wrapped_f, args=(q,)+args, kwargs=kwargs)
		t.daemon = daemon
		t.start()
		t.result_queue = q
		return t

	return wrap
