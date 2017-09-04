from tkinter import ttk
from io import StringIO
import traceback
import tkinter
import logging
__FORM_BACKGROUND_COLOR__ = "light gray"
__MSG_BOX_BG_COLOR__ = "light green"
__FORM_WIDTH__ = 325


class FrameBase(tkinter.Frame):
	__POSITION__ = 0

	def __init__(self, root, bg=__FORM_BACKGROUND_COLOR__, height=0):
		super().__init__(master=root, height=height, background=bg)

	def place_me(self):
		self.grid(row=FrameBase.__POSITION__)
		FrameBase.__POSITION__ += 1


class MsgFrame(FrameBase):
	def __init__(self, root, locale_info):
		super().__init__(root, bg="white", height=200)
		self.msg_number = 1
		self.__MSG_BOX_WIDTH__ = 25
		self.__MSG_BOX_ROWS__ = 8
		title_label = ttk.Label(self, style="title.TLabel", text="Exit does not end connections...")
		title_label.grid(row=0)
		self.msg_var = tkinter.StringVar()
		self.main_msg = tkinter.Text(master=self, width=self.__MSG_BOX_WIDTH__, height=self.__MSG_BOX_ROWS__, background=__MSG_BOX_BG_COLOR__, foreground="dark green", relief="sunken", font=("courier", 16))
		self.update_msg(locale_info)
		self.main_msg.grid(row=1, sticky=tkinter.EW)

	def update_msg(self, msg):
		"""Dict to msg formatter."""
		if isinstance(msg, dict):
			msg = ["{}: {}".format(k, v) for k, v in msg.items()]
		else:  # assume string...
			msg = msg.split("\n")
		size_spec = self.__MSG_BOX_WIDTH__ * self.__MSG_BOX_ROWS__
		_out = "{}#:\n".format(self.msg_number)
		for v in msg:
			_line_prefix = "___"
			_v = StringIO(v)
			while True:
				chunk = _v.read(self.__MSG_BOX_WIDTH__ - len(_line_prefix))
				if not chunk:
					break
				chunk = chunk.strip()
				if len(chunk) + len(_line_prefix) < self.__MSG_BOX_WIDTH__:
					chunk += " " * (self.__MSG_BOX_WIDTH__ - len(chunk))
				_out += _line_prefix + chunk + "\n"
			_out = _out[:size_spec]
		if not _out.endswith("\n"):
			_out += "\n"
		self.main_msg.insert(tkinter.END, _out)
		self.main_msg.see("end")
		self.msg_number += 1


class VpnManager(FrameBase):
	def __init__(self, root, onfun, offfun, alivefun, progress_bar, msg_box):
		super().__init__(root)
		self.onbutton = ttk.Button(self, text="CONNECT", width=10, command=lambda: self.do_async_show_progress(onfun, "Connecting..."))
		self.onbutton.grid(row=0, column=0, sticky=tkinter.EW)
		self.offbutton = ttk.Button(self, text="DISCONNECT", width=10, command=lambda: self.do_async_show_progress(offfun, "Disconnecting..."))
		self.offbutton.grid(row=0, column=1, sticky=tkinter.EW)
		self.alivebutton = ttk.Button(self, text="?", width=1, command=lambda: self.do_async_show_progress(alivefun, "Checking pulse..."))
		self.alivebutton.grid(row=0, column=2, sticky=tkinter.EW)
		self.msg_box = msg_box
		self.progress_form = progress_bar
		self._running = False

	def do_async_show_progress(self, fun, execution_text):
		if self._running:
			return
		logger = logging.getLogger(__name__)
		logger.info("Executing function: {}.".format(execution_text))
		self._running = True

		try:
			self.onbutton.config(state="disabled")
			self.offbutton.config(state="disabled")
			self.alivebutton.config(state="disabled")
			self.progress_form.reset()
			t = fun()  # async!
			self.msg_box.update_msg(execution_text)
			while t.is_alive():
				self.progress_form.progress.step(1)
				self.after(100, self.update())
			status, msg = t.result_queue.get()
			{
				True: self.progress_form.success,
				False: self.progress_form.fail
			}[status]()
			{
				True: lambda: self.offbutton.config(state="enabled"),
				False: lambda: self.onbutton.config(state="enabled")
			}[status]()
			self.alivebutton.config(state="enabled")
			self.msg_box.update_msg(msg)
		except:
			logger.error("Error executing async function in gui!\n{}".format(traceback.format_exc()))
			self.msg_box.update_msg("Encountered error; State unknown.\n".format(traceback.format_exc()))
			self.offbutton.config(state="enabled")
			self.onbutton.config(state="enabled")
			self.alivebutton.config(state="enabled")
			self.progress_form.fail()
		finally:
			self.after(100, self.update())
			self._running = False


class ProgressBar(FrameBase):
	def __init__(self, root):
		super().__init__(root)
		self.failed_task = ttk.Progressbar(master=self, style="red.Horizontal.TProgressbar", length=__FORM_WIDTH__, orient="horizontal", mode="determinate")
		self.progress = ttk.Progressbar(master=self, style="green.Horizontal.TProgressbar", length=__FORM_WIDTH__, orient="horizontal", mode="determinate")
		self.failed_task.grid(row=0, column=0, sticky=tkinter.EW)
		self.progress.grid(row=0, column=0, sticky=tkinter.EW)
		self.progress.tkraise()

	def success(self):
		self.progress["maximum"] = 100
		self.progress["value"] = 100
		self.progress.tkraise()

	def fail(self):
		self.failed_task["maximum"] = 100
		self.failed_task["value"] = 100
		self.failed_task.tkraise()

	def reset(self):
		self.progress["maximum"] = 100
		self.progress["value"] = 0
		self.progress.tkraise()


def start_gui(locale_info, start_fun, stop_fun, alive_fun):
	tk = tkinter.Tk()
	tk.resizable(0, 0)
	s = ttk.Style()
	s.theme_use('clam')
	s.configure("title.TLabel", foreground="black", background="white", font=("courier", 18))
	s.configure("red.Horizontal.TProgressbar", foreground="red", background="red")
	s.configure("green.Horizontal.TProgressbar", foreground="green", background="green")
	s.configure("TButton", foreground="black", background="white", font=("courier", 18), take_focus=True)
	# tk.configure(background=__FORM_BACKGROUND_COLOR__)
	tk.title("VPN Connector (NORDVPN)")
	b = MsgFrame(tk, locale_info=locale_info)
	pb = ProgressBar(tk)
	vm = VpnManager(tk, onfun=start_fun, offfun=stop_fun, alivefun=alive_fun, progress_bar=pb, msg_box=b)
	b.place_me()
	pb.place_me()
	vm.place_me()
	tkinter.mainloop()
