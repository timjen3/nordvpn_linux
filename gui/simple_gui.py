from tkinter import ttk
import traceback
import tkinter
__FORM_BACKGROUND_COLOR__ = "light gray"
__MSG_BOX_BG_COLOR__ = "light green"


class FrameBase(tkinter.Frame):
	__POSITION__ = 0

	def __init__(self, root, bg=__FORM_BACKGROUND_COLOR__, height=0):
		super().__init__(master=root, height=height, background=bg)

	def place_me(self):
		self.grid(row=FrameBase.__POSITION__)
		FrameBase.__POSITION__ += 1


class MsgFrame(FrameBase):
	def __init__(self, root, start_text):
		super().__init__(root, bg="white", height=200)
		self.msg_var = tkinter.StringVar()
		self.msg_var.set(start_text)
		title_label = ttk.Label(self, style="title.TLabel", text="Close at any time.")
		main_msg = tkinter.Label(master=self, height=2, width=25, textvariable=self.msg_var, background=__MSG_BOX_BG_COLOR__, foreground="dark green", relief="sunken", justify="center", font=("courier", 16))
		title_label.grid(row=0)
		main_msg.grid(row=1)


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
		self.progress_bar = progress_bar.progress
		self._running = False

	def do_async_show_progress(self, fun, execution_text):
		if self._running:
			return
		self.onbutton.config(state="disabled")
		self.offbutton.config(state="disabled")
		self.alivebutton.config(state="disabled")
		self.progress_form.reset()
		self._running = True
		t = fun()  # async!
		try:
			self.msg_box.set(execution_text)
			while t.is_alive():
				self.progress_bar.step(1)
				self.after(100, self.update())
		except:
			self.progress_form.fail()
			self.msg_box.set("Encountered error: {}\n".format(traceback.format_exc()))
			self.after(3000, self.msg_box.set(""))
		finally:
			status, msg = t.result_queue.get()
			{
				True: self.progress_form.success,
				False: self.progress_form.fail
			}[status]()
			self.msg_box.set(msg)
			{
				True: lambda: self.onbutton.config(state="enabled"),
				False: lambda: self.onbutton.config(state="enabled")
			}[status]()
			self.alivebutton.config(state="enabled")
			self._running = False


class ProgressBar(FrameBase):
	def __init__(self, root):
		super().__init__(root)
		self.failed_task = ttk.Progressbar(master=self, style="red.Horizontal.TProgressbar", length=330, orient="horizontal", mode="determinate")
		self.progress = ttk.Progressbar(master=self, style="green.Horizontal.TProgressbar", length=330, orient="horizontal", mode="determinate")
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


def start_gui(locale_info, start_fun, stop_fun, alive_fun=None):
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
	b = MsgFrame(tk, start_text=locale_info)
	pb = ProgressBar(tk)
	vm = VpnManager(tk, onfun=start_fun, offfun=stop_fun, alivefun=alive_fun, progress_bar=pb, msg_box=b.msg_var)
	b.place_me()
	pb.place_me()
	vm.place_me()
	vm.do_async_show_progress(alive_fun, "Checking pulse...")
	tkinter.mainloop()
