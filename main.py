import customtkinter
from tkinter import *
from PIL import Image
from plyer import notification
from playsound3 import playsound
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


work_time=25
break_time=5

time_left=work_time * 60

running=False
after_id=None
mode = "Work"

settings_window = None

font="Segoe UI"

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}" 

def update_label():
    timer_label.configure(text=format_time(time_left))

def update_status_label():
    status_label.configure(text=mode)


def countdown():
    global time_left, after_id, running, mode

    if not running:
        return
        

    if time_left > 0:
        time_left -= 1

    else:
        if mode == "Work":
            mode = "Break"
            time_left = break_time * 60

            playsound("./assets/notify.mp3")

            notification.notify(
            title='Alert',
            message='Work done. Take a break.',
            app_name='Pomoly',
            timeout=4
            )
        else:
            mode = "Work"
            time_left = work_time * 60

            playsound("./assets/notify.mp3")

            notification.notify(
            title='Alert',
            message='Work session started. Focus.',
            app_name='Pomoly',
            timeout=4
            )

    update_label()
    update_status_label()
    after_id = app.after(1000, countdown)


def set_work_time(event=None):
    global work_time

    value = clamp_time(work_entry.get())
    work_time = value

    if value == "":
        return

    value = int(value)

    if value > 60:
        value = 60

    work_time = value
    update_label()

def set_break_time(event=None):
    global break_time

    value = clamp_time(break_entry.get())
    break_time = value

    if value == "":
        return

    value = int(value)

    if value > 60:
        value = 60

    break_time = value

def apply_settings(event=None):
    global work_time, break_time, time_left, mode

    work_time = clamp_time(work_entry.get())
    break_time = clamp_time(break_entry.get())

    if mode == "Work":
        time_left = work_time * 60
    else:
        time_left = break_time * 60

    update_label()

def clamp_time(value):
    try:
        value = int(value)
    except:
        return 1

    return max(1, min(value, 60))

def start_timer():
    global running

    if not running:
        running=True
        countdown()

def pause_timer():
    global running, after_id

    if running:
        running=False
        if after_id:
            app.after_cancel(after_id)

def reset_timer():
    global time_left, running, after_id

    running = False

    if mode == "Work":
        time_left = work_time * 60
    else:
        time_left = break_time * 60

    if after_id:
        app.after_cancel(after_id)

    update_label()

def open_settings():
    global work_entry, break_entry, work_entry_text, break_entry_text, apply_button, settings_window

    pause_timer()

    if settings_window is not None:
        settings_window.destroy()

    settings_window = customtkinter.CTkToplevel(app)
    settings_window.geometry("300x200")
    settings_window.title("Settings")
    settings_window.transient(app)
    settings_window.geometry("+500+250")
    settings_window.iconbitmap(resource_path("icon.ico"))

    settings_window.grid_columnconfigure(0, weight=1)

    work_entry_text=customtkinter.CTkLabel(settings_window, text="Set Work Time (Min)", font=(font, 15))
    work_entry = customtkinter.CTkEntry(settings_window, placeholder_text=f"Default is {work_time}", font=(font, 15))
    work_entry_text.grid(row=1, column=0, pady=5)
    work_entry.grid(row=2, column=0)

    break_entry_text=customtkinter.CTkLabel(settings_window, text="Set Break Time (Min)", font=(font, 15))
    break_entry = customtkinter.CTkEntry(settings_window, placeholder_text=f"Default is {break_time}", font=(font, 15))
    break_entry_text.grid(row=3, column=0, pady=5)
    break_entry.grid(row=4, column=0)

    apply_button = customtkinter.CTkButton(settings_window, text="Apply", font=(font, 15), command=apply_settings)
    apply_button.grid(row=6, column=0, pady=20)

    work_entry.bind("<Return>", apply_settings)
    break_entry.bind("<Return>", apply_settings)




app = customtkinter.CTk()
app.geometry("800x700")
app.title("Pomoly")
app.iconbitmap(resource_path("icon.ico"))

play_icon = customtkinter.CTkImage(
    light_image=Image.open(resource_path("assets/play.png")),
    size=(64, 64)
)

pause_icon = customtkinter.CTkImage(
    light_image=Image.open(resource_path("assets/pause.png")),
    size=(64, 64)
)

reset_icon = customtkinter.CTkImage(
    light_image=Image.open(resource_path("assets/reset.png")),
    size=(64, 64)
)

settings_icon = customtkinter.CTkImage(
    light_image=Image.open(resource_path("assets/settings.png")),
    size=(42, 42)
)

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(2, weight=1)

timer_label = customtkinter.CTkLabel(app, text="25:00", font=(font, 55))

status_label= customtkinter.CTkLabel(app, text=f"{mode}", font=(font, 40), text_color="orange")

settings_button = customtkinter.CTkButton(app, image=settings_icon, command=open_settings, text="", height=40, width=20, fg_color="transparent", hover=False)

start_button = customtkinter.CTkButton(app, image = play_icon, text="", command=start_timer, font=(font, 15), fg_color="white",width=20, height=40)
pause_button = customtkinter.CTkButton(app, image= pause_icon , text="", command=pause_timer, font=(font, 15), fg_color="white", width=20, height=40)
reset_button = customtkinter.CTkButton(app, image= reset_icon, text="", command=reset_timer, font=(font, 15), fg_color="red", width=20, height=40)

timer_label.place(anchor="center", rely=0.35, relx=0.5)

settings_button.place(anchor="center", rely=0.35, relx=0.62)

status_label.place(anchor="center", rely=0.24, relx=0.5)

start_button.grid(row=1, column=0, padx=10, pady=300, sticky="e")
pause_button.grid(row=1, column=1, padx=10, pady=300)
reset_button.grid(row=1, column=2, padx=10, pady=300, sticky="w")



app.mainloop()


