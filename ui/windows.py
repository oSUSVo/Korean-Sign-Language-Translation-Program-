# -*- coding: utf-8 -*-
from pathlib import Path
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextBrowser, QComboBox, QPushButton, QCheckBox, QFrame, QSlider
from PyQt5.QtCore import pyqtSignal
from config.paths import HELP_IMG
from PyQt5.QtCore import pyqtSignal, Qt

class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("도움말")
        self.resize(591, 642)
        lay, title, body = QVBoxLayout(self), QLabel("<b>수어 예시</b>"), QTextBrowser()
        help_image = Path(HELP_IMG)
        if not help_image.exists():
            body.setText("도움말 이미지 파일을 찾을 수 없습니다.")
        else:
            body.setHtml(f'<br><img src="{help_image.as_uri()}" width="550"><br>')
        lay.addWidget(title); lay.addWidget(body)

class SettingsWindow(QDialog):
    speed_changed = pyqtSignal(float)
    landmark_visibility_changed = pyqtSignal(bool)
    volume_changed = pyqtSignal(int)

    def __init__(self, current_speed, landmark_visible, current_volume, parent=None):
        super().__init__(parent)
        self.setWindowTitle("설정"); self.resize(350, 250)
        self.info_label1 = QLabel("인식 속도 조절")
        self.info_label2 = QLabel("숫자가 낮을수록 인식 간격이 짧아져 빨라집니다.")
        self.speed_combo = QComboBox(); self.apply_button = QPushButton("적용")
        self.landmark_checkbox = QCheckBox("랜드마크 표시"); self.landmark_checkbox.setChecked(landmark_visible)
        self.speed_options = {"매우 느림 (5.0초)": 5.0, "느림 (4.0초)": 4.0, "보통 (3.0초)": 3.0, "빠름 (2.0초)": 2.0, "매우 빠름 (1.0초)": 1.0}
        for text, value in self.speed_options.items():
            self.speed_combo.addItem(text, value)
        for i, value in enumerate(self.speed_options.values()):
            if value == current_speed:
                self.speed_combo.setCurrentIndex(i); break

        # 🟢 볼륨 조절 슬라이더 추가
        self.volume_label = QLabel("TTS 볼륨 조절")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(current_volume)
        self.volume_value_label = QLabel(f"{current_volume}%")
        self.volume_slider.valueChanged.connect(
            lambda v: self.volume_value_label.setText(f"{v}%")
        )

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)

        layout = QVBoxLayout(self)
        layout.addWidget(self.info_label1)
        layout.addWidget(self.info_label2)
        layout.addWidget(self.speed_combo)
        layout.addWidget(separator)
        layout.addWidget(self.landmark_checkbox)

        # 🟢 볼륨 관련 UI 배치
        layout.addWidget(self.volume_label)
        layout.addWidget(self.volume_slider)
        layout.addWidget(self.volume_value_label)

        layout.addStretch(1)
        layout.addWidget(self.apply_button)

        self.apply_button.clicked.connect(self.apply_settings)

    def apply_settings(self):
        selected_speed = self.speed_combo.currentData()
        self.speed_changed.emit(selected_speed)
        is_visible = self.landmark_checkbox.isChecked()
        self.landmark_visibility_changed.emit(is_visible)

        vol = self.volume_slider.value()
        self.volume_changed.emit(vol)  # 🟢 TTS 볼륨 변경 신호 발생
        self.accept()