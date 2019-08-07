# import threading
# import tkinter as tk
# from tkinter import ttk


# class Progress():
#     """ threaded progress bar for tkinter gui """
#     def __init__(self, parent, row, column, columnspan):
#         self.maximum = 100
#         self.interval = 10
#         self.progressbar = ttk.Progressbar(parent, orient=tk.HORIZONTAL,
#                                            mode="indeterminate",
#                                            maximum=self.maximum)
#         self.progressbar.grid(row=row, column=column,
#                               columnspan=columnspan, sticky="we")
#         self.thread = threading.Thread()
#         self.thread.__init__(target=self.progressbar.start(self.interval),
#                              args=())
#         self.thread.start()

#     def pb_stop(self):
#         """ stops the progress bar """
#         if not self.thread.isAlive():
#             VALUE = self.progressbar["value"]
#             self.progressbar.stop()
#             self.progressbar["value"] = VALUE

#     def pb_start(self):
#         """ starts the progress bar """
#         if not self.thread.isAlive():
#             VALUE = self.progressbar["value"]
#             self.progressbar.configure(mode="indeterminate",
#                                        maximum=self.maximum,
#                                        value=VALUE)
#             self.progressbar.start(self.interval)

#     def pb_clear(self):
#         """ stops the progress bar """
#         if not self.thread.isAlive():
#             self.progressbar.stop()
#             self.progressbar.configure(mode="determinate", value=0)

#     def pb_complete(self):
#         """ stops the progress bar and fills it """
#         if not self.thread.isAlive():
#             self.progressbar.stop()
#             self.progressbar.configure(mode="determinate",
#                                        maximum=self.maximum,
#                                        value=self.maximum)

# def printmsg():
#     """ prints a message in a seperate thread to tkinter """
#     print("proof a seperate thread is running")


# class AppGUI(tk.Frame):
#     """ class to define tkinter GUI"""
#     def __init__(self, parent,):
#         tk.Frame.__init__(self, master=parent)
#         prog_bar = Progress(parent, row=0, column=0, columnspan=2)
#         # Button 1
#         start_button = ttk.Button(parent, text="start",
#                                   command=prog_bar.pb_start)
#         start_button.grid(row=1, column=0)
#         # Button 2
#         stop_button = ttk.Button(parent, text="stop",
#                                  command=prog_bar.pb_stop)
#         stop_button.grid(row=1, column=1)
#         # Button 3
#         complete_button = ttk.Button(parent, text="complete",
#                                      command=prog_bar.pb_complete)
#         complete_button.grid(row=2, column=0)
#         # Button 4
#         clear_button = ttk.Button(parent, text="clear",
#                                   command=prog_bar.pb_clear)
#         clear_button.grid(row=2, column=1)
#         # Button 5
#         test_print_button = ttk.Button(parent, text="thread test",
#                                        command=printmsg)
#         test_print_button.grid(row=3, column=0, columnspan=2, sticky="we")


# ROOT = tk.Tk()
# APP = AppGUI(ROOT)
# ROOT.mainloop()

import threading
import time

                    
def wait_for_event(e):
    print('wait_for_event starting')
    event_is_set = e.wait()
    print('event set_: %s', event_is_set)

def wait_for_event_timeout(e, t):
    while not e.isSet():
        print('wait_for_event_timeout starting')
        event_is_set = e.wait(t)
        print('event set: %s', event_is_set)
        if event_is_set:
            print('processing event')
        else:
            print('doing other things')

if __name__ == '__main__':
    e = threading.Event()
    t1 = threading.Thread(name='blocking', 
                      target=wait_for_event,
                      args=(e,))
    t1.start()

    t2 = threading.Thread(name='non-blocking', 
                      target=wait_for_event_timeout, 
                      args=(e, 2))
    t2.start()

    print('Waiting before calling Event.set()')
    time.sleep(5)
    e.set()
    print('Event is set')