from tkinter import *
from tkinter import Canvas, PhotoImage, ttk,messagebox, filedialog
from tkinter.colorchooser import askcolor
from datetime import datetime
from winsound import Beep
from pyglet import font
from subprocess import check_output
from PIL import Image
from time import sleep
import psutil
import pytz
import os
import backend
import winreg as reg
import webbrowser
import wmi

path_db = "Completed/mahab.db"

backend.connect_user(path_db)
backend.connect_seeting(path_db)

if backend.view_setting(path_db) == []:
    backend.insert_setting(90, 25, "vazir", 15, "no", "#f5f7b2", "red", path_db)

try:
    if backend.view_setting(path_db)[0][4] == "yes":
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER , "Software\Microsoft\Windows\CurrentVersion\Run" ,0 , reg.KEY_ALL_ACCESS) # Open The Key
            reg.SetValueEx(key ,"mahab" , 0 , reg.REG_SZ , "mahab.exe") # Appending Script Address
            reg.CloseKey(key) # Close The Key
        except:
            pass
    elif backend.view_setting(path_db)[0][4] == "no":
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER , "Software\Microsoft\Windows\CurrentVersion\Run" ,0 , reg.KEY_ALL_ACCESS) # Open The Key
            reg.DeleteValue(key, "mahab")
            reg.CloseKey(key)
        except:
            pass
except:
    pass



def find_path(name_file, type_file):
    type = f"{type_file.title()}s"
    path = f"Completed/{type}/{name_file}"
    return path

#فونت ها:
try:
    font.add_file(find_path("Vazir.ttf", "font"))
    font.add_file(find_path("Aban.ttf", "font"))
    font.add_file(find_path("Mitra.ttf", "font"))
    font.add_file(find_path("Titr.ttf", "font"))
    font.add_file(find_path("Yekan.ttf", "font"))
except:
    pass

try:
    font = backend.view_setting(path_db)[0][2]
except:
    font = "vazir"

try:
    max = backend.view_setting(path_db)[0][0]
except:
    max = 90

try:
    min = backend.view_setting(path_db)[0][1]
except:
    min = 25

try:
    start_with_win = backend.view_setting(path_db)[0][4]
except:
    start_with_win = "no"

try:
    bg = backend.view_setting(path_db)[0][5]
except:
    bg = "#f5f7b2"

try:
    fg = backend.view_setting(path_db)[0][6]
except:
    fg="red"

#صفحه پروفایل
def run():
            try:
                mini_page.destroy()
            except:
                pass
            # صفحه اصلی
            profile_Root = Tk()
            profile_Root.title("پروفایل")
            profile_Root.configure(background=bg)
            img = PhotoImage(file=find_path("icon.png", "image"))
            profile_Root.call('wm', 'iconphoto', profile_Root._w, img)
            profile_Root.minsize('710', '448')
            profile_Root.maxsize('710', '448')

            # خط جداکننده
            w = Canvas(profile_Root, width=710, height=488, bd=0, bg=bg, highlightthickness=0)
            w.pack()
            w.create_line(480, 0, 480, 448, fill="red")

            # جداکننده بین پروفایل و عکس
            w.create_line(480, 140, 710, 140, fill="red")

            profile_label = Label(profile_Root,text="پروفایل",font=(font, "15"), bg=bg, fg=fg, width=18)
            profile_label.place(x=490,y=150)

            # جداکننده بین پروفایل و تنظیمات
            w.create_line(480, 219, 710, 219, fill="red")

            setting_label = Label(profile_Root,text="تنظیمات",font=(font, "15"), bg=bg, fg=fg, width=18)
            setting_label.place(x=490,y=230)

            #جداکننده بین تنظیمات و درباره ما
            w.create_line(480, 292, 710, 292, fill="red")

            about_label = Label(profile_Root,text="درباره ما",font=(font, "15"), bg=bg, fg=fg, width=18)
            about_label.place(x=490,y=300)

            #جداکننده بین درباره ما و خروج
            w.create_line(480, 375, 710, 375, fill="red")

            exit_label = Label(profile_Root,text="خروج",font=(font, "15"), bg=bg, fg=fg, width=18)
            exit_label.place(x=490,y=380)

            #عکس پروفایل و نام
            def select_image():
                filename = filedialog.askopenfilename(
                    title='انتخاب تصویر',
                    initialdir='/',
                    filetypes=(('image file', '*.png'),))
                img = Image.open(filename)
                out = img.resize((100,130))
                base_name = os.path.basename(filename)
                out.save(f"Completed/Images/{base_name}")
                first_name = backend.view_user(path_db)[0][0]
                last_name = backend.view_user(path_db)[0][1]
                user_name = backend.view_user(path_db)[0][2]
                password = backend.view_user(path_db)[0][3]
                backend.update_user(first_name, last_name, user_name, password, base_name, "yes", "no", path_db)
                exit = messagebox.showinfo("اعمال تغییرات", "!برای اعمال تغییرات باید برنامه را بسته و دوباره باز کنید\n?ادامه می دهید")
                if exit == "ok":
                    profile_Root.destroy()
            if backend.view_user(path_db)[0][4] == "icon":
                img_p = PhotoImage(file=find_path("icon_p.png", "image"))
            else:
                try:
                    img_p = PhotoImage(file=find_path(backend.view_user(path_db)[0][4], "image"))
                except:
                    img_p = PhotoImage(file=find_path("icon_p.png", "image"))
            img_profile = Button(profile_Root,image=img_p, command=select_image, width=100, height=100, bd=0)
            img_profile.place(x=540,y=0)

            Name = f"{backend.view_user(path_db)[0][0]} {backend.view_user(path_db)[0][1]}"
            Show_name = Label(profile_Root,text=Name,font=(font, "15"), bg=bg, fg=fg, width=18)
            Show_name.place(x=490,y=95)

            #صفحات
            def profile_page():
                # صفحه پروفایل
                profile_Page = Frame(profile_Root, width=480, height=448, bg=bg)
                profile_Page.place(x=0, y=0)

                n_Profile = Label(profile_Page, text="پروفایل", font=(font, "20"), bg=bg, fg=fg, width=10).place(x=180)

                Level_Battry = Label(profile_Page, font=(font, "20"), fg="#F0FAF7", relief="sunken")
                Level_Battry.place(x=100, y=150)

                Title_Battry = Label(profile_Page, text=": میزان شارژ رایانه", font=(font, "20"), bg=bg, fg=fg, width=15)
                Title_Battry.place(x=150,y=150)

                To_final_label = Label(profile_Page, text=" : مانده تا پایان شارژ(ساعت)", font=(font, "20"), bg=bg, fg=fg)
                To_final_label.place(x=150, y=220)

                To_Final = Label(profile_Page, text="", font=(font, "20"), bg="white", fg=fg, relief="sunken")
                To_Final.place(x=95, y=220)

                Clock = Label(profile_Page, font=(font, "17"), bg=bg, fg=fg)
                Clock.place(x=10, y=400)

                    # میزان شارژ
                def level_battry():
                    import psutil
                    battery = psutil.sensors_battery()
                    def convertTime(seconds):
                        minutes, seconds = divmod(seconds, 60)
                        hours, minutes = divmod(minutes, 60)
                        return "%d:%02d:%02d" % (hours, minutes, seconds)

                    Battery_percentage = battery.percent
                    if Battery_percentage <= 30:
                        Level_Battry.config(bg="red")
                    elif Battery_percentage <= 50:
                        Level_Battry.config(bg="orange")
                    elif Battery_percentage <= 70:
                        Level_Battry.config(bg="lightgreen")
                    elif Battery_percentage > 70:
                        Level_Battry.config(bg="green")
                    Level_Battry.config(text=str(Battery_percentage) + "%")
                    if str(battery.secsleft) != "BatteryTime.POWER_TIME_UNLIMITED":
                        to_final = str(convertTime(battery.secsleft))
                        if len(to_final) <= 7:
                            To_Final.config(text=to_final[0:4])
                            To_Final.place(x=95, y=220)
                        elif  len(to_final) == 8:
                            To_Final.config(text=to_final[0:6])
                            To_Final.place(x=85, y=220)
                        else:
                            To_Final.config(text="در حال دریافت")
                            To_Final.place(x=0, y=220)
                    else:
                        To_Final.config(text="در شارژ است")
                        To_Final.place(x=5, y=220)
                    Level_Battry.after(1000, level_battry)

                level_battry()

                # ساعت تهران
                def tick():
                    tz_Tehran = pytz.timezone('Asia/Tehran')
                    datetime_Tehran = datetime.now(tz_Tehran)
                    v = "زمان به وقت تهران:" + datetime_Tehran.strftime("%H:%M:%S")
                    Clock.config(text=v)
                    Clock.after(1000, tick)

                tick()

            profile_page()

            def change_info_page():
                close(None)
                # صفحه تغییر اطلاعات کاربری
                change_info_Page = Frame(profile_Root, width=480, height=448, bg=bg)
                change_info_Page.place(x=0, y=0)

                change_label = Label(change_info_Page, text="تغییر اطلاعات کاربری", font=(font, "20"), bg=bg, fg=fg).place(x=150)

                name_label = Label(change_info_Page, text=": نام شما", font=(font, "17"), bg=bg, fg=fg, width=15).place(x=300, y=100)

                family_label = Label(change_info_Page, text=": نام خانوادگی شما", font=(font, "17"), bg=bg, fg=fg, width=15).place(x=260, y=150)

                username_label = Label(change_info_Page, text=": نام‌ کاربری شما", font=(font, "17"), bg=bg, fg=fg, width=15).place(x=270, y=200)

                password_label = Label(change_info_Page, text=": رمز شما", font=(font, "17"), bg=bg, fg=fg, width=15).place(x=300, y=250)

                name_field = Entry(change_info_Page,justify="right",font=(font, "10"),fg=fg)
                name_field.insert(0, backend.view_user(path_db)[0][0])
                name_field.place(x=220, y=110)

                family_field = Entry(change_info_Page,justify="right",font=(font, "10"),fg=fg)
                family_field.insert(0, backend.view_user(path_db)[0][1])
                family_field.place(x=140, y=155)

                username_field = Entry(change_info_Page,justify="left",font="andalus 10",fg=fg)
                username_field.insert(0, backend.view_user(path_db)[0][2])
                username_field.place(x=160, y=210)

                password_field = Entry(change_info_Page,justify="left",fg=fg, show="*")
                password_field.place(x=215, y=255)

                def message():
                    messagebox.showinfo("دکمه دیدن رمز","!لطفا برای دیدن رمز ماوس خود را روی دکمه قرار دهید")

                see1 = Button(change_info_Page,text="دیدن", font="vazir 7",command=message)
                see1.place(y=255,x=185)

                def see_1(event):
                    password_field.config(show="")

                def dont_see_1(event):
                    password_field.config(show="*")

                see1.bind('<Enter>', see_1)
                see1.bind('<Leave>',dont_see_1)

                def change_info():
                    name = name_field.get()
                    family = family_field.get()
                    username = username_field.get()
                    password = password_field.get()
                    if  not name == "" and not family == "" and not username == "" and not password=="":
                        backend.update_user(name, family, username, password, "icon", "yes", "no", path_db)
                        name = f"{backend.view_user(path_db)[0][0]} {backend.view_user(path_db)[0][1]}"
                        Show_name.config(text=name)
                        profile_page()
                    else:
                        messagebox.showerror("کامل نکردن مشخصات","!شما یکی از قسمت ها را کامل نکرده اید")


                submit_info = Button(change_info_Page, text="ثبت", fg=fg, bg=bg, font=(font, "15"), activebackground="#f5f7b2",activeforeground="blue", command=change_info, width=10)
                submit_info.place(x=150, y=320)

            def battry_setting_page():
                close(None)
                # صفحه تنظیمات باتری
                battry_setting_page = Frame(profile_Root, width=480, height=448, bg=bg)
                battry_setting_page.place(x=0, y=0)

                setting_label = Label(battry_setting_page, text="تنظیمات باتری", font=(font, "20"), bg=bg, fg=fg).place(x=150)

                Power_saver_label = Label(battry_setting_page, text=": میزان مصرف باتری", font=(font, "17"), bg=bg, fg=fg).place(x=250, y=100)

                max_amount_label = Label(battry_setting_page, text=": هشدار برای بیشترین مقدار", font=(font, "17"), bg=bg, fg=fg).place(x=175, y=150)

                min_amount_label = Label(battry_setting_page, text=": هشدار برای کمترین مقدار", font=(font, "17"), bg=bg, fg=fg).place(x=185, y=200)

                start_with_win_label = Label(battry_setting_page, text=":  اجرا شدن همراه با روشن شدن رایانه ", font=(font, "17"), bg=bg, fg=fg).place(x=80, y=250)

                Power_saver = StringVar()
                Power_savers = ttk.Combobox(battry_setting_page, textvariable=Power_saver,
                                    values=("بیشترین مقدار", "مقدار معمولی(پیشفرض)", "کمترین مقدار"),
                                    state='readonly', justify="center", font=(font, "8"))
                Power_savers.place(x=100, y=110)

                max_val = IntVar(value=max)
                max_amount = Spinbox(battry_setting_page, from_=50, to=100, font=(font, "8"), textvariable=max_val)
                max_amount.place(x=30, y=160)

                min_val = IntVar(value=min)
                min_amount = Spinbox(battry_setting_page, from_=5, to=50, font=(font, "8"), textvariable=min_val)
                min_amount.place(x=30, y=210)

                start_with_win_quistion = StringVar(value=backend.view_setting(path_db)[0][4])
                start_with_win_check = Checkbutton(battry_setting_page, variable=start_with_win_quistion, onvalue="yes", offvalue="no", justify="center", bg=bg, fg=fg, )
                start_with_win_check.place(x=50, y=260)
                def change_seetting():
                    power_saver = Power_saver.get()
                    max_select = max_amount.get()
                    min_select = min_amount.get()

                    if power_saver == "بیشترین مقدار":
                        check_output("powercfg -SETACTIVE SCHEME_MIN")
                    elif power_saver == "مقدار معمولی(پیشفرض)":
                        check_output("powercfg -SETACTIVE SCHEME_BALANCED")
                    elif power_saver == "کمترین مقدار":
                        check_output("powercfg -SETACTIVE SCHEME_MAX")


                    if max_select.isnumeric() and min_select.isnumeric():
                        if int(max_select) > 100 or int(max_select) < 50:
                            messagebox.showerror("مقدار اشتباه", "برای بیشترین مقدار ، اندازه اشتباهی وارد کرده اید")
                        elif int(min_select) > 50 or int(min_select) <5:
                            messagebox.showerror("مقدار اشتباه", "برای کمترین مقدار ، اندازه اشتباهی را وارد کرده اید")
                        else:
                            backend.update_setting(max_select, min_select, font, 1, start_with_win_quistion.get(), bg, fg, path_db)
                            exit = messagebox.showinfo("اعمال تغییرات", "!برای اعمال تغییرات باید برنامه را بسته و دوباره باز کنید\n?ادامه می دهید")
                            if exit == "ok":
                                profile_Root.destroy()
                    else:
                        messagebox.showerror("مقدار اشتباه", "مقدار وارد شده شما برای بیشترین مقدار یا کمترین مقدار عدد نیست")




                submit_setting = Button(battry_setting_page, text="ثبت", fg=fg, bg=bg, font=(font, "15"), activebackground=fg,activeforeground="blue", command=change_seetting, width=10)
                submit_setting.place(x=150, y=320)

                def guide_page():
                    file = open(find_path("guide_battry_setting.txt", "text"), encoding="utf-8")
                    text = file.read()
                    guidepage = Tk()
                    guidepage.title("راهنمای صفحه تنظیمات باتری")
                    guidepage.configure(background=bg)
                    Label(guidepage, text=text , justify="center", font=(font, "16"), bg=bg, fg=fg, width=1500).pack()

                    guidepage.mainloop()
                    file.close()

                guide = Button(battry_setting_page, text="?", fg="red", bg="white", font=(font, "10"), activebackground="#f5f7b2",activeforeground="blue", command=guide_page)
                guide.place(x=200, y=400)

            def appr_setting_page():
                close(None)
                appr_setting_page = Frame(profile_Root, width=480, height=448, bg=bg)
                appr_setting_page.place(x=0, y=0)

                setting_label = Label(appr_setting_page, text="تنظیمات ظاهری", font=(font, "20"), bg=bg, fg=fg).place(x=150)

                font_label = Label(appr_setting_page, text=": فونت", font=(font, "17"), bg=bg, fg=fg).place(x=374, y=100)

                bg_label = Label(appr_setting_page, text=": رنگ پس زمینه", font=(font, "17"), bg=bg, fg=fg).place(x=300, y=150)

                fg_label = Label(appr_setting_page, text=": رنگ متون", font=(font, "17"), bg=bg, fg=fg).place(x=345, y=200)

                Font = StringVar()
                Fonts = ttk.Combobox(appr_setting_page, textvariable=Font,
                                    values=("وزیر(پیشفرض)", "آبان", "میترا", "تیتر", "یکان"),
                                    state='readonly', justify="center", font=(font, "8"))
                Fonts.place(x=210, y=110)

                a = Label(text="no", font="a")

                def bg_select_color():
                    bg_color = askcolor(color=bg, title="انتخاب رنگ پس زمنیه")
                    if bg_color == (None, None):
                        bg_color = bg
                        a.config(bg=bg_color, text="yes")
                    else:
                        bg_color = bg_color[1]
                        a.config(bg=bg_color, text="yes")

                bg_button = Button(appr_setting_page, text="انتخاب رنگ", fg=fg, bg=bg, font=(font, "10"), activebackground=bg,activeforeground="blue", command=bg_select_color)
                bg_button.place(x=200, y=160, height=25)

                def fg_select_color():
                    fg_color = askcolor(color=fg, title="انتخاب رنگ متون")
                    if fg_color == (None, None):
                        fg_color = fg
                        a.config(fg=fg_color, font="b")
                    else:
                        fg_color = fg_color[1]
                        a.config(fg=fg_color, font="b")


                fg_button = Button(appr_setting_page, text="انتخاب رنگ", fg=fg, bg=bg, font=(font, "10"), activebackground=bg,activeforeground="blue", command=fg_select_color)
                fg_button.place(x=250, y=210, height=25)

                def change_appr():
                    font_select = Font.get()
                    if font_select != "":
                        if font_select == "وزیر(پیشفرض)":font_select="vazir"
                        if font_select == "آبان":font_select="IRAban"
                        if font_select == "میترا":font_select="B Mitra"
                        if font_select == "تیتر":font_select="B Titr"
                        if font_select == "یکان":font_select="B Yekan"
                        if a["text"] == "yes":
                            bg_color = a["bg"]
                        else:
                            bg_color = bg
                        if a["font"] == "b":
                            fg_color = a["fg"]
                        else:
                            fg_color = fg
                        backend.update_setting(max, min, font_select, 1, "no", bg_color, fg_color, path_db)
                        exit = messagebox.showinfo("اعمال تغییرات", "!برای اعمال تغییرات باید برنامه را بسته و دوباره باز کنید\n?ادامه می دهید")
                        if exit == "ok":
                            profile_Root.destroy()
                    else:
                        messagebox.showerror("فونت", "فونت انتخاب نشده است")

                submit_appr = Button(appr_setting_page, text="ثبت", fg=fg, bg=bg, font=(font, "15"), activebackground=bg,activeforeground="blue", command=change_appr, width=10)
                submit_appr.place(x=150, y=320)

                def guide_appr():
                    messagebox.showinfo("اخطار", "توصیه می شود از فونت و رنگ پیش فرض استفاده نمایید زیرا ممکن است اختلالات ظاهری زیادی به وجود آید")

                guide = Button(appr_setting_page, text="!", fg="red", bg="white", font=(font, "10"), activebackground="#f5f7b2",activeforeground="blue", command=guide_appr)
                guide.place(x=200, y=400)

            def help_app_page_1():
                close(None)
                help_app_page_1 = Frame(profile_Root, width=480, height=448, bg=bg)
                help_app_page_1.place(x=0, y=0)

                help_label = Label(help_app_page_1, text="راهنمای نرم افزار", font=(font, "20"), bg=bg, fg=fg).place(x=150)

                file_help = open(find_path("help_app.txt", "text"), encoding="utf-8")
                texts = file_help.read().split("__________")
                text = texts[0]
                part1 = Label(help_app_page_1, text=text, font=(font, "10"), bg=bg, fg=fg, justify="center").place(y=100, x=10)

                next = Button(help_app_page_1, text="بعدی »", font=(font, "12"), bg=bg, fg=fg, command=help_app_page_2)
                next.place(x=200, y=390)
            def help_app_page_2():
                close(None)
                help_app_page_2 = Frame(profile_Root, width=480, height=448, bg=bg)
                help_app_page_2.place(x=0, y=0)

                help_label = Label(help_app_page_2, text="راهنمای نرم افزار", font=(font, "20"), bg=bg, fg=fg).place(x=150)

                file_help = open(find_path("help_app.txt", "text"), encoding="utf-8")
                texts = file_help.read().split("__________")
                text = texts[1]
                part1 = Label(help_app_page_2, text=text, font=(font, "10"), bg=bg, fg=fg, justify="center").place(y=100, x=10)

                next = Button(help_app_page_2, text="بعدی »", font=(font, "12"), bg=bg, fg=fg, command=help_app_page_3)
                next.place(x=250, y=390)
                previous = Button(help_app_page_2, text="« قبلی", font=(font, "12"), bg=bg, fg=fg, command=help_app_page_1)
                previous.place(x=150, y=390)
            def help_app_page_3():
                close(None)
                help_app_page_3 = Frame(profile_Root, width=480, height=448, bg=bg)
                help_app_page_3.place(x=0, y=0)

                help_label = Label(help_app_page_3, text="راهنمای نرم افزار", font=(font, "20"), bg=bg, fg=fg).place(x=150)

                file_help = open(find_path("help_app.txt", "text"), encoding="utf-8")
                texts = file_help.read().split("__________")
                text = texts[2]
                part1 = Label(help_app_page_3, text=text, font=(font, "10"), bg=bg, fg=fg, justify="center").place(y=100, x=10)

                next = Button(help_app_page_3, text="بعدی »", font=(font, "12"), bg=bg, fg=fg, command=help_app_page_4)
                next.place(x=250, y=390)
                previous = Button(help_app_page_3, text="« قبلی", font=(font, "12"), bg=bg, fg=fg, command=help_app_page_2)
                previous.place(x=150, y=390)
            def help_app_page_4():
                close(None)
                help_app_page_4 = Frame(profile_Root, width=480, height=448, bg=bg)
                help_app_page_4.place(x=0, y=0)

                help_label = Label(help_app_page_4, text="راهنمای نرم افزار", font=(font, "20"), bg=bg, fg=fg).place(x=150)

                file_help = open(find_path("help_app.txt", "text"), encoding="utf-8")
                texts = file_help.read().split("__________")
                text = texts[3]
                part1 = Label(help_app_page_4, text=text, font=(font, "10"), bg=bg, fg=fg, justify="center").place(y=100, x=10)

                next = Button(help_app_page_4, text="بعدی »", font=(font, "12"), bg=bg, fg=fg, command=help_app_page_5)
                next.place(x=250, y=390)
                previous = Button(help_app_page_4, text="« قبلی", font=(font, "12"), bg=bg, fg=fg, command=help_app_page_3)
                previous.place(x=150, y=390)
            def help_app_page_5():
                help_app_page_5 = Frame(profile_Root, width=480, height=448, bg=bg)
                help_app_page_5.place(x=0, y=0)

                help_label = Label(help_app_page_5, text="راهنمای نرم افزار", font=(font, "20"), bg=bg, fg=fg).place(x=150)

                file_help = open(find_path("help_app.txt", "text"), encoding="utf-8")
                texts = file_help.read().split("__________")
                text = texts[4]
                part1 = Label(help_app_page_5, text=text, font=(font, "10"), bg=bg, fg=fg, justify="center").place(y=100, x=10)

                previous = Button(help_app_page_5, text="« قبلی", font=(font, "12"), bg=bg, fg=fg, command=help_app_page_4)
                previous.place(x=200, y=390)

            def about_me_page():
                close(None)
                about_me_page = Frame(profile_Root, width=480, height=448, bg=bg)
                about_me_page.place(x=0, y=0)

                about_label = Label(about_me_page, text="درباره سازنده نرم افزار", font=(font, "20"), bg=bg, fg=fg).place(x=150)

                about_file = open(find_path("about_me.txt", "text"), encoding="utf-8")
                info = about_file.read().split("__________")[0]

                about_text = Label(about_me_page, text=info, font=(font, "12"), bg=bg, fg=fg, justify="center").place(y=60, x=70)

                skill_label = Label(about_me_page, text="مهارت ها", font=(font, "20"), bg=bg, fg=fg).place(x=200, y=120)

                python_skill = Label(about_me_page, text="(Python)پایتون", font=(font, "11"), bg=bg, fg=fg).place(x=320, y=170)
                html_skill = Label(about_me_page, text="HTML", font=(font, "11"), bg=bg, fg=fg).place(x=370, y=200)
                css_skill = Label(about_me_page, text="CSS", font=(font, "11"), bg=bg, fg=fg).place(x=375, y=230)
                bootstrap_skill = Label(about_me_page, text="(Bootstrap)بوت استرپ", font=(font, "11"), bg=bg, fg=fg).place(x=275, y=260)
                django_skill = Label(about_me_page, text="(Django)جنگو", font=(font, "11"), bg=bg, fg=fg).place(x=325, y=290)

                Percent_bar = Label(about_me_page, bg=bg, borderwidth=2, relief="solid", width=25).place(x=90, y=175)
                Percent_bar = Label(about_me_page, bg=bg, borderwidth=2, relief="solid", width=25).place(x=90, y=205)
                Percent_bar = Label(about_me_page, bg=bg, borderwidth=2, relief="solid", width=25).place(x=90, y=235)
                Percent_bar = Label(about_me_page, bg=bg, borderwidth=2, relief="solid", width=25).place(x=90, y=265)
                Percent_bar = Label(about_me_page, bg=bg, borderwidth=2, relief="solid", width=25).place(x=90, y=295)

                Percent_python = Label(about_me_page, bg="lightgreen", width=16, borderwidth=0).place(x=92, y=177)
                Percent_python_labrl = Label(about_me_page,  text="65%", font=(font, 8), justify="center", width=3, bg="black", fg="white", borderwidth=0).place(x=250, y=175)

                Percent_html = Label(about_me_page, bg="red", width=6, borderwidth=0).place(x=92, y=207)
                Percent_html_labrl = Label(about_me_page,  text="25%", font=(font, 8), justify="center", width=3, bg="black", fg="white", borderwidth=0).place(x=250, y=205)

                Percent_css = Label(about_me_page, bg="red", width=4, borderwidth=0).place(x=92, y=237)
                Percent_css_labrl = Label(about_me_page,  text="15%", font=(font, 8), justify="center", width=3, bg="black", fg="white", borderwidth=0).place(x=250, y=235)

                Percent_bootstrap = Label(about_me_page, bg="red", width=3, borderwidth=0).place(x=92, y=267)
                Percent_bootstrap_labrl = Label(about_me_page,  text="10%", font=(font, 8), justify="center", width=3, bg="black", fg="white", borderwidth=0).place(x=250, y=265)

                Percent_django = Label(about_me_page, bg="orange", width=11, borderwidth=0).place(x=92, y=297)
                Percent_django_labrl = Label(about_me_page,  text="45%", font=(font, 8), justify="center", width=3, bg="black", fg="white", borderwidth=0).place(x=250, y=295)

                contect_label = Label(about_me_page, text="راه های ارتباطی", font=(font, "20"), bg=bg, fg=fg).place(x=170, y=320)

                contact_text = Label(about_me_page, text="شماره تماس من : ۰۹۱۵۸۸۸۹۳۵۳\nabolfazlramazani86@gmail.com : آدرس ایمیل من", font=(font, "11"), bg=bg, fg=fg, justify="center").place(y=370, x=70)

            def exit_account_page():
                close(None)
                exit_account_page = Frame(profile_Root, width=480, height=448, bg=bg)
                exit_account_page.place(x=0, y=0)

                exitpage_label = Label(exit_account_page, text="خروج از حساب کاربری", font=(font, "20"), bg=bg, fg=fg).place(x=150)

                def exit():
                    first_name = backend.view_user(path_db)[0][0]
                    last_name = backend.view_user(path_db)[0][1]
                    user_name = backend.view_user(path_db)[0][2]
                    password = backend.view_user(path_db)[0][3]
                    image = backend.view_user(path_db)[0][4]
                    backend.update_user(first_name, last_name, user_name, password, image, "no", "no", path_db)
                    profile_Root.destroy()

                def delete():
                    ok_delete = messagebox.showwarning("حذف اطلاعات", "توجه داشته باشید با حذف حساب تمامی اطلاعات حذف خواهد شد\nادامه می دهید؟")
                    if ok_delete == "ok":
                        backend.delete(path_db)
                        profile_Root.destroy()

                exit_b = Button(exit_account_page, text="خروج از حساب کاربری", font=(font, "15"), bg=bg, fg=fg, command=exit).place(x=180, y=100)
                delete_b = Button(exit_account_page, text="حذف حساب کاربری", font=(font, "15"), bg=bg, fg=fg, command=delete).place(x=185, y=180)

                thanks = Label(exit_account_page, text="ممنون از انتخاب این نرم افزار\nاگر مشکلی در اجرای این نرم افزار داشته اید حتما گزارش دهید", font=(font, "12"), bg=bg, fg=fg, justify="center").place(x=50, y=300)
            #عمل دکمه های سمت راست
            #دکمه پروفایل
            def open_profile(event):
                global option_profile
                option_profile = Frame(profile_Root, width=50, height=100)
                option_profile.place(x=365, y=115)
                profile_root = Button(option_profile,text="پروفایل", width=15, height=2, font=(font, "10"), command=profile_page)
                profile_root.pack()
                change_info = Button(option_profile,text="تغییر اطلاعات کاربری", width=15, height=2, font=(font, "10"), command=change_info_page)
                change_info.pack()

            profile_label.bind("<ButtonPress-1>", open_profile)

            #دکمه تنظیمات
            def open_setting(event):
                global option_setting
                option_setting = Frame(profile_Root, width=50, height=100)
                option_setting.place(x=365, y=205)
                battry_seeting = Button(option_setting,text="تنظیمات باتری", width=15, height=2, font=(font, "10"), command=battry_setting_page)
                battry_seeting.pack()
                appr_setting = Button(option_setting,text="تنظیمات ظاهری", width=15, height=2, font=(font, "10"), command=appr_setting_page)
                appr_setting.pack()

            setting_label.bind("<ButtonPress-1>", open_setting)

            #دکمه درباره ما
            def open_about(event):
                global option_about
                option_about = Frame(profile_Root, width=50, height=100)
                option_about.place(x=365, y=265)
                app_guide = Button(option_about,text="راهنمای نرم افزار", width=15, height=2, font=(font, "10"), command=help_app_page_1)
                app_guide.pack()
                about_me = Button(option_about,text="درباره سازنده", width=15, height=2, font=(font, "10"), command=about_me_page)
                about_me.pack()

            about_label.bind("<ButtonPress-1>", open_about)

            #دکمه خروج
            def open_exit(event):
                global option_exit
                option_exit = Frame(profile_Root, width=50, height=100)
                option_exit.place(x=360, y=360)
                exit_user = Button(option_exit,text="خروج از حساب کاربری", width=16, height=1, font=(font, "10"), command=exit_account_page)
                exit_user.pack()
                exit_app = Button(option_exit,text="خروج از نرم افزار", width=16, height=1, font=(font, "10"), command=profile_Root.destroy)
                exit_app.pack()


            exit_label.bind("<ButtonPress-1>", open_exit)

            #تابع بستن گزینه ها
            def close(event):
                try :
                    option_profile.destroy()
                except:
                    pass

                try :
                    option_setting.destroy()
                except:
                    pass

                try :
                    option_about.destroy()
                except:
                    pass

                try:
                    option_exit.destroy()
                except:
                    pass

            profile_Root.bind("<Double-Button-1>", close)

            profile_Root.mainloop()

# آیا ثبت نام کرده؟
if backend.view_user(path_db) == []:
    # پنجره اصلی

    start = Tk()

    #صفحه ثبت نام

    def sign_in_page():
        start.destroy()
        #صفحه ثبت نام
        signin_page = Tk()


        signin_page.geometry("500x500")
        signin_page.title("ثبت نام")
        signin_page.configure(background="#f5f7b2")
        img = PhotoImage(file=find_path("icon.png", "image"))
        signin_page.call('wm', 'iconphoto', signin_page._w, img)
        signin_page.minsize('500','500')
        signin_page.maxsize('500','500')

        see = PhotoImage(file=find_path("see.png", "image"))
        icon_signin = PhotoImage(file=find_path("sign_in.png", "image"))

        icon_inpage = Label(signin_page,image=icon_signin).pack()

        Name = Label(signin_page,text=":نام",bg="#f5f7b2",font="vazir 20")
        Name.place(width=50,x=450,y=100)

        Family = Label(signin_page,text=":نام خانوادگی",bg="#f5f7b2",font="vazir 20")
        Family.place(width=500,x=175,y=150)

        userName = Label(signin_page,text=":نام کاربری(حروف انگلیسی)",bg="#f5f7b2",font="vazir 20")
        userName.place(width=500,x=95,y=200)

        Password = Label(signin_page,text=":رمز(حروف انگلیسی + اعداد)",bg="#f5f7b2",font="vazir 20").place(width=500,x=90,y=250)

        Password_egain = Label(signin_page,text=":تکرار رمز",bg="#f5f7b2",font="vazir 20").place(width=500,x=190,y=300)

        Name_cadr = Entry(signin_page,justify="right",font="vazir 10",fg="red")
        Name_cadr.place(width=150,y=110,x=300)

        Family_cadr = Entry(signin_page,justify="right",font="vazir 10",fg="red")
        Family_cadr.place(width=150,y=160,x=200)

        userName_cadr = Entry(signin_page,justify="left",font="andalus 10",fg="red")
        userName_cadr.place(width=150,y=210,x=40)

        Password_cadr = Entry(signin_page,justify="left",font="10",fg="red",show="*")
        Password_cadr.place(width=150,y=260,x=35)

        Error = Label(signin_page,text="حساس به حروف بزرگ و کوچک",bg="#f5f7b2",font="vazir 10",fg="red").place(width=200,y=290,x=10)

        def see_1(event):
            Password_cadr.config(show="")

        def dont_see_1(event):
            Password_cadr.config(show="*")

        Password_egain_cadr = Entry(signin_page,justify="left",font="10",fg="red",show="*")
        Password_egain_cadr.place(width=150,y=310,x=235)

        def see_2(event):
            Password_egain_cadr.config(show="")

        def dont_see_2(event):
            Password_egain_cadr.config(show="*")

        def message():
            messagebox.showinfo("دکمه دیدن رمز","!لطفا برای دیدن رمز ماوس خود را روی دکمه قرار دهید")

        def register():
            name = Name_cadr.get()
            family = Family_cadr.get()
            UserName = userName_cadr.get()
            password = Password_cadr.get()
            if Password_cadr.get() == Password_egain_cadr.get() and not name == "" and not family == "" and not UserName == "" and not password=="":
                signin_page.destroy()
                backend.insert_user(str(name), str(family), str(UserName), str(password), "icon", "yes", "no", path_db)
                run()
            elif not Password_cadr.get() == Password_egain_cadr.get():
                messagebox.showerror("تکرار رمز","!تکرار رمز با خود رمز یکسان نیست")
            if len(name) == 0 or len(family) == 0 or len(UserName) == 0 or len(password)==0:
                messagebox.showerror("کامل نکردن مشخصات","!شما یکی از قسمت ها را کامل نکرده اید")
        Regester = Button(signin_page,text="ثبت",fg="red",bg="#f5f7b2",activebackground="#f5f7b2",activeforeground="blue",font="vazir 15 bold",width=10,command=register).pack(side='bottom',pady=20)

        see1 = Button(signin_page,image=see,command=message)
        see1.place(y=260,x=0)
        see2 = Button(signin_page,image=see,command=message)
        see2.place(y=310,x=200)

        see1.bind('<Enter>', see_1)
        see1.bind('<Leave>',dont_see_1)

        see2.bind('<Enter>', see_2)
        see2.bind('<Leave>', dont_see_2)

        signin_page.mainloop()




    start.geometry("500x500")
    start.title("محافظ باتری محاب")
    start.configure(background="#f5f7b2")
    img = PhotoImage(file=find_path("icon.png", "image"))
    start.call('wm', 'iconphoto', start._w, img)
    start.minsize('500', '500')
    start.maxsize('500', '500')

    icon = PhotoImage(file=find_path("icon.png", "image"))

    icontext = Label(start, image=icon).pack()

    Hi = Label(start, text="! سلام \nبه نرم افزار محافظ باتری خوش آمدید", fg="red", bg="#f5f7b2",
               font="vazir 16").pack()

    Go = Button(start, text="شروع", fg="red", bg="#f5f7b2", font="vazir 15 bold", activebackground="#f5f7b2",
                activeforeground="blue", command=sign_in_page)
    Go.pack(side="bottom", pady=20)


    def enter(event):
        Go.config(text='ثبت نام')


    def leave(event):
        Go.config(text='شروع')


    Go.bind('<Enter>', enter)

    Go.bind('<Leave>', leave)

    start.mainloop()
elif backend.view_user(path_db)[0][5] == "no":
    #صفحه ثبت نام
    signin_page = Tk()


    signin_page.geometry("500x500")
    signin_page.title("ورود")
    signin_page.configure(background="#f5f7b2")
    img = PhotoImage(file=find_path("icon.png", "image"))
    signin_page.call('wm', 'iconphoto', signin_page._w, img)
    signin_page.minsize('500','500')
    signin_page.maxsize('500','500')

    see = PhotoImage(file=find_path("see.png", "image"))
    icon_signin = PhotoImage(file=find_path("login.png", "image"))

    icon_inpage = Label(signin_page,image=icon_signin).pack()

    userName = Label(signin_page,text=":نام کاربری(حروف انگلیسی)",bg="#f5f7b2",font="vazir 20")
    userName.place(width=500,x=95,y=100)

    Password = Label(signin_page,text=":رمز(حروف انگلیسی + اعداد)",bg="#f5f7b2",font="vazir 20").place(width=500,x=90,y=150)

    Password_egain = Label(signin_page,text=":تکرار رمز",bg="#f5f7b2",font="vazir 20").place(width=500,x=190,y=200)

    userName_cadr = Entry(signin_page,justify="left",font="andalus 10",fg="red")
    userName_cadr.place(width=150,y=110,x=40)

    Password_cadr = Entry(signin_page,justify="left",font="10",fg="red",show="*")
    Password_cadr.place(width=150,y=160,x=35)

    Error = Label(signin_page,text="حساس به حروف بزرگ و کوچک",bg="#f5f7b2",font="vazir 10",fg="red").place(width=200,y=190,x=10)

    def see_1(event):
        Password_cadr.config(show="")

    def dont_see_1(event):
        Password_cadr.config(show="*")

    Password_egain_cadr = Entry(signin_page,justify="left",font="10",fg="red",show="*")
    Password_egain_cadr.place(width=150,y=215,x=230)

    def see_2(event):
        Password_egain_cadr.config(show="")

    def dont_see_2(event):
        Password_egain_cadr.config(show="*")

    def message():
        messagebox.showinfo("دکمه دیدن رمز","!لطفا برای دیدن رمز ماوس خود را روی دکمه قرار دهید")

    def register():
        UserName = userName_cadr.get()
        password = Password_cadr.get()
        if Password_cadr.get() == Password_egain_cadr.get() and not UserName == "" and not password=="":
            if backend.view_user(path_db)[0][2] == UserName and backend.view_user(path_db)[0][3] == password:
                signin_page.destroy()
                run()
            else:
                messagebox.showerror("کاربر","!کاربری با این اطلاعات یافت نشد")
        elif not Password_cadr.get() == Password_egain_cadr.get():
            messagebox.showerror("تکرار رمز","!تکرار رمز با خود رمز یکسان نیست")
        if len(UserName) == 0 or len(password)==0:
            messagebox.showerror("کامل نکردن مشخصات","!شما یکی از قسمت ها را کامل نکرده اید")
    Regester = Button(signin_page,text="ورود",fg="red",bg="#f5f7b2",activebackground="#f5f7b2",activeforeground="blue",font="vazir 15 bold",width=10,command=register).pack(side='bottom',pady=20)
    def delete():
        ok_delete = messagebox.showwarning("حذف اطلاعات", "توجه داشته باشید با حذف حساب تمامی اطلاعات حذف خواهد شد\nادامه می دهید؟")
        if ok_delete == "ok":
            backend.delete(path_db)
            signin_page.destroy()
    delete = Button(signin_page,text="حذف حساب کاربری",fg="red",bg="#f5f7b2",activebackground="#f5f7b2",activeforeground="blue",font="vazir 15 bold",width=14,command=delete).pack(side='bottom')

    see1 = Button(signin_page,image=see,command=message)
    see1.place(y=160,x=0)
    see2 = Button(signin_page,image=see,command=message)
    see2.place(y=210,x=200)

    see1.bind('<Enter>', see_1)
    see1.bind('<Leave>',dont_see_1)

    see2.bind('<Enter>', see_2)
    see2.bind('<Leave>', dont_see_2)

    signin_page.mainloop()
elif backend.view_user(path_db)[0][5] == "yes" and backend.view_setting(path_db)[0][4] == "no":
    run()
elif backend.view_user(path_db)[0][5] == "yes" and backend.view_setting(path_db)[0][4] == "yes":
    def get_time():
        tz_Tehran = pytz.timezone('Asia/Tehran')
        datetime_Tehran = datetime.now(tz_Tehran)
        clock = datetime_Tehran.strftime("%H:%M:%S")
        hour = int(datetime_Tehran.strftime("%H")) * 60
        seconds = int(datetime_Tehran.strftime("%S")) / 60
        minutes = int(datetime_Tehran.strftime("%M"))
        minutes = hour + seconds + minutes
        return clock, minutes


    def get_battery():
        battery = psutil.sensors_battery()
        Battery_percentage = battery.percent
        return Battery_percentage

    def power_plugged():
        battery = psutil.sensors_battery()
        result = battery.power_plugged
        return result



    def make_html_max(battery_start, time_start, battery_now, time_now, minutes_start, minutes_now):
        file = open(find_path("main_html_max.txt", "text"), "r",encoding="utf-8")
        text = file.read()
        text2 = ""
        for i in text:
            if i == "}":
                i = backend.view_user(path_db)[0][2]
            elif i == "{":
                i = max
            elif i == "[":
                i = str(battery_start)
            elif i == "]":
                i = time_start
            elif i == ",":
                i = str(battery_now)
            elif i == "؛":
                i = time_now
            elif i == "،":
                battery_add = battery_now - battery_start
                in_time = minutes_now - minutes_start
                avg = battery_add / in_time
                i = str(avg)
            text2 += str(i)
        file.close()
        file = open("max.html", "w",encoding="utf-8")
        file.write(text2)
        file.close()
        webbrowser.open(f"file://{os.getcwd()}/max.html")



    def make_html_min(battery_start, time_start, battery_now, time_now, minutes_start, minutes_now):
        file = open(find_path("main_html_min.txt", "text"), "r",encoding="utf-8")
        text = file.read()
        text2 = ""
        for i in text:
            if i == "}":
                i = backend.view_user(path_db)[0][2]
            elif i == "{":
                i = min
            elif i == "[":
                i = str(battery_start)
            elif i == "]":
                i = time_start
            elif i == ",":
                i = str(battery_now)
            elif i == "؛":
                i = time_now
            elif i == "،":
                battery_sub = battery_now - battery_start
                in_time = minutes_start - minutes_now
                avg = battery_sub / in_time
                i = str(avg)
            text2 += str(i)
        file.close()
        file = open("min.html", "w+",encoding="utf-8")
        file.write(text2)
        file.close()
        webbrowser.open(f"file://{os.getcwd()}/min.html")


    def start_work():
        messagebox.showinfo("شروع", "کار آغاز شد\nمی توانید با خیال آسوده از رایانه خود استفاده کنید")
        try:
            mini_page.destroy()
        except:
            pass
        beeb_max = False
        beeb_min = False
        is_first_max = True
        is_first_min = True
        while True:
            battery = psutil.sensors_battery()
            Battery_percentage = battery.percent
            is_plugged = power_plugged()
            if is_plugged is True:
                if is_first_max is True:
                    time_start,minutes_start = get_time()
                    battery_start = get_battery()
                    is_first_max = False
                    is_first_min = True
                    beeb_max = False
                    beeb_min = False
                if Battery_percentage >= max and beeb_max is False:
                    for i in range(1, 4):
                        Beep(1000, 500)
                    make_html_max(battery_start, time_start, get_battery(), get_time()[0], minutes_start, get_time()[1])
                    beeb_max = True
                    beeb_min = False
                    sleep(5)


            if is_plugged is False:
                if is_first_min is True:
                    time_start,minutes_start = get_time()
                    battery_start = get_battery()
                    is_first_max = True
                    is_first_min = False
                    beeb_max = False
                    beeb_min = False
                if Battery_percentage <= min and beeb_min is False:
                    for i in range(1, 4):
                        Beep(1000, 500)
                    make_html_min(battery_start, time_start, get_battery(), get_time()[0], minutes_start, get_time()[1])
                    beeb_max = False
                    beeb_min = True
                    sleep(5)
            sleep(5)


    mini_page = Tk()
    mini_page.title("صفحه اولیه")
    mini_page.configure(background=bg)
    img = PhotoImage(file=find_path("icon.png", "image"))
    mini_page.call('wm', 'iconphoto', mini_page._w, img)
    mini_page.minsize('300', '150')
    mini_page.maxsize('300', '150')

    battry_label = Label(mini_page, text=":میزان شارژ", bg=bg, fg=fg, font=(font, "15")).pack()

    battry = Label(mini_page, text="", bg=bg, fg=fg, font=(font, "15"))
    battry.pack()

    Clock = Label(mini_page, text="", bg=bg, fg=fg, font=(font, "10"))
    Clock.pack()

    def get_battery1():
        battery = psutil.sensors_battery()
        Battery_percentage = battery.percent
        text = f"{Battery_percentage}%"
        battry.config(text=text)
        battry.after(5, get_battery1)

    get_battery1()

    def tick():
        tz_Tehran = pytz.timezone('Asia/Tehran')
        datetime_Tehran = datetime.now(tz_Tehran)
        v = "زمان به وقت تهران:" + datetime_Tehran.strftime("%H:%M:%S")
        Clock.config(text=v)
        Clock.after(1, tick)

    tick()

    def running_status():
        f = wmi.WMI()
        count = 0
        for process in f.Win32_Process():
            if process.Name == "mahab.exe":
                count += 1

        if count >= 2:
            messagebox.showinfo("وضعیت اجرا", "برنامه در حال اجراست\nنیاز به اجرای دوباره نمی باشد")
        else:
            messagebox.showinfo("وضعیت اجرا", "برنامه در حال اجرا نیست\nبرای اجرا، روی آغاز کار کلیک کنید")

    go_to_profile = Button(mini_page, text="رفتن به پروفایل", bg=bg, fg=fg, font=(font, "10"), command=run)
    go_to_profile.place(x=200, y=120)

    start = Button(mini_page, text="آغاز کار", bg=bg, fg=fg, font=(font, "10"), command=start_work)
    start.place(x=120, y=120)

    run_status = Button(mini_page, text="وضعیت اجرا", bg=bg, fg=fg, font=(font, "10"), command=running_status)
    run_status.place(x=5, y=120)

    mini_page.mainloop()
