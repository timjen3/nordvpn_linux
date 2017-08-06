import tkinter


class FrameBase(tkinter.Frame):
	__POSITION__ = 0

	def __init__(self, root):
		super().__init__(root)

	def place_me(self):
		self.grid(row=MsgFrame.__POSITION__, column=0)
		MsgFrame.__POSITION__ += 1


class MsgFrame(FrameBase):
	def __init__(self, root):
		super().__init__(root)
		self.msg_var = tkinter.StringVar()
		self.msg_var.set("connect / disconnect vpn...")
		tkinter.Label(self, textvariable=self.msg_var, font=(None, 18)).grid(row=0, column=0, columnspan=4)
		self.place_me()


class VpnManager(FrameBase):
	def __init__(self, root, onfun, offfun, msg_box):
		super().__init__(root)
		self.onbutton = tkinter.Button(self, text="CONNECT", font=(None, 18), command=lambda: self.before_do(onfun))
		self.onbutton.grid(row=0, column=0, sticky=tkinter.EW)
		self.offbutton = tkinter.Button(self, text="DISCONNECT", font=(None, 18), command=lambda: self.before_do(offfun))
		self.offbutton.grid(row=0, column=1, sticky=tkinter.EW)
		self.msg_box = msg_box
		self.place_me()

	def before_do(self, fun):
		self.offbutton.config(state="disabled")
		self.onbutton.config(state="disabled")
		msg = fun()
		self.msg_box.set(msg)
		self.offbutton.config(state="active")
		self.onbutton.config(state="active")


def start_gui(start_fun, stop_fun):
	tk = tkinter.Tk()
	b = MsgFrame(tk)
	VpnManager(tk, onfun=start_fun, offfun=stop_fun, msg_box=b.msg_var)
	tkinter.mainloop()
