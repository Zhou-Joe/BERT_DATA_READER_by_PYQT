#coding:utf-8

import accdata
import matplotlib
import MplPlot
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np

colors = ['k', 'r', 'g', 'b', 'm', 'maroon', 'grey']

colors_code= ['#000000','#FF0000','#008000','#0000FF','#FF00FF','#800000','#808080']



class truncateTimeWindow(QtWidgets.QDialog):
    def __init__(self, mainui, data):
        super(truncateTimeWindow, self).__init__()
        overalllayout = QtWidgets.QGridLayout()
        lb_starttime = QtWidgets.QLabel('Start Time: ', self)
        lb_endtime = QtWidgets.QLabel('End Time: ', self)
        self.input_starttime = QtWidgets.QSpinBox()
        self.input_endtime = QtWidgets.QSpinBox()
        self.input_starttime.setRange(0,10000)
        self.input_endtime.setRange(0, 10000)
        ok_button = QtWidgets.QPushButton('OK', self)
        ok_button.clicked.connect(lambda: self.ok_bt_func(mainui=mainui, data=data))
        cancel_button = QtWidgets.QPushButton('Cancel', self)
        cancel_button.clicked.connect(lambda: self.cancel_bt_func())
        overalllayout.addWidget(lb_starttime, 0, 0)
        overalllayout.addWidget(lb_endtime, 1, 0)
        overalllayout.addWidget(self.input_starttime, 0, 1)
        overalllayout.addWidget(self.input_endtime, 1, 1)
        overalllayout.addWidget(ok_button, 0, 2)
        overalllayout.addWidget(cancel_button, 1, 2)
        self.setLayout(overalllayout)

    def ok_bt_func(self, mainui, data):
        try:
            data.truncate_data(starttime=self.input_starttime.value(), endtime=self.input_endtime.value())
            mainui.trendplot.initplotxyz()
            mainui.clearlayout(mainui.statlayout)
            mainui.replot_all()
            self.close()

        except Exception as e:
            pass

    def cancel_bt_func(self):
        self.close()

class inputExportFilename(QtWidgets.QDialog):
    def __init__(self, mainui, data):
        super(inputExportFilename, self).__init__()
        overalllayout = QtWidgets.QGridLayout()
        self.lb_inputfilename = QtWidgets.QLabel('Input Filename: ', self)
        self.input_filename = QtWidgets.QLineEdit()
        self.suffix = QtWidgets.QComboBox(self)
        self.suffix.addItems(['.sup', '.sups', '.txt'])
        ok_button = QtWidgets.QPushButton('OK', self)
        ok_button.clicked.connect(lambda: self.ok_bt_func(mainui=mainui, data=data))
        cancel_button = QtWidgets.QPushButton('Cancel', self)
        cancel_button.clicked.connect(lambda: self.cancel_bt_func())
        overalllayout.addWidget(self.lb_inputfilename, 0, 0, 1, 2)
        overalllayout.addWidget(self.input_filename, 1, 0)
        overalllayout.addWidget(self.suffix, 1,1)
        overalllayout.addWidget(ok_button, 2, 0)
        overalllayout.addWidget(cancel_button, 2, 1)
        self.setLayout(overalllayout)

    def ok_bt_func(self, mainui, data):
        try:
            data.export_to_file(path=self.input_filename.text() + self.suffix.currentText())

            self.close()

        except Exception as e:
            pass

    def cancel_bt_func(self):
        self.close()


class inputEditData(QtWidgets.QWidget):
    def __init__(self, mainui, data):
        super(inputEditData, self).__init__()
        overalllayout = QtWidgets.QGridLayout()
        lb_add = QtWidgets.QLabel('Add a value to: ', self)
        lb_multiply = QtWidgets.QLabel('Multiply a value to ')
        lb_addx = QtWidgets.QLabel('Add to Fore\Back (x)')
        lb_addy = QtWidgets.QLabel('Add to Left\Right (y)')
        lb_addz = QtWidgets.QLabel('Add to Up\Down (z)')

        self.input_addx=QtWidgets.QDoubleSpinBox()
        self.input_addy = QtWidgets.QDoubleSpinBox()
        self.input_addz = QtWidgets.QDoubleSpinBox()

        lb_mulx = QtWidgets.QLabel('Multiply to Fore\Back (x)')
        lb_muly = QtWidgets.QLabel('Multiply to Left\Right (y)')
        lb_mulz = QtWidgets.QLabel('Multiply to Up\Down (z)')

        self.input_mulx = QtWidgets.QDoubleSpinBox()
        self.input_muly = QtWidgets.QDoubleSpinBox()
        self.input_mulz = QtWidgets.QDoubleSpinBox()

        for spinbox in [self.input_addz, self.input_addy, self.input_addx, self.input_mulx, self.input_muly, self.input_mulz]:
            spinbox.setRange(-5, 5)
            if spinbox in [self.input_mulx, self.input_muly, self.input_mulz]:
                spinbox.setValue(1)


        ok_button1 = QtWidgets.QPushButton('Apply Add', self)
        ok_button1.clicked.connect(lambda: self.ok_bt_func1(mainui=mainui, data=data))

        ok_button2 = QtWidgets.QPushButton('Apply Multiply', self)
        ok_button2.clicked.connect(lambda: self.ok_bt_func2(mainui=mainui, data=data))

        cancel_button = QtWidgets.QPushButton('Close', self)
        cancel_button.clicked.connect(lambda: self.cancel_bt_func())


        overalllayout.addWidget(lb_add, 0, 0)
        overalllayout.addWidget(lb_addx, 1, 0)
        overalllayout.addWidget(lb_addy, 2, 0)
        overalllayout.addWidget(lb_addz, 3, 0)
        overalllayout.addWidget(self.input_addx, 1, 1)
        overalllayout.addWidget(self.input_addy, 2, 1)
        overalllayout.addWidget(self.input_addz, 3, 1)

        overalllayout.addWidget(lb_multiply, 4, 0)
        overalllayout.addWidget(lb_mulx, 5, 0)
        overalllayout.addWidget(lb_muly, 6, 0)
        overalllayout.addWidget(lb_mulz, 7, 0)

        overalllayout.addWidget(self.input_mulx, 5, 1)
        overalllayout.addWidget(self.input_muly, 6, 1)
        overalllayout.addWidget(self.input_mulz, 7, 1)



        overalllayout.addWidget(ok_button1, 0, 2)
        overalllayout.addWidget(ok_button2, 4, 2)
        overalllayout.addWidget(cancel_button, 7, 2)
        self.setLayout(overalllayout)

    def ok_bt_func1(self, mainui, data):
        try:
            data.edit_data(method='add', value_array=[self.input_addx.value(), self.input_addy.value(), self.input_addz.value()])
            mainui.trendplot.initplotxyz()
            mainui.clearlayout(mainui.statlayout)
            mainui.replot_all()
        except Exception as e:
            print (e)

    def ok_bt_func2(self, mainui, data):
        try:
            data.edit_data(method='multiply',
                           value_array=[self.input_mulx.value(), self.input_muly.value(), self.input_mulz.value()])
            mainui.trendplot.initplotxyz()
            mainui.clearlayout(mainui.statlayout)

            mainui.replot_all()
        except Exception as e:
            print (e)

    def cancel_bt_func(self):
        self.close()










class inputAngleWindow(QtWidgets.QDialog):
    def __init__(self, data, mainui):
        super(inputAngleWindow, self).__init__()
        overalllayout = QtWidgets.QGridLayout()
        lb_pitch_angle = QtWidgets.QLabel('Pitch Angle (°): ', self)
        lb_seatback_angle = QtWidgets.QLabel('Seatback Angle (°): ', self)
        lb_roll_angle = QtWidgets.QLabel('Roll Angle (°): ', self)
        lb_yaw_angle = QtWidgets.QLabel('Yaw Angle (°): ', self)

        self.input_pitch = QtWidgets.QSpinBox()
        self.input_seatback = QtWidgets.QSpinBox()
        self.input_roll = QtWidgets.QSpinBox()
        self.input_yaw = QtWidgets.QSpinBox()
        for spinbox in [self.input_pitch, self.input_roll, self.input_seatback, self.input_yaw]:
            spinbox.setRange(-180, 180)
        ok_button = QtWidgets.QPushButton('OK', self)
        ok_button.clicked.connect(lambda: self.ok_bt_func(data, mainui))
        cancel_button = QtWidgets.QPushButton('Cancel', self)
        cancel_button.clicked.connect(lambda: self.cancel_bt_func())
        overalllayout.addWidget(lb_pitch_angle, 0, 0)
        overalllayout.addWidget(lb_seatback_angle, 1, 0)
        overalllayout.addWidget(lb_roll_angle, 2, 0)
        overalllayout.addWidget(lb_yaw_angle, 3, 0)
        overalllayout.addWidget(self.input_pitch, 0, 1)
        overalllayout.addWidget(self.input_seatback, 1, 1)
        overalllayout.addWidget(self.input_roll, 2, 1)
        overalllayout.addWidget(self.input_yaw, 3, 1)
        overalllayout.addWidget(ok_button, 0, 2)
        overalllayout.addWidget(cancel_button, 1,2)

        self.setLayout(overalllayout)

    def ok_bt_func(self, data, mainui):
        try:
            data.reformat(overwrite = True, setting_angle=True, pitch_angle=int(self.input_pitch.value()),
                          seatback_angle=int(self.input_seatback.value()), roll_angle=int(self.input_roll.value()),
                          yaw_angle=int(self.input_yaw.value()))
            mainui.trendplot.initplotxyz()
            mainui.clearlayout(mainui.statlayout)

            mainui.replot_all()



            self.close()

        except Exception as e:
            pass

    def cancel_bt_func(self):
        self.close()




class exportWindow(QtWidgets.QDialog):
    def __init__(self, data):
        super(exportWindow, self).__init__()
        overalllayout = QtWidgets.QGridLayout()


class infobar_content(QtWidgets.QWidget):
    def __init__(self, data, plottype, statlayout, plot_order, func_remove, mainui):
        label = QtWidgets.QLabel()
        label.setMaximumHeight(65)
        label.setStyleSheet("color:{};font-size:11px;".format(colors_code[plot_order-1]));
        label.setText(data.get_angle_info())
        label.setAutoFillBackground(True)
        label.setMaximumWidth(300)
        label.setWordWrap(True)
        statlayout.addWidget(label)
        table = QtWidgets.QTableView()
        table.setFixedHeight(80)
        table.setFixedWidth(300)
        if plottype is "Standard":
            model = DataStatusTable(data.get_data_stats(data.std_data))
        elif plottype is "Raw":
            model = DataStatusTable(data.get_data_stats(data.data))
        elif plottype is "Filter":
            model = DataStatusTable(data.get_data_stats(data.filtered_data))
        table.setModel(model)

        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        statlayout.addWidget(table)
        statlayout.setAlignment(QtCore.Qt.AlignTop)

        btlayout = QtWidgets.QHBoxLayout()
        btlayout.setSpacing(1)

        bt_export = QtWidgets.QPushButton("Export")
        bt_export.clicked.connect(lambda: self.popupInputFilename(data=data, mainui=mainui))
        bt_edit = QtWidgets.QPushButton("Edit Angle")
        bt_edit.clicked.connect(lambda: self.popupInputAngle(data, mainui))
        bt_remove = QtWidgets.QPushButton("Remove")
        bt_remove.clicked.connect(func_remove)
        bt_truncate = QtWidgets.QPushButton('Truncate')
        bt_truncate.clicked.connect(lambda: self.popupInputTime(data=data, mainui=mainui))
        bt_manipulate = QtWidgets.QPushButton('Modify')
        bt_manipulate.clicked.connect(lambda: self.popupEditData(data=data, mainui=mainui))


        for bt in [bt_truncate, bt_edit, bt_export, bt_remove, bt_manipulate]:
            bt.setStyleSheet("QPushButton{font-size:10px;}")
            bt.setFixedWidth(50)
        btlayout.addWidget(bt_truncate)
        btlayout.addWidget(bt_edit)
        btlayout.addWidget(bt_manipulate)
        btlayout.addWidget(bt_remove)
        btlayout.addWidget(bt_export)



        statlayout.addLayout(btlayout)

    def popupEditData(self, data, mainui):
        try:
            self.win = inputEditData(data=data, mainui=mainui)
            self.win.show()
        except Exception as e:
            print(e)


    def popupInputFilename(self, data, mainui):
        try:
            win = inputExportFilename(data=data, mainui=mainui)
            win.show()
        except Exception as e:
            pass

    def popupInputAngle(self, data, mainui):
        try:
            win = inputAngleWindow(data, mainui)
            win.show()

        except Exception as e:
            pass

    def popupInputTime(self, mainui, data):
        try:
            win = truncateTimeWindow(mainui, data)
            win.show()
        except Exception as e:
            pass




class DataStatusTable(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(DataStatusTable, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return str(value)

    def rowCount(self, index):
        # The length of the outer list.
        return self._data.shape[0]

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == QtCore.Qt.Vertical:
                return str(self._data.index[section])

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Ui_MainWindow, self).__init__(*args, **kwargs)
        self.plottype = "Standard"
        self.annot_mode = "Single"
        self.select_plot_tab2 = QtWidgets.QComboBox()
        self.select_plot_tab3 = QtWidgets.QComboBox()
        self.select_plot_tab4 = QtWidgets.QComboBox()
        self.stat_content=[]
        self.data_namelist=[]
        self.datadict=dict()
        self.setupUi()
        self.init_plotdata()


    def init_plotdata(self):
        self.datalist = []

    def setupUi(self):
        self.resize(1600, 1280)
        self.centralwidget = QtWidgets.QWidget(self)
        self.overallLayout = QtWidgets.QHBoxLayout()
        self.centralwidget.setLayout(self.overallLayout)
        self.setCentralWidget(self.centralwidget)
        self.scrollbar = QtWidgets.QScrollArea(self)
        self.statlayout = QtWidgets.QVBoxLayout()
        self.overallLayout.addWidget(self.scrollbar)
        self.scrollbar.setFixedWidth(300)
        self.scrollbar.setWidgetResizable(True)
        widget=QtWidgets.QWidget()
        widget.setLayout(self.statlayout)
        self.scrollbar.setWidget(widget)
        self.set_toolbar()
        self.set_tabUI()


    def set_toolbar(self):
        toolbar = QtWidgets.QToolBar('Toolbar')
        self.addToolBar(toolbar)

        button_add_rawdata = QtWidgets.QAction("Add Raw Data |", self)
        button_add_rawdata.triggered.connect(lambda: self.openraw())

        button_add_data = QtWidgets.QAction("Add Accel Data |", self)
        button_add_data.setStatusTip("Add Standard Acceleration Data")
        button_add_data.triggered.connect(lambda: self.openandplot())


        button_clear = QtWidgets.QAction("Clear all|", self)
        button_clear.setStatusTip("Clear all Datasets")
        button_clear.triggered.connect(lambda: self.resettrendplot(reset_datalist=True))

        toolbar.addAction(button_add_rawdata)
        toolbar.addAction(button_add_data)
        toolbar.addAction(button_clear)

        self.annot_text=QtWidgets.QLabel('(Currently: {})'.format(self.annot_mode), self)
        self.annot_text.setStyleSheet("color:#ff0000;");

        annot_switch = QtWidgets.QAction("Switch Annotation Mode", self)
        annot_switch.triggered.connect(self.switch_annot_mode)
        toolbar.addAction(annot_switch)
        toolbar.addWidget(self.annot_text)


    def switch_annot_mode(self):
        if self.annot_mode is "Single":
            self.annot_mode = "Multiple"
        else:
            self.annot_mode = 'Single'

        for canvas in [self.canvasASTM,self.canvasGB, self.canvasAccZone, self.trendplot]:
            try:
                canvas.annot_mode=self.annot_mode
            except:
                pass
        self.annot_text.setText('Currently: {}'.format(self.annot_mode))



    def clearlayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clearlayout(item.layout())

    def set_infobar(self, data, plottype, plot_order):

        info = infobar_content(statlayout=self.statlayout,data=data, plottype=plottype,
                               plot_order=plot_order,func_remove=lambda:self.remove_button_func(plot_order),
                               mainui=self)
        self.stat_content.append(info)


    def reduce_data(self, plot_order):
        self.datalist.pop(plot_order-1)
        self.data_namelist.pop(plot_order - 1)
        self.datadict = dict(zip(self.data_namelist, self.datalist))


    def replot_all(self):
        i=1
        for d in self.datalist:
            self.addtrendplot(data=d, plottype=self.plottype, plot_order=i)
            i+=1


    def switch_to_fitmax(self, axis):
        if len(self.datalist)>1:
            self.trendplot.initplotxyz()
            self.clearlayout(self.statlayout)
            self.replot_fitmax(axis=axis)


    def replot_fitmax(self, axis):
        offset=np.array(self.get_argmax(axis=axis))-self.get_argmax(axis=axis)[0]
        i=1
        for d in self.datalist:
            self.addtrendplot_fitmax(data=d, plottype=self.plottype, plot_order=i, offset=offset[i-1])
            i+=1

    def addtrendplot_fitmax(self, data, plottype, plot_order, offset):
        try:
            if plottype is "Raw":
                self.trendplot.addplotxyz_fitmax(data.data, plot_order, offset)
            elif plottype is "Standard":
                self.trendplot.addplotxyz_fitmax(data.std_data, plot_order, offset)
            elif plottype is "Filter":
                self.trendplot.addplotxyz_fitmax(data.filtered_data, plot_order, offset)
            self.trendplot.draw_idle()
            self.set_infobar(data, plottype, plot_order)
        except Exception as e:
            pass

    def remove_button_func(self, plot_order):
        self.reduce_data(plot_order=plot_order)
        self.clearlayout(self.statlayout)

        self.stat_content=[]

        self.trendplot.initplotxyz()
        self.clearlayout(self.statlayout)
        self.replot_all()
        for combobox in [self.select_plot_tab2,self.select_plot_tab3, self.select_plot_tab4]:
            combobox.clear()
            combobox.addItems(self.datadict.keys())

    def set_tabUI(self):
        self.tabWidget = QtWidgets.QTabWidget()
        self.tab1 = QtWidgets.QWidget()



        self.label_type = QtWidgets.QLabel()
        self.label_type.setText("\tCurrent Plot Data Type: {}".format(self.plottype))

        self.label_type.setStyleSheet("color:#ff0000;");



        ##Tab3

        l3=QtWidgets.QAction('Select Data to Plot: ', self)
        self.tab3 = QtWidgets.QWidget()
        self.GBlayout=QtWidgets.QGridLayout(self.tab3)
        self.canvasGB = MplPlot.GBPlot()
        self.canvasGB.fig.canvas.mpl_connect("button_press_event", lambda: self.canvasGB.onclick)

        mpltoolbar3 = NavigationToolbar(self.canvasGB, self.tab3)
        toolbar_tab3=QtWidgets.QToolBar('Toolbar for Plot')
        toolbar_tab3.addAction(l3)
        gen_plot_tab3 = QtWidgets.QAction("\t\tGenerate/Update",self)
        gen_plot_tab3.triggered.connect(lambda: self.plotGB(canvas=self.canvasGB, combobox=self.select_plot_tab3))
        toolbar_tab3.addWidget(self.select_plot_tab3)
        toolbar_tab3.addAction(gen_plot_tab3)


        self.GBlayout.addWidget(toolbar_tab3)
        self.GBlayout.addWidget(self.canvasGB)
        self.GBlayout.addWidget(mpltoolbar3)
        self.tab3.setLayout(self.GBlayout)







        ##Tab 1
        button_raw = QtWidgets.QAction("Show Raw Data ", self)
        button_raw.triggered.connect(lambda: self.switch_to_plottype(plottype="Raw"))

        button_filter = QtWidgets.QAction("Filter Only ", self)
        button_filter.triggered.connect(lambda: self.switch_to_plottype(plottype="Filter"))

        button_stdformat = QtWidgets.QAction("Filter and Calibrate", self)
        button_stdformat.triggered.connect(lambda: self.switch_to_plottype(plottype="Standard"))

        button_fitmaxX = QtWidgets.QAction("Fit Max X", self)
        button_fitmaxX.triggered.connect(lambda: self.switch_to_fitmax(axis=1))

        button_fitmaxY = QtWidgets.QAction("Fit Max Y", self)
        button_fitmaxY.triggered.connect(lambda: self.switch_to_fitmax(axis=2))

        button_fitmaxZ = QtWidgets.QAction("Fit Max Z", self)
        button_fitmaxZ.triggered.connect(lambda: self.switch_to_fitmax(axis=3))


        toolbar_tab1 = QtWidgets.QToolBar('Toolbar for Plot')
        toolbar_tab1.autoFillBackground()
        toolbar_tab1.addAction(button_raw)
        toolbar_tab1.addAction(button_filter)
        toolbar_tab1.addAction(button_stdformat)
        toolbar_tab1.addAction(button_fitmaxX)
        toolbar_tab1.addAction(button_fitmaxY)
        toolbar_tab1.addAction(button_fitmaxZ)
        toolbar_tab1.addWidget(self.label_type)

        self.trendlayout = QtWidgets.QGridLayout(self.tab1)
        self.trendplot = MplPlot.MplCanvas()
        self.trendlayout.addWidget(toolbar_tab1)
        self.trendlayout.addWidget(self.trendplot)
        toolbar2 = NavigationToolbar(self.trendplot, self.tab1)
        self.trendlayout.addWidget(toolbar2)

        # Tab 4

        self.tab4 = QtWidgets.QWidget()
        l4 = QtWidgets.QAction('Select Data to Plot: ', self)
        self.AccZonelayout = QtWidgets.QGridLayout(self.tab4)
        self.canvasAccZone = MplPlot.AccZonePlot()
        self.canvasAccZone.fig.canvas.mpl_connect("button_press_event", self.canvasAccZone.onclick)

        mpltoolbar4 = NavigationToolbar(self.canvasAccZone, self.tab4)
        toolbar_tab4 = QtWidgets.QToolBar('Toolbar for Plot')
        toolbar_tab4.addAction(l4)
        gen_plot_tab4 = QtWidgets.QAction("Generate/Update", self)
        gen_plot_tab4.triggered.connect(lambda: self.plotGB(canvas=self.canvasAccZone, combobox=self.select_plot_tab4))

        toolbar_tab4.addWidget(self.select_plot_tab4)
        toolbar_tab4.addAction(gen_plot_tab4)
        self.AccZonelayout.addWidget(toolbar_tab4)
        self.AccZonelayout.addWidget(self.canvasAccZone)
        self.AccZonelayout.addWidget(mpltoolbar4)
###
        #tab2

        self.tab2 = QtWidgets.QWidget()

        l2 = QtWidgets.QAction('Select Data to Plot:  ', self)
        self.ASTMlayout = QtWidgets.QGridLayout(self.tab2)
        self.canvasASTM = MplPlot.ASTMPlot()
        self.canvasASTM.fig.canvas.mpl_connect("button_press_event", self.canvasASTM.onclick)

        mpltoolbar2 = NavigationToolbar(self.canvasASTM, self.tab4)
        toolbar_tab2 = QtWidgets.QToolBar('Toolbar for Plot')
        toolbar_tab2.addAction(l2)
        gen_plot_tab2 = QtWidgets.QAction("Generate/Update", self)
        gen_plot_tab2.triggered.connect(lambda: self.plotASTM(canvas=self.canvasASTM, name=self.select_plot_tab2))

        self.select_restraint = QtWidgets.QComboBox()
        self.select_restraint.addItems(['None','Individual Lower Body','Upper Body','Group Lower Body','Convenience Restraint','No Restraint'])

        self.select_cond = QtWidgets.QComboBox()
        self.select_cond.addItems(['Normal', 'E-Stop', 'Expected/Permitted Bumping'])

        self.height_input = QtWidgets.QSpinBox()
        toolbar_tab2.addAction(l2)
        toolbar_tab2.addWidget(self.select_plot_tab2)


        toolbar_tab2.addAction(QtWidgets.QAction('Select Restraint Type:  ', self))
        toolbar_tab2.addWidget(self.select_restraint)
        toolbar_tab2.addAction(QtWidgets.QAction('Select Run Condition:  ', self))
        toolbar_tab2.addWidget(self.select_cond)
        toolbar_tab2.addAction(QtWidgets.QAction('Input Patron Height: ', self))
        toolbar_tab2.addWidget(self.height_input)
        toolbar_tab2.addAction(gen_plot_tab2)
        self.ASTMlayout.addWidget(toolbar_tab2)
        self.ASTMlayout.addWidget(self.canvasASTM)
        self.ASTMlayout.addWidget(mpltoolbar2)









        self.overallLayout.addWidget(self.tabWidget, 1)
        self.tabWidget.addTab(self.tab1, "Trend")
        self.tabWidget.addTab(self.tab2, "Fit ASTM Contour")
        self.tabWidget.addTab(self.tab3, "Fit GB Contour")
        self.tabWidget.addTab(self.tab4, "Fit Acceleration Zone")




    def get_argmax(self, axis):
        arg_max=[]
        if self.plottype is "Raw":
            for data in self.datalist:
                arg_max.append(data.data.iloc[:,axis].idxmax())
        if self.plottype is "Standard":
            for data in self.datalist:
                arg_max.append(data.std_data.iloc[:,axis].idxmax())
        if self.plottype is "Filter":
            for data in self.datalist:
                arg_max.append(data.filtered_data.iloc[:,axis].idxmax())

        return arg_max


    def plotGB(self, canvas, combobox):
        try:
            data = self.datadict[combobox.currentText()]
            if self.plottype is "Standard":
                canvas.addplotxyz(data=data.std_data)
            elif self.plottype is "Filter":
                canvas.addplotxyz(data=data.filtered_data)
            elif self.plottype is "Raw":
                canvas.addplotxyz(data=data.data)
        except Exception as e:
            pass

    def plotASTM(self, canvas, name):
        try:
            data = self.datadict[name.currentText()]
            restraint = self.select_restraint.currentText()
            cond = self.select_cond.currentText()
            input_height = self.height_input.value()
            if self.plottype is "Standard":
                data=data.std_data
            elif self.plottype is "Filter":
                data=data.filtered_data
            elif self.plottype is "Raw":
                data=data.data

            canvas.addplotxyz(data=data, restraint = restraint, cond = cond, input_height = input_height)
        except Exception as e:
            pass


    def set_datalist(self, data):
        self.datalist.append(data)
        self.data_namelist.append(data.filename)
        self.datadict=dict(zip(self.data_namelist, self.datalist))
        for combobox in [self.select_plot_tab2,self.select_plot_tab3, self.select_plot_tab4]:
            combobox.clear()
            combobox.addItems(self.datadict.keys())







    def openandplot(self):
        options = QtWidgets.QFileDialog.Options()
        # options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Open File", "", "All Files (*)")
        if fileName:
            try:
                data = accdata.AccData(fileName)
                self.set_datalist(data)
                self.addtrendplot(data=self.datalist[-1], plottype=self.plottype, plot_order=len(self.datalist))
            except Exception as e:
                pass

    def openraw(self):
        options = QtWidgets.QFileDialog.Options()
        # options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Open File", "", "All Files (*)")
        if fileName:
            try:
                data = accdata.RawData(fileName)
                data_GB, data_ASTM = data.export_data()
                data_GB.reformat(overwrite=True, setting_angle=True, pitch_angle=0, seatback_angle=0, roll_angle=0,
                                 yaw_angle=0)
                data_ASTM.reformat(overwrite=True, setting_angle=True, pitch_angle=0, seatback_angle=0, roll_angle=0,
                                   yaw_angle=0)
                self.set_datalist(data_GB)

                self.set_datalist(data_ASTM)

                for i in [-2, -1]:
                    self.addtrendplot(data=self.datalist[i], plottype=self.plottype, plot_order=len(self.datalist)+i+1)

            except Exception as e:
                pass

    def switch_to_plottype(self, plottype):
        self.plottype = plottype
        self.label_type.setText("\tCurrent Plot Data Type: {}".format(self.plottype))
        self.trendplot.initplotxyz()
        self.clearlayout(self.statlayout)
        self.replot_all()


    def resettrendplot(self, reset_datalist=False):
        try:
            if reset_datalist is True:
                self.datalist = []
                self.data_namelist=[]
                self.datadict=dict()
                for combobox in [self.select_plot_tab2, self.select_plot_tab3, self.select_plot_tab4]:
                    combobox.clear()


            self.trendplot.initplotxyz()
            self.canvasASTM.initplotxyz()
            self.canvasGB.initplotxyz()
            self.canvasAccZone.initplotxyz()
            self.clearlayout(self.statlayout)
            self.trendplot.draw_idle()
            self.canvasAccZone.draw_idle()
            self.canvasGB.draw_idle()
            self.canvasASTM.draw_idle()
            
        except Exception as e:
            pass

    def addtrendplot(self, data, plottype, plot_order):
        try:
            if plottype is "Raw":
                self.trendplot.addplotxyz(data.data, plot_order)
            elif plottype is "Standard":
                self.trendplot.addplotxyz(data.std_data, plot_order)
            elif plottype is "Filter":
                self.trendplot.addplotxyz(data.filtered_data, plot_order)
            self.trendplot.draw_idle()
            self.set_infobar(data, plottype, plot_order)
        except Exception as e:
            pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())

