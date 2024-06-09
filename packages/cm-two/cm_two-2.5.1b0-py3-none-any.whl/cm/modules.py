import time
import tkinter.filedialog
import traceback
import re
import uuid
from cm.terminal import Terminal
from tkinter import *
from gtki_module_treeview.main import CurrentTreeview, NotificationTreeview, \
    HistroryTreeview, KPPTreeview
from cm.widgets.dropDownCalendar import MyDateEntry
from cm.widgets.drop_down_combobox import AutocompleteCombobox, \
    AutocompleteComboboxCarNumber
from cm.widgets.password_entry import PasswordEntry
import datetime
from cm.styles import color_solutions as cs
from cm.styles import fonts
from cm.styles import element_sizes as el_sizes
from gtki_module_exex.main import CreateExcelActs
import threading
from PIL import ImageFilter, Image, ImageTk


class Statistic(Terminal):
    """ Окно статистики """

    def __init__(self, root, settings, operator, can):
        super(Statistic, self).__init__(root, settings, operator, can)
        self.btns_height = self.h / 4.99
        self.records_amount = 0
        self.uncount_records = []
        self.name = 'Statistic'
        self.buttons = settings.statBtns
        # self.font = '"Montserrat SemiBold" 14'
        self.history = {}
        self.chosenType = ''
        self.chosenContragent = ''
        self.choosenCat = ''
        self.typePopup = ...
        self.carnums = []
        self.filterColNA = '#2F8989'
        self.filterColA = '#44C8C8'
        self.tree = self.create_tree()
        self.posOptionMenus()
        self.calendarsDrawn = False
        self.btn_name = self.settings.statisticBtn
        self.weight_sum = 0
        self.changed_record = None
        self.page_buttons = self.create_btns_and_hide(self.buttons)

    def create_tree(self):
        self.tar = HistroryTreeview(self.root, self.operator, height=28)
        self.tar.createTree()
        self.tree = self.tar.get_tree()
        self.tree.bind("<Double-Button-1>", self.OnDoubleClick)
        return self.tree

    def rebind_btns_after_orup_close(self):
        self.tree.bind("<Double-Button-1>", self.OnDoubleClick)

    def excel_creator(self):
        file_name = self.get_excel_file_path()
        data_list = self.generate_excel_content()
        self.form_excel(file_name, data_list)

    def generate_excel_content(self):
        items = self.tree.get_children()
        data_list = []
        for item in items:
            record_id = self.tree.item(item, 'text')
            data = self.tree.item(item, 'values')
            data = list(data)
            data.insert(0, record_id)
            data_list.append(data)
        return data_list

    def get_excel_file_path(self):
        name = tkinter.filedialog.asksaveasfilename(defaultextension='.xlsx',
                                                    filetypes=[("Excel files",
                                                                "*.xls *.xlsx")])
        return name

    def form_excel(self, file_name, data_list):
        inst = CreateExcelActs(file_name, data_list, self.amount_weight)
        inst.create_document()

    def OnDoubleClick(self, event):
        ''' Реакция на дабл-клик по заезду '''
        item = self.tree.selection()[0]
        self.chosenStr = self.tree.item(item, "values")
        self.record_id = self.tree.selection()[0]
        self.draw_change_records(self.chosenStr, item)

    def draw_change_records(self, string, record_id):
        self.parsed_string = self.parse_string(string)
        self.orupState = True
        btnsname = 'record_change_btns'
        record_info = self.history[int(record_id)]
        self.initBlockImg('record_change_win', btnsname=btnsname,
                          hide_widgets=self.statisticInteractiveWidgets)
        self.posEntrys(
            carnum=self.parsed_string["car_number"],
            trashtype=self.parsed_string["trash_type"],
            trashcat=self.parsed_string["trash_cat"],
            contragent=self.parsed_string["carrier"],
            client=self.parsed_string['client'],
            notes=self.parsed_string['notes'],
            polygon=self.operator.get_polygon_platform_repr(record_info['id']),
            object=self.operator.get_pol_object_repr(record_info['object_id']),
            spec_protocols=False,
            call_method='manual',
        )
        self.root.bind('<Return>', lambda event: self.change_record())
        self.root.bind('<Escape>',
                       lambda event: self.destroyORUP(mode="decline"))
        self.root.bind("<Double-Button-1>",
                       lambda event: self.clear_optionmenu(event))
        self.unbindArrows()

    def mark_changed_rec(self):
        if not self.changed_record:
            return
        try:
            self.tree.selection_set(self.changed_record)
            self.tree.see(self.changed_record)
        except:
            print(traceback.format_exc())
            pass

    def destroyORUP(self, mode=None):
        super().destroyORUP(mode)

    def parse_string(self, string):
        # Парсит выбранную строку из окна статистики и возвращает словарь с элементами
        parsed = {}
        parsed["car_number"] = string[0]
        parsed["carrier"] = string[2]
        parsed["trash_cat"] = string[6]
        parsed["trash_type"] = string[7]
        parsed["notes"] = string[10]
        parsed['client'] = string[1]
        return parsed

    def change_record(self):
        self.changed_record = self.tree.selection()
        info = self.get_orup_entry_reprs()
        self.try_upd_record(info['carnum'], info['carrier'], info['trash_cat'],
                            info['trash_type'], info['comm'],
                            info['polygon_platform'], info['client'],
                            info['polygon_object'])

    def try_upd_record(self, car_number, carrier, trash_cat, trash_type,
                       comment, polygon, client, pol_object):
        self.car_protocol = self.operator.fetch_car_protocol(car_number)
        data_dict = {}
        data_dict['car_number'] = car_number
        data_dict['chosen_trash_cat'] = trash_cat
        data_dict['type_name'] = trash_type
        data_dict['carrier_name'] = carrier
        data_dict['client_name'] = client
        data_dict['sqlshell'] = object
        data_dict['photo_object'] = self.settings.redbg[3]
        data_dict['client'] = client
        data_dict['comment'] = comment
        data_dict['platform_name'] = self.platform_choose_var.get()
        data_dict['object_name'] = self.objectOm.get()
        response = self.operator.orup_error_manager.check_orup_errors(
            orup='brutto',
            xpos=self.settings.redbg[1],
            ypos=self.settings.redbg[2],
            **data_dict)
        if not response:
            auto_id = self.operator.get_auto_id(car_number)
            carrier_id = self.operator.get_client_id(carrier)
            trash_cat_id = self.operator.get_trash_cat_id(trash_cat)
            trash_type_id = self.operator.get_trash_type_id(trash_type)
            polygon_id = self.operator.get_polygon_platform_id(polygon)
            client_id = self.operator.get_client_id(client)
            pol_object_id = self.operator.get_polygon_object_id(pol_object)
            self.operator.ar_qdk.change_opened_record(record_id=self.record_id,
                                                      auto_id=auto_id,
                                                      carrier=carrier_id,
                                                      trash_cat_id=trash_cat_id,
                                                      trash_type_id=trash_type_id,
                                                      comment=comment,
                                                      car_number=car_number,
                                                      polygon=polygon_id,
                                                      client=client_id,
                                                      pol_object=pol_object_id)
            self.destroyORUP()
            self.upd_statistic_tree()

    def upd_statistic_tree(self):
        """ Обновить таблицу статистики """
        self.get_history()
        self.draw_stat_tree()

    def draw_add_comm(self):
        btnsname = 'addCommBtns'
        self.add_comm_text = self.getText(h=5, w=42, bg=cs.orup_bg_color)
        self.initBlockImg(name='addComm', btnsname=btnsname,
                          seconds=('second'),
                          hide_widgets=self.statisticInteractiveWidgets)
        self.can.create_window(self.w / 2, self.h / 2.05,
                               window=self.add_comm_text, tag='blockimg')
        self.root.bind('<Return>', lambda event: self.add_comm())
        self.root.bind('<Escape>',
                       lambda event: self.destroyBlockImg(mode="total"))

    def add_comm(self):
        comment = self.add_comm_text.get("1.0", 'end-1c')
        self.operator.ar_qdk.add_comment(record_id=self.record_id,
                                         comment=comment)
        self.destroyBlockImg()
        self.upd_statistic_tree()

    def posOptionMenus(self):
        self.placeTypeOm()
        self.placeCatOm(bg=self.filterColNA)
        self.placeContragentCombo()
        self.placePoligonOm()
        self.placeObjectOm()
        self.placeCarnumCombo()
        self.placeClientsOm()
        self.statisticInteractiveWidgets = [self.stat_page_polygon_combobox,
                                            self.trashTypeOm, self.trashCatOm,
                                            self.carriers_stat_om,
                                            self.stat_page_carnum_cb,
                                            self.clientsOm,
                                            self.stat_page_pol_object_combobox]
        self.hide_widgets(self.statisticInteractiveWidgets)

    def abortFiltres(self):
        """ Сбросить все фильтры на значения по умолчанию
        """
        for combobox in self.statisticInteractiveWidgets:
            if isinstance(combobox, AutocompleteCombobox):
                combobox.set_default_value()
        self.startCal.set_date(datetime.datetime.today())
        self.endCal.set_date(datetime.datetime.today())
        self.upd_statistic_tree()
        self.changed_record = None

    def placePoligonOm(self):
        listname = ['площадка'] + self.operator.get_polygon_platforms_reprs()
        self.poligonVar = StringVar()
        self.stat_page_polygon_combobox = AutocompleteCombobox(self.root,
                                                               textvariable=self.poligonVar,
                                                               default_value=
                                                               listname[0])
        self.configure_combobox(self.stat_page_polygon_combobox)
        self.stat_page_polygon_combobox.set_completion_list(listname)
        self.stat_page_polygon_combobox.config(width=8, height=30,
                                               font=fonts.statistic_filtres)
        self.can.create_window(self.w / 2.475 - 100, self.btns_height,
                               window=self.stat_page_polygon_combobox,
                               tags=('filter', 'typeCombobox'))

    def placeObjectOm(self):
        listname = ['объект'] + self.operator.get_pol_objects_reprs()
        self.pol_object_var = StringVar()
        self.stat_page_pol_object_combobox = AutocompleteCombobox(self.root,
                                                                  textvariable=self.pol_object_var,
                                                                  default_value=
                                                                  listname[0])
        self.configure_combobox(self.stat_page_pol_object_combobox)
        self.stat_page_pol_object_combobox.set_completion_list(listname)
        self.stat_page_pol_object_combobox.config(width=16, height=36,
                                                  font=fonts.statistic_filtres)
        self.can.create_window(self.w / 1.91 - 30, self.h / 3.85,
                               window=self.stat_page_pol_object_combobox,
                               tags=('filter', 'typeCombobox'))

    def placeTypeOm(self):
        listname = ['вид груза'] + self.operator.get_trash_types_reprs()
        self.stat_page_trash_type_var = StringVar()
        self.trashTypeOm = AutocompleteCombobox(self.root,
                                                textvariable=self.stat_page_trash_type_var,
                                                default_value=listname[0])
        self.configure_combobox(self.trashTypeOm)
        self.trashTypeOm.set_completion_list(listname)
        self.trashTypeOm.config(width=9, height=30,
                                font=fonts.statistic_filtres)
        self.can.create_window(self.w / 3.435 - 40, self.btns_height,
                               window=self.trashTypeOm,
                               tags=('filter', 'typeCombobox'))

    def placeCatOm(self, bg, deffvalue='кат. груза'):
        listname = ['кат. груза'] + self.operator.get_trash_cats_reprs()
        self.stat_page_trash_cat_var = StringVar()
        self.trashCatOm = AutocompleteCombobox(self.root,
                                               textvariable=self.stat_page_trash_cat_var,
                                               default_value=listname[0])
        self.trashCatOm.set_completion_list(listname)
        self.trashCatOm.config(width=9, height=30,
                               font=fonts.statistic_filtres)
        self.can.create_window(self.w / 5.45, self.btns_height,
                               window=self.trashCatOm,
                               tags=('filter', 'catOm'))
        self.configure_combobox(self.trashCatOm)

    def placeClientsOm(self):
        # listname = ['клиенты'] + self.operator.get_clients_reprs()
        self.stat_page_clients_var = StringVar()
        self.clientsOm = AutocompleteCombobox(self.root,
                                              textvariable=self.stat_page_clients_var,
                                              default_value='Клиенты')
        self.configure_combobox(self.clientsOm)
        self.full_clients()
        self.clientsOm['style'] = 'orup.TCombobox'
        # self.clientsOm.set_completion_list(listname)
        self.clientsOm.config(width=23, height=int(self.h / 40),
                              font=fonts.statistic_filtres)
        self.can.create_window(self.w / 1.278 - 60, self.btns_height,
                               window=self.clientsOm,
                               tags=('filter', 'typeCombobox'))

    def full_clients(self):
        self.clientsOm.set_completion_list(self.operator.get_clients_reprs())

    def full_carriers(self):
        self.carriers_stat_om.set_completion_list(
            self.operator.get_clients_reprs())

    def placeContragentCombo(self):
        # carriers = ['перевозчики'] + self.operator.get_clients_reprs()
        self.stat_page_carrier_var = StringVar()
        self.carriers_stat_om = AutocompleteCombobox(self.root,
                                                     textvariable=self.stat_page_carrier_var,
                                                     default_value='Перевозчики')
        self.configure_combobox(self.carriers_stat_om)
        self.full_carriers()
        self.carriers_stat_om.config(width=25, height=int(self.h / 40),
                                     font=fonts.statistic_filtres)
        self.can.create_window(self.w / 1.91 - 70, self.btns_height,
                               window=self.carriers_stat_om,
                               tags=('filter', 'stat_page_carrier_var'))

    def placeCarnumCombo(self):
        listname = ['гос.номер'] + self.operator.get_auto_reprs()
        self.stat_page_carnum_cb = AutocompleteComboboxCarNumber(self.root,
                                                                 default_value=
                                                                 listname[
                                                                     0])
        self.stat_page_carnum_cb.set_completion_list(listname)
        self.configure_combobox(self.stat_page_carnum_cb)
        self.stat_page_carnum_cb.config(width=11, height=20,
                                        font=fonts.statistic_filtres)
        self.can.create_window(self.w / 1.53 - 50, self.btns_height,
                               window=self.stat_page_carnum_cb,
                               tags=('stat_page_carnum_cb', 'filter'))

    def place_amount_info(self, weight, amount, tag='amount_weight'):
        """ Разместить итоговую информацию (количество взвешиваний (amount), тоннаж (weigh) )"""
        if self.operator.current == 'Statistic' and self.blockImgDrawn == False:
            self.can.delete(tag)
            weight = self.formatWeight(weight)
            self.amount_weight = 'ИТОГО: {} ({} взвешиваний)'.format(weight,
                                                                     amount)
            self.can.create_text(self.w / 2, self.h / 1.113,
                                 text=self.amount_weight,
                                 font=fonts.general_text_font,
                                 tags=(tag, 'statusel'),
                                 fill=self.textcolor, anchor='s',
                                 justify='center')

    def place_uncount_records(self, uncount_records, ):
        self.can.delete('amount_weight')
        uncount_records.sort()
        if uncount_records:
            amount_weight_nc = f'\nНекоторые акты {tuple(uncount_records)} ' \
                               f'были отменены.\n'
            self.can.create_text(self.w / 2, self.h / 1.062,
                                 text=amount_weight_nc,
                                 font=self.font,
                                 tags=('amount_weight', 'statusel'),
                                 fill=self.textcolor, anchor='s',
                                 justify='center')

    def formatWeight(self, weight):
        weight = str(weight)
        if len(weight) < 4:
            ed = 'кг'
        else:
            weight = int(weight) / 1000
            ed = 'тонн'
        return f"{weight} {ed}"

    def placeText(self, text, xpos, ypos, tag='maincanv', color='black',
                  font='deff', anchor='center'):
        if font == 'deff': font = self.font
        xpos = int(xpos)
        ypos = int(ypos)
        self.can.create_text(xpos, ypos, text=text, font=self.font, tag=tag,
                             fill=color, anchor=anchor)

    def placeCalendars(self):
        self.startCal = MyDateEntry(self.root, date_pattern='dd/mm/yy')
        self.startCal.config(width=7, font=fonts.statistic_calendars)
        self.endCal = MyDateEntry(self.root, date_pattern='dd/mm/yy')
        self.endCal.config(width=7, font=fonts.statistic_calendars)
        # self.startCal['style'] = 'stat.TCombobox'
        # self.endCal['style'] = 'stat.TCombobox'
        self.startCal['style'] = 'orup.TCombobox'
        self.endCal['style'] = 'orup.TCombobox'

        self.can.create_window(self.w / 3.86, self.h / 3.85,
                               window=self.startCal,
                               tags=('statCal'))
        self.can.create_window(self.w / 2.75, self.h / 3.85,
                               window=self.endCal,
                               tags=('statCal'))
        self.statisticInteractiveWidgets.append(self.startCal)
        self.statisticInteractiveWidgets.append(self.endCal)
        self.calendarsDrawn = True

    def drawing(self):
        super().drawing()
        self.drawWin('maincanv', 'statisticwin')
        if not self.calendarsDrawn:
            self.placeCalendars()
        self.get_history()
        self.draw_stat_tree()
        self.show_widgets(self.statisticInteractiveWidgets)

    def get_history(self):
        """ Запрашивает истоию заездов у GCore """
        trash_cat = self.operator.get_trash_cat_id(
            self.stat_page_trash_cat_var.get())
        trash_type = self.operator.get_trash_type_id(
            self.stat_page_trash_type_var.get())
        carrier = self.operator.get_client_id(self.stat_page_carrier_var.get())
        auto = self.operator.get_auto_id(self.stat_page_carnum_cb.get())
        platform_id = self.operator.get_polygon_platform_id(
            self.stat_page_polygon_combobox.get())
        pol_object_id = self.operator.get_polygon_object_id(
            self.stat_page_pol_object_combobox.get())
        client = self.operator.get_client_id(self.stat_page_clients_var.get())
        self.operator.ar_qdk.get_history(
            time_start=self.startCal.get_date(),
            time_end=self.endCal.get_date(),
            trash_cat=trash_cat,
            trash_type=trash_type,
            carrier=carrier, auto_id=auto,
            polygon_object_id=pol_object_id,
            client=client, platform_id=platform_id
        )

    def draw_stat_tree(self, tree=None):
        self.can.delete('tree')
        if not tree:
            tree = self.tree
        try:
            self.tar.sortId(tree, '#0', reverse=True)
        except TypeError:
            pass
        self.can.create_window(self.w / 1.9, self.h / 1.7,
                               window=tree,
                               tag='tree')

    def openWin(self):
        super().openWin()
        self.show_main_navbar_btns()
        self.changed_record = None
        self.root.bind("<Double-Button-1>",
                       lambda event: self.clear_optionmenu(event))
        self.root.bind('<Escape>',
                       lambda event: self.operator.mainPage.openWin())

    def page_close_operations(self):
        super().page_close_operations()
        self.changed_record = None
        self.hide_widgets(self.statisticInteractiveWidgets)
        self.root.unbind("<Button-1>")
        self.can.delete('amount_weight', 'statusel', 'tree')
        self.hide_main_navbar_btns()

    def initBlockImg(self, name, btnsname=None, slice='shadow', mode='new',
                     seconds=[], hide_widgets=[], **kwargs):
        super(Statistic, self).initBlockImg(name, btnsname)
        self.hide_widgets(self.statisticInteractiveWidgets)
        self.hide_widgets(self.page_buttons)
        self.hide_main_navbar_btns()

    def destroyBlockImg(self, mode='total'):
        super(Statistic, self).destroyBlockImg()
        self.show_widgets(self.statisticInteractiveWidgets)
        self.show_widgets(self.page_buttons)
        self.show_main_navbar_btns()
        self.show_time()

class AuthWin(Terminal):
    '''Окно авторизации'''

    def __init__(self, root, settings, operator, can):
        super(AuthWin, self).__init__(root, settings, operator, can)
        self.name = 'AuthWin'
        self.buttons = settings.authBtns
        self.right_corner_sys_buttons_objs = self.create_btns_and_hide([
            self.settings.minimize_btn, self.settings.exitBtnAuth])
        self.s = settings
        self.r = root
        self.currentUser = 'Андрей'
        self.font = '"Montserrat Regular" 14'
        self.page_buttons = self.create_btns_and_hide(self.buttons)

    def send_auth_command(self):
        """ Отправить команду на авторизацию """
        pw = self.auth_page_password_entry.get()
        login = self.auth_page_login_var.get()
        self.operator.ar_qdk.try_auth_user(username=login, password=pw)
        self.currentUser = login

    def createPasswordEntry(self):
        var = StringVar(self.r)
        pwEntry = PasswordEntry(self.r, border=0,
                                width=
                                el_sizes.entrys['authwin.password'][
                                    self.screensize][
                                    'width'],
                                textvariable=var, bg=cs.auth_background_color,
                                font=self.font, fg='#BABABA',
                                insertbackground='#BABABA',
                                highlightthickness=0)
        return pwEntry

    def incorrect_login_act(self):
        self.auth_page_password_entry.incorrect_login_act()

    def get_login_type_cb(self):
        self.auth_page_login_var = StringVar()
        self.usersComboBox = AutocompleteCombobox(self.root,
                                                  textvariable=self.auth_page_login_var)
        self.usersComboBox['style'] = 'authwin.TCombobox'
        self.configure_combobox(self.usersComboBox)
        users = self.operator.get_users_reprs()
        self.usersComboBox.set_completion_list(users)
        if len(users) == 1:
            self.usersComboBox.set(users[0])
        self.usersComboBox.config(
            width=el_sizes.comboboxes['authwin.login'][self.screensize][
                'width'],
            height=el_sizes.comboboxes['authwin.login'][self.screensize][
                'height'],
            font=self.font)
        self.usersComboBox.bind('<Return>',
                                lambda event: self.send_auth_command())
        return self.usersComboBox

    def rebinding(self):
        self.usersComboBox.unbind('<Return>')
        self.auth_page_password_entry.unbind('<Return>')
        self.bindArrows()

    def drawing(self):
        super().drawing(self)
        self.create_auth_entries()
        self.drawSlices(mode=self.name)

    def create_auth_entries(self):
        self.auth_page_password_entry = self.createPasswordEntry()
        self.auth_page_password_entry.bind('<Return>', lambda
            event: self.send_auth_command())
        self.usersChooseMenu = self.get_login_type_cb()
        self.can.create_window(self.s.w / 2, self.s.h / 1.61,
                               window=self.auth_page_password_entry,
                               tags=('maincanv', 'pw_win'))
        self.can.create_window(self.s.w / 2, self.s.h / 1.96,
                               window=self.usersChooseMenu, tag='maincanv')

    def initBlockImg(self, name, btnsname=None, slice='shadow', mode='new',
                     seconds=[], hide_widgets=[], picture=None, **kwargs):
        super(AuthWin, self).initBlockImg(name, btnsname)
        self.auth_page_password_entry.lower()
        self.usersChooseMenu.lower()
        self.hide_buttons(self.page_buttons)

    def destroyBlockImg(self, mode='total'):
        super(AuthWin, self).destroyBlockImg()
        self.auth_page_password_entry.lift()
        self.usersChooseMenu.lift()
        self.show_buttons(self.page_buttons)

    def openWin(self):
        super().openWin()
        self.drawWin('maincanv', 'start_background', 'login', 'password')
        #self.hide_buttons(self.right_corner_sys_buttons_objs)
        self.can.delete("clockel")
        self.can.itemconfigure('btn', state='hidden')
        self.auth_page_password_entry.config(show='\u2022',
                                             highlightthickness=0)

    def page_close_operations(self):
        super().page_close_operations()
        self.can.itemconfigure('btn', state='normal')


class MainPage(Terminal):
    def __init__(self, root, settings, operator, can):
        super(MainPage, self).__init__(root, settings, operator, can)
        self.name = 'MainPage'
        self.buttons = settings.gateBtns + settings.manual_gate_control_btn
        self.count = 0
        self.orupState = False
        self.errorShown = False
        self.chosenTrashCat = 'deff'
        self.tree = self.create_tree()
        self.win_widgets.append(self.tree)
        self.btn_name = self.settings.mainLogoBtn
        self.make_abort_unactive()
        self.page_buttons = self.create_btns_and_hide(self.buttons)
        self.cameras = ["auto_exit", "cad_gross", "main"]

    def cam_zoom_callback(self, cam_type=None):
        print("T229")
        self.tree.lower()
        self.abort_round_btn.lower()
        super(MainPage, self).cam_zoom_callback(cam_type)
        self.hide_widgets(self.hide_while_cam_zoom_widgets)

    def cam_hide_callback(self, cam_type=None):
        super(MainPage, self).cam_hide_callback(cam_type)
        self.operator.turn_cams(True)
        self.operator.currentPage.abort_round_btn.lift()
        self.operator.currentPage.tree.lift()

    def after_destroy_block_operations(self):
        self.operator.draw_road_anim()
        self.operator.turn_cams(True)

    def draw_set_arrow(self, arrow_attr):
        if (
                self.operator.current == 'MainPage' or self.operator.current == 'ManualGateControl') and \
                self.operator.currentPage.blockImgDrawn == False:
            super().draw_set_arrow(arrow_attr)

    def create_tree(self):
        self.tar = CurrentTreeview(self.root, self.operator, height=18)
        self.tar.createTree()
        self.tree = self.tar.get_tree()
        self.tree.bind("<Double-Button-1>", self.OnDoubleClick)
        return self.tree

    def rebind_btns_after_orup_close(self):
        self.tree.bind("<Double-Button-1>", self.OnDoubleClick)

    def create_abort_round_btn(self):
        self.can.create_window(self.settings.abort_round[0][1],
                               self.settings.abort_round[0][2],
                               window=self.abort_round_btn,
                               tag='winBtn')

    def make_abort_active(self):
        btn = self.abort_round_btn
        btn['state'] = 'normal'

    def make_abort_unactive(self):
        btn = self.abort_round_btn
        btn['state'] = 'disabled'

    def drawMainTree(self):
        self.operator.ar_qdk.get_unfinished_records()
        self.can.create_window(self.w / 1.495, self.h / 2.8, window=self.tree,
                               tag='tree')
        # self.tar.sortId(self.tree, '#0', reverse=True)

    def drawing(self):
        super().drawing(self)
        self.operator.ar_qdk.get_status()
        self.drawMainTree()
        self.drawWin('win', 'road', 'order', 'currentEvents',
                     'entry_gate_base', 'exit_gate_base')

    def drawRegWin(self):
        self.draw_block_win(self, 'regwin')

    def updateTree(self):
        self.operator.ar_qdk.get_unfinished_records()

    def OnDoubleClick(self, event):
        """ Реакция на дабл-клик по текущему заезду """
        self.record_id = self.tree.selection()[0]
        self.chosenStr = self.tree.item(self.record_id, "values")
        if self.chosenStr[2] == '-':
            self.draw_rec_close_win()
        else:
            self.draw_cancel_tare()

    def draw_rec_close_win(self):
        btnsname = 'closeRecBtns'
        self.initBlockImg(name='ensureCloseRec', btnsname=btnsname,
                          seconds=('second'),
                          hide_widgets=self.win_widgets)
        self.root.bind('<Return>', lambda event: self.operator.close_record(
            self.record_id))
        self.root.bind('<Escape>',
                       lambda event: self.destroyBlockImg(mode="total"))

    def draw_cancel_tare(self):
        btnsname = 'cancel_tare_btns'
        self.initBlockImg(name='cancel_tare', btnsname=btnsname,
                          seconds=('second'),
                          hide_widgets=self.win_widgets)
        self.root.bind('<Escape>',
                       lambda event: self.destroyBlockImg(mode="total"))

    def initBlockImg(self, name, btnsname=None, slice='shadow', mode='new',
                     seconds=[], hide_widgets=[], picture=None, **kwargs):
        super(MainPage, self).initBlockImg(name, btnsname)
        self.hide_widgets(self.page_buttons)
        self.hide_main_navbar_btns()

    def destroyBlockImg(self, mode='total'):
        super(MainPage, self).destroyBlockImg()
        self.drawMainTree()
        self.show_main_navbar_btns()
        self.show_time()

    def openWin(self):
        super(MainPage, self).openWin()
        # cams_zoom = [cam['name']+cam['zoom'] for cam in self.operator.cameras_info]
        if not self.cam_zoom:
            self.hide_zoomed_cam(True)
        # self.operator.turn_cams(True)
        self.operator.ar_qdk.execute_method("get_gates_states")
        self.operator.draw_road_anim()
        self.draw_gate_arrows()
        self.draw_weight()
        self.abort_round_btn.lift()
        self.create_abort_round_btn()
        self.show_main_navbar_btns()
        self.turn_on_cameras()

    def page_close_operations(self):
        super(MainPage, self).page_close_operations()
        self.can.delete('win', 'statusel', 'tree', 'road', 'order',
                        'currentEvents',
                        'entry_gate_base', 'exit_gate_base')
        self.operator.turn_cams(False)
        self.abort_round_btn.lower()
        self.unbindArrows()
        self.hide_main_navbar_btns()
        self.can.delete("kgel")

# -gross_cam True -auto_exit_cam True -main_cam True

class ManualGateControl(Terminal):
    def __init__(self, root, settings, operator, can):
        super(ManualGateControl, self).__init__(root, settings, operator, can)
        self.name = 'ManualGateControl'
        self.buttons = self.settings.auto_gate_control_btn + self.settings.manual_open_internal_gate_btn + self.settings.manual_close_internal_gate_btn + \
                       self.settings.manual_open_external_gate_btn + self.settings.manual_close_external_gate_btn + self.settings.null_weight_btn
        self.btn_name = self.settings.mainLogoBtn
        self.external_gate_state = 'close'
        self.enternal_gate_state = 'close'
        self.page_buttons = self.create_btns_and_hide(self.buttons)
        self.cameras = ["auto_exit", "cad_gross"]

    def draw_set_arrow(self, arrow_attr):
        if (
                self.operator.current == 'MainPage' or self.operator.current == 'ManualGateControl') and \
                self.operator.currentPage.blockImgDrawn == False:
            super().draw_set_arrow(arrow_attr)

    def drawing(self):
        super().drawing(self)
        self.drawWin('maincanv', 'road', 'manual_control_info_bar',
                     'entry_gate_base', 'exit_gate_base')

    def initBlockImg(self, name, btnsname=None, slice='shadow', mode='new',
                     seconds=[], hide_widgets=[], picture=None, **kwargs):
        super(ManualGateControl, self).initBlockImg(name, btnsname)
        self.hide_buttons(self.page_buttons)
        self.hide_main_navbar_btns()

    def destroyBlockImg(self, mode='total'):
        super(ManualGateControl, self).destroyBlockImg()
        self.show_time()
        self.show_buttons(self.page_buttons)
        self.show_main_navbar_btns()

    def openWin(self):
        super(ManualGateControl, self).openWin()
        self.operator.draw_road_anim()
        self.draw_gate_arrows()
        self.draw_weight()
        self.root.bind('<Escape>',
                       lambda event: self.operator.mainPage.openWin())
        self.show_main_navbar_btns()

    def page_close_operations(self):
        super(ManualGateControl, self).page_close_operations()
        self.root.unbind("Escape")
        self.can.delete('win', 'statusel', 'tree')
        self.hide_main_navbar_btns()


class KPP(Terminal):
    def __init__(self, root, settings, operator, can):
        super(KPP, self).__init__(root, settings, operator, can)
        self.name = 'KPP'
        self.kpp_info = {}
        self.ok_btn = self.create_button_and_hide(self.settings.kpp_ok_btn)
        self.abort_btn = self.create_button_and_hide(
            self.settings.kpp_abort_btn)
        self.other_footer_btns = self.create_btns_and_hide(
            self.settings.kpp_internal_btn + self.settings.kpp_external_btn + self.settings.kpp_lift_up_btn)
        self.page_buttons = [self.ok_btn] + [
            self.abort_btn] + self.other_footer_btns
        self.btn_name = self.settings.kpp_icon
        self.gate_state = 'close'
        self.arrivals = []
        self.plase_kpp_tree_btns()
        self.tree = self.create_tree()
        self.draw_elements = ["kpp_road", "kpp_main_background",
                              "kpp_barrier_base"]
        self.gates = [{"name": "kpp_gate_arrow",
                       "image": ...}]
        self.info = {}
        # self.cameras = {"external": {},
        #                "internal": {}}
        self.kpp_get_info()
        self.kpp_preloader_tags = ["foo", "bar"]
        self.kpp_preloader_img = Image.open(
            self.settings.imgsysdir + 'kpp_preloader_img.png')
        self.plate_recognition_in_progress = False
        self.kpp_success_recognition = ImageTk.PhotoImage(Image.open(
            self.settings.imgsysdir + 'kpp_recognition_success.png'))
        self.kpp_failed_recognition = ImageTk.PhotoImage(Image.open(
            self.settings.imgsysdir + 'kpp_recognition_failed.png'))
        self.close_arrival_without_pass_out = False
        self.pass_out_without_time_in = False
        self.hide_while_cam_zoom_widgets = []
        self.arriving_in_progress = False
        self.hide_kpp_tree_btns()
        self.cameras = ["kpp_cam_external", "kpp_cam_internal"]
        self.abort_photocell_waiting_btn = self.create_button_and_hide(
            self.settings.kpp_abort_photocell_waiting)

    def lift_up_btn(self):
        # Логгировать нажатие
        self.initBlockImg("kpp_lift_up_win", "kpp_lift_up_win_btns")
        self.kpp_password_entry = PasswordEntry(self.root, border=0,
                                                width=26, bg=cs.orup_bg_color,
                                                font=fonts.kpp_lift_up_password,
                                                fg='#BABABA',
                                                insertbackground='#BABABA',
                                                highlightthickness=0)
        self.can.create_window(1072, 806,
                               window=self.kpp_password_entry,
                               tags=("win_widgets",))
        self.can.bind('<Return>', lambda event: self.send_auth_lift_up())

    def send_auth_lift_up(self):
        password = self.kpp_password_entry.get()
        self.operator.ar_qdk.execute_method(
            "kpp_send_auth_lift_up",
            username=self.operator.username, password=password)

    def lets_recognise(self, side_name):
        self.operator.ar_qdk.execute_method("kpp_lets_recognise",
                                            side_name=side_name)

    def lift_up_auth_success(self, username):
        self.destroyBlockImg()
        self.hide_kpp_tree_btns()
        self.operator.kpp_lift_page.openWin()

    def lift_up_incorrect_password(self):
        self.kpp_password_entry.incorrect_login_act(
            f"Неправильный пароль для {self.operator.username}")

    def trying_start_new_arrival_while_current(self):
        threading.Thread(target=self.kpp_arriving_attention_thread).start()

    def kpp_arriving_attention_thread(self):
        init_font = fonts.kpp_status
        init_font_size = int(re.findall(r'\d+', init_font)[0])
        current_font_size = init_font_size
        max_font = 18
        anim_speed = 0.02
        font_animation_speed = 1
        color = "#F0B33E"
        while current_font_size < max_font:
            new_font = init_font.replace(
                str(init_font_size), str(current_font_size))
            current_font_size += font_animation_speed
            self.set_arriving_status(font=new_font, fill=color)
            time.sleep(anim_speed)
        while current_font_size != init_font_size:
            new_font = init_font.replace(
                str(init_font_size), str(current_font_size))
            current_font_size -= font_animation_speed
            self.set_arriving_status(font=new_font, fill=color)
            time.sleep(anim_speed)
        while current_font_size < max_font:
            new_font = init_font.replace(
                str(init_font_size), str(current_font_size))
            current_font_size += font_animation_speed
            self.set_arriving_status(font=new_font, fill=color)
            time.sleep(anim_speed)
        while current_font_size != init_font_size:
            new_font = init_font.replace(
                str(init_font_size), str(current_font_size))
            current_font_size -= font_animation_speed
            self.set_arriving_status(font=new_font, fill=color)
            time.sleep(anim_speed)
        self.set_arriving_status(font=init_font, fill=color)
        time.sleep(1)
        self.can.delete("kpp_status")
        if self.arriving_in_progress:
            self.set_arriving_status()

    def set_arriving_status(
            self, font=fonts.kpp_status, fill="#E4A731",
            text="Ожидается проезд авто"):
        self.can.delete("kpp_status")
        self.can.create_text(
            1038.24, 710,
            tag='kpp_status',
            text=text,
            fill=fill,
            font=font,
            anchor='n')
        if text.lower() == "ожидается проезд авто":
            self.create_abort_photocell_waiting_btn()
        elif text.lower() == "авто проехало":
            self.destroyBlockImg()
            self.delete_abort_photocell_waiting_btn()
        elif text.lower() == "время ожидания истекло":
            self.destroyBlockImg()
            self.delete_abort_photocell_waiting_btn()

    def external_button_pressed(self):
        if self.arriving_in_progress:
            self.trying_start_new_arrival_while_current()
            return
        if self.kpp_info["recognise"]:
            self.draw_preloader_recognition()
            self.lets_recognise("external")
        else:
            self.draw_manual_pass_entry()

    def internal_button_pressed(self):
        if self.arriving_in_progress:
            self.trying_start_new_arrival_while_current()
            return
        if self.kpp_info["recognise"]:
            self.draw_preloader_recognition()
            self.lets_recognise("internal")
        else:
            self.draw_manual_pass_exit()

    def draw_preloader_recognition(self):
        self.drawBlurScreen()
        self.can.create_text(
            960, 620, text="Пытаемся распознать гос. номер",
            font=fonts.kpp_preloader_text, fill="#F2F2F2", tags=("trying_text",
                                                                 "plate_recognition"))
        self.operator.turn_cams(False)
        self.plate_recognition_in_progress = True
        threading.Thread(target=self.rotate_preloader).start()

    def set_recognition_count(self, count, max_count=3):
        self.can.delete("try_count")
        self.can.create_text(
            960, 675, text=f"{count}/{max_count}",
            font=fonts.kpp_preloader_text, fill="#F2F2F2", tags=("trying_text",
                                                                 "plate_recognition",
                                                                 "try_count"))

    def draw_recognition_success(self):
        # self.drawBlurScreen()
        self.plate_recognition_in_progress = False
        self.can.delete("plate_recognition")
        self.can.create_text(
            960, 620, text="Гос. номер распознан",
            font=fonts.kpp_preloader_text, fill="#F2F2F2",
            tags=("success_text",
                  "plate_recognition"))
        self.can.create_image(960, 516, image=self.kpp_success_recognition,
                              tags=("preloader_circle",
                                    "plate_recognition"))

    def draw_recognition_failed(self):
        # self.drawBlurScreen()
        self.plate_recognition_in_progress = False
        self.can.delete("plate_recognition")
        self.can.create_text(
            960, 620, text="Гос. номер не распознан!",
            font=fonts.kpp_preloader_text, fill="#F2F2F2",
            tags=("success_text",
                  "plate_recognition"))
        self.can.create_image(960, 516, image=self.kpp_failed_recognition,
                              tags=("preloader_circle",
                                    "plate_recognition"))

    def destroy_recognition_win(self):
        self.can.delete("plate_recognition")
        self.destroyBlockImg()

    def rotate_preloader(self):
        start_pos = 0
        cur_pos = start_pos
        self.el_list = []
        while self.plate_recognition_in_progress:
            tkimage = ImageTk.PhotoImage(
                self.kpp_preloader_img.rotate(cur_pos, expand=True))
            # center=(start_pos, end_pos)))
            self.el_list.append(tkimage)
            cur_pos += 1.5
            self.can.create_image(960, 516, image=tkimage,
                                  tags=("preloader_circle",
                                        "plate_recognition"))
            try:
                self.el_list = self.el_list[-5:]
            except IndexError:
                pass
            time.sleep(0.001)

    def after_destroy_block_operations(self):
        self.turn_on_cameras()

    def kpp_get_info(self):
        self.operator.ar_qdk.execute_method("kpp_get_info")

    def draw_gate_arrows(self):
        self.draw_set_arrow("kpp_barrier_arrow")

    def open_barrier(self):
        threading.Thread(target=self.rotate_gate_arrow, args=(
            "kpp_barrier_arrow", 'open', 'OUT', 1, 85)).start()

    def close_barrier(self):
        threading.Thread(target=self.rotate_gate_arrow, args=(
            "kpp_barrier_arrow", 'close', 'OUT', -1, 0)).start()

        # self.plase_kpp_tree_btns()
        # threading.Thread(target=self.test).start()

    def create_abort_photocell_waiting_btn(self):
        self.abort_photocell_waiting_btn.lift()

    def delete_abort_photocell_waiting_btn(self):
        self.abort_photocell_waiting_btn.lower()

    def abort_photocell_waiting_pressed(self):
        # make_log
        # self.draw_block_win()
        self.operator.ar_qdk.execute_method(
            "log_event",
            event="Оператор нажал на кнопку прерывания ожидания фотоэлементов")
        self.abort_photocell_waiting_btn.lower()
        self.initBlockImg('kpp_abort_photocell_waiting_confirmation_win',
                          "kpp_abort_photocell_waiting_win_btns")
        self.photocell_waiting_abort_note = self.getText(
            h=3, w=32, bg=cs.orup_bg_color, font=fonts.orup_font,
            tags=("block_win_els",))
        self.can.create_window(1072, 539,
                               window=self.photocell_waiting_abort_note,
                               tag='block_win_els')

    def continue_photocell_waiting(self):
        self.operator.ar_qdk.execute_method(
            "log_event",
            event="Оператор решил продолжить ожидание пересечения фотоэлементов")
        self.destroyBlockImg()
        if self.arriving_in_progress:
            self.create_abort_photocell_waiting_btn()

    def abort_photocell_waiting(self):
        # self.operator.ar_qdk.execute_method(
        #    "log_event",
        #    event="Оператор прервал ожидание фотоэлементов вручную!",
        #    level="warning")
        operator_comment = self.photocell_waiting_abort_note.get(
            "1.0", 'end-1c')
        if len(operator_comment) == 0:
            self.photocell_waiting_abort_note["highlightcolor"] = "#E14B50"
            self.photocell_waiting_abort_note["highlightthickness"] = 1
            return
        print("ABORT PHOTOCELL WAITING!")
        self.operator.ar_qdk.execute_method(
            "kpp_break_photocell_waiting",
            comment=operator_comment)
        self.destroyBlockImg()
        self.arriving_in_progress = False
        self.delete_abort_photocell_waiting_btn()
        self.can.delete("kpp_status")

    def abort_round(self):
        operator_comment = self.photocell_waiting_abort_note.get(
            "1.0", 'end-1c')
        if len(operator_comment) == 0:
            self.photocell_waiting_abort_note["highlightcolor"] = "#E14B50"
            self.photocell_waiting_abort_note["highlightthickness"] = 1
            return
        print("ABORT PHOTOCELL ARRIVING!")
        self.operator.ar_qdk.execute_method(
            "kpp_abort_arriving",
            comment=operator_comment)
        self.destroyBlockImg()
        self.arriving_in_progress = False
        self.delete_abort_photocell_waiting_btn()
        self.can.delete("kpp_status")

    # def init_photocell_waiting_abort_window(self):
    #    self.initBlockImg('kpp_abort_photocell_waiting_confirmation_win')

    def test(self):
        time.sleep(10)
        self.draw_manual_pass_entry(
            alert_text=f"Автоматический доступ для машины В060ХА702 запрещен!\nВы можете пропустить ее вручную, но это будет отражено в журнале")
        time.sleep(5)
        self.destroyBlockImg()
        self.draw_manual_pass_entry()

    def plase_kpp_tree_btns(self):
        self.place_car_number_combobox()
        self.place_clients_combobox()
        self.place_carriers_combobox()
        self.place_calendars()

    def hide_kpp_tree_btns(self):
        self.kpp_tree_carnum_cb.lower()
        self.kpp_tree_carriers_cb.lower()
        self.kpp_tree_clients_cb.lower()
        self.kpp_end_calendar.lower()
        self.kpp_start_calendar.lower()

    def show_kpp_tree_btns(self):
        self.kpp_tree_carnum_cb.lift()
        self.kpp_tree_carriers_cb.lift()
        self.kpp_tree_clients_cb.lift()
        self.kpp_end_calendar.lift()
        self.kpp_start_calendar.lift()

    def configure_combobox(self, om):
        om.master.option_add('*TCombobox*Listbox.background', '#3D3D3D')
        om.master.option_add('*TCombobox*Listbox.foreground',
                             cs.kpp_filter_font)
        om.master.option_add('*TCombobox*Listbox.selectBackground',
                             cs.orup_active_color)
        om.master.option_add('*TCombobox*Listbox.font',
                             fonts.kpp_filters_content)
        om.config(font=fonts.kpp_filters)
        om['style'] = 'kpp_filters.TCombobox'

    def place_car_number_combobox(self):
        listname = self.operator.get_auto_reprs()
        self.kpp_tree_carnum_cb = AutocompleteComboboxCarNumber(
            self.root, default_value="Гос. номер")
        self.kpp_tree_carnum_cb.set_completion_list(listname)
        self.configure_combobox(self.kpp_tree_carnum_cb)
        self.kpp_tree_carnum_cb.config(width=10, height=21)
        self.can.create_window(348, 186.5,
                               window=self.kpp_tree_carnum_cb,
                               tags=(
                                   'kpp_carnum_cb', 'kpp_filter'))
        self.hide_while_cam_zoom_widgets.append(self.kpp_tree_carnum_cb)
        self.page_widgets.append(self.kpp_tree_carnum_cb)

    def place_clients_combobox(self):
        self.kpp_tree_clients_cb = AutocompleteCombobox(
            self.root, default_value='Клиенты')
        self.configure_combobox(self.kpp_tree_clients_cb)
        self.kpp_tree_clients_cb.set_completion_list(
            self.operator.get_clients_reprs())
        self.kpp_tree_clients_cb['style'] = 'orup.TCombobox'
        self.configure_combobox(self.kpp_tree_clients_cb)
        self.kpp_tree_clients_cb.config(width=20, height=21)
        self.can.create_window(530, 186.5,
                               window=self.kpp_tree_clients_cb,
                               tags=(
                                   "kpp_filter", 'typeCombobox'))

    def place_carriers_combobox(self):
        self.kpp_tree_carriers_cb = AutocompleteCombobox(
            self.root, default_value='Перевозчики')
        self.configure_combobox(self.kpp_tree_carriers_cb)
        self.kpp_tree_carriers_cb.set_completion_list(
            self.operator.get_clients_reprs())
        self.kpp_tree_carriers_cb['style'] = 'orup.TCombobox'
        self.configure_combobox(self.kpp_tree_carriers_cb)
        self.kpp_tree_carriers_cb.config(width=20, height=21)
        self.can.create_window(750, 186.5,
                               window=self.kpp_tree_carriers_cb,
                               tags=(
                                   "kpp_filter", 'typeCombobox'))

    def place_calendars(self):
        self.kpp_start_calendar = MyDateEntry(self.root,
                                              date_pattern='dd.mm.Y')
        self.kpp_start_calendar.config(width=9, font=fonts.kpp_calendar)
        self.kpp_end_calendar = MyDateEntry(self.root, date_pattern='dd.mm.Y')
        self.kpp_end_calendar.config(width=9, font=fonts.kpp_calendar)
        self.kpp_start_calendar['style'] = 'kpp_filters.TCombobox'
        self.kpp_end_calendar['style'] = 'kpp_filters.TCombobox'
        self.can.create_window(1108, 186.5,
                               window=self.kpp_start_calendar,
                               tags=(
                                   "kpp_filter", "kpp_calendar"))
        self.can.create_window(1285, 186.5,
                               window=self.kpp_end_calendar,
                               tags=(
                                   "kpp_filter", "kpp_calendar"))

    def get_cars_inside_full_info(self):
        if not self.arrivals:
            return []
        return [car for car in self.arrivals if not car['time_out']]

    def draw_manual_pass_exit(
            self, car_number=None, note=None,
            alert_text="Гос.номер не обнаружен!\n"
                       "Если машина есть, выберите ее из списка въехавших ранее.\n"
                       "Такой пропуск будет отмечен как пропуск без распознавания.\n",
            without_time_in=False):
        self.pass_out_without_time_in = without_time_in
        self.kpp_internal_init_carnum = car_number
        self.initBlockImg(name='kpp_manual_pass_internal_win',
                          btnsname="kpp_manual_pass_internal_btns")
        # creating car number combobox
        self.kpp_cars_inside = self.get_cars_inside_full_info()
        car_numbers = [self.operator.get_auto_repr(car['auto_id']) for car in
                       self.kpp_cars_inside]
        self.kpp_manual_pass_internal_number_var = StringVar()
        self.kpp_manual_pass_internal_number_var.trace_add(
            'write', self.manual_pass_internal_number_react)
        self.kpp_car_number_internal = self.create_orup_combobox(
            500, 172,
            textvariable=self.kpp_manual_pass_internal_number_var,
            width=36, height=7, tags=("block_win_els",))
        if car_numbers:
            self.kpp_car_number_internal.set_completion_list(car_numbers)
            if not car_number:
                self.kpp_manual_pass_internal_number_var.set(car_numbers[0])
        self.kpp_manual_pass_internal_number_var.trace_add(
            'write', self.manual_pass_internal_number_change_react)
        if car_number:
            self.kpp_manual_pass_internal_number_var.set(car_number)
            alert_text = f"Въезд {car_number} не был зарегистрирован!\n" \
                         "Вы можете выпустить ее, но это будет зафиксировано в системе.\n" \
                         "Если же считало неправильно, пожалуйста, исправьте гос.номер.\n"
        elif not car_number and not car_numbers:
            alert_text = f"Гос.номер не распознан!\nТак же в системе не зафиксированы машины на территории." \
                         f"\nЕсли действительно есть машина, укажите ее гос.номер перед выпуском."
        elif not car_number and car_number:
            alert_text = f"Гос.номер не распознан!\nНо в системе зафиксированы другие машины." \
                         f"\nПроверьте, может гос.номер распознан неверно?."
        self.manual_pass_note_internal = self.getText(
            h=3, w=32, bg=cs.orup_bg_color, font=fonts.orup_font,
            tags=("block_win_els",))
        if note:
            self.manual_pass_note_internal.insert(1.0, note)
        self.can.create_window(500, 250,
                               window=self.manual_pass_note_internal,
                               tag='block_win_els')
        self.can.create_text(385, 390,
                             text=alert_text,
                             font=fonts.general_text_font,
                             tags=('block_win_els', 'statusel'),
                             fill=self.textcolor, anchor='n',
                             justify='center')
        self.turn_on_cameras()
        self.unbindArrows()
        self.show_camera("kpp_cam_internal")
        self.root.bind('<Return>',
                       lambda event: self.kpp_manual_pass_internal())

    def kpp_manual_pass_internal(self):
        valid_entries = self.validate_internal_entries()
        if not valid_entries:
            return
        self.operator.ar_qdk.execute_method(
            "kpp_close_arrival",
            car_number=self.kpp_manual_pass_internal_number_var.get().capitalize(),
            note=self.manual_pass_note_internal.get("1.0", "end-1c"),
            pass_out_without_time_in=self.pass_out_without_time_in,
            init_car_number=self.kpp_internal_init_carnum)
        self.destroyBlockImg()

    def manual_pass_internal_number_change_react(self, *args):
        for car in self.kpp_cars_inside:
            if self.kpp_manual_pass_internal_number_var.get() == self.operator.get_auto_repr(
                    car["auto_id"]):
                if car["note"]:
                    self.manual_pass_note_internal.delete(1.0, END)
                    self.manual_pass_note_internal.insert(1.0, car["note"])
                else:
                    self.manual_pass_note_internal.delete(1.0, END)

    def draw_manual_pass_entry(
            self, car_number=None, client_id=None,
            carrier_id=None, notes=None,
            alert_text="Гос.номер не распознан. Если машина есть, укажите гос.номер сами."
                       "\nВ системе такой проезд будет отмечен как пропуск без распознавания.",
            close_opened_id=False):
        self.kpp_external_init_carnum = car_number
        self.close_arrival_without_pass_out = close_opened_id
        self.initBlockImg(name='kpp_manual_pass_win',
                          btnsname="kpp_manual_pass_entry_btns")
        # creating car number combobox
        self.kpp_manual_pass_number_string = StringVar()
        self.manual_pass_entry_number_cb = self.create_orup_combobox(
            500, 172, textvariable=self.kpp_manual_pass_number_string,
            width=36, height=7, tags=("block_win_els",))
        self.kpp_manual_pass_number_string.trace_add(
            'write', self.manual_pass_external_number_react)
        self.manual_pass_entry_number_cb.set_completion_list(
            self.operator.get_auto_reprs())
        if car_number: self.kpp_manual_pass_number_string.set(car_number)
        # creating client combobox
        self.manual_pass_entry_client_cb = self.create_orup_combobox(
            500, 235, width=36, height=7, tags=("block_win_els",))
        self.manual_pass_entry_client_cb.set_completion_list(
            self.operator.get_clients_reprs())
        if client_id:
            self.manual_pass_entry_client_cb.set(
                self.operator.get_client_repr(client_id))
        # creating carrier combobox
        self.manual_pass_entry_carrier_cb = self.create_orup_combobox(
            500, 298, width=36, height=7, tags=("block_win_els",))
        self.manual_pass_entry_carrier_cb.set_completion_list(
            self.operator.get_clients_reprs())
        if carrier_id:
            self.manual_pass_entry_client_cb.set(
                self.operator.get_client_repr(carrier_id))
        self.manual_pass_note = self.getText(
            h=3, w=32, bg=cs.orup_bg_color, font=fonts.orup_font,
            tags=("block_win_els",))
        if notes:
            self.manual_pass_note.insert(1.0, notes)
        self.can.create_window(500, 378,
                               window=self.manual_pass_note,
                               tags=("block_win_els", 'orupentry'))
        self.can.create_text(385, 530,
                             text=alert_text,
                             font=fonts.general_text_font,
                             tags=('block_win_els', 'statusel'),
                             fill=self.textcolor, anchor='n',
                             justify='center')
        self.turn_on_cameras()
        self.root.bind('<Return>',
                       lambda event: self.send_manual_pass_command_external())
        self.root.bind('<Escape>',
                       lambda event: self.destroyORUP())
        self.root.bind("<Double-Button-1>",
                       lambda event: self.clear_optionmenu(event))
        self.unbindArrows()
        self.show_camera("kpp_cam_external")

    def validate_external_entries(self):
        car_number = self.kpp_manual_pass_number_string.get()
        car_number_valid = self.validate_car_number(car_number)
        if car_number_valid:
            self.manual_pass_entry_number_cb['style'] = 'orup.TCombobox'
        else:
            self.manual_pass_entry_number_cb[
                'style'] = 'orupIncorrect.TCombobox'
        client = self.manual_pass_entry_client_cb.get()
        if client:
            client_valid = self.validate_client(
                client, self.operator.get_clients_reprs())
            if client_valid:
                self.manual_pass_entry_client_cb['style'] = 'orup.TCombobox'
            else:
                self.manual_pass_entry_client_cb[
                    'style'] = 'orupIncorrect.TCombobox'
        carrier = self.manual_pass_entry_client_cb.get()
        if carrier:
            carrier_valid = self.validate_client(
                client, self.operator.get_clients_reprs())
            if carrier_valid:
                self.manual_pass_entry_carrier_cb['style'] = 'orup.TCombobox'
            else:
                self.manual_pass_entry_carrier_cb[
                    'style'] = 'orupIncorrect.TCombobox'
        if car_number_valid and (client and client_valid or not client) and (
                carrier and carrier_valid or not carrier):
            return True

    def validate_internal_entries(self):
        car_number = self.kpp_car_number_internal.get()
        car_number_valid = self.validate_car_number(car_number)
        if car_number_valid:
            self.kpp_car_number_internal['style'] = 'orup.TCombobox'
            return True
        else:
            self.kpp_car_number_internal[
                'style'] = 'orupIncorrect.TCombobox'

    def validate_client(self, client, clients):
        if client in clients:
            return True

    def show_camera(self, camera_type):
        #        camera_type = "kpp_cam_external"
        video_inst = self.operator.get_camera_inst(camera_type)
        if video_inst:
            video_inst.set_new_params(x=1331, y=341, width=1110, height=614)

    def hide_camera(self, camera_type):
        video_inst = self.operator.get_camera_inst(camera_type)
        if video_inst:
            video_inst.hide_callback()

    def send_manual_pass_command_external(self):
        validate = self.validate_external_entries()
        if not validate:
            return
        if self.close_arrival_without_pass_out:
            self.operator.ar_qdk.execute_method(
                "kpp_close_arrival_without_pass_out",
                arrival_id=self.close_arrival_without_pass_out,
                note=self.manual_pass_note.get("1.0", "end-1c", ))
        self.operator.ar_qdk.execute_method(
            "kpp_create_arrival",
            car_number=self.kpp_manual_pass_number_string.get().capitalize(),
            client_id=self.operator.get_client_id(
                self.manual_pass_entry_client_cb.get()),
            carrier_id=self.operator.get_client_id(
                self.manual_pass_entry_carrier_cb.get()),
            note=self.manual_pass_note.get("1.0", "end-1c"),
            init_car_number=self.kpp_external_init_carnum)
        self.hide_camera("kpp_cam_external")
        self.destroyBlockImg()

    def validate_car_number(self, carnum):
        valid_car = re.match(
            '^[АВЕКМНОРСТУХ]\d{3}(?<!000)[АВЕКМНОРСТУХ]{2}\d{2,3}$',
            carnum)
        valid_agro = re.match("^\d{4}(?<!0000)[АВЕКМНОРСТУХ]{2}\d{2,3}$",
                              carnum)
        valid_trailer = re.match("^[АВЕКМНОРСТУХ]{2}\d{4}(?<!0000)\d{2,3}$",
                                 carnum)
        if (valid_car or valid_trailer or valid_agro):
            return True

    def manual_pass_external_number_react(self, *args):
        # Функция реакции программы на совершение действий типа write в combobox для ввода гос.номера
        self.validate_car_number_combobox(self.manual_pass_entry_number_cb)

    def manual_pass_internal_number_react(self, *args):
        # Функция реакции программы на совершение действий типа write в combobox для ввода гос.номера
        self.validate_car_number_combobox(self.kpp_car_number_internal)

    def validate_car_number_combobox(self, combobox):
        carnum = combobox.get()
        carnum = carnum.upper()
        value = len(carnum)
        combobox.set(carnum)
        valid_car_number = self.validate_car_number(carnum)
        if not valid_car_number or value < 8:
            # Сделать красную обводку
            combobox['style'] = 'orupIncorrect.TCombobox'
        else:
            # Оставить обычное оформление
            combobox['style'] = 'orup.TCombobox'

    def get_arrivals(self):
        self.operator.ar_qdk.execute_method(
            "kpp_get_arrivals",
            auto_id=self.operator.get_auto_id(self.kpp_tree_carnum_cb.get()),
            carrier_id=self.operator.get_client_id(
                self.kpp_tree_carriers_cb.get()),
            client_id=self.operator.get_client_id(
                self.kpp_tree_clients_cb.get()),
            time_in=self.kpp_start_calendar.get(),
            time_out=self.kpp_end_calendar.get())

    def abort_filters(self):
        """ Сбросить все фильтры на значения по умолчанию"""
        self.kpp_tree_carnum_cb.set_default_value()
        self.kpp_tree_carriers_cb.set_default_value()
        self.kpp_tree_clients_cb.set_default_value()
        self.kpp_start_calendar.set_date(datetime.datetime.today())
        self.kpp_end_calendar.set_date(datetime.datetime.today())
        self.get_arrivals()

    def create_tree(self):
        self.tar = KPPTreeview(self.root, self.operator, height=18)
        self.tar.createTree()
        self.tree = self.tar.get_tree()
        return self.tree

    def bindArrows(self):
        if self.settings.kpp_mirrored:
            left_button = self.internal_button_pressed
            right_button = self.external_button_pressed
        elif not self.settings.kpp_mirrored:
            left_button = self.external_button_pressed
            right_button = self.internal_button_pressed
        self.root.bind('<Left>', lambda event: left_button())
        self.root.bind('<Right>', lambda event: right_button())

    def cam_zoom_callback(self, cam_type=None):
        self.hide_kpp_tree_btns()
        self.hide_buttons((self.ok_btn, self.abort_btn))
        super().cam_zoom_callback(cam_type)
        try:
            self.abort_photocell_waiting_btn.lower()
        except:
            pass

    def cam_hide_callback(self, cam_type=None):
        super(KPP, self).cam_hide_callback(cam_type)
        self.show_kpp_tree_btns()
        self.turn_on_cameras()
        try:
            self.abort_photocell_waiting_btn.lift()
        except:
            pass

    def initBlockImg(self, name, btnsname=None, slice='shadow', mode='new',
                     seconds=[], hide_widgets=[], picture=None, **kwargs):
        self.hide_kpp_tree_btns()
        self.hide_widgets(self.page_buttons)
        super(KPP, self).initBlockImg(
            name, btnsname, slice, mode, seconds, hide_widgets,
            picture, **kwargs)
        self.hide_main_navbar_btns()
        self.delete_abort_photocell_waiting_btn()

    def destroyBlockImg(self, mode="total"):
        super(KPP, self).destroyBlockImg()
        self.turn_on_cameras()
        self.get_arrivals()
        self.show_kpp_tree_btns()
        self.show_main_navbar_btns()
        self.show_time()

    def drawBlurScreen(self):
        super(KPP, self).drawBlurScreen()

    def openWin(self):
        super(KPP, self).openWin()
        if not self.clockLaunched:
            self.start_clock()
            self.clockLaunched = True
        self.get_arrivals()
        self.can.create_window(1038.5, 435, window=self.tree, tag='tree')
        self.draw_gate_arrows()
        self.show_widgets(self.page_widgets)
        self.show_kpp_tree_btns()
        if self.arriving_in_progress:
            self.create_abort_photocell_waiting_btn()
        self.show_main_navbar_btns()

    def page_close_operations(self):
        super(KPP, self).page_close_operations()
        self.delete_abort_photocell_waiting_btn()
        self.operator.turn_cams(False)
        self.hide_kpp_tree_btns()
        self.root.unbind("Escape")
        self.hide_main_navbar_btns()


class KPPLift(Terminal):
    def __init__(self, root, settings, operator, can):
        super(KPPLift, self).__init__(root, settings, operator, can)
        self.name = 'KPPLift'
        self.page_buttons = self.create_btns_and_hide(
            [self.settings.kpp_lift_down_btn])
        self.gate_state = 'open'
        self.draw_elements = ["kpp_road", "lift_up_mode_background_text",
                              "kpp_barrier_base", "lift_up_timer_background"]
        self.hide_while_cam_zoom_widgets = []
        self.cameras = ["kpp_cam_internal", "kpp_cam_external"]

    def destroyBlockImg(self, mode="total"):
        super(KPPLift, self).destroyBlockImg()
        self.operator.turn_cams("kpp_cam_external")
        self.operator.turn_cams("kpp_cam_internal")
        self.show_main_navbar_btns()
        self.show_time()


    def cam_hide_callback(self, cam_type=None):
        super().cam_hide_callback(cam_type)
        self.turn_on_cameras()

    def start_timer(self, seconds=300):
        while seconds != 0:
            self.draw_timer(seconds)
            seconds -= 1
            time.sleep(1)
            if not self.operator.current == "KPPLift":
                self.operator.ar_qdk.execute_method(
                    "log_event", event="Таймер опускания шлагбаума в "
                                       "беспрепятственном доступе остановился, "
                                       "поскольку был переход между окнами")
                return
        self.auto_lift_down()

    def auto_lift_down(self):
        self.operator.ar_qdk.execute_method(
            "log_event", event="Таймер опускания шлагбаума в "
                               "беспрепятственном доступе истек")
        self.lift_down("auto")

    def draw_timer(self, seconds_left):
        minutes = 0
        if self.blockImgDrawn or self.operator.kpp_page.cam_zoom:
            return
        if seconds_left > 60:
            minutes = int(seconds_left / 60)
            seconds_left = seconds_left % 60
        if minutes:
            text = f"До закрытия шлагбаума: {minutes} мин {seconds_left} сек"
        else:
            text = f"До закрытия шлагбаума: {seconds_left} сек"
        self.can.delete("kpp_lift_timer")
        self.can.create_text(
            1053, 625, text=text, anchor='n', font=fonts.kpp_lift_up_timer,
            fill="#F2F2F2",
            tags=("page_elements", "kpp_lift_timer"))

    def openWin(self):
        super().openWin()
        self.operator.turn_cams("kpp_external")
        self.operator.turn_cams("kpp_internal")
        # self.operator.kpp_page.open_barrier()
        self.operator.ar_qdk.execute_method("kpp_lift_up")
        threading.Thread(target=self.start_timer, args=(300,)).start()
        self.show_main_navbar_btns()

    def page_close_operations(self):
        super(KPPLift, self).page_close_operations()
        self.hide_main_navbar_btns()

    def lift_down(self, mode="manual"):
        self.operator.ar_qdk.execute_method("kpp_lift_down", mode=mode)
        self.page_close_operations()
        # self.operator.kpp_page.close_barrier()
        self.operator.kpp_page.openWin()

    def after_destroy_block_operations(self):
        self.turn_on_cameras()
