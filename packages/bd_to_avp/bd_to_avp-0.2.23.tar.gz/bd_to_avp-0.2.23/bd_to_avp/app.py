import sys
from pathlib import Path


from PyQt6.QtGui import QIcon, QTextCursor
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFileDialog,
    QCheckBox,
    QSpinBox,
    QTextEdit,
    QComboBox,
)
from PyQt6.QtCore import QObject, QThread, Qt, pyqtSignal

from bd_to_avp.modules.config import config, Stage
from bd_to_avp.modules.disc import DiscInfo
from bd_to_avp.process import process
from bd_to_avp.modules.util import OutputHandler, Spinner


class ProcessingSignals(QObject):
    progress_updated = pyqtSignal(str)


class ProcessingThread(QThread):
    error_occurred = pyqtSignal(str)

    def __init__(
        self, main_window: "MainWindow", parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.signals = ProcessingSignals()
        # noinspection PyUnresolvedReferences
        self.output_handler = OutputHandler(self.signals.progress_updated.emit)
        self.main_window = main_window

    def run(self) -> None:
        sys.stdout = self.output_handler  # type: ignore

        try:
            process()
        except (RuntimeError, ValueError) as error:
            # noinspection PyUnresolvedReferences
            self.error_occurred.emit(str(error))
        finally:
            sys.stdout = sys.__stdout__
            # noinspection PyUnresolvedReferences
            self.signals.progress_updated.emit("Process Completed.")


class CustomWarningDialog(QDialog):
    def __init__(self, parent: QWidget | None = None, message: str = "") -> None:
        super().__init__(parent)

        self.setWindowTitle("Warning")
        self.setFixedSize(400, 100)

        # Setup layout
        layout = QVBoxLayout()
        content_layout = QHBoxLayout()

        # Icon
        icon_label = QLabel()
        icon = QIcon.fromTheme("dialog-warning")
        icon_label.setPixmap(icon.pixmap(64, 64))
        content_layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignTop)

        # Message
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        content_layout.addWidget(
            message_label, 1, Qt.AlignmentFlag.AlignLeft
        )  # Add message to layout

        layout.addLayout(content_layout)

        # OK Button
        ok_button = QPushButton("OK")
        # noinspection PyUnresolvedReferences
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

        # Center dialog on parent window
        if parent is not None:
            parent_center = parent.frameGeometry().center()
            dialog_x = parent_center.x() - self.width() // 2
            dialog_y = parent_center.y() - self.height() // 2
            self.move(dialog_x, dialog_y)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("3D Blu-ray (and mts) to AVP")
        self.setGeometry(100, 100, 800, 600)

        # Create the main layout
        main_widget = QWidget()
        main_widget.setMinimumWidth(300)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(5)

        save_load_layout = QHBoxLayout()
        self.load_config_button = QPushButton("Load Config")
        # noinspection PyUnresolvedReferences
        self.load_config_button.clicked.connect(self.load_config_and_update_ui)
        save_load_layout.addWidget(self.load_config_button)

        self.save_config_button = QPushButton("Save Config")
        # noinspection PyUnresolvedReferences
        self.save_config_button.clicked.connect(self.save_config_to_file)
        save_load_layout.addWidget(self.save_config_button)

        main_layout.addLayout(save_load_layout)

        self.read_from_disc_checkbox = QCheckBox("Read from Disc")
        # noinspection PyUnresolvedReferences
        self.read_from_disc_checkbox.stateChanged.connect(self.toggle_read_from_disc)
        main_layout.addWidget(self.read_from_disc_checkbox)

        # Source and output folder selection
        source_folder_layout = QHBoxLayout()
        self.source_folder_label = QLabel("Source Folder")
        self.source_folder_entry = QLineEdit()
        self.source_folder_button = QPushButton("Browse")
        # noinspection PyUnresolvedReferences
        self.source_folder_button.clicked.connect(self.browse_source_folder)
        source_folder_layout.addWidget(self.source_folder_label)
        source_folder_layout.addWidget(self.source_folder_entry)
        source_folder_layout.addWidget(self.source_folder_button)
        main_layout.addLayout(source_folder_layout)

        source_file_layout = QHBoxLayout()
        self.source_file_label = QLabel("Source File")
        self.source_file_entry = QLineEdit()
        self.source_file_button = QPushButton("Browse")
        # noinspection PyUnresolvedReferences
        self.source_file_button.clicked.connect(self.browse_source_file)
        source_file_layout.addWidget(self.source_file_label)
        source_file_layout.addWidget(self.source_file_entry)
        source_file_layout.addWidget(self.source_file_button)
        main_layout.addLayout(source_file_layout)

        output_layout = QHBoxLayout()
        self.output_folder_label = QLabel("Output Folder")
        self.output_folder_entry = QLineEdit()
        self.output_folder_button = QPushButton("Browse")
        # noinspection PyUnresolvedReferences
        self.output_folder_button.clicked.connect(self.browse_output_folder)
        output_layout.addWidget(self.output_folder_label)
        output_layout.addWidget(self.output_folder_entry)
        output_layout.addWidget(self.output_folder_button)

        main_layout.addLayout(output_layout)

        # Configuration options
        config_layout = QVBoxLayout()

        left_right_layout = QHBoxLayout()
        self.left_right_bitrate_label = QLabel("Left/Right Bitrate (Mbps)")
        self.left_right_bitrate_spinbox = QSpinBox()
        self.left_right_bitrate_spinbox.setRange(1, 100)
        self.left_right_bitrate_spinbox.setValue(config.left_right_bitrate)
        self.left_right_bitrate_spinbox.setMaximumWidth(75)
        left_right_layout.addWidget(self.left_right_bitrate_spinbox)
        left_right_layout.addWidget(self.left_right_bitrate_label)
        config_layout.addLayout(left_right_layout)

        audio_bitrate_layout = QHBoxLayout()
        self.audio_bitrate_label = QLabel("Audio Bitrate (kbps)")
        self.audio_bitrate_spinbox = QSpinBox()
        self.audio_bitrate_spinbox.setRange(0, 1000)
        self.audio_bitrate_spinbox.setValue(config.audio_bitrate)
        self.audio_bitrate_spinbox.setMaximumWidth(75)
        audio_bitrate_layout.addWidget(self.audio_bitrate_spinbox)
        audio_bitrate_layout.addWidget(self.audio_bitrate_label)
        config_layout.addLayout(audio_bitrate_layout)

        mv_hevc_quality_layout = QHBoxLayout()
        self.mv_hevc_quality_label = QLabel("MV-HEVC Quality (0-100)")
        self.mv_hevc_quality_spinbox = QSpinBox()
        self.mv_hevc_quality_spinbox.setRange(0, 100)
        self.mv_hevc_quality_spinbox.setValue(config.mv_hevc_quality)
        self.mv_hevc_quality_spinbox.setMaximumWidth(75)
        mv_hevc_quality_layout.addWidget(self.mv_hevc_quality_spinbox)
        mv_hevc_quality_layout.addWidget(self.mv_hevc_quality_label)
        config_layout.addLayout(mv_hevc_quality_layout)

        fov_layout = QHBoxLayout()
        self.fov_label = QLabel("Field of View")
        self.fov_spinbox = QSpinBox()
        self.fov_spinbox.setRange(0, 360)
        self.fov_spinbox.setValue(config.fov)
        self.fov_spinbox.setMaximumWidth(75)
        fov_layout.addWidget(self.fov_spinbox)
        fov_layout.addWidget(self.fov_label)
        config_layout.addLayout(fov_layout)

        self.frame_rate_label = QLabel("Frame Rate (Leave blank to use source value)")
        self.frame_rate_entry = QLineEdit()
        self.frame_rate_entry.setText(config.frame_rate)
        self.frame_rate_entry.setMaximumWidth(75)
        self.frame_rate_entry.setPlaceholderText(DiscInfo.frame_rate)
        config_layout.addWidget(self.frame_rate_label)
        config_layout.addWidget(self.frame_rate_entry)

        self.resolution_label = QLabel("Resolution (Leave blank to use source value)")
        self.resolution_entry = QLineEdit()
        self.resolution_entry.setText(config.resolution)
        self.resolution_entry.setPlaceholderText(DiscInfo.resolution)
        self.resolution_entry.setMaximumWidth(150)
        config_layout.addWidget(self.resolution_label)
        config_layout.addWidget(self.resolution_entry)

        self.crop_black_bars_checkbox = QCheckBox("Crop Black Bars")
        self.crop_black_bars_checkbox.setChecked(config.crop_black_bars)
        config_layout.addWidget(self.crop_black_bars_checkbox)

        self.swap_eyes_checkbox = QCheckBox("Swap Eyes")
        self.swap_eyes_checkbox.setChecked(config.swap_eyes)
        config_layout.addWidget(self.swap_eyes_checkbox)

        self.keep_files_checkbox = QCheckBox("Keep Temporary Files")
        self.keep_files_checkbox.setChecked(config.keep_files)
        config_layout.addWidget(self.keep_files_checkbox)

        self.output_commands_checkbox = QCheckBox("Output Commands")
        self.output_commands_checkbox.setChecked(config.output_commands)
        config_layout.addWidget(self.output_commands_checkbox)

        self.software_encoder_checkbox = QCheckBox("Use Software Encoder")
        self.software_encoder_checkbox.setChecked(config.software_encoder)
        config_layout.addWidget(self.software_encoder_checkbox)

        self.fx_upscale_checkbox = QCheckBox("AI FX Upscale (2x resolution)")
        self.fx_upscale_checkbox.setChecked(config.fx_upscale)
        config_layout.addWidget(self.fx_upscale_checkbox)

        self.remove_original_checkbox = QCheckBox("Remove Original")
        self.remove_original_checkbox.setChecked(config.remove_original)
        config_layout.addWidget(self.remove_original_checkbox)

        self.overwrite_checkbox = QCheckBox("Overwrite")
        self.overwrite_checkbox.setChecked(config.overwrite)
        config_layout.addWidget(self.overwrite_checkbox)

        self.transcode_audio_checkbox = QCheckBox("Transcode Audio")
        self.transcode_audio_checkbox.setChecked(config.transcode_audio)
        config_layout.addWidget(self.transcode_audio_checkbox)

        self.start_stage_label = QLabel("Start Stage")
        self.start_stage_combobox = QComboBox()
        self.start_stage_combobox.addItems(Stage.list())
        self.start_stage_combobox.setCurrentText(config.start_stage.name)
        config_layout.addWidget(self.start_stage_label)
        config_layout.addWidget(self.start_stage_combobox)

        # Add more configuration options as needed

        main_layout.addLayout(config_layout)

        # Processing button
        self.process_button = QPushButton("Start Processing")
        # noinspection PyUnresolvedReferences
        self.process_button.clicked.connect(self.toggle_processing)
        main_layout.addWidget(self.process_button)

        self.processing_output_textedit = QTextEdit()
        self.processing_output_textedit.setReadOnly(True)

        # Create a QSplitter and add the main widget and processing output widget
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(main_widget)
        self.splitter.addWidget(self.processing_output_textedit)

        # Set the initial sizes of the splitter sections
        self.splitter.setSizes([400, 400])  # Adjust the sizes as needed

        # Set the QSplitter as the central widget of the main window
        self.setCentralWidget(self.splitter)

        # Processing status and output
        self.processing_status_label = QLabel("Processing Status")
        main_layout.addWidget(self.processing_status_label)
        self.processing_status_label.hide()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.hide()

        # noinspection PyUnresolvedReferences
        self.splitter.splitterMoved.connect(self.update_status_bar)

        # Create the processing thread
        self.processing_thread = ProcessingThread(main_window=self)
        # noinspection PyUnresolvedReferences
        self.processing_thread.signals.progress_updated.connect(
            self.update_processing_output
        )
        # noinspection PyUnresolvedReferences
        self.processing_thread.error_occurred.connect(self.handle_processing_error)

    def handle_processing_error(self, error: str) -> None:
        self.popup_warning_centered("Failure in processing.")
        self.update_processing_output(error)
        self.process_button.setEnabled(True)
        self.process_button.setText("Start Processing")

    def toggle_read_from_disc(self) -> None:
        self.source_folder_entry.setEnabled(
            not self.read_from_disc_checkbox.isChecked()
        )
        self.source_folder_button.setEnabled(
            not self.read_from_disc_checkbox.isChecked()
        )
        self.source_file_entry.setEnabled(not self.read_from_disc_checkbox.isChecked())
        self.source_file_button.setEnabled(not self.read_from_disc_checkbox.isChecked())

    def update_status_bar(self) -> None:
        central_widget = self.centralWidget()
        if not central_widget:
            return
        # noinspection PyUnresolvedReferences
        splitter_sizes = central_widget.sizes()  # type: ignore
        if splitter_sizes[-1] == 0:
            last_line = (
                self.processing_output_textedit.toPlainText().strip().split("\n")[-1]
            )
            self.status_bar.showMessage(last_line)
            self.processing_status_label.show()
            self.status_bar.show()
        else:
            self.status_bar.clearMessage()
            self.processing_status_label.hide()
            self.status_bar.hide()

    def load_config_and_update_ui(self) -> None:
        config.load_config_from_file()
        self.source_folder_entry.setText(
            config.source_folder_path.as_posix() if config.source_folder_path else ""
        )
        self.source_file_entry.setText(
            config.source_path.as_posix() if config.source_path else ""
        )
        self.output_folder_entry.setText(config.output_root_path.as_posix())
        self.left_right_bitrate_spinbox.setValue(config.left_right_bitrate)
        self.audio_bitrate_spinbox.setValue(config.audio_bitrate)
        self.mv_hevc_quality_spinbox.setValue(config.mv_hevc_quality)
        self.fov_spinbox.setValue(config.fov)
        self.frame_rate_entry.setText(config.frame_rate)
        self.resolution_entry.setText(config.resolution)
        self.crop_black_bars_checkbox.setChecked(config.crop_black_bars)
        self.swap_eyes_checkbox.setChecked(config.swap_eyes)
        self.keep_files_checkbox.setChecked(config.keep_files)
        self.output_commands_checkbox.setChecked(config.output_commands)
        self.software_encoder_checkbox.setChecked(config.software_encoder)
        self.fx_upscale_checkbox.setChecked(config.fx_upscale)
        self.remove_original_checkbox.setChecked(config.remove_original)
        self.overwrite_checkbox.setChecked(config.overwrite)
        self.transcode_audio_checkbox.setChecked(config.transcode_audio)
        self.start_stage_combobox.setCurrentText(config.start_stage.name)

    def browse_source_folder(self) -> None:
        source_folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if source_folder:
            self.source_folder_entry.setText(source_folder)

    def browse_source_file(self) -> None:
        source_file, _ = QFileDialog.getOpenFileName(self, "Select Source File")
        if source_file:
            self.source_file_entry.setText(source_file)

    def browse_output_folder(self) -> None:
        output_folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if output_folder:
            self.output_folder_entry.setText(output_folder)

    def popup_warning_centered(self, message: str) -> None:
        dialog = CustomWarningDialog(self, message)
        dialog.exec()  # Show dialog as modal

    def toggle_processing(self) -> None:
        if self.process_button.text() == "Start Processing":
            source_folder_set = bool(self.source_folder_entry.text())
            source_file_set = bool(self.source_file_entry.text())
            if (source_folder_set and source_file_set) or (
                not source_folder_set and not source_file_set
            ):
                self.popup_warning_centered(
                    "Either Source Folder or Source File must be set, but not both."
                )
                return
            self.process_button.setEnabled(False)
            self.start_processing()
            # self.process_button.setText("Stop Processing")
        else:
            self.stop_processing()
            self.process_button.setEnabled(True)
            self.process_button.setText("Start Processing")

    def start_processing(self) -> None:
        self.save_config()

        self.processing_thread.start()

    def save_config_to_file(self) -> None:
        self.save_config()
        config.save_config_to_file()

    def save_config(self) -> None:
        if self.read_from_disc_checkbox.isChecked():
            config.source_str = "disc:0"
            config.source_folder_path = None
            config.source_path = None
        else:
            config.source_folder_path = (
                Path(self.source_folder_entry.text())
                if self.source_folder_entry.text()
                else None
            )
            config.source_path = (
                Path(self.source_file_entry.text())
                if self.source_file_entry.text()
                else None
            )
        config.output_root_path = Path(self.output_folder_entry.text())
        config.left_right_bitrate = self.left_right_bitrate_spinbox.value()
        config.audio_bitrate = self.audio_bitrate_spinbox.value()
        config.mv_hevc_quality = self.mv_hevc_quality_spinbox.value()
        config.fov = self.fov_spinbox.value()
        config.frame_rate = self.frame_rate_entry.text()
        config.resolution = self.resolution_entry.text()
        config.crop_black_bars = self.crop_black_bars_checkbox.isChecked()
        config.swap_eyes = self.swap_eyes_checkbox.isChecked()
        config.keep_files = self.keep_files_checkbox.isChecked()
        config.output_commands = self.output_commands_checkbox.isChecked()
        config.software_encoder = self.software_encoder_checkbox.isChecked()
        config.fx_upscale = self.fx_upscale_checkbox.isChecked()
        config.remove_original = self.remove_original_checkbox.isChecked()
        config.overwrite = self.overwrite_checkbox.isChecked()
        config.transcode_audio = self.transcode_audio_checkbox.isChecked()
        selected_stage = int(self.start_stage_combobox.currentText().split(" - ")[0])
        config.start_stage = Stage.get_stage(selected_stage)

    def stop_processing(self) -> None:
        self.processing_thread.terminate()

    def update_processing_output(self, message: str) -> None:
        cursor = self.processing_output_textedit.textCursor()
        self.status_bar.showMessage(message.split("\n")[-1])

        if any(symbol in message for symbol in Spinner.symbols):
            cursor.movePosition(QTextCursor.MoveOperation.End)
            cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
            cursor.removeSelectedText()
            cursor.insertText(message)
        else:
            self.processing_output_textedit.append(message.strip())

        cursor.movePosition(QTextCursor.MoveOperation.Start)
        while cursor.movePosition(QTextCursor.MoveOperation.Down):
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            if cursor.selectedText().strip() == "":
                cursor.deleteChar()
            if any(symbol in cursor.selectedText() for symbol in Spinner.symbols):
                if cursor.movePosition(QTextCursor.MoveOperation.Down):
                    cursor.movePosition(QTextCursor.MoveOperation.Up)
                    cursor.select(QTextCursor.SelectionType.LineUnderCursor)
                    cursor.removeSelectedText()
                else:
                    break

        self.processing_output_textedit.setTextCursor(cursor)


def start_gui() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    start_gui()
