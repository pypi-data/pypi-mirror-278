import sys
import tomllib
from pathlib import Path

from PySide6.QtGui import QAction, QFont, QIcon, QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QCheckBox,
    QSpinBox,
    QTextEdit,
    QComboBox,
)
from PySide6.QtCore import QObject, QThread, Qt, Signal

from bd_to_avp.gui.dialogs import AboutDialog
from bd_to_avp.gui.widgets import FileFolderPicker
from bd_to_avp.modules.config import config, Stage
from bd_to_avp.modules.disc import DiscInfo, MKVCreationError
from bd_to_avp.process import process
from bd_to_avp.modules.util import OutputHandler, Spinner, terminate_process


class ProcessingSignals(QObject):
    progress_updated = Signal(str)


class ProcessingThread(QThread):
    error_occurred = Signal(Exception)
    mkv_creation_error = Signal(MKVCreationError)

    def __init__(self, main_window: "MainWindow", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.signals = ProcessingSignals()
        self.output_handler = OutputHandler(self.signals.progress_updated.emit)
        self.main_window = main_window

    def run(self) -> None:
        sys.stdout = self.output_handler  # type: ignore

        try:
            process()
        except MKVCreationError as error:
            self.mkv_creation_error.emit(error)
        except (RuntimeError, ValueError) as error:
            self.error_occurred.emit(error)
        finally:
            sys.stdout = sys.__stdout__
            self.signals.progress_updated.emit("Process Completed.")
            self.main_window.process_button.setText(self.main_window.START_PROCESSING_TEXT)

    def terminate(self) -> None:
        terminate_process()
        super().terminate()


class MainWindow(QMainWindow):
    START_PROCESSING_TEXT = "Start Processing (⌘+P)"
    STOP_PROCESSING_TEXT = "Stop Processing (⌘+P)"

    def __init__(self) -> None:
        super().__init__()
        app = QApplication.instance()
        if not isinstance(app, QApplication):
            raise RuntimeError("No QApplication instance found.")
        self.setWindowTitle(app.applicationDisplayName())
        self.setGeometry(100, 100, 800, 600)

        # Create the main layout
        main_widget = QWidget()
        main_widget.setMinimumWidth(300)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(5)

        save_load_layout = QHBoxLayout()
        self.load_config_button = QPushButton("Load Config (⌘+L)")
        self.load_config_button.clicked.connect(self.load_config_and_update_ui)
        self.load_config_button.setShortcut("Ctrl+L")
        save_load_layout.addWidget(self.load_config_button)

        self.save_config_button = QPushButton("Save Config (⌘+S)")
        self.save_config_button.clicked.connect(self.save_config_to_file)
        self.save_config_button.setShortcut("Ctrl+S")
        save_load_layout.addWidget(self.save_config_button)

        main_layout.addLayout(save_load_layout)

        self.read_from_disc_checkbox = QCheckBox("Read from Disc")
        self.read_from_disc_checkbox.stateChanged.connect(self.toggle_read_from_disc)
        main_layout.addWidget(self.read_from_disc_checkbox)

        self.source_folder_widget = FileFolderPicker("Source Folder")
        main_layout.addWidget(self.source_folder_widget)

        self.source_file_widget = FileFolderPicker("Source File", for_files=True)
        main_layout.addWidget(self.source_file_widget)

        self.output_folder_widget = FileFolderPicker("Output Folder")
        main_layout.addWidget(self.output_folder_widget)

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

        frame_rate_layout = QHBoxLayout()
        self.frame_rate_label = QLabel("Frame Rate (Leave blank to use source value)")
        self.frame_rate_entry = QLineEdit()
        self.frame_rate_entry.setText(config.frame_rate)
        self.frame_rate_entry.setMaximumWidth(100)
        self.frame_rate_entry.setPlaceholderText(DiscInfo.frame_rate)
        frame_rate_layout.addWidget(self.frame_rate_entry)
        frame_rate_layout.addWidget(self.frame_rate_label)
        config_layout.addLayout(frame_rate_layout)

        resolution_layout = QHBoxLayout()
        self.resolution_label = QLabel("Resolution (Leave blank to use source value)")
        self.resolution_entry = QLineEdit()
        self.resolution_entry.setText(config.resolution)
        self.resolution_entry.setPlaceholderText(DiscInfo.resolution)
        self.resolution_entry.setMaximumWidth(100)
        resolution_layout.addWidget(self.resolution_entry)
        resolution_layout.addWidget(self.resolution_label)
        config_layout.addLayout(resolution_layout)

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

        self.continue_on_error = QCheckBox("Continue Processing On Error")
        self.continue_on_error.setChecked(config.continue_on_error)
        config_layout.addWidget(self.continue_on_error)

        self.start_stage_label = QLabel("Start Stage")
        self.start_stage_combobox = QComboBox()
        self.start_stage_combobox.addItems(Stage.list())
        self.start_stage_combobox.setCurrentText(config.start_stage.name)
        config_layout.addWidget(self.start_stage_label)
        config_layout.addWidget(self.start_stage_combobox)

        main_layout.addLayout(config_layout)

        # Processing button
        self.process_button = QPushButton(self.START_PROCESSING_TEXT)
        self.process_button.clicked.connect(self.toggle_processing)
        self.process_button.setShortcut("Ctrl+P")
        main_layout.addWidget(self.process_button)

        self.processing_output_textedit = QTextEdit()
        self.processing_output_textedit.setReadOnly(True)
        self.processing_output_textedit.setFont(QFont("Helvetica", 10))

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

        self.splitter.splitterMoved.connect(self.update_status_bar)

        # Create the processing thread
        self.processing_thread = ProcessingThread(main_window=self)
        self.processing_thread.signals.progress_updated.connect(self.update_processing_output)
        self.processing_thread.error_occurred.connect(self.handle_processing_error)
        self.processing_thread.mkv_creation_error.connect(self.handle_mkv_creation_error)

    def handle_processing_error(self, error: Exception) -> None:
        self.popup_warning_centered("Failure in processing.")
        self.update_processing_output(str(error))
        self.stop_processing()
        self.process_button.setText(self.START_PROCESSING_TEXT)

    def handle_mkv_creation_error(self, error: MKVCreationError) -> None:

        result = QMessageBox.critical(
            self,
            "MKV Creation Error",
            "Do you want to continue?\n\n" + str(error),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Abort,
        )

        if result == QMessageBox.StandardButton.Yes:
            config.continue_on_error = True
            config.start_stage = Stage.EXTRACT_MVC_AUDIO_AND_SUB
            self.start_processing(is_continuing=True)
            return

        self.handle_processing_error(error)

    def toggle_read_from_disc(self) -> None:
        self.source_folder_widget.setEnabled(not self.read_from_disc_checkbox.isChecked())
        self.source_file_widget.setEnabled(not self.read_from_disc_checkbox.isChecked())

    def update_status_bar(self) -> None:
        splitter_sizes = self.splitter.sizes()
        if splitter_sizes[-1] == 0:
            last_line = self.processing_output_textedit.toPlainText().strip().split("\n")[-1]
            self.status_bar.showMessage(last_line)
            self.processing_status_label.show()
            self.status_bar.show()
        else:
            self.status_bar.clearMessage()
            self.processing_status_label.hide()
            self.status_bar.hide()

    def load_config_and_update_ui(self) -> None:
        config.load_config_from_file()
        self.source_folder_widget.set_text(config.source_folder_path.as_posix() if config.source_folder_path else "")
        self.source_file_widget.set_text(config.source_path.as_posix() if config.source_path else "")
        self.output_folder_widget.set_text(config.output_root_path.as_posix())
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
        self.continue_on_error.setChecked(config.continue_on_error)

    def popup_warning_centered(self, message: str) -> None:
        QMessageBox.warning(self, "Warning", message)

    def toggle_processing(self) -> None:
        if self.process_button.text() == self.START_PROCESSING_TEXT:
            self.processing_output_textedit.clear()
            source_folder_set = bool(self.source_folder_widget.text())
            source_file_set = bool(self.source_file_widget.text())
            if (source_folder_set and source_file_set) or (not source_folder_set and not source_file_set):
                self.popup_warning_centered("Either Source Folder or Source File must be set, but not both.")
                return
            self.start_processing()
            self.process_button.setText(self.STOP_PROCESSING_TEXT)
        else:
            self.stop_processing()
            self.process_button.setText(self.START_PROCESSING_TEXT)

        self.process_button.setShortcut("Ctrl+P")
        # self.process_button.clicked.connect(self.toggle_processing)

    def start_processing(self, is_continuing: bool = False) -> None:
        if not is_continuing:
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
                Path(self.source_folder_widget.text()) if self.source_folder_widget.text() else None
            )
            config.source_path = Path(self.source_file_widget.text()) if self.source_file_widget.text() else None
        config.output_root_path = Path(self.output_folder_widget.text())
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
        config.continue_on_error = self.continue_on_error.isChecked()

    def stop_processing(self) -> None:
        self.processing_thread.terminate()

    def update_processing_output(self, message: str) -> None:
        output_textedit = self.processing_output_textedit
        output_textedit_scrollbar = output_textedit.verticalScrollBar()
        is_output_at_end = output_textedit_scrollbar.value == output_textedit_scrollbar.maximum()

        last_line_of_textedit = output_textedit.toPlainText().rsplit("\n", 1)[-1]

        spinner_dict = str.maketrans("", "", "".join(Spinner.symbols))
        message_stripped = message.translate(spinner_dict).strip()
        last_line_stripped = last_line_of_textedit.translate(spinner_dict).strip()

        cursor = output_textedit.textCursor()

        if any(symbol in last_line_of_textedit for symbol in Spinner.symbols):
            cursor.movePosition(QTextCursor.MoveOperation.End)
            cursor.deletePreviousChar()

        if any(symbol in message for symbol in Spinner.symbols):
            if message_stripped == last_line_stripped:
                cursor.movePosition(QTextCursor.MoveOperation.End)
                cursor.select(QTextCursor.SelectionType.LineUnderCursor)
                cursor.removeSelectedText()
                cursor.deletePreviousChar()
                output_textedit.append(message.strip())

        else:
            output_textedit.append(message.strip())

        if is_output_at_end:
            output_textedit_scrollbar.setValue(output_textedit_scrollbar.maximum())

        self.status_bar.showMessage(message.strip().rsplit("\n", 1)[-1])

    def create_menu_bar(self) -> None:
        # menu_bar = QMenuBar(None)
        menu_bar = self.menuBar()
        self.setMenuBar(self.menuBar())

        app_menu = menu_bar.addMenu(QApplication.applicationName())
        about_action = QAction(f"About {QApplication.applicationName()}", self)
        about_action.triggered.connect(self.show_about_dialog)
        app_menu.addAction(about_action)

        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(QAction("Open", self))

        help_menu = menu_bar.addMenu("Help")
        update_action = QAction("Update", self)
        update_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(update_action)

        self.setMenuBar(menu_bar)

    def show_about_dialog(self) -> None:
        dialog = AboutDialog(self)
        dialog.exec()


def start_gui() -> None:
    app = QApplication(sys.argv)
    load_app_info_from_pyproject(app)

    window = MainWindow()
    window.show()

    window.create_menu_bar()
    window.setMenuBar(window.menuBar())

    sys.exit(app.exec())


def load_app_info_from_pyproject(app: QApplication) -> None:
    pyproject_data = load_data_from_pyproject()
    if not pyproject_data:
        return

    tool = pyproject_data.get("tool", {})
    poetry = tool.get("poetry", {})
    briefcase = tool.get("briefcase", {})

    app.setApplicationName(poetry.get("name"))
    app.setOrganizationName(briefcase.get("organization"))
    app.setApplicationVersion(config.code_version)
    app.setOrganizationDomain(briefcase.get("bundle"))
    app.setApplicationDisplayName(briefcase.get("project_name"))

    briefcase_icon_path = Path(briefcase.get("icon"))
    icon_path = Path(*briefcase_icon_path.parts[1:]).with_suffix(".icns")
    icon_absolute_path = Path(__file__).parent / icon_path
    app.setWindowIcon(QIcon(icon_absolute_path.as_posix()))

    app.setProperty("authors", poetry.get("authors", []))
    app.setProperty("url", poetry.get("homepage"))


def load_data_from_pyproject() -> dict[str, dict] | None:
    project_root = Path(__file__).parent.parent
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists():
        return None

    with open(pyproject_path, "rb") as pyproject_file:
        pyproject_data = tomllib.load(pyproject_file)
        return pyproject_data


if __name__ == "__main__":
    start_gui()
