import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import subprocess  # For running external scripts
from visualization import DataShow

class ScraperGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FlipKart Scraper')
        self.setWindowIcon(QIcon('icon.png'))
        self.setFixedSize(800, 200)
        self.setGeometry(500, 100, 800, 200)
        self.initUI()
        
    def initUI(self):
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        vLayout = QVBoxLayout()

        # File Name Input
        file_label = QLabel('File name:')
        self.file_input = QLineEdit()
        layout1.addWidget(file_label)
        layout1.addWidget(self.file_input)

        # Search Term Input
        search_label = QLabel('Search term:')
        self.search_input = QLineEdit()
        layout2.addWidget(search_label)
        layout2.addWidget(self.search_input)

        # Scrape Button
        scrape_button = QPushButton('Scrape')
        scrape_button.clicked.connect(self.start_scraping) 
        layout3.addWidget(scrape_button)

        #Count input: 
        count_label = QLabel('Count: ')
        self.count_input = QLineEdit()
        layout2.addWidget(count_label)
        layout2.addWidget(self.count_input)

        vLayout.addLayout(layout1)
        vLayout.addLayout(layout2)
        vLayout.addLayout(layout3)
        self.setLayout(vLayout)

    def start_scraping(self):
        file_name = self.file_input.text().replace(' ', '_')
        search_term = self.search_input.text().replace(' ', '+')
        count = self.count_input.text()

        if not file_name or not search_term or not count:
            QMessageBox.warning(self, "Missing Input", "Please enter both a file name ,search term, count.")
            return

        try:
            # Execute your scraping script (modify the command as needed)
            subprocess.run(["python", "visualization.py", file_name, search_term, count], check=True) 
            QMessageBox.information(self, "Scraping Complete", f"Data saved to {file_name}.csv")
            
            self.close()
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Scraping Error", f"An error occurred during scraping:\n{e}")

    def file_name(self):
        return self.file_input.text()

class DataWindow(QWidget):
    close_signal = pyqtSignal()
    def __init__(self, file_name):
        super().__init__()
        self.setWindowTitle('Analyze Data')
        self.setGeometry(500,200, 250, 300)
        self.setWindowIcon(QIcon('icon.png'))
        self.function(file_name)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        #Creating buttons
        sale = QPushButton('Visualise Sales')
        sale.clicked.connect(self.df.visualise_sale)
        rating = QPushButton('Visualize Ratings')
        rating.clicked.connect(self.df.visualise_rating)
        file = QPushButton('Open File')
        file.clicked.connect(self.open_file)
        #Adding buttons to layout
        layout.addWidget(sale)
        layout.addWidget(rating)
        layout.addWidget(file)
        #Setting the layout
        self.setLayout(layout) 
    def function(self, file_name):
        self.file = file_name
        self.df = DataShow(file_name)

    def open_file(self):
        try:
             os.system(f'cmd /c "start {self.file}.csv"')
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "File Error", f"Cannot open {self.file}.csv")

    def closeEvent(self, event):
        self.close_signal.emit()
        super().closeEvent(event)
        reply = QMessageBox.question(self, "Save File..?", 
                                         f"Do you want to save {self.file}.csv?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.No:
            os.system(f'cmd /c del /Q {self.file}.csv')
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ScraperGUI()
    main.show()
    app.exec_()
    file_name = main.file_name()
    data = DataWindow(file_name)
    data.show()
    app.exec_()

    
