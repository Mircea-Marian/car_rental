from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Rectangle

from datetime import datetime

import cx_Oracle

def logInFunc(instance):
    con = cx_Oracle.connect('hr', 'AAaa12345', 'localhost:1521/ORCL')
    cur = con.cursor()

    loginInfoIsOk =\
    cur.callfunc("hr.proj_bd2.checkCredentials", cx_Oracle.NUMBER, [instance.parent.username.text, instance.parent.password.text])

    cur.close()
    con.close()

    if loginInfoIsOk == 1:
        clearAllFields(instance)
        instance.parent.intManager.clear_widgets()
        instance.parent.intManager.add_widget(instance.parent.intManager.searchScreen)
    else:
        popup = Popup(
            title='Error !',
            content=Label(text='Wrong username or password !'),
            size_hint=(None, None),
            size=(400, 400)
        )
        popup.open()

def logOutFunc(instance):
    instance.parent.intManager.clear_widgets()
    instance.parent.intManager.add_widget(instance.parent.intManager.logInScreen)

def reqRes(instance):
    con = cx_Oracle.connect('hr', 'AAaa12345', 'localhost:1521/ORCL')
    cur = con.cursor()

    global p_start_date , p_start_city ,p_end_date ,p_end_city ,p_end_street ,p_end_number

    # p_start_date = datetime.strptime(instance.parent.startDate.text, '%d-%b-%Y %I')
    # p_start_city = instance.parent.startCity.text
    # p_end_date = datetime.strptime(instance.parent.endDate.text, '%d-%b-%Y %I')
    # p_end_city = instance.parent.endCity.text
    # p_end_street = instance.parent.endStreet.text
    # p_end_number = int(instance.parent.endNumber.text)

    # rez = cur.callfunc(
    #     "hr.proj_bd2.get_ups",
    #     cx_Oracle.CURSOR,
    #     [
    #         p_start_date,
    #         p_start_city,
    #         p_end_date,
    #         instance.parent.brand.text,
    #         instance.parent.model.text,
    #         instance.parent.fuel.text,
    #         instance.parent.doorsBtn.text,
    #         instance.parent.car_type.text,
    #     ]
    # )

    p_start_date = datetime.strptime('10-JAN-2018 12', '%d-%b-%Y %I')
    p_start_city = 'Bucharest'
    p_end_date = datetime.strptime('13-JAN-2018 12', '%d-%b-%Y %I')
    p_end_city = 'Bucharest'
    p_end_street = 'Calea Victoriei'
    p_end_number = 23

    rez = cur.callfunc(
        "hr.proj_bd2.get_ups",
        cx_Oracle.CURSOR,
        [
            datetime.strptime('10-JAN-2018 12', '%d-%b-%Y %I'),
            'Bucharest',
            datetime.strptime('13-JAN-2018 12', '%d-%b-%Y %I'),
            "",
            "",
            "",
            "Any",
            "",
        ]
    )

    instance.parent.intManager.clear_widgets()
    instance.parent.intManager.add_widget(ReservationSet(instance.parent.intManager,rez, instance.parent))

    cur.callproc("hr.close_cursor", [rez])
    del rez
    cur.close()
    con.close()

class FeedBackButton(Button):
    def __init__(self, **kwargs):
        super(FeedBackButton, self).__init__(**kwargs)
        self.selectDropdown = DropDown()

        for i in range(5):
            twoBtn = Button(text=str(i+1), font_size=14, size_hint_y=None, height=30, background_color=(1.0, 0.0, 0.0, 1.0))
            twoBtn.bind(on_release=lambda btn: self.selectDropdown.select(btn.text))
            self.selectDropdown.add_widget(twoBtn);

        self.bind(on_release=self.selectDropdown.open)
        self.selectDropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))

def submitFeedback(instance):
    con = cx_Oracle.connect('hr', 'AAaa12345', 'localhost:1521/ORCL')
    cur = con.cursor()

    print instance.parent.resID.text + " " + instance.parent.intQualityBtn.text

    cur.callproc("hr.proj_bd2.updateStatistics",\
        [\
            instance.parent.resID.text,\
            int(instance.parent.intQualityBtn.text),\
            int(instance.parent.extQualityBtn.text),\
            int(instance.parent.engineBtn.text),\
        ]\
    )

    cur.close()
    con.close()

def backUp(instance):
    instance.parent.intManager.clear_widgets()
    instance.parent.intManager.add_widget(instance.parent.intManager.searchScreen)

class FeedbackScreen(GridLayout):
    def __init__(self, intManager,**kwargs):
        super(FeedbackScreen, self).__init__(**kwargs)

        self.intManager = intManager

        self.cols = 2

        self.add_widget(Label(text='Reservation ID:'))
        self.resID = TextInput(multiline=False)
        self.add_widget(self.resID)

        self.add_widget(Label(text='What do you think of the interior quality ?'))
        self.intQualityBtn = FeedBackButton(text='1', font_size=14, background_color=(0.0, 0.0, 1.0, 1.0))
        self.add_widget(self.intQualityBtn)

        self.add_widget(Label(text='What do you think of the exterior quality ?'))
        self.extQualityBtn = FeedBackButton(text='1', font_size=14, background_color=(0.0, 0.0, 1.0, 1.0))
        self.add_widget(self.extQualityBtn)

        self.add_widget(Label(text='What do you think of the engine quality ?'))
        self.engineBtn = FeedBackButton(text='1', font_size=14, background_color=(0.0, 0.0, 1.0, 1.0))
        self.add_widget(self.engineBtn)

        self.submitBtn = Button(text='Submit feedback')
        self.submitBtn.bind(on_press=submitFeedback)
        self.add_widget(self.submitBtn)

        self.backBtn = Button(text='Back')
        self.backBtn.bind(on_press=backUp)
        self.add_widget(self.backBtn)

class ReservationSet(GridLayout):
    def __init__(self, intManager, cursor, caller,**kwargs):
        super(ReservationSet, self).__init__(**kwargs)

        self.intManager = intManager;
        self.caller = caller

        self.cols = 8

        for colName in (\
            "Number",\
            "Plate Number",\
            "Brand",\
            "Model",\
            "Type of Fuel",\
            "Number of doors",\
            "Type of car",\
            "Price",\
            ):
             self.add_widget(MyLabel(\
                text="[color=FD0000]" + colName + "[/color]",\
                markup=True,\
                font_size=20,\
                underline=True,multiline=True))

        self.cursorList = []

        selectDropdown = DropDown()
        counter = 0
        ff = 0
        for row in cursor:
            self.cursorList.append(row)
            self.add_widget(
                    MyLabelAlt1(text=str(counter)) if ff == 0 else
                    MyLabelAlt2(text=str(counter))
            )
            for el in row:
                self.add_widget(
                    MyLabelAlt1(text=str(el)) if ff == 0 else
                    MyLabelAlt2(text=str(el))
                )
            ff = (ff + 1)%2

            twoBtn = Button(text=str(counter), font_size=14, size_hint_y=None, height=30, background_color=(1.0, 0.0, 0.0, 1.0))
            twoBtn.bind(on_release=lambda btn: selectDropdown.select(btn.text))
            selectDropdown.add_widget(twoBtn);
            counter = counter + 1

        self.selectionBtn = Button(text='1', font_size=14, background_color=(0.0, 0.0, 1.0, 1.0))
        self.selectionBtn.bind(on_release=selectDropdown.open)
        selectDropdown.bind(on_select=lambda instance, x: setattr(self.selectionBtn, 'text', x))
        self.add_widget(self.selectionBtn)

        submitBtn = Button(text='Make reservation', font_size=14)
        submitBtn.bind(on_press=processReservation)
        self.add_widget(submitBtn)

        backBtn = Button(text='Back', font_size=14)
        backBtn.bind(on_press=backCall)
        self.add_widget(backBtn)

def processReservation(instance):
    global p_start_date , p_start_city ,p_end_date ,p_end_city ,p_end_street ,p_end_number
    con = cx_Oracle.connect('hr', 'AAaa12345', 'localhost:1521/ORCL')
    cur = con.cursor()

    rezId = "nimica"

    rezId = cur.callfunc(\
        "hr.proj_bd2.manageReservation",\
        cx_Oracle.STRING,\
        [\
            instance.parent.cursorList[int(instance.parent.selectionBtn.text)][0],\
            p_start_date,\
            p_start_city,\
\
            p_end_date,\
            p_end_city,\
            p_end_street,\
            23\
        ]\
    )

    print rezId

    popup = Popup(
            title='Reservation ID',
            content=Label(text=('Code: ' + rezId) if rezId != "0" else 'Unable to make reservation !'),
            size_hint=(None, None),
            size=(400, 400)
        )
    popup.open()

    cur.close()
    con.close()

def showStats(instance):
    con = cx_Oracle.connect('hr', 'AAaa12345', 'localhost:1521/ORCL')
    cur = con.cursor()

    rez = cur.callfunc("hr.proj_bd2.get_statistics", cx_Oracle.CURSOR)

    instance.parent.intManager.clear_widgets()
    instance.parent.intManager.add_widget(\
        ReportScreen(\
            instance.parent.intManager,\
            instance.parent,\
            (\
                "Brand",\
                "Model",\
                "Number of requests",\
                "Interior Quality",\
                "Exterior Quality",\
                "Engine Quality",\
            ),\
            rez\
        )\
    )

    cur.callproc("hr.close_cursor", [rez])

    del rez

    cur.close()
    con.close()

def showCars(instance):
    con = cx_Oracle.connect('hr', 'AAaa12345', 'localhost:1521/ORCL')
    cur = con.cursor()

    rez = cur.callfunc("hr.proj_bd2.get_car_details", cx_Oracle.CURSOR)

    instance.parent.intManager.clear_widgets()
    instance.parent.intManager.add_widget(\
        ReportScreen(\
            instance.parent.intManager,\
            instance.parent,\
            (\
                "Brand",\
                "Model",\
                "Type of Fuel",\
                "Number of doors",\
                "Type of car",\
            ),\
            rez\
        )\
    )

    cur.callproc("hr.close_cursor", [rez])

    del rez

    cur.close()
    con.close()

def clearAllFields(instance):
    for child in instance.parent.children:
        if child.__class__.__name__ == "TextInput":
            child.text = ""
    if instance.parent.__class__.__name__ == "SelectionFields":
        instance.parent.doorsBtn.text = "Any"

class MyLabel(Label):
    def __init__(self, **kwargs):
        super(MyLabel, self).__init__(**kwargs)

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 1, 0.25)
            Rectangle(pos=self.pos, size=self.size)

class MyLabelAlt1(Label):
    def __init__(self, **kwargs):
        super(MyLabelAlt1, self).__init__(**kwargs)

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 1, 1, 0.25)
            Rectangle(pos=self.pos, size=self.size)

class MyLabelAlt2(Label):
    def __init__(self, **kwargs):
        super(MyLabelAlt2, self).__init__(**kwargs)

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 0, 1, 0.25)
            Rectangle(pos=self.pos, size=self.size)

def backCall(instance):
    instance.parent.intManager.clear_widgets()
    instance.parent.intManager.add_widget(instance.parent.caller)

class ReportScreen(GridLayout):
    def __init__(self, intManager, p_parent, columnNames, cursor,**kwargs):
        super(ReportScreen, self).__init__(**kwargs)
        self.intManager = intManager

        self.caller = p_parent

        self.cols = len(columnNames)

        for colName in columnNames:
             self.add_widget(MyLabel(\
                text="[color=FD0000]" + colName + "[/color]",\
                markup=True,\
                font_size=20,\
                underline=True))

        ff = 0
        for row in cursor:
            for el in row:
                self.add_widget(\
                    MyLabelAlt1(text=str(el)) if ff == 0 else
                    MyLabelAlt2(text=str(el))
                )
            ff = (ff + 1)%2

        backBtn = Button(text='Back', font_size=14)
        backBtn.bind(on_press=backCall)
        self.add_widget(backBtn)

class LoginScreen(GridLayout):
    def __init__(self, intManager,**kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        self.intManager = intManager

        self.cols = 2

        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text='Password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        btn1 = Button(text='Log  in', font_size=14)
        btn1.bind(on_press=logInFunc)
        self.add_widget(btn1)

        clearBtn = Button(text='Clear all fields', font_size=14)
        clearBtn.bind(on_press=clearAllFields)
        self.add_widget(clearBtn)

class SelectionFields(GridLayout):
    def __init__(self, intManager, **kwargs):
        super(SelectionFields, self).__init__(**kwargs)
        self.intManager = intManager

        self.cols = 2

        self.add_widget(Label(text='[color=ff3333]Start Date[/color]', markup=True))
        self.startDate = TextInput(multiline=False)
        self.add_widget(self.startDate)

        self.add_widget(Label(text='[color=ff3333]Start City[/color]', markup=True))
        self.startCity = TextInput(multiline=False)
        self.add_widget(self.startCity)

        self.add_widget(Label(text='[color=ff3333]End Date[/color]', markup=True))
        self.endDate = TextInput(multiline=False)
        self.add_widget(self.endDate)

        self.add_widget(Label(text='[color=ff3333]End City[/color]', markup=True))
        self.endCity = TextInput(multiline=False)
        self.add_widget(self.endCity)

        self.add_widget(Label(text='[color=ff3333]End Street[/color]', markup=True))
        self.endStreet = TextInput(multiline=False)
        self.add_widget(self.endStreet)

        self.add_widget(Label(text='[color=ff3333]End Number[/color]', markup=True))
        self.endNumber = TextInput(multiline=False)
        self.add_widget(self.endNumber)

        self.add_widget(Label(text='Brand'))
        self.brand = TextInput(multiline=False)
        self.add_widget(self.brand)

        self.add_widget(Label(text='Model'))
        self.model = TextInput(multiline=False)
        self.add_widget(self.model)

        self.add_widget(Label(text='Fuel Type'))
        self.fuel = TextInput(multiline=False)
        self.add_widget(self.fuel)

        self.add_widget(Label(text='Number of doors'))

        doorsDropdown = DropDown()

        twoBtn = Button(text='2', font_size=14, size_hint_y=None, height=30, background_color=(1.0, 0.0, 0.0, 1.0))
        twoBtn.bind(on_release=lambda btn: doorsDropdown.select(btn.text))
        doorsDropdown.add_widget(twoBtn);

        fourBtn = Button(text='4', font_size=14, size_hint_y=None, height=30, background_color=(1.0, 0.0, 0.0, 1.0))
        fourBtn.bind(on_release=lambda btn: doorsDropdown.select(btn.text))
        doorsDropdown.add_widget(fourBtn);

        anyDoorBtn = Button(text='Any', font_size=14, size_hint_y=None, height=30, background_color=(1.0, 0.0, 0.0, 1.0))
        anyDoorBtn.bind(on_release=lambda btn: doorsDropdown.select(btn.text))
        doorsDropdown.add_widget(anyDoorBtn);

        self.doorsBtn = Button(text='Any', font_size=14, background_color=(0.0, 0.0, 1.0, 1.0))
        self.doorsBtn.bind(on_release=doorsDropdown.open)
        doorsDropdown.bind(on_select=lambda instance, x: setattr(self.doorsBtn, 'text', x))
        self.add_widget(self.doorsBtn)

        self.add_widget(Label(text='Type of car'))
        self.car_type = TextInput(multiline=False)
        self.add_widget(self.car_type)

        self.add_widget(Label(text='[color=ff3333]^^^ Fields marked with red must be filled in ! ^^^[/color]', markup=True))

        btn1 = Button(text='Log  out', font_size=14)
        btn1.bind(on_press=logOutFunc)
        self.add_widget(btn1)

        submitBtn = Button(text='Submit', font_size=14)
        submitBtn.bind(on_press=reqRes)
        self.add_widget(submitBtn)

        clearBtn = Button(text='Clear all fields', font_size=14)
        clearBtn.bind(on_press=clearAllFields)
        self.add_widget(clearBtn)

        statsBtn = Button(text='Show Statistics', font_size=14)
        statsBtn.bind(on_press=showStats)
        self.add_widget(statsBtn)

        showCarsBtn = Button(text='Show available cars', font_size=14)
        showCarsBtn.bind(on_press=showCars)
        self.add_widget(showCarsBtn)

        feedbackBtn = Button(text='Feedback', font_size=14)
        feedbackBtn.bind(on_press=switchToFeedback)
        self.add_widget(feedbackBtn)

def switchToFeedback(instance):
    instance.parent.intManager.clear_widgets()
    instance.parent.intManager.add_widget(instance.parent.intManager.feedbackScreen)

class InterfaceManager(BoxLayout):
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        self.col = 1
        self.logInScreen = LoginScreen(self)
        self.searchScreen = SelectionFields(self)
        self.feedbackScreen = FeedbackScreen(self)
        self.add_widget(self.logInScreen)

class MyApp(App):

    def build(self):
        return InterfaceManager(orientation='vertical')

if __name__ == '__main__':
    MyApp().run()