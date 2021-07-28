from threading import Thread
from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox as m_box
from tkinter import ttk
import validators as valid
import pafy
from PIL import Image, ImageTk
# from urllib import request
import requests
import os


def Delete():
    global stream
    global url
    global a_v_object
    global object__
    global information
    link_entry.delete(0, tk.END)
    link_entry.insert(0, "Enter the link here")
    url = stream = a_v_object = object__ = None
    for _, l in information.items():
        l[0].config(text="")
    Title()
    Ext()


def Path(path):
    return filedialog.asksaveasfilename(initialdir=path, defaultextension='.mp4',
                                        initialfile=f"{stream.title}", title="save File",
                                        filetypes=(
                                            ('All Files', '*.*'), ('mp3', '.mp3'), ('m4a', '.m4a'),
                                            ('mp4', '.mp4'), ('webm', '.webm')))


def Save():
    with open("path.txt", 'a+') as e:
        with open('path.txt', 'r+', encoding="utf-8") as rwFile:
            data = rwFile.read()
            if data == "":
                path = Path(os.getcwd())
                if path == True and path != "":
                    rwFile.writelines(path)
            else:
                path = Path(data)
                if path == True and path != "":
                    rwFile.seek(0)
                    rwFile.writelines(path)
                    rwFile.truncate()

    if len(path) != 0:
        return path
    else:
        path = False
    return path


def btn_disable():
    download_btn.config(state="disable")
    HD_download_btn.config(state="disable")


def btn_enable():
    download_btn.config(state="normal")
    HD_download_btn.config(state="normal")


# def all_children():
#     _list = root.winfo_children()
#     print(_list[3].winfo_children())


def progressBar(total, recvd, ratio, rate, ETA):
    percent = round((recvd / total) * 100, 2)
    p_bar['value'] = percent
    downloading_status.config(
        text=f"Downloading Start   {percent} %   remaining: {ETA}sec   downloading speed: {round(rate, 2)}KB/s")
    root.update_idletasks()


def download(file):
    try:
        path = Save()
        if path is not False:
            downloading_status.config(text="Downloading Start")
            btn_disable()
            d = file.download(path, callback=progressBar)
            downloading_status.config(text="Downloading Completed")
            # p_bar.stop()
            btn_enable()
    except Exception as e:
        pass


def check_thread(th):
    if th.is_alive():
        root.after(1, lambda: check_thread(th))
    else:
        root.after(3000, lambda: downloading_status.config(text="Downloading Stop"))
        p_bar['value'] = 0


def Down_Thread(file=None):
    if file is not None:
        th4 = Thread(target=download, daemon=True, args=(file,))
        th4.start()
        root.after(1, lambda: check_thread(th4))


def Download():
    ext = c_box3.get()
    qua_file = c_box2.get()
    qua_file = qua_file[0:qua_file.index(' ')]
    downloadable_file = object__[ext][qua_file][1]
    Down_Thread(downloadable_file)


def HD_Download():
    all_hd_exe = a_v_object['Normal']
    selected_hd = c_HD.get()
    hd_extn = selected_hd[0:selected_hd.index(":")]
    hd_qua = selected_hd[selected_hd.index(" ") + 1: selected_hd.index(",")]
    downloadable_file = all_hd_exe[hd_extn][hd_qua][1]
    Down_Thread(downloadable_file)


def Cal_Size(size_in_bytes):
    count = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        count += 1
    switch = {
        1: "KB",
        2: "MB",
        3: "GB",
        4: "TB",
    }
    return f"  {round(size_in_bytes, 2)}{switch[count]}"


def Thumbnail(thumb_img=None):
    if thumb_img is not None:
        global img
        global thum_image

        img = Image.open(requests.get(thumb_img, stream=True).raw)
        img.thumbnail((200, 200), Image.ANTIALIAS)
        thum_image = ImageTk.PhotoImage(img)
        thumbnail_image.config(image=thum_image)
    else:
        thumbnail_image.config(image="")


def Title(thumb_img=None):
    if stream is not None:
        title = stream.title
        title_label.configure(text=title)
        Thumbnail(thumb_img)
    else:
        title_label.configure(text="")
        Thumbnail()


def Show_Informations():
    data = {
        "Author": stream.author,
        "Category": stream.category,
        "Duration": stream.duration,
        "Rating": stream.rating,
        "Likes": stream.likes,
        "Dislikes": stream.dislikes,
        "Length": stream.length,
        "Username": stream.username,
        "VideoId": stream.videoid,
        "ViewCount": stream.viewcount,
    }
    for keys, lst in information.items():
        lst[0].config(text=data[keys])


def Object(files):
    obj = {}
    if len(files) > 0:
        for file in files:
            if file.extension not in obj.keys():
                obj[file.extension] = dict()
            dict_obj = obj[file.extension]
            if file.quality not in dict_obj.keys():
                dict_obj[file.quality] = [Cal_Size(file.get_filesize()), file]
    return obj


def AudioStream():
    return Object(stream.audiostreams)


def VideoStream():
    return Object(stream.videostreams)


def NormalStream():
    return Object(stream.streams)


def Change_Qua(delete=None):
    try:
        if delete is not True and stream is not None:
            extension = c_box3.get()
            c_box2['values'] = list(f"{quality}  {size[0]}" for quality, size in object__[extension].items())
            c_box2.current(0)
        else:
            c_box2['values'] = "Quality"
            c_box2.current(0)

            c_HD['values'] = "Select"
            c_HD.current(0)
    except Exception as e:
        pass


def Ext():
    if object__ is not None:
        c_box3['values'] = list(object__.keys())
        c_box3.current(0)
        Change_Qua()
    else:
        c_box3['values'] = "Extension"
        c_box3.current(0)
        Change_Qua(True)


def HD_videos():
    c_HD['values'] = list(f"{normal.extension}: {normal.quality},{Cal_Size(normal.get_filesize())}"
                          for normal in stream.streams)
    c_HD.current(0)


def Audio_video():
    try:
        global object__
        global a_v_object

        if stream is not None:
            selection = c_box1.get()
            if selection == 'Video':
                object__ = a_v_object["Video"]
            else:
                object__ = a_v_object["Audio"]
            Ext()
    except Exception as e:
        pass


def Th():
    try:
        Title(stream.bigthumbhd)
    except Exception as e:
        pass


def Info():
    try:
        Show_Informations()
    except Exception as e:
        pass


def Run():
    global url
    global stream
    global a_v_object
    stream = url = None
    url = link_entry.get()
    try:
        if valid.url(url) and url is not None:
            stream = pafy.new(url)
            if stream is not None:
                a_v_object = {"Audio": AudioStream(), "Video": VideoStream(), 'Normal': NormalStream()}

                th1 = Thread(target=Audio_video, daemon=True)
                th1.start()

                th2 = Thread(target=Info, daemon=True)
                th2.start()

                th3 = Thread(target=Th, daemon=True)
                th3.start()

                HD_videos()
        else:
            m_box.showerror("Error", "Invalid Link")
    except Exception as e:
        pass


def Show_Info():
    try:
        run = Thread(target=Run, daemon=True)
        run.start()
    except Exception as e:
        pass


def Signature(master, name):
    label1 = Label(master, text=name, relief=SUNKEN, anchor=E)
    label1.pack(side=BOTTOM, fill=X)
    label1.configure(font="Helvetica 10 bold")


global url
global stream
global a_v_object
global object__

root = tk.Tk()
root.title('Video Downloader')
root.wm_iconbitmap(r"YouTube.ico")
root.geometry("1200x600+0+40")
root.minsize(1150, 640)

# ########################################################################-windows_cover
# -######################################

# ###-signature###
Signature(root, "Manish Tirkey")

# ##-progressbar

p_bar = ttk.Progressbar(root, length=400, orient=HORIZONTAL)
p_bar.config(maximum=100, mode='determinate')
p_bar.pack(side=BOTTOM)

# ##-Downloading Status
downloading_status = Label(root, text=f"Downloading Stop!")
downloading_status.pack(side=BOTTOM)

# ##-main frame-#####
root_frame = Frame(root)
root_frame.pack(side=LEFT, expand="yes", fill=BOTH)

# --------------------------------------------end windows------------------------------------

# #####--frame-1 #############--frame -2 -----------frame -3   ----###########################

frame1 = Frame(root_frame)
frame1.grid(row=0, column=1, padx=(20, 10), pady=(10, 0))

frame2 = ttk.Labelframe(root_frame, text="Information")
frame2.grid(row=0, column=2, padx=(10, 10), pady=(0, 0), sticky=N)

frame3 = Frame(root_frame)
frame3.grid(row=0, column=3, sticky=N)
# -------------------------------------------------------------------------------------

# ################################-inside-frame1-####################################
full = E + W

label = Label(frame1, text="Enter the link", font="Castellar 10 bold italic", border=2, relief=SUNKEN)
label.grid(row=0, column=0, columnspan=2, sticky=full, pady=(20, 10))

clean = Button(frame1, text="Refresh     ctrl+r", command=Delete)
clean.grid(row=1, column=1, sticky=full, pady=(8, 0))

link_entry = Entry(frame1)
link_entry.grid(row=2, column=0, columnspan=2, sticky=full, ipadx=100, ipady=8, padx=5, pady=(20, 0))
link_entry.focus_set()
link_entry.insert(0, "Enter the link here")
link_entry.configure(font="Garamond 12 bold")

btn = Button(frame1, text="Show Information", command=Show_Info)
btn.grid(row=3, column=0, columnspan=2, pady=(10, 0), padx=5, sticky=full)

select_label = Label(frame1, text="Select :")
select = 20
select_label.grid(row=4, column=0, sticky=W, pady=(select, 0))

c_box1 = ttk.Combobox(frame1, state="readonly")
c_box1['values'] = ("Audio", "Video")
c_box1.current(0)
c_box1.grid(row=4, column=1, pady=(select, 0), sticky=full)

quality_label = Label(frame1, text="Quality :")
res = 50
quality_label.grid(row=5, column=0, sticky=W, pady=(res, 0))

c_box2 = ttk.Combobox(frame1, state="readonly")
c_box2['values'] = "Quality"
c_box2.current(0)
c_box2.grid(row=5, column=1, pady=(res, 0), sticky=full)

extension_label = Label(frame1, text="Extension :")
qua = 50
extension_label.grid(row=6, column=0, sticky=W, pady=(qua, 0))

c_box3 = ttk.Combobox(frame1, state="readonly")
c_box3['values'] = "Extension"
c_box3.current(0)
c_box3.grid(row=6, column=1, pady=(qua, 0), sticky=full)

HD = Label(frame1, text="HD Audio_Video :")
hd = 40
HD.grid(row=7, column=0, sticky=W, pady=(hd, 0))

c_HD = ttk.Combobox(frame1, state='readonly')
c_HD['values'] = "Select"
c_HD.current(0)
c_HD.grid(row=7, column=1, sticky=full, pady=(hd, 0))

download_btn = Button(frame1, text="Download", command=Download)
download_btn.grid(row=8, column=0, sticky=full, pady=(60, 0))

HD_download_btn = Button(frame1, text="HD Audio Video Download", command=HD_Download)
HD_download_btn.grid(row=8, column=1, sticky=full, pady=(60, 0))

# ------------------------------------end-inside-frame1--------------------------------


# ########################################-inside-frame1-####################################
information = {
    "Author": [],
    "Category": [],
    "Duration": [],
    "Rating": [],
    "Likes": [],
    "Dislikes": [],
    "Length": [],
    "Username": [],
    "VideoId": [],
    "ViewCount": [],
}


def Insert_Info():
    row = 0
    for info_labels_name, values in information.items():
        info_label = Label(frame2, text=f"{info_labels_name}: ", anchor=W, relief=SUNKEN)
        info_label.grid(row=row * 2, column=0, pady=(3, 0), padx=(3, 3), sticky=(E + W), ipadx=100)
        info = Label(frame2, text="", anchor=E)
        info.grid(row=(row * 2) + 1, column=0, pady=(5, 0))
        row += 1
        values.append(info)


Insert_Info()

# --------------------------------------end-inside-frame2--------------------------------

# ##############################################################################################-inside-frame-3##########################


name_label = Label(frame3, text="Title:", relief=SUNKEN)
name_label.grid(row=0, column=0, ipadx=200)

thumnail_label = Label(frame3, text="Thumbnail")
thumnail_label.grid(row=1, column=0, pady=(20, 0), sticky=W)

thumbnail_image = Label(frame3)
thumbnail_image.grid(row=2, column=0)

title_label = Label(frame3, wraplength=445)
title_label.grid(row=3, column=0, sticky=E + W, pady=(10, 0))


# ---------------------------------------------end-inside-frame-3------------------------------------

# #####################-binding-#######################################################


def Destroy(master):
    Exit = m_box.askyesno("EXIT", "Are you Sure You Want to Exit!")
    if Exit:
        master.destroy()


root.protocol("WM_DELETE_WINDOW", lambda: Destroy(root))
root.bind('<Control-x>', lambda event: root.destroy())
root.bind('<Control-r>', lambda event: Delete())
root.bind("<Return>", lambda event: Show_Info())
c_box1.bind("<<ComboboxSelected>>", lambda event: Audio_video())
c_box3.bind("<<ComboboxSelected>>", lambda event: Change_Qua())
root.mainloop()
