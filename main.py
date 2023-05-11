from PySide6.QtCore import QTime, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from chef import main

class Timer(QWidget):
    def __init__(self, recipe_name, steps, times):
        super().__init__()

        self.recipe_name = recipe_name
        self.steps = steps
        self.times = times
        self.current_step = 0
        self.remaining_time = self.times[self.current_step]

        # set window properties
        self.setWindowTitle(f"{self.recipe_name}")
        self.setGeometry(100, 100, 400, 200)

        # create widgets
        self.title_label = QLabel(f"{self.recipe_name}")
        self.step_label = QLabel(self.steps[self.current_step])
        self.time_label = QLabel(self.format_time(self.remaining_time))
        self.start_button = QPushButton("Start")
        self.pause_button = QPushButton("Pause")
        self.reset_button = QPushButton("Reset")
        self.startbot_button = QPushButton("Start bot")
        self.time_edits = [QLineEdit(str(time)) for time in self.times]

        # create layouts
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.step_label)
        h_layout.addWidget(self.time_label)
        v_layout.addWidget(self.title_label)
        v_layout.addLayout(h_layout)
        for i, step in enumerate(self.steps):
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(f"{i+1}. {step}"))
            h_layout.addWidget(self.time_edits[i])
            v_layout.addLayout(h_layout)
        v_layout.addWidget(self.startbot_button)
        v_layout.addWidget(self.start_button)
        v_layout.addWidget(self.pause_button)
        v_layout.addWidget(self.reset_button)

        # set layout
        self.setLayout(v_layout)

        # connect buttons to functions
        self.startbot_button.clicked.connect(self.startbot)
        self.start_button.clicked.connect(self.start_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.reset_button.clicked.connect(self.reset_timer)

        # create timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)

    def format_time(self, seconds):
        time = QTime(0, 0, 0)
        time = time.addSecs(seconds)
        return time.toString("mm:ss")

    def start_timer(self):
        self.timer.start(1000) # update every second
        for i in range(len(self.times)):
            self.times[i] = int(self.time_edits[i].text())

    def pause_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.current_step = 0
        self.step_label.setText(self.steps[self.current_step])
        self.remaining_time = self.times[self.current_step]
        self.time_label.setText(self.format_time(self.remaining_time))
        for i in range(len(self.times)):
            self.times[i] = int(self.time_edits[i].text())
        self.timer.stop()

    def update_time(self):
        self.remaining_time -= 1
        if self.remaining_time < 0:
            self.timer.stop()
            self.time_label.setText("Done!")
            self.current_step += 1
            if self.current_step < len(self.steps):
                self.step_label.setText(self.steps[self.current_step])
                self.remaining_time = self.times[self.current_step]
                self.time_label.setText(self.format_time(self.remaining_time))
        else:
            self.time_label.setText(self.format_time(self.remaining_time))
            
    def startbot(self):
        main()

if __name__ == "__main__":
    app = QApplication([])
    cooking_window = Timer("", ["timer"], [0])
    cooking_window.show()
    app.exec()
