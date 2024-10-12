import sys
import os
import io
import time
import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import QWebEngineView
from base.BaseTSP import BaseTSP
from ui.Ui_MainWindow import Ui_MainWindow
from ga.population import PopulationGA
from ga.route import RouteGA
from Worker import  Worker
import ga.ga_tsp as ga_tsp
import sa.sa_tsp as sa_tsp
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot

sys.path.append(os.path.abspath("."))
default_dir = "./src/"


class MainWindow(Ui_MainWindow, QMainWindow):
    tsp = None
    running = False
    last_best_distance = -1
    magic_button_case_ga = "Start"
    magic_button_case_sa = "Start"

    
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setWindowTitle("Rota Optimizasyonu")

        
        self.webView = QWebEngineView(self)
        self.webView.showFullScreen()
        self.vbox.addWidget(self.webView)
        
        self.btn_start_ga.setEnabled(False)
        self.btn_start_sa.setEnabled(False)
        
        
        self.btn_export.setEnabled(False)

        self.btn_import.clicked.connect(self.import_data)
        self.btn_start_ga.clicked.connect(self.start_btn_ga)
        self.btn_start_sa.clicked.connect(self.start_btn_sa)
        self.btn_export.clicked.connect(self.save_results)

        self.cmbYontem.currentIndexChanged.connect(self.yontem_changed)
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.auto_draw)
    def closeEvent(self, event):
        # Ask for confirmation before closing
        confirmation = QMessageBox.question(self, "Kapat", "Pencereyi kapatmak istediğinize emin misiniz?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirmation == QMessageBox.StandardButton.Yes:
            
            event.accept()  # Close the app
        else:
            event.ignore() 


    def closeThreat(self, worker_thread: QThread):
        try:
            if worker_thread.isRunning():
                worker_thread.quit()
                worker_thread.wait()
        except Exception as ex:
            print('Exception :', ex)

        try: 
            print('thread.isRunning() after quit :', worker_thread.isRunning())
                
        except:
            print('quitted')
    
    
    def yontem_changed(self):
        print("yontem_changed")
       
            

  
    def import_data(self):
        options = QFileDialog.Option(QFileDialog.Option.DontUseNativeDialog)
        self.fileName, _ = QFileDialog.getOpenFileName(
            None,
            "Import Data File",
            default_dir,
            "Excel Files (*.xlsx)",
            options=options,
        )
        # sadece haritada gösterebilsin diye ekledim.
        self.tsp = BaseTSP(
                data_path=self.fileName,
            )
        
        
        self.import_data_thread()
        self.draw_locations()


        # self.save_settings()
        # worker = Worker(self.import_data_thread)
        # worker.signals.started.connect(self.save_settings)
        # worker.signals.finished.connect(self.draw_locations)
        # self.threads.start(worker)
        
    def print_output(self, s):
        print("print_output")
        print(s)
    def thread_complete(self):
        print("THREAD COMPLETE!")
    def import_data_thread(self):
        print("import_data_thread")
        try:

            self.lbl_locations_value.setText(str(len(self.tsp.data.dataset)))
            # self.tsp.outSignalList.connect(self.resultIterationList)
            # self.tsp.outSignalInt.connect(self.resultIteration)
            # self.tsp.outSignalDistance.connect(self.resultIterationDistance)
            
            # Activate parameter controls
            # self.txt_maxgeneration_value.setEnabled(True)
            # self.txt_pop_size_value.setEnabled(True)
            # self.txt_childrensize_value.setEnabled(True)
            # self.txt_mutationpercent_value.setEnabled(True)

            self.txt_maxgeneration_value.setText("500")
            self.txt_pop_size_value.setText("50")
            self.txt_childrensize_value.setText("10")
            self.txt_mutationpercent_value.setText("0.01")

            self.btn_start_ga.setEnabled(True)
            self.btn_start_sa.setEnabled(True)
            self.btn_export.setEnabled(True)

            self.last_best_distance = -1
            self.lbl_distance_value.setText("")
            self.lbl_generation_value.setText("")



        except Exception as ex:
            pass

    def save_settings(self):
        try:
            print("save_settings")
            maxgeneration = int(self.txt_maxgeneration_value.text())
            pop_size = int(self.txt_pop_size_value.text())
            childrensize = int(self.txt_childrensize_value.text())
            start = int(self.edtBaslangic.text())
            stop = int(self.edtBitis.text())

            if type(self.tsp) == sa_tsp.SA_TSP:
                t= float(self.txt_t_value.text())
                t_min = float(self.txt_t_min_value.text())
                alpha = float(self.txt_alpha_value.text())
                self.tsp.set_problem(
                    pop_size=pop_size,
                    number_of_children=childrensize,
                    max_generation=maxgeneration,
                    start = start,
                    stop = stop,
                    T = t,
                    T_min = t_min,
                    alpha = alpha
                )
            elif type(self.tsp) == ga_tsp.GA_TSP:
                
                mutationpercent = float(self.txt_mutationpercent_value.text())
                self.tsp.set_problem(
                    pop_size=pop_size,
                    number_of_children=childrensize,
                    max_generation=maxgeneration,
                    mutation_percent=mutationpercent,
                    start = start,
                    stop = stop
                )
                

            self.btn_start_sa.setEnabled(True)
            self.btn_start_ga.setEnabled(True)

            # Deactivate parameter controls
            # self.txt_maxgeneration_value.setEnabled(False)
            # self.txt_pop_size_value.setEnabled(False)
            # self.txt_childrensize_value.setEnabled(False)
            # self.txt_mutationpercent_value.setEnabled(False)

            self.lbl_generation_value.setText("")
            self.lbl_distance_value.setText("")
            self.btn_export.setEnabled(True)

        except Exception as ex:
            pass

    def start_btn_ga(self):
        if self.magic_button_case_ga == "Start":
            self.start_ga()
            self.magic_button_case_ga = "Stop"
            self.btn_start_ga.setText("Stop")
        elif self.magic_button_case_ga == "Stop":
            self.stop()
            self.magic_button_case_ga = "Start"
            self.btn_start_ga.setText("Start")
        else:
            pass
        
    def start_btn_sa(self):
        if self.magic_button_case_sa == "Start":
            self.start_sa()
            self.magic_button_case_sa = "Stop"
            self.btn_start_sa.setText("Stop")
        elif self.magic_button_case_sa == "Stop":
            self.stop()
            self.magic_button_case_sa = "Start"
            self.btn_start_sa.setText("Start")
        else:
            pass
    
    def start(self):
        self.running = True
        self.refresh_drawing = True
           

    def stop(self):
        self.running = False
        self.refresh_drawing = False
        

    def start_ga(self):
        print("start_ga")

        self.start()
        
        self.btn_start_ga.setText("Stop")      
        
        
        self.tsp = ga_tsp.GA_TSP(
                data_path=self.fileName,
            ) 
  
        self.save_settings()
        
        # self.tsp.start_ga(self.progress_ga)
        
        
        
        self.worker_thread = QThread()
        self.tsp.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.start_ga_thread)
        self.worker_thread.finished.connect(self.stop_ga_thread)
        self.tsp.result.connect(self.progress_)
        self.worker_thread.start()


        
    def start_sa(self):
        print("start_sa")

        self.start()
        
        self.btn_start_sa.setText("Stop")      
        
        
        self.tsp = sa_tsp.SA_TSP(
                data_path=self.fileName,
            )
        self.save_settings()
        
        # self.tsp.start_sa(self.progress_ga)
        

           
        
        self.worker_thread = QThread()
        self.tsp.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.start_sa_thread)
        self.worker_thread.finished.connect(self.stop_sa_thread)
        self.tsp.result.connect(self.progress_)
        self.worker_thread.start()
           


           
    def start_ga_thread(self):
        print("start_ga_thread")
        self.tsp.start_ga_thread()
  
  
    def stop_ga_thread(self):
        print("stop_ga_thread")
        self.btn_start_ga.setText("Start")


    def start_sa_thread(self):
        print("start_sa_thread")
        self.tsp.start_sa_thread()
  
  
    def stop_sa_thread(self):
        print("stop_sa_thread")
        self.btn_start_sa.setText("Start")
        
        
    def progress_(self, population : PopulationGA):
        # time.sleep(1)
        print(population.best_route)
        self.lbl_generation_value.setText(str(population.current_generation))
        self.lbl_distance_value.setText(str("%.2f" % population.best_distance))    
        self.lbl_route_value.setText(str(population.best_route.sequence))
        self.draw_route(population.best_route.sequence)    
        self.closeThreat(self.worker_thread)
   




    def draw_locations(self):
        
        m = self.tsp.draw_locations()
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())
        
        
        
        # m.save("map.html", close_file=False)
        # self.webView.setUrl(QUrl.fromLocalFile("map.html"))        
        # self.webView.setHtml(open("map.html").read())
        

    def draw_route(self,sequence:list ):
        # if self.threadpool.State() ==  self.threadpool.Running:
        
        seq = sequence.copy()
        
        seq.insert(0, self.tsp.start +1)
        seq.append(self.tsp.stop + 1)
        
        m = self.tsp.draw_route(seq)
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())
        
        # m.save("maproute.html", close_file=False)
        # self.webView.setUrl(QUrl.fromLocalFile("map.html"))


    def save_results(self):
        new_index = self.sort_by_route(self.tsp.population.best_route.sequence)

        results_df = self.tsp.data.dataset.copy()

        results_df.index = new_index
        results_df.sort_index(inplace=True)

        default_file = f"{default_dir}/best_route.xlsx"
        options = QFileDialog.Option(QFileDialog.Option.DontUseNativeDialog)
        # options = QFileDialog.Option()
        # options |= QFileDialog..DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save File", default_file, "Excel File (*.xlsx)", options=options
        )
        if fileName:
            results_df.to_excel(fileName, index=False)
            show_alert("File saved.")

    # Moves to center
    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def sort_by_route(self, sequence: list):
        order_df = pd.DataFrame({"sequence": sequence})
        order_df.sort_values("sequence", inplace=True)
        return list(order_df.index)


def show_alert(text):
    alert = QMessageBox()
    alert.setText(text)
    alert.exec()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
