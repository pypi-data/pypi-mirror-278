# Python modules
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import qdarkstyle
import numpy as np
import matplotlib
import os
matplotlib.use('QT5Agg')
import pandas as pd
import matplotlib.backends.backend_qt5agg as backend_qt5agg
from matplotlib.figure import Figure
import sys
import threading
from PyQt5.QtWidgets import QPushButton, QSlider
from PyQt5 import QtGui, QtWidgets
# Local application modules
from resources import resources
from utils.sphere_response import SphereResponse
from PyQt5.QtWidgets import QMessageBox

APP_NAME = 'EM sphere-overburden response'
AUTHOR = 'Double Blind'


class OptionsMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Create the spinbox widgets used for inputting sphere-overburden parameters (thickness, conductivity)
        self.thick_ob_sb = QtWidgets.QDoubleSpinBox()
        self.sigma_sp_sb = QtWidgets.QDoubleSpinBox()
        self.sigma_ob_sb = QtWidgets.QDoubleSpinBox()
        self.strike = QtWidgets.QDoubleSpinBox()
        self.dip = QtWidgets.QDoubleSpinBox()
        self.dipole = QtWidgets.QDoubleSpinBox()
        self.pulse = QtWidgets.QDoubleSpinBox()
        self.a_sb = QtWidgets.QDoubleSpinBox()
        self.timedelta_sb = QtWidgets.QDoubleSpinBox()

        # Create text input widget for transmitter-receiver geometry
        # Set position / offset values using .setText
        self.tx = QtWidgets.QLineEdit()
        self.tx.setText('0,0,60')

        self.rx = QtWidgets.QLineEdit()
        self.rx.setText('0,0,120')

        self.txrx = QtWidgets.QLineEdit()
        self.txrx.setText('12.5,0,56')

        self.rspop = QtWidgets.QLineEdit()
        self.rspop.setText('-200')

        self.user_profile = QtWidgets.QLineEdit()
        self.user_profile.setText('1000')

        self.read_data_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/chart_line_delete.png'), 'Import Waveform Data',
        )

        self.PlotPoint = QtWidgets.QComboBox()
        PointList = ['Rx', 'Tx', 'Mid point']
        self.PlotPoint.addItems(PointList)

        self.Xconvention = QtWidgets.QComboBox()
        Sign = ["+ve", "-ve"]
        self.Xconvention.addItems(Sign)

        # Setting labels and positions of variables in widgets
        # Defining limits for integers values
        for widget in (self.thick_ob_sb, self.sigma_sp_sb, self.sigma_ob_sb, self.strike, self.dip, self.pulse,
                       self.dipole, self.a_sb, self.timedelta_sb):
            if widget == self.strike or widget == self.dip:
                widget.setRange(0, 360)
                widget.setSingleStep(1)
                widget.setDecimals(0)
            if widget == self.pulse:
                widget.setRange(0, 100000000)
                widget.setDecimals(8)
            if widget == self.timedelta_sb:
                widget.setRange(0, 1000)
                widget.setDecimals(4)
            if widget == self.a_sb:
                widget.setRange(0, 10000)
                widget.setDecimals(0)
                widget.setSingleStep(1)
            if widget == self.dipole:
                widget.setRange(0, 1000000000)
                widget.setDecimals(2)
            if widget == self.sigma_ob_sb:
                widget.setRange(0, 10000)
                widget.setDecimals(4)
            if widget == self.sigma_sp_sb:
                widget.setRange(0, 10000)
                widget.setDecimals(2)
                widget.setSingleStep(0.1)
            if widget == self.thick_ob_sb:
                widget.setRange(0.1, 10000)
                widget.setDecimals(6)
                widget.setSingleStep(0.1)

        coeff_grid = QtWidgets.QGridLayout()
        coeff_grid.addWidget(QtWidgets.QLabel('Transmitter Position(m)'), 0, 0)
        coeff_grid.addWidget(self.tx, 0, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Tx-Rx Offset (m)'), 1, 0)
        coeff_grid.addWidget(self.txrx, 1, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Overburden Conductivity (S/m)'), 2, 0)
        coeff_grid.addWidget(self.sigma_ob_sb, 2, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Overburden Thickness (m)'), 3, 0)
        coeff_grid.addWidget(self.thick_ob_sb, 3, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Sphere Conductivity (S/m)'), 4, 0)
        coeff_grid.addWidget(self.sigma_sp_sb, 4, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Sphere Radius (m)'), 5, 0)
        coeff_grid.addWidget(self.a_sb, 5, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Sphere Depth (m)'), 0, 2)  # a_sp
        coeff_grid.addWidget(self.rspop, 0, 3)
        coeff_grid.addWidget(QtWidgets.QLabel('Strike'), 1, 2)
        coeff_grid.addWidget(self.strike, 1, 3)
        coeff_grid.addWidget(QtWidgets.QLabel('Dip'), 2, 2)
        coeff_grid.addWidget(self.dip, 2, 3)
        coeff_grid.addWidget(QtWidgets.QLabel('Pulse Length'), 3, 2)
        coeff_grid.addWidget(self.pulse, 3, 3)
        coeff_grid.addWidget(QtWidgets.QLabel('Period'), 4, 2)
        coeff_grid.addWidget(self.timedelta_sb, 4, 3)
        coeff_grid.addWidget(QtWidgets.QLabel('Dipole Moment'), 5, 2)
        coeff_grid.addWidget(self.dipole, 5, 3)
        coeff_grid.addWidget(QtWidgets.QLabel('Profile length'), 6, 2)
        coeff_grid.addWidget(self.user_profile, 6, 3)
        coeff_grid.addWidget(QtWidgets.QLabel('Plotting point'), 6, 0)
        coeff_grid.addWidget(self.PlotPoint, 6, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('X sign convention'), 7, 0)
        coeff_grid.addWidget(self.Xconvention, 7, 1)
        coeff_grid.addWidget(self.read_data_btn, 7, 2, 1, 2)

        # Create the "Graph Options" widgets
        # Create checkbox for user to choose which components of response to plot
        self.sphere_x = QtWidgets.QCheckBox('x-component')
        self.sphere_x.setChecked(False)

        self.sphere_z = QtWidgets.QCheckBox('z-component')
        self.sphere_z.setChecked(False)

        self.sphere_y = QtWidgets.QCheckBox('y-component')
        self.sphere_y.setChecked(False)

        self.alltime = QtWidgets.QCheckBox('default')
        self.alltime.setChecked(True)

        self.earlytime = QtWidgets.QCheckBox('early')
        self.earlytime.setChecked(False)

        self.midtime = QtWidgets.QCheckBox('mid')
        self.midtime.setChecked(False)

        self.latetime = QtWidgets.QCheckBox('late')
        self.latetime.setChecked(False)

        self.alltime.stateChanged.connect(self.onWindowChange)
        self.earlytime.stateChanged.connect(self.onWindowChange)
        self.midtime.stateChanged.connect(self.onWindowChange)
        self.latetime.stateChanged.connect(self.onWindowChange)

        cb_box = QtWidgets.QHBoxLayout()
        cb_box.addWidget(self.sphere_x)
        cb_box.addWidget(self.sphere_z)
        cb_box.addWidget(self.sphere_y)

        legend_box = QtWidgets.QHBoxLayout()
        legend_box.addStretch()

        self.graph_box = QtWidgets.QVBoxLayout()
        self.graph_box.addLayout(cb_box)
        self.graph_box.addLayout(legend_box)
        self.graph_gb = QtWidgets.QGroupBox('Plot options')

        self.scaleLinear = QtWidgets.QCheckBox('linear')
        self.scaleLinear.setChecked(True)

        self.scaleLog = QtWidgets.QCheckBox('log')
        self.scaleLog.setChecked(False)

        self.scaleLog.stateChanged.connect(self.onScaleChange)
        self.scaleLinear.stateChanged.connect(self.onScaleChange)

        self.plotSphere = QtWidgets.QCheckBox('sphere-ob')
        self.plotSphere.setChecked(True)
        self.plotSphere.stateChanged.connect(self.on_plot_option_change)

        self.plotImport = QtWidgets.QCheckBox('imported data')
        self.plotImport.setChecked(False)
        self.plotImport.stateChanged.connect(self.on_plot_option_change)

        self.dBdT = QtWidgets.QCheckBox('dB/dT')
        self.dBdT.setChecked(True)

        self.BF = QtWidgets.QCheckBox('B Field')
        self.BF.setChecked(False)

        self.ChannelBox = QtWidgets.QComboBox()
        ChannelList = ['Default channels', 'Early channels', 'Mid channels', 'Late channels']
        self.ChannelBox.addItems(ChannelList)

        self.plot_container = QtWidgets.QGridLayout()
        self.plot_container.addWidget(self.ChannelBox)
        self.plot_container.addWidget(self.plotSphere)
        self.plot_container.addWidget(self.scaleLinear)
        self.plot_container.addWidget(self.plotImport, 1, 1)
        self.plot_container.addWidget(self.ChannelBox, 0, 0)
        self.plot_container.addWidget(self.scaleLog, 2, 1)
        self.plot_container.addLayout(self.graph_box, 6, 0, 1, 20)
        self.graph_gb.setLayout(self.plot_container)

        coeff_gb = QtWidgets.QGroupBox('Sphere overburden parameters')
        coeff_gb.setLayout(coeff_grid)

        other_grid = QtWidgets.QGridLayout()
        self.read_tem_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/chart_line_delete.png'),
            'Import TEM, XYZ ',
        )

        self.lineBox = QtWidgets.QLineEdit()
        self.lineBox.setEnabled(False)
        self.slider_label = QtWidgets.QLabel('Select Line to be plotted', self)

        other_grid.addWidget(self.slider_label)
        other_grid.addWidget(self.read_tem_btn)
        other_grid.addWidget(self.lineBox)
        self.window_box = QtWidgets.QHBoxLayout()
        self.window_box.addWidget(self.ChannelBox)

        other_gb = QtWidgets.QGroupBox('Imported data plotter')
        other_gb.setLayout(other_grid)

        # Create the update/reset plot buttons
        self.update_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/calculator.png'),
            'Plot Response',
        )
        self.reset_values_btn = QPushButton(
            QtGui.QIcon(':/resources/arrow_undo.png'),
            'Reset Values',
        )
        self.clear_graph_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/arrow_undo.png'),
            'Clear Plot',
        )
        self.reset_values_btn.clicked.connect(self.reset_values)
        self.read_tem_btn.clicked.connect(self.read_tem)

        container = QtWidgets.QVBoxLayout()
        container.addWidget(coeff_gb)
        container.addWidget(other_gb)
        container.addWidget(self.graph_gb)
        container.addStretch()
        container.addWidget(self.update_btn)
        container.addWidget(self.reset_values_btn)
        container.addWidget(self.clear_graph_btn)
        self.setLayout(container)
        self.reset_values()

    def reset_values(self):
        self.a_sb.setValue(100)
        self.rspop.setText('-200')
        self.thick_ob_sb.setValue(4)
        self.sigma_sp_sb.setValue(0.5)
        self.sigma_ob_sb.setValue(0.03)
        self.strike.setValue(90)
        self.dip.setValue(0)
        self.dipole.setValue(1847300)
        self.pulse.setValue(0.00398)
        self.timedelta_sb.setValue(0.03)
        self.txrx.setText('12,0,56')

    def on_plot_option_change(self, state):
        if self.sender() == self.plotSphere and state == Qt.Checked:
            self.plotImport.setChecked(False)
        elif self.sender() == self.plotImport and state == Qt.Checked:
            self.plotSphere.setChecked(False)

    def read_tem(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select TEM File:', "", "TEM data files (*.TEM *.XYZ)")
        if fileName:
            try:
                # Read the file into a DataFrame
                with open(fileName, 'r') as file:
                    lines = file.readlines()

                # Find the header row
                header_row = None
                for i, line in enumerate(lines):
                    if 'CH' in line:
                        header_row = i
                        break

                if header_row is None:
                    QMessageBox.critical(self, "Error", "Invalid file format: No channel data found")
                    return

                # Read the data starting from the header row
                self.TEM = pd.read_csv(fileName, sep='\s+', header=header_row)

                # Drop unnecessary columns if they exist
                columns_to_drop = ['No', 'F']
                for col in columns_to_drop:
                    if col in self.TEM.columns:
                        self.TEM.drop(columns=[col], inplace=True)

                # Ensure EAST and NORTH columns are treated as numeric
                if 'EAST' in self.TEM.columns:
                    self.TEM['EAST'] = pd.to_numeric(self.TEM['EAST'], errors='coerce')
                if 'NORTH' in self.TEM.columns:
                    self.TEM['NORTH'] = pd.to_numeric(self.TEM['NORTH'], errors='coerce')

                # Determine the profile (x-axis) based on the column with more variation
                if 'EAST' in self.TEM.columns and 'NORTH' in self.TEM.columns:
                    east_range = self.TEM['EAST'].max() - self.TEM['EAST'].min()
                    north_range = self.TEM['NORTH'].max() - self.TEM['NORTH'].min()
                    if east_range > north_range:
                        self.profile_column = 'EAST'
                    else:
                        self.profile_column = 'NORTH'
                elif 'EAST' in self.TEM.columns:
                    self.profile_column = 'EAST'
                elif 'NORTH' in self.TEM.columns:
                    self.profile_column = 'NORTH'
                else:
                    QMessageBox.critical(self, "Error", "Invalid file format: No EAST or NORTH column found")
                    return

                self.channels = [col for col in self.TEM.columns if col.startswith('CH')]

                self.lineBox.setText(os.path.basename(fileName))
                QMessageBox.information(self, "Success", f"Successfully loaded {len(self.channels)} channels")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Warning", "No file selected")

    def onScaleChange(self, state):
        if state == Qt.Checked:
            if self.sender() == self.scaleLinear:
                self.scaleLog.setChecked(False)
            elif self.sender() == self.scaleLog:
                self.scaleLinear.setChecked(False)

    def onWindowChange(self, state):
        if state == Qt.Checked:
            if self.sender() == self.alltime:
                self.earlytime.setChecked(False)
                self.midtime.setChecked(False)
                self.latetime.setChecked(False)
            elif self.sender() == self.earlytime:
                self.alltime.setChecked(False)
                self.latetime.setChecked(False)
                self.midtime.setChecked(False)
            elif self.sender() == self.midtime:
                self.earlytime.setChecked(False)
                self.alltime.setChecked(False)
                self.latetime.setChecked(False)
            elif self.sender() == self.latetime:
                self.alltime.setChecked(False)
                self.earlytime.setChecked(False)
                self.midtime.setChecked(False)


class AppForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setWindowTitle(APP_NAME)
        self.imported = False
        self.wave = 0
        self.profile_column = None

        self.options_menu = OptionsMenu()
        dock = QtWidgets.QDockWidget('Options', self)
        dock.setFeatures(
            QtWidgets.QDockWidget.NoDockWidgetFeatures |
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFloatable
        )
        dock.setAllowedAreas(
            Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea,
        )
        dock.setWidget(self.options_menu)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        self.options_menu.update_btn.clicked.connect(self.launch_selenium_Thread)
        self.options_menu.clear_graph_btn.clicked.connect(self.clear_graph)
        self.options_menu.read_data_btn.clicked.connect(self.readCSV)

        self.fig = Figure()
        self.canvas = backend_qt5agg.FigureCanvasQTAgg(self.fig)
        self.canvas.setParent(self)

        self.status_text = QtWidgets.QLabel("Set parameters and select response components to be plotted")
        self.statusBar().addWidget(self.status_text, 0)
        self.statusBar().setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        self.progressBar = QtWidgets.QProgressBar(self)
        self.statusBar().addPermanentWidget(self.progressBar, 1)
        self.statusBar().addWidget(self.progressBar)

        self.clear_graph()
        self.setCentralWidget(self.canvas)

        file_exit_action = QtWidgets.QAction('E&xit', self)
        file_exit_action.setToolTip('Exit')
        file_exit_action.setIcon(QtGui.QIcon(':/resources/door_open.png'))
        file_exit_action.triggered.connect(self.close)

        file_menu = self.menuBar().addMenu('&File')
        file_menu.addAction(file_exit_action)


    def get_start_stop(self):
        index = self.options_menu.ChannelBox.currentIndex()
        if index == 0:
            return 0, len(self.sphere.H_tot_x)
        elif index == 3:
            return 0, self.sphere.nw // 3
        elif index == 2:
            return self.sphere.nw // 3, 2 * (self.sphere.nw // 3)
        elif index == 1:
            return 2 * (self.sphere.nw // 3), self.sphere.nw

    def plot_component(self, ax, component, label):
        start, stop = self.get_start_stop()
        for i in range(start, stop):
            ax.plot(np.linspace(self.sphere.profile[0][0], self.sphere.profile[0][100], 101), component[i], color='0.4')
        ax.set_xlabel('Profile (m)')
        ax.set_ylabel(label)
        ax.grid(True, which='both', ls='-')
        if self.options_menu.scaleLog.isChecked():
            ax.set_yscale('log')

    def plot_sphere_components(self, components):
        self.fig.clf()
        num_components = len(components)
        for idx, (component, label) in enumerate(components):
            ax = self.fig.add_subplot(num_components, 1, idx + 1)
            self.plot_component(ax, component, label)
        self.canvas.draw()

    def plot_imported_data(self):
        self.fig.clf()
        ax = self.fig.add_subplot(111)

        # Access profile_column from options_menu
        profile_column = self.options_menu.profile_column
        print(f"Profile column: {profile_column}")

        profile_data = self.options_menu.TEM.drop(columns=['LEVEL', 'ELEV', 'STATION', 'COMPONENT'], errors='ignore')

        # Handle case where COMPONENT column might be missing
        if 'COMPONENT' in self.options_menu.TEM.columns:
            num_comp = self.options_menu.TEM['COMPONENT'].unique()
            print(f"Components: {num_comp}")
        else:
            num_comp = []

        # Ensure profile column is numeric
        profile_data[profile_column] = pd.to_numeric(profile_data[profile_column], errors='coerce')
        profile_data.dropna(subset=[profile_column], inplace=True)
        print(f"Profile data after cleaning: {profile_data}")

        # Extract channel data
        channel_columns = [col for col in profile_data.columns if col.startswith('CH')]
        print(f"Channel columns: {channel_columns}")
        channel_data = profile_data[channel_columns].apply(pd.to_numeric, errors='coerce')
        channel_data.dropna(inplace=True)
        print(f"Channel data: {channel_data}")

        # Get profile (x-axis) data
        profile = profile_data[profile_column].astype(float)
        print(f"Profile (x-axis) data: {profile}")

        # Plot each channel
        if not channel_data.empty:
            for col in channel_data.columns:
                ax.plot(profile, channel_data[col], label=col)

            ax.set_xlabel('Profile (m)')
            ax.set_ylabel('Response (pT)')
            ax.legend()
            ax.grid(True, which='both', ls='-')
            if self.options_menu.scaleLog.isChecked():
                ax.set_yscale('log')
        else:
            ax.set_title('No data to plot')

        self.canvas.draw()

    def plot_combined_data(self):
        self.plot_imported_data()
        ax = self.fig.add_subplot(2, 1, 2)
        z = self.sphere.H_tot_z
        for k in range(len(z)):
            ax.plot(np.linspace(self.sphere.profile[0][0], self.sphere.profile[0][100], 101), z[k], color='0.4')
        ax.set_xlabel('Profile (m)')
        ax.set_ylabel('z-component (nT/s)' if not isinstance(self.wave, int) else 'z-component (A/m)')
        ax.grid(True, which='both', ls='-')
        if self.options_menu.scaleLog.isChecked():
            ax.set_yscale('log')
        self.canvas.draw()

    def plot_data(self):
        components = []
        if self.options_menu.sphere_x.isChecked():
            components.append(
                (self.sphere.H_tot_x, 'x-component (nT/s)' if not isinstance(self.wave, int) else 'x-component (A/m)'))
        if self.options_menu.sphere_y.isChecked():
            components.append(
                (self.sphere.H_tot_y, 'y-component (nT/s)' if not isinstance(self.wave, int) else 'y-component (A/m)'))
        if self.options_menu.sphere_z.isChecked():
            components.append(
                (self.sphere.H_tot_z, 'z-component (nT/s)' if not isinstance(self.wave, int) else 'z-component (A/m)'))

        if len(components) > 0 and self.options_menu.plotSphere.isChecked():
            self.plot_sphere_components(components)
        elif self.options_menu.plotImport.isChecked() and not self.options_menu.plotSphere.isChecked():
            self.plot_imported_data()
        elif self.options_menu.plotImport.isChecked() and self.options_menu.plotSphere.isChecked():
            self.plot_combined_data()

    def calculate_data(self):
        sphere = SphereResponse()
        sphere.a = self.options_menu.a_sb.value()
        sphere.rsp = np.array([0, 0, int(self.options_menu.rspop.text())])
        sphere.offset_tx_rx = np.array([int(n) for n in self.options_menu.txrx.text().split(',')], dtype=np.int64)
        sphere.rtx = np.array([int(n) for n in self.options_menu.tx.text().split(',')], dtype=np.int64)
        sphere.thick_ob = self.options_menu.thick_ob_sb.value()
        sphere.sigma_sp = self.options_menu.sigma_sp_sb.value()
        sphere.sigma_ob = self.options_menu.sigma_ob_sb.value()
        sphere.strike = self.options_menu.strike.value()
        sphere.dip = self.options_menu.dip.value()
        sphere.P = self.options_menu.pulse.value()
        sphere.T = self.options_menu.timedelta_sb.value()
        sphere.prof_length = int(self.options_menu.user_profile.text())
        if self.options_menu.Xconvention.currentIndex() == 0:
            sphere.Xsign = '+ve'
        if self.options_menu.Xconvention.currentIndex() == 1:
            sphere.Xsign = '-ve'

        if self.imported:
            sphere.wave = self.wave
            sphere.windows = self.windows[~np.isnan(self.windows)]

        if self.options_menu.PlotPoint.currentIndex() == 0:
            sphere.PlottingPoint = 'Rx'
        if self.options_menu.PlotPoint.currentIndex() == 1:
            sphere.PlottingPoint = 'Tx'
        if self.options_menu.PlotPoint.currentIndex() == 2:
            sphere.PlottingPoint = 'Mid point'

        if self.options_menu.dip.value() == 0:
            sphere.apply_dip = 0
        else:
            sphere.apply_dip = 1

        if sphere.sigma_sp == 0:
            sphere.sigma_sp = 1e-15
        if sphere.sigma_ob == 0:
            sphere.sigma_ob = 1e-15
        results = sphere.calculate()
        self.sphere = sphere  # Store the sphere instance in the class variable
        self.plot_data()
        self.progressBar.setRange(0, 1)
        self.status_text.setText("Finished")
        self.statusBar().setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))

    def clear_graph(self):
        self.redraw_graph()

    def redraw_graph(self):
        self.fig.clf()
        self.canvas.draw()

    def readCSV(self):
        DataName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select CSV File:', '', "CSV data files (*.csv)")
        if DataName == "":
            self.status_text.setText("No waveform data selected")
            return
        else:
            with open(DataName) as input_file:
                self.imported = True
                self.waveformdata = np.genfromtxt(input_file, delimiter=',')
                self.status_text.setText("Successfully loaded and updated waveform parameters")
                if self.waveformdata.shape[1] >= 2:
                    self.windows = self.waveformdata.T[0]
                    self.wave = self.waveformdata.T[1]
                else:
                    self.windows = self.waveformdata.T[0]

    def launch_selenium_Thread(self):
        t = threading.Thread(target=self.calculate_data)
        self.status_text.setText("Generating response")
        self.statusBar().setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        self.progressBar.setRange(0, 0)
        t.start()

    def show_about(self):
        message = '''<font size="+2">%s</font>
            <p>A sphere - overburden response plotter written in Python.
            <p>Written by %s,
            <a href="http://opensource.org/licenses/MIT">MIT Licensed</a>
            <p>Icons from <a href="http://www.famfamfam.com/">famfamfam</a> and
            <a href="http://commons.wikimedia.org/">Wikimedia
            Commons</a>.''' % (APP_NAME, AUTHOR)
        QtWidgets.QMessageBox.about(self, 'About ' + APP_NAME, message)


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(':/resources/icon.svg'))
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    form = AppForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
