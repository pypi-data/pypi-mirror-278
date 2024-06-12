# ViCodePy - A video coder for psychological experiments
#
# Copyright (C) 2024 Esteban Milleret
# Copyright (C) 2024 Rafael Laboissière
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.

import yaml
import csv
import os
import re
import platform
import colour
from abc import abstractmethod
from enum import IntEnum
from pathlib import Path

from .ticklocator import TickLocator

from PySide6.QtCore import (
    Qt,
    QUrl,
    QSize,
    QTimer,
    QRectF,
    QLine,
    QPointF,
    QSizeF,
    Signal,
)
from PySide6.QtGui import (
    QAction,
    QPainter,
    QColor,
    QKeySequence,
    QPolygonF,
    QPen,
    QFontMetrics,
)
from PySide6.QtMultimedia import (
    QMediaPlayer,
    QAudioOutput,
    QMediaMetaData,
    QMediaFormat,
)
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QStyle,
    QVBoxLayout,
    QWidget,
    QLabel,
    QDialog,
    QLineEdit,
    QColorDialog,
    QComboBox,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
    QGraphicsItem,
    QMenu,
    QMessageBox,
)


def milliseconds_to_formatted_string(milliseconds):
    """
    Converts milliseconds to a string in the format hh:mm:ss.ssss.
    """

    # Convert milliseconds to seconds
    total_seconds = milliseconds / 1000

    # Extract hours, minutes, seconds
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Format time string with leading zeros
    time_string = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

    # Extract milliseconds (avoiding floating-point rounding issues)
    milliseconds = milliseconds % 1000
    millisecond_string = f"{milliseconds:03d}"  # Pad with leading zeros

    return f"{time_string}.{millisecond_string}"


def milliseconds_to_seconds(milliseconds) -> float:
    """Converts milliseconds to seconds"""
    return milliseconds / 1000


def seconds_to_milliseconds(seconds) -> float:
    """Converts milliseconds to seconds"""
    return seconds * 1000


class Player(QMainWindow):
    """A simple Media Player using Qt"""

    def __init__(self, master=None):
        QMainWindow.__init__(self, master)
        self.setWindowTitle("Media Player")
        self.setMinimumSize(QSize(640, 320))

        self.mediaplayer = QMediaPlayer()
        self.media = None
        self.mfps = None
        self.timeline = None

        self.__create_ui()

    def __create_ui(self):
        """Set up the user interface, signals & slots"""
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        btn_size = QSize(16, 16)

        # Create the video widget
        self.videoframe = QVideoWidget()

        # Create the time box
        self.htimebox = QHBoxLayout()

        # Create the time label
        self.timeLabel = QLabel()
        self.timeLabel.setText("00:00:00.000")
        self.timeLabel.setFixedHeight(24)
        self.htimebox.addWidget(self.timeLabel)

        # Create the position slider
        self.positionslider = QSlider(Qt.Orientation.Horizontal, self)
        self.positionslider.setToolTip("Position")
        self.positionslider.setRange(0, 0)
        self.positionslider.sliderMoved.connect(self.set_position)
        # Add the position slider to the time box
        self.htimebox.addWidget(self.positionslider)

        # Create the duration time box
        self.durationLabel = QLabel()
        self.durationLabel.setText("00:00:00.000")
        self.durationLabel.setFixedHeight(24)
        self.htimebox.addWidget(self.durationLabel)

        # Create the button layout
        self.hbuttonbox = QHBoxLayout()

        # Create the previous frame button
        self.previousframe = QPushButton()
        self.previousframe.setEnabled(False)
        self.previousframe.setFixedHeight(24)
        self.previousframe.setIconSize(btn_size)
        self.previousframe.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipBackward)
        )
        self.previousframe.setToolTip("Previous Frame")
        self.previousframe.clicked.connect(self.on_previous_frame)
        # Add the previous frame button to the button layout
        self.hbuttonbox.addWidget(self.previousframe)

        # Create the play/pause button
        self.playbutton = QPushButton()
        self.playbutton.setEnabled(False)
        self.playbutton.setFixedHeight(24)
        self.playbutton.setIconSize(btn_size)
        self.playbutton.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        )
        self.playbutton.setToolTip("Play")
        self.playbutton.clicked.connect(self.play_pause)
        # Add the play/pause button to the button layout
        self.hbuttonbox.addWidget(self.playbutton)

        # Create the stop button
        self.stopbutton = QPushButton()
        self.stopbutton.setEnabled(False)
        self.stopbutton.setFixedHeight(24)
        self.stopbutton.setIconSize(btn_size)
        self.stopbutton.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop)
        )
        self.stopbutton.setToolTip("Stop")
        self.hbuttonbox.addWidget(self.stopbutton)
        # Add the stop button to the button layout
        self.stopbutton.clicked.connect(self.stop)

        # Create the next frame button
        self.nextframe = QPushButton()
        self.nextframe.setEnabled(False)
        self.nextframe.setFixedHeight(24)
        self.nextframe.setIconSize(btn_size)
        self.nextframe.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward)
        )
        self.nextframe.setToolTip("Next Frame")
        self.nextframe.clicked.connect(self.on_next_frame)
        # Add the next frame button to the button layout
        self.hbuttonbox.addWidget(self.nextframe)
        self.hbuttonbox.addStretch(1)

        # Create the volume slider
        self.volumeslider = QSlider(Qt.Orientation.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(100)
        self.volumeslider.setToolTip("Volume")
        # Add the volume slider to the button layout
        self.hbuttonbox.addWidget(self.volumeslider)
        self.volumeslider.valueChanged.connect(self.set_volume)

        # Create the main layout and add the button layout and video widget
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addLayout(self.htimebox)
        self.vboxlayout.addLayout(self.hbuttonbox)

        # Add TimeLineWidget
        self.timeline = TimeLineWidget(self)
        self.vboxlayout.addWidget(self.timeline)

        # Setup the media player
        self.mediaplayer.setVideoOutput(self.videoframe)
        self.mediaplayer.playbackStateChanged.connect(self.playback_state_changed)
        self.mediaplayer.mediaStatusChanged.connect(self.media_status_changed)
        self.mediaplayer.positionChanged.connect(self.position_changed)
        self.mediaplayer.durationChanged.connect(self.duration_changed)

        # Setup the audio output
        self.audiooutput = QAudioOutput()
        self.mediaplayer.setAudioOutput(self.audiooutput)

        # Prevent the individual UIs from getting the focus
        for ui in [
            self.playbutton,
            self.stopbutton,
            self.nextframe,
            self.previousframe,
            self.volumeslider,
            self.positionslider,
            self.videoframe,
        ]:
            ui.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Add the main layout to the main window
        self.widget.setLayout(self.vboxlayout)

        # Create menu bar
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("&File")

        # Add actions to file menu
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon)
        open_action = QAction(
            icon,
            "&Open...",
            self,
            shortcut=QKeySequence.StandardKey.Open,
            triggered=self.open_file,
        )
        close_action = QAction(
            "Quit",
            self,
            shortcut=(
                QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Q)
                if platform.system() == "Windows"
                else QKeySequence.StandardKey.Quit
            ),
            triggered=self.close,
        )
        export_action = QAction(
            "Export...",
            self,
            shortcut=QKeySequence(Qt.Modifier.CTRL | Qt.Modifier.SHIFT | Qt.Key.Key_S),
            triggered=self.export_file,
        )

        file_menu.addAction(open_action)
        file_menu.addAction(close_action)
        file_menu.addAction(export_action)

        # Add actions to play menu
        play_menu = menu_bar.addMenu("&Play")
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        self.play_action = QAction(
            icon,
            "Play/Pause",
            self,
            shortcut=Qt.Key.Key_Space,
            triggered=self.play_pause,
            enabled=False,
        )

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop)
        self.stop_action = QAction(
            icon,
            "Stop",
            self,
            shortcut=Qt.Key.Key_S,
            triggered=self.stop,
            enabled=False,
        )

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipBackward)
        self.previous_frame_action = QAction(
            icon,
            "Go to the previous frame",
            self,
            shortcut=Qt.Key.Key_Left,
            triggered=self.on_previous_frame,
            enabled=False,
        )

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward)
        self.next_frame_action = QAction(
            icon,
            "Go to the next frame",
            self,
            shortcut=Qt.Key.Key_Right,
            triggered=self.on_next_frame,
            enabled=False,
        )

        play_menu.addAction(self.play_action)
        play_menu.addAction(self.stop_action)
        play_menu.addAction(self.previous_frame_action)
        play_menu.addAction(self.next_frame_action)

        annotation_menu = menu_bar.addMenu("&Annotation")

        # Add actions to annotation menu
        self.add_annotation_action = QAction(
            "Add Annotation",
            self,
            triggered=self.timeline.handle_annotation,
            enabled=False,
        )
        self.add_annotation_action.setShortcuts([Qt.Key.Key_Return, Qt.Key.Key_Enter])

        annotation_menu.addAction(self.add_annotation_action)

        # Add actions to view menu
        view_menu = menu_bar.addMenu("&View")
        self.fullscreen_action = QAction(
            "Toggle Fullscreen",
            self,
            shortcut=Qt.Key.Key_F11,
            triggered=self.on_fullscreen,
        )

        view_menu.addAction(self.fullscreen_action)

        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_time_label)

        # Search for supported video file formats
        file_extensions = []
        for f in QMediaFormat().supportedFileFormats(QMediaFormat.Decode):
            mime_type = QMediaFormat(f).mimeType()
            name = mime_type.name()
            if re.search("^video/", name):
                file_extensions.extend(mime_type.suffixes())
        self.file_name_filters = [
            f"Video Files ({' '.join(['*.' + x for x in file_extensions])})",
            "All Files (*.*)",
        ]

    def on_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def play_pause(self):
        """Toggle play/pause status"""
        if self.mediaplayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.mediaplayer.pause()
        else:
            self.mediaplayer.play()

    def stop(self):
        """Stop player"""
        self.mediaplayer.stop()
        self.playbutton.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        )

    def no_video_loaded(self):
        QMessageBox.information(self, "Open a video file", "Choose a video file to start coding")

    def open_file(self, filename=None):
        """Open a media file in a MediaPlayer"""

        if not filename:
            dialog_txt = "Open Video File"
            file_dialog = QFileDialog(self)
            file_dialog.setWindowTitle(dialog_txt)
            file_dialog.setNameFilters(self.file_name_filters)
            file_dialog.exec()
            # Load only the first of the selected file
            filename = file_dialog.selectedFiles()[0]
            if not filename:
                return

        # getOpenFileName returns a tuple, so use only the actual file name
        self.media = QUrl.fromLocalFile(filename)

        # Enable the buttons
        self.playbutton.setEnabled(True)
        self.stopbutton.setEnabled(True)

        # Put the media in the media player
        self.mediaplayer.setSource(self.media)

        # Set the title of the track as window title
        self.setWindowTitle(filename)

        # Show first frame
        self.mediaplayer.play()
        self.mediaplayer.pause()

        # Clear the timeline
        self.timeline.clear()

    def set_volume(self, volume):
        """Set the volume"""
        self.audiooutput.setVolume(volume / 100)

    def playback_state_changed(self, state):
        """Set the button icon when media changes state"""
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.timer.start()
            self.playbutton.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)
            )
        else:
            self.timer.stop()
            self.playbutton.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
            )
            # Fix : stop to the write frame
            self.set_position(self.mediaplayer.position())

        self.stopbutton.setEnabled(state != QMediaPlayer.PlaybackState.StoppedState)
        self.stop_action.setEnabled(state != QMediaPlayer.PlaybackState.StoppedState)
        self.previousframe.setEnabled(state == QMediaPlayer.PlaybackState.PausedState)
        self.previous_frame_action.setEnabled(
            state == QMediaPlayer.PlaybackState.PausedState
        )
        self.nextframe.setEnabled(state == QMediaPlayer.PlaybackState.PausedState)
        self.next_frame_action.setEnabled(
            state == QMediaPlayer.PlaybackState.PausedState
        )
        self.add_annotation_action.setEnabled(
            state == QMediaPlayer.PlaybackState.PausedState
        )

    def media_status_changed(self, state):
        if state == QMediaPlayer.MediaStatus.LoadedMedia:
            # Enable play button
            self.play_action.setEnabled(True)
            # Check if metadata is available
            metadata = self.mediaplayer.metaData()
            if metadata:
                # If metadata is available, set the frame rate
                fps = metadata.value(QMediaMetaData.Key.VideoFrameRate)
                self.mfps = int(1000 / fps)
            else:
                self.mfps = None

    def position_changed(self, position):
        """Update the position slider"""
        self.positionslider.setValue(position)
        self.timeline.value = position
        self.timeLabel.setText(milliseconds_to_formatted_string(position))
        self.timeline.update()

    def duration_changed(self, duration):
        """Update the duration slider"""
        self.positionslider.setRange(0, duration)
        self.timeline.duration = duration
        self.durationLabel.setText(milliseconds_to_formatted_string(duration))
        self.timeline.update()

    def set_position(self, position):
        """Set the position"""
        self.mediaplayer.setPosition(position)

    def on_previous_frame(self):
        """Set the position to the previous frame"""
        state = self.mediaplayer.playbackState()
        if self.mfps is None or state != QMediaPlayer.PlaybackState.PausedState:
            return
        self.set_position(self.mediaplayer.position() - self.mfps)

    def on_next_frame(self):
        """Set the position to the next frame"""
        state = self.mediaplayer.playbackState()
        if self.mfps is None or state != QMediaPlayer.PlaybackState.PausedState:
            return
        self.set_position(self.mediaplayer.position() + self.mfps)

    def export_file(self):
        """Export data in CSV file"""
        if (
            self.mediaplayer is None
            or self.timeline is None
            or not self.timeline.annotations
        ):
            QMessageBox.warning(self, "No Data", "There is no data to save to CSV.")
            return

        # Construct the default file name from the QUrl of the video file
        target_directory = (
            os.path.dirname(self.media.path())
            + "/"
            + os.path.splitext(os.path.basename(self.media.path()))[0]
            + ".csv"
        )

        path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", target_directory, "CSV Files (*.csv);;All Files (*)"
        )
        if path:
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                # Write headers
                writer.writerow(header for header in TimeLineWidget.CSV_HEADERS)

                # Write data
                for annotation in sorted(
                    self.timeline.annotations, key=lambda x: x.startTime
                ):
                    row = [
                        milliseconds_to_seconds(annotation.startTime),
                        milliseconds_to_seconds(annotation.endTime),
                        annotation.group.name,
                        "",
                    ]
                    writer.writerow(row)

    def update_time_label(self):
        """Update the time label"""
        self.timeLabel.setText(
            milliseconds_to_formatted_string(self.mediaplayer.position())
        )


class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, scene: QGraphicsScene, parent=None):
        super().__init__(scene, parent)
        self.zoomFactor = 1.0
        self.zoomStep = 1.2
        self.zoomShift = None
        self.minimum_zoomFactor = 1.0
        self.initialSceneRect = None

    def wheelEvent(self, event):
        if not self.parent().player.media:
            return
        mouse_pos = self.mapToScene(event.position().toPoint()).x()
        if event.angleDelta().y() > 0:
            self.zoomShift = mouse_pos * (1 - self.zoomStep)
            self.zoom_in()
        else:
            self.zoomShift = mouse_pos * (1 - 1 / self.zoomStep)
            self.zoom_out()
        self.zoomShift = None

    def zoom_in(self):
        self.zoomFactor *= self.zoomStep
        self.update_scale()

    def zoom_out(self):
        if self.zoomFactor / self.zoomStep >= self.minimum_zoomFactor:
            self.zoomFactor /= self.zoomStep
            self.update_scale()

    def update_scale(self):
        # First initialisation of sceneRect after resizeEvent
        if self.initialSceneRect is None:
            self.initialSceneRect = QRectF(self.scene().sceneRect())

        # Update the width of the scene with zoomFactor
        self.scene().setSceneRect(
            0,
            0,
            self.initialSceneRect.width() * self.zoomFactor,
            self.sceneRect().height(),
        )

        if self.zoomShift:
            previousAnchor = self.transformationAnchor()
            self.setTransformationAnchor(QGraphicsView.NoAnchor)
            self.translate(self.zoomShift, 0)
            self.setTransformationAnchor(previousAnchor)

        # Update position of indicator
        self.parent().update_indicator_X()

        # Update annotations
        for annotation in self.parent().annotations:
            annotation.update_rect()

        # Update timelineScale display
        self.parent().timelineScale.update()


class TimeLineWidget(QWidget):
    CSV_HEADERS = ["begin", "end", "label", "timeline"]
    valueChanged = Signal(int)
    durationChanged = Signal(int)

    def __init__(self, player=None):
        """Initializes the timeline widget"""
        super().__init__(player)
        self._duration = 0
        self._value = 0

        self.annotations: list[Annotation] = []
        self.currentAnnotation: Annotation = None
        self.groups: list[AnnotationGroup] = []
        self.player = player
        self.scene = QGraphicsScene()
        self.view = ZoomableGraphicsView(self.scene, self)
        self.indicator = None
        self.timelineScale = None
        self.lower_bound = None
        self.upper_bound = None

        self.view.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.FullViewportUpdate
        )
        self.default_height_timeline = 60
        max_height = 75
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.view.setMaximumHeight(max_height)
        self.view.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.setMinimumSize(1, 60)
        self.setFixedHeight(max_height)
        self.setMouseTracking(True)
        self.scene.setSceneRect(0, 0, self.view.width(), self.default_height_timeline)

        self.valueChanged.connect(self.on_value_changed)
        self.durationChanged.connect(self.on_duration_changed)
        # Load the QSS file
        with open(Path(__file__).parent.joinpath("style.qss"), "r") as f:
            qss = f.read()

        if qss:
            self.setStyleSheet(qss)

        self.__init_groups()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value != self._value:
            self._value = value
            self.valueChanged.emit(value)

    def on_value_changed(self, new_value):

        # First, update the current annotation, if it exists. If the cursor
        # value goes beyond the allowed bounds, bring it back and do not update
        # the other widgets.
        if self.currentAnnotation:
            if self.lower_bound and new_value < self.lower_bound:
                self.player.on_next_frame()
                return
            if self.upper_bound and new_value > self.upper_bound:
                self.player.on_previous_frame()
                return
            self.currentAnnotation.update_end_time(new_value)

        # Update indicator position
        if self.indicator:
            self.indicator.setX(new_value * self.scene.width() / self.duration)
        else:
            self.indicator = Indicator(self)

        if isinstance(self.scene.focusItem(), AnnotationHandle):
            annotation_handle: AnnotationHandle = self.scene.focusItem()
            annotation_handle.change_time(new_value)

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        if duration != self._duration:
            self._duration = duration
            self.durationChanged.emit(duration)

    def on_duration_changed(self, new_duration):
        # Update timeline Scale
        self.timelineScale = TimelineScale(self)
        self.update()

    def __init_groups(self):
        """Add inital groups from config.yml file"""
        # Read the YAML file
        config_file = Path(__file__).parent.joinpath("config").joinpath("config.yml")
        with open(config_file, "r") as fid:
            config = yaml.load(fid, Loader=yaml.Loader)

        # Access the values
        if "timelines" in config:
            groups = config["timelines"][0]["groups"]
            for i, group in enumerate(groups):
                self.groups.append(
                    AnnotationGroup(i, str(group["name"]), QColor(group["color"]), self)
                )

    def clear(self):
        # Clear timelineScene
        self.scene.clear()
        self.groups.clear()
        self.annotations.clear()

        # Recreate timeline
        self.indicator = Indicator(self)
        self.timelineScale = TimelineScale(self)

        # Recreate default group
        self.__init_groups()

    def add_group(self, group):
        """Adds a group to the groups list"""
        self.groups.append(group)

    def remove_group(self, group):
        """Removes a group from the list"""
        self.groups.remove(group)

    def handle_annotation(self):
        """Handles the annotation"""
        if self.currentAnnotation is None:
            self.lower_bound = None
            self.upper_bound = None
            valid = True
            for a in self.scene.items():
                if isinstance(a, Annotation):
                    if self.value >= a.startTime and self.value <= a.endTime:
                        valid = False
                        break
                    if not self.lower_bound:
                        if a.endTime < self.value:
                            self.lower_bound = a.endTime
                    else:
                        if a.endTime < self.value:
                            if self.lower_bound < a.endTime:
                                self.lower_bound = a.endTime
                    if not self.upper_bound:
                        if a.startTime > self.value:
                            self.upper_bound = a.startTime
                    else:
                        if a.startTime > self.value:
                            if self.upper_bound > a.startTime:
                                self.upper_bound = a.startTime
            if not valid:
                return
            self.currentAnnotation = Annotation(self)
            self.scene.addItem(self.currentAnnotation)
        else:
            # End the current annotation
            agd = AnnotationGroupDialog(self)
            agd.exec()

            if agd.result() == AnnotationDialogCode.Accepted:
                if agd.state == "create":
                    # When creating a new group, create the group and add the
                    # current annotation to it
                    group = AnnotationGroup(
                        len(self.groups) + 1,
                        agd.group_name_text.text(),
                        agd.color,
                        self,
                    )
                    group.add_annotation(self.currentAnnotation)
                    self.add_group(group)
                else:
                    # Otherwise, we are selecting an existing group, and will
                    # retrieve the group and add the annotation to it
                    group = agd.combo_box.currentData()
                    group.add_annotation(self.currentAnnotation)
                self.currentAnnotation.finish_create()
                self.add_annotation(self.currentAnnotation)
                self.currentAnnotation = None
            elif agd.result() == AnnotationDialogCode.Aborted:
                self.currentAnnotation.remove()
            self.update()

    def add_annotation(self, annotation):
        self.annotations.append(annotation)

    def remove_annotation(self, annotation):
        if annotation in self.annotations:
            self.annotations.remove(annotation)
        elif annotation == self.currentAnnotation:
            self.currentAnnotation = None

    def update_indicator_X(self):
        self.indicator.setX(self.value * self.scene.width() / self.duration)

    def resizeEvent(self, a0):
        if self.timelineScale:
            self.view.initialSceneRect = QRectF(
                0, 0, self.view.width(), self.default_height_timeline
            )
            self.view.update_scale()
            self.timelineScale.init_nb_ticks()
        else:
            self.scene.setSceneRect(
                0, 0, self.view.width(), self.default_height_timeline
            )

        self.update()

    def keyPressEvent(self, event):
        # if key pressed is escape key
        if event.key() == Qt.Key.Key_Escape:
            # Delete annotation
            if self.currentAnnotation is not None:
                confirm_box = AnnotationConfirmMessageBox(self)
                if (
                    confirm_box.result()
                    == AnnotationConfirmMessageBox.DialogCode.Accepted
                ):
                    self.currentAnnotation.remove()
                    self.update()


class Indicator(QGraphicsItem):
    def __init__(self, timeline: TimeLineWidget = None):
        super().__init__()
        self.pressed = False
        self.timeline = timeline
        self.y = 15
        self.height = 10
        self.poly: QPolygonF = QPolygonF(
            [
                QPointF(-10, self.y),
                QPointF(10, self.y),
                QPointF(0, self.y + self.height),
            ]
        )
        self.line: QLine = QLine(0, self.y, 2, 10000)

        self.timeline.scene.addItem(self)

        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setZValue(101)

    def paint(self, painter, option, widget=...):
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.black)
        painter.drawLine(self.line)
        painter.drawPolygon(self.poly)

    def calculate_size(self):
        min_x: float = self.poly[0].x()
        max_x: float = self.poly[0].x()

        for i, point in enumerate(self.poly):
            if point.x() < min_x:
                min_x = point.x()
            if point.x() > max_x:
                max_x = point.x()

        return QSizeF(max_x - min_x, self.height)

    def boundingRect(self):
        size: QSizeF = self.calculate_size()
        return QRectF(-10, self.y, size.width(), size.height())

    def focusInEvent(self, event):
        self.pressed = True
        super().focusInEvent(event)
        self.update()

    def focusOutEvent(self, event):
        self.pressed = False
        super().focusOutEvent(event)
        self.update()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        pos: QPointF = event.scenePos()
        if self.pressed:
            self.timeline.player.set_position(
                int(pos.x() * self.timeline.duration / self.timeline.scene.width())
            )
            if pos.x() < 0:
                self.setPos(0, 0)
            elif pos.x() > self.timeline.scene.width():
                self.setPos(self.timeline.scene.width(), 0)
            else:
                self.setPos(pos.x(), 0)

        self.update()


class TimelineScale(QGraphicsRectItem):

    def __init__(self, timeline: TimeLineWidget):
        super().__init__()
        self.timeline = timeline
        self.height = 25
        self.timeline.scene.addItem(self)
        self.init_nb_ticks()

    def paint(self, painter, option, widget=...):
        self._draw_rect(painter)

        if self.timeline.duration != 0:
            self._draw_scale(painter)

    def _draw_rect(self, painter):
        """Draw the background rectangle of the timeline scale"""
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.lightGray)
        self.setRect(QRectF(0, 0, self.timeline.scene.width(), self.height))
        painter.drawRect(self.rect())

    def _draw_scale(self, painter):
        tl = TickLocator()
        min_gap = 0.05
        dur = self.timeline.duration
        wid = self.timeline.scene.width()
        font = painter.font()
        fm = QFontMetrics(font)
        loc = tl.find_locations(
            0, milliseconds_to_seconds(dur), wid, font, min_gap
        )
        # Calculate the height of the text
        font_height = painter.fontMetrics().height()
        line_height = 5
        y = self.y() + self.rect().height()

        for p in loc:

            i = seconds_to_milliseconds(p[0] * wid / dur)

            # Calculate the position of the text
            text_width = fm.boundingRect(p[1]).width()
            text_position = QPointF(i - text_width / 2, font_height)

            # Draw the text
            painter.drawText(text_position, p[1])

            # Calculate the position of the line
            painter.drawLine(QPointF(i, y), QPointF(i, y - line_height))

    def init_nb_ticks(self):
        self.nb_ticks = 16
        if self.timeline.width() < 768:
            self.nb_ticks = 8
        elif self.timeline.width() < 1024:
            self.nb_ticks = 12


class Annotation(QGraphicsRectItem):
    DEFAULT_PEN_COLOR = QColor(0, 0, 0, 255)
    DEFAULT_BG_COLOR = QColor(255, 48, 48, 128)
    DEFAULT_FONT_COLOR = QColor(0, 0, 0, 255)

    def __init__(self, timeline: TimeLineWidget = None, group=None):
        """Initializes the Annotation widget"""
        super().__init__()
        self.brushColor = self.DEFAULT_BG_COLOR
        self.penColor = self.DEFAULT_PEN_COLOR
        self.fontColor = self.DEFAULT_FONT_COLOR
        self.group = group
        self.name = None
        self.timeline = timeline
        self.startTime = timeline.value
        self.endTime = timeline.value
        self.startXPosition = int(
            self.startTime * self.timeline.scene.width() / self.timeline.duration
        )
        self.endXPosition = self.startXPosition
        self.set_default_rect()
        self.selected = False
        self.startHandle: AnnotationHandle = None
        self.endHandle: AnnotationHandle = None

        self.setX(self.startXPosition)
        self.setY(self.timeline.timelineScale.rect().height())

        self.rectItem = QGraphicsRectItem(self)

    def set_default_rect(self):
        self.setRect(
            QRectF(
                0,
                0,
                self.endXPosition - self.startXPosition,
                self.timeline.scene.height()
                - self.timeline.timelineScale.rect().height(),
            )
        )

    def isSelected(self):
        return self.selected

    def setSelected(self, selected):
        self.selected = selected

    def mouseDoubleClickEvent(self, event):
        self.setSelected(True)
        super().mouseDoubleClickEvent(event)
        self.update()

    def focusOutEvent(self, event):
        self.setSelected(False)
        super().focusOutEvent(event)
        self.update()

    def contextMenuEvent(self, event):
        if not self.isSelected():
            super().contextMenuEvent(event)
            return
        menu = QMenu()
        menu.addAction("Delete").triggered.connect(self.on_remove)
        menu.exec(event.screenPos())

    def on_remove(self):
        self.remove()

    def remove(self):
        self.timeline.scene.removeItem(self)
        self.timeline.remove_annotation(self)
        if self.group:
            self.group.remove_annotation(self)
        del self

    def paint(self, painter, option, widget=...):
        # Draw the annotation rectangle
        self._draw_rect(painter)

        # Draw the name of the annotation in the annotation rectangle
        self._draw_name(painter)

        if self.isSelected():
            self.show_handles()
        else:
            self.hide_handles()

    def _draw_rect(self, painter):
        """Draw the annotation rectangle"""
        pen: QPen = QPen(self.penColor)

        if self.isSelected():
            # Set border dotline if annotation is selected
            pen.setStyle(Qt.PenStyle.DotLine)
        painter.setPen(pen)
        painter.setBrush(self.brushColor)

        # Draw the rectangle
        painter.drawRect(self.rect())

    def _draw_name(self, painter):
        """Draws the name of the annotation"""
        if self.name:
            if colour.Color(self.brushColor.name()).luminance < 0.5:
                col = Qt.GlobalColor.white
            else:
                col = Qt.GlobalColor.black
            painter.setPen(col)
            painter.setBrush(col)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.name)

    def set_group(self, group=None):
        """Updates the group"""
        if group is None:
            self.group = None
            self.brushColor = self.DEFAULT_BG_COLOR
        else:
            self.group = group
            self.brushColor = group.color
            if self.name is None:
                self.name = group.name
            self.setToolTip(self.name)

    def update_rect(self):
        # Calculate position to determine width
        self.startXPosition = (
            self.startTime * self.timeline.scene.width() / self.timeline.duration
        )
        self.endXPosition = (
            self.endTime * self.timeline.scene.width() / self.timeline.duration
        )
        self.setX(self.startXPosition)

        # Update the rectangle
        rect = self.rect()
        rect.setWidth(self.endXPosition - self.startXPosition)
        self.setRect(rect)

        if self.startHandle:
            self.startHandle.setX(self.rect().x())
            self.endHandle.setX(self.rect().width())

    def update_start_time(self, startTime: int):
        self.startTime = startTime
        self.update_rect()
        self.update()

    def update_end_time(self, endTime: int):
        """Updates the end time"""
        self.endTime = endTime
        self.update_rect()
        self.update()

    def update_selectable_flags(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.update()

    def create_handles(self):
        self.startHandle = AnnotationStartHandle(self)
        self.endHandle = AnnotationEndHandle(self)

    def finish_create(self):
        self.update_selectable_flags()
        self.create_handles()
        if self.startTime > self.endTime:
            self.startTime, self.endTime = self.endTime, self.startTime
            self.update_rect()
        self.update()

    def show_handles(self):
        if self.startHandle:
            self.startHandle.setVisible(True)
        if self.endHandle:
            self.endHandle.setVisible(True)

    def hide_handles(self):
        if self.startHandle:
            self.startHandle.setVisible(False)
        if self.endHandle:
            self.endHandle.setVisible(False)


class AnnotationHandle(QGraphicsRectItem):
    def __init__(self, annotation: Annotation, value: int, x: float):
        super().__init__(annotation)
        self.annotation = annotation
        self.value = value

        self.setPen(self.annotation.penColor)
        self.setBrush(self.annotation.brushColor)
        self.setVisible(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setAcceptDrops(True)

        width = 9
        self._height = annotation.rect().height() / 2
        self.setRect(QRectF(-4.5, 0, width, self._height))

        self.setX(x)
        self.setY(self._height / 2)

    @abstractmethod
    def change_time(self, new_time):
        self.value = new_time

    def focusInEvent(self, event):
        self.annotation.setSelected(True)
        self.annotation.timeline.player.set_position(self.value)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.annotation.setSelected(False)
        super().focusOutEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.setY(self._height / 2)

            # A la souris on déplace le X, il faut changer le temps
            time = int(
                event.scenePos().x()
                * self.annotation.timeline.duration
                / self.annotation.timeline.scene.width()
            )
            self.annotation.timeline.player.set_position(time)


class AnnotationStartHandle(AnnotationHandle):

    def __init__(self, annotation: Annotation):
        super().__init__(annotation, annotation.startTime, 0)

    def change_time(self, time):
        super().change_time(time)
        self.annotation.update_start_time(time)


class AnnotationEndHandle(AnnotationHandle):
    def __init__(self, annotation: Annotation):
        super().__init__(annotation, annotation.endTime, annotation.rect().width())

    def change_time(self, time):
        super().change_time(time)
        self.annotation.update_end_time(time)


class AnnotationGroup:
    def __init__(
        self, id: int, name: str, color: QColor = None, timeline: TimeLineWidget = None
    ):
        """Initializes the annotation group"""
        self.id = id
        self.name = name
        self.color = color
        self.timeline = timeline
        self.annotations = []

    def add_annotation(self, annotation: Annotation):
        annotation.name = self.name
        annotation.set_group(self)
        self.annotations.append(annotation)

    def remove_annotation(self, annotation: Annotation):
        annotation.name = None
        annotation.set_group(None)
        self.annotations.remove(annotation)


class AnnotationGroupDialog(QDialog):
    DEFAULT_COLOR = QColor(255, 255, 255)
    """Dialog to select or create a new annotation group"""

    def __init__(self, timeline: TimeLineWidget = None):
        super().__init__(timeline)
        self.setWindowTitle("New annotation")

        self.color = self.DEFAULT_COLOR
        self.combo_box = QComboBox()
        for group in timeline.groups:
            self.combo_box.addItem(group.name, group)
        self.combo_box.setEditable(True)

        self.label_2 = QLabel("New label")
        self.group_name_text = QLineEdit()

        self.button_color_2 = QPushButton("Color")
        self.button_color_2.clicked.connect(self.on_button_color_2_clicked)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        self.abort_button = QPushButton("Abort")
        self.abort_button.clicked.connect(self.abort)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)

        # Create layout for contents
        layout = QHBoxLayout()
        layout.addWidget(self.combo_box)
        layout.addWidget(self.label_2)
        layout.addWidget(self.group_name_text)
        layout.addWidget(self.button_color_2)

        # Create layout for main buttons
        main_button_layout = QHBoxLayout()
        main_button_layout.addWidget(self.cancel_button)
        main_button_layout.addWidget(self.abort_button)
        main_button_layout.addWidget(self.save_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(main_button_layout)

        self.setLayout(main_layout)

        if timeline.groups:
            self.state = "choose"
        else:
            self.state = "create"

        self.set_visibility()

    def accept(self):
        if self.combo_box.currentData() or self.state == "create":
            super().accept()
        else:
            self.state = "create"
            self.group_name_text.setText(self.combo_box.currentText())
            self.set_visibility()
            self.group_name_text.setFocus()

    def abort(self):
        confirm_box = AnnotationConfirmMessageBox(self)
        if confirm_box.result() == QMessageBox.DialogCode.Accepted:
            self.done(AnnotationDialogCode.Aborted)

    def on_button_color_2_clicked(self):
        self.color = QColorDialog.getColor()

    def set_visibility(self):
        if self.state == "choose":
            self.combo_box.setVisible(True)
            self.label_2.setVisible(False)
            self.group_name_text.setVisible(False)
            self.button_color_2.setVisible(False)
        else:
            self.combo_box.setVisible(False)
            self.label_2.setVisible(True)
            self.group_name_text.setVisible(True)
            self.button_color_2.setVisible(True)
        self.save_button.setDefault(True)


class AnnotationConfirmMessageBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(
            QMessageBox.Icon.Warning,
            "Warning",
            "Are you sure to abort the creation of this annotation ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            parent,
        )

        self.button(QMessageBox.StandardButton.Yes).clicked.connect(self.accept)
        self.button(QMessageBox.StandardButton.No).clicked.connect(self.reject)
        self.exec()


class AnnotationDialogCode(IntEnum):
    Accepted: int = QDialog.DialogCode.Accepted  # 0
    Canceled: int = QDialog.DialogCode.Rejected  # 1
    Aborted: int = 2
