# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2018-2022 Andrew Rechnitzer
# Copyright (C) 2020-2024 Colin B. Macdonald
# Copyright (C) 2020 Victoria Schuster
# Copyright (C) 2022 Joey Shi
# Copyright (C) 2024 Aden Chan

# a different kind of annotations... this is about code typing
from __future__ import annotations

from copy import deepcopy
from itertools import cycle
import logging
from pathlib import Path
from typing import Any

import PIL.Image

from PyQt6.QtCore import Qt, QEvent, QRectF, QLineF, QPointF
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QCursor,
    QImage,
    QImageReader,
    QFont,
    QGuiApplication,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QTransform,
    QUndoStack,
)
from PyQt6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QGraphicsPathItem,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsSceneDragDropEvent,
    QGraphicsTextItem,
    QGraphicsView,
    QGraphicsItemGroup,
    QMessageBox,
    QToolButton,
    QMenu,
)

from plom import AnnFontSizePts, ScenePixelHeight
from plom.plom_exceptions import PlomInconsistentRubric
from plom.client.image_view_widget import mousewheel_delta_to_scale

from .tools import (
    CrossItem,
    DeltaItem,
    GhostComment,
    RubricItem,
    TextItem,
    TickItem,
)
from .tools import (
    CommandArrow,
    CommandArrowDouble,
    CommandBox,
    CommandEllipse,
    CommandImage,
    CommandDelete,
    CommandText,
    CommandRubric,
    CommandLine,
    CommandTick,
    CommandQMark,
    CommandCross,
    CommandPen,
    CommandHighlight,
    CommandPenArrow,
    CommandCrop,
)
from .elastics import (
    which_horizontal_step,
    which_sticky_corners,
    which_classic_shortest_corner_side,
    which_centre_to_centre,
)
from plom.client.rubrics import compute_score


log = logging.getLogger("pagescene")


class ScoreBox(QGraphicsTextItem):
    """Indicate the current total mark in the top-left.

    Drawn with a rounded-rectangle border.
    """

    def __init__(self, style, fontsize, maxScore, score, question_label=None):
        """Initialize a new ScoreBox.

        Args:
            style (dict): pen width, annotation colour, etc.
            fontsize (int): A non-zero, positive font value.
            maxScore (int): A non-zero, positive maximum score.
            score (int): A non-zero, positive current score for the paper.
            question_label (str/None): how to display the question
                number, or `None` to display no label at the beginning
                of the score box.
        """
        super().__init__()
        self.score = score
        self.maxScore = maxScore
        self.question_label = question_label
        self.style = style
        self.setDefaultTextColor(self.style["annot_color"])
        font = QFont("Helvetica")
        # Note: PointSizeF seems effected by DPI on Windows (Issue #1071).
        # Strangely, it seems like setPixelSize gives reliable sizes!
        font.setPixelSize(round(1.25 * fontsize))
        self.setFont(font)
        # Not editable.
        self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.setPos(0, 0)
        self._update_text()

    def _update_text(self):
        """Update the displayed text."""
        s = ""
        if self.question_label:
            s += self.question_label + ": "
        if self.score is None:
            s += "Unmarked"
        else:
            s += "{} out of {}".format(self.score, self.maxScore)
        self.setPlainText(s)

    def get_text(self):
        return self.toPlainText()

    def update_style(self):
        self.style = self.scene().style
        self.setDefaultTextColor(self.style["annot_color"])

    def changeScore(self, x: int | None) -> None:
        """Set the score to x.

        Args:
            x: a value or zero for no score yet assigned.

        Returns:
            None
        """
        self.score = x
        self._update_text()

    def changeMax(self, x: int) -> None:
        """Set the max possible mark to x.

        Args:
            x: A non-zero, positive new maximum mark.

        Returns:
            None
        """
        # set the max-mark.
        self.maxScore = x
        self._update_text()

    def paint(self, painter, option, widget):
        """Paint a rounded rectangle border around the scorebox text.

        Args:
            painter (QPainter): Current painter object.
            option (QStyleOptionGraphicsItem): Style options.
            widget (QWidget): Associated widgets.

        Returns:
            None

        Notes:
            Overrides parent method.
        """
        painter.setPen(QPen(self.style["annot_color"], self.style["pen_width"]))
        painter.setBrush(QBrush(QColor(255, 255, 255, 192)))
        painter.drawRoundedRect(option.rect, 10, 10)
        super().paint(painter, option, widget)


class UnderlyingRect(QGraphicsRectItem):
    """A simple white rectangle with dotted border.

    Used to add a nice white margin with dotted border around everything.
    """

    def __init__(self, rect):
        super().__init__()
        self.setPen(QPen(QColor("black"), 4, style=Qt.PenStyle.DotLine))
        self.setBrush(QBrush(QColor(249, 249, 249, 255)))
        self.setRect(rect)
        self.setZValue(-10)


class MaskingOverlay(QGraphicsItemGroup):
    """A transparent rectangular border to place over the images."""

    def __init__(self, outer_rect, inner_rect):
        super().__init__()
        self.outer_rect = outer_rect
        self.inner_rect = inner_rect
        # keep the original inner rectangle for uncropping.
        self.original_inner_rect = inner_rect

        # set rectangles for semi-transparent boundaries - needs some tmp rectangle.
        self.top_bar = QGraphicsRectItem(outer_rect)
        self.bottom_bar = QGraphicsRectItem(outer_rect)
        self.left_bar = QGraphicsRectItem(outer_rect)
        self.right_bar = QGraphicsRectItem(outer_rect)
        self.dotted_boundary = QGraphicsRectItem(inner_rect)
        transparent_paint = QBrush(QColor(249, 249, 249, 220))
        dotted_pen = QPen(QColor(0, 0, 0, 128), 2, style=Qt.PenStyle.DotLine)
        self.top_bar.setBrush(transparent_paint)
        self.bottom_bar.setBrush(transparent_paint)
        self.left_bar.setBrush(transparent_paint)
        self.right_bar.setBrush(transparent_paint)
        self.top_bar.setPen(QPen(Qt.PenStyle.NoPen))
        self.bottom_bar.setPen(QPen(Qt.PenStyle.NoPen))
        self.left_bar.setPen(QPen(Qt.PenStyle.NoPen))
        self.right_bar.setPen(QPen(Qt.PenStyle.NoPen))
        self.dotted_boundary.setPen(dotted_pen)
        # now set the size correctly
        self.set_bars()
        self.addToGroup(self.top_bar)
        self.addToGroup(self.bottom_bar)
        self.addToGroup(self.left_bar)
        self.addToGroup(self.right_bar)
        self.addToGroup(self.dotted_boundary)
        self.setZValue(-1)

    def crop_to_focus(self, crop_rect):
        self.inner_rect = crop_rect
        self.set_bars()
        self.update()

    def get_original_inner_rect(self):
        return self.original_inner_rect

    def set_bars(self):
        # reset the dotted boundary rectangle
        self.dotted_boundary.setRect(self.inner_rect)
        # set rectangles using rectangle defined by top-left and bottom-right points.
        self.top_bar.setRect(
            QRectF(
                self.outer_rect.topLeft(),
                QPointF(
                    self.outer_rect.topRight().x(),
                    self.inner_rect.topRight().y(),
                ),
            )
        )
        self.bottom_bar.setRect(
            QRectF(
                QPointF(
                    self.outer_rect.bottomLeft().x(),
                    self.inner_rect.bottomLeft().y(),
                ),
                self.outer_rect.bottomRight(),
            )
        )
        self.left_bar.setRect(
            QRectF(
                QPointF(
                    self.outer_rect.topLeft().x(),
                    self.inner_rect.topLeft().y(),
                ),
                self.inner_rect.bottomLeft(),
            )
        )
        self.right_bar.setRect(
            QRectF(
                self.inner_rect.topRight(),
                QPointF(
                    self.outer_rect.bottomRight().x(),
                    self.inner_rect.bottomRight().y(),
                ),
            )
        )


class UnderlyingImages(QGraphicsItemGroup):
    """Group for the images of the underlying pages being marked.

    Puts a dotted border around all the images.
    """

    def __init__(self, image_data):
        """Initialize a new series of underlying images.

        Args:
            image_data (list[dict]): each dict has keys 'filename'
                and 'orientation' (and possibly others).  Currently
                every image is used and the list order determines
                the order.  That is subject to change.
        """
        super().__init__()
        self.images = {}
        x = 0
        for n, data in enumerate(image_data):
            qir = QImageReader(str(data["filename"]))
            # deal with jpeg exif rotations
            qir.setAutoTransform(True)
            # In principle scaling in QImageReader or QPixmap can give better
            # zoomed out quality: https://gitlab.com/plom/plom/-/issues/1989
            # qir.setScaledSize(QSize(768, 1000))
            pix = QPixmap(qir.read())
            if pix.isNull():
                raise RuntimeError(f"Could not read an image from {data['filename']}")
            # after metadata rotations, we might have a further DB-level rotation
            rot = QTransform()
            # 90 means CCW, but we have a minus sign b/c of a y-downward coordsys
            rot.rotate(-data["orientation"])
            pix = pix.transformed(rot)
            img = QGraphicsPixmapItem(pix)
            # this gives (only) bilinear interpolation
            img.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
            # works but need to adjust the origin of rotation, probably faster
            # img.setTransformOriginPoint(..., ...)
            # img.setRotation(img['orientation'])
            img.setPos(x, 0)
            sf = float(ScenePixelHeight) / float(pix.height())
            img.setScale(sf)
            # TODO: why not?
            # x += img.boundingRect().width()
            # help prevent hairline: subtract one pixel before converting
            x += sf * (pix.width() - 1.0)
            # TODO: don't floor here if units of scene are large!
            x = int(x)
            self.images[n] = img
            self.addToGroup(self.images[n])

        self.setZValue(-1)

    @property
    def min_dimension(self):
        return min(self.boundingRect().height(), self.boundingRect().width())


# Dictionaries to translate tool-modes into functions
# for mouse press, move and release
mousePress = {
    "box": "mousePressBox",
    "rubric": "mousePressRubric",
    "cross": "mousePressCross",
    "delete": "mousePressDelete",
    "line": "mousePressLine",
    "move": "mousePressMove",
    "pan": "mousePressPan",
    "pen": "mousePressPen",
    "text": "mousePressText",
    "tick": "mousePressTick",
    "zoom": "mousePressZoom",
    "image": "mousePressImage",
    "crop": "mousePressCrop",
}
mouseMove = {
    "box": "mouseMoveBox",
    "cross": "mouseMoveCross",
    "delete": "mouseMoveDelete",
    "line": "mouseMoveLine",
    "pen": "mouseMovePen",
    "rubric": "mouseMoveRubric",
    "text": "mouseMoveText",
    "tick": "mouseMoveTick",
    "zoom": "mouseMoveZoom",
    "crop": "mouseMoveCrop",
}
mouseRelease = {
    "box": "mouseReleaseBox",
    "cross": "mouseReleaseCross",
    "delete": "mouseReleaseDelete",
    "line": "mouseReleaseLine",
    "move": "mouseReleaseMove",
    "pen": "mouseReleasePen",
    "pan": "mouseReleasePan",
    "zoom": "mouseReleaseZoom",
    "rubric": "mouseReleaseRubric",
    "text": "mouseReleaseText",
    "tick": "mouseReleaseTick",
    "crop": "mouseReleaseCrop",
}

# things for nice rubric/text drag-box tool
# work out how to draw line from current point
# to nearby point on a given rectangle
# also need a minimum size threshold for that box
# in order to avoid drawing very very small boxes
# by accident when just "clicking"
# see #1435

minimum_box_side_length = 24


class PageScene(QGraphicsScene):
    """An extended QGraphicsScene for interacting with annotations on top of underlying images.

    Extend the graphics scene so that it knows how to translate
    mouse-press/move/release into operations on QGraphicsItems and
    QTextItems.
    """

    def __init__(self, parent, src_img_data, maxMark, question_label):
        """Initialize a new PageScene.

        Args:
            parent (Annotator): the parent of the scene.  Currently
                this *must* be an Annotator, because we call various
                functions from that Annotator.
            src_img_data (list[dict]): metadata for the underlying
                source images.  Each dict has (at least) keys for
               `filename` and `orientation`.
            maxMark(int): maximum possible mark.
            question_label (str/None): how to display this question, for
                example a string like "Q7", or `None` if not relevant.
        """
        super().__init__(parent)
        self.src_img_data = deepcopy(src_img_data)
        self.maxMark = maxMark
        self.score = None
        self._page_hack_buttons = []
        # Tool mode - initially set it to "move"
        self.mode = "move"

        self.underImage = None
        self.underRect = None
        self.overMask = None
        self.buildUnderLay()

        self.whichLineToDraw_init()

        # initialise the undo-stack
        self.undoStack = QUndoStack()

        # we don't want current font size from UI; use fixed physical size
        self.fontSize = AnnFontSizePts
        self._scale = 1.0

        self.scoreBox = None
        # Define standard pen, highlight, fill, light-fill
        self.set_annotation_color(QColor("red"))
        self.deleteBrush = QBrush(QColor(255, 0, 0, 16))
        self.zoomBrush = QBrush(QColor(0, 0, 255, 16))
        # Flags to indicate if drawing an arrow (vs line), highlight (vs
        # regular pen), box (vs ellipse), area-delete vs point.
        self.arrowFlag = 0
        self.penFlag = 0
        self.boxFlag = 0
        self.deleteFlag = 0
        self.zoomFlag = 0
        # The box-drag-rubric composite object is constructed in stages
        # 0 = no box-drag-rubric is currently in progress (default)
        # 1 = drawing the box
        # 2 = drawing the line
        # 3 = drawing the rubric - this should only be very briefly mid function.
        # 4 = some sort of error
        self.boxLineStampState = 0

        # Will need origin, current position, last position points.
        self.originPos = QPointF(0, 0)
        self.currentPos = QPointF(0, 0)
        self.lastPos = QPointF(0, 0)

        # Builds path for different tool items.
        self.path = QPainterPath()
        self.pathItem = QGraphicsPathItem()
        # TODO: should we be reusing these instead of instantiating new ones later?
        self.boxItem = QGraphicsRectItem()
        self.delBoxItem = QGraphicsRectItem()
        self.zoomBoxItem = QGraphicsRectItem()
        self.ellipseItem = QGraphicsEllipseItem()
        self.lineItem = QGraphicsLineItem()

        # Add a ghost comment to scene, but make it invisible
        self.ghostItem = GhostComment("1", "blah", self.fontSize)
        self._hideGhost()
        self.addItem(self.ghostItem)

        # cache some data about the currently selected rubric
        self.current_rubric = None

        # Build a scorebox and set it above all our other graphicsitems
        # so that it cannot be overwritten.
        # set up "k out of n" where k=current score, n = max score.
        self.scoreBox = ScoreBox(
            self.style, self.fontSize, self.maxMark, self.score, question_label
        )
        self.scoreBox.setZValue(10)
        self.addItem(self.scoreBox)

        # make a box around the scorebox where mouse-press-event won't work.
        # make it fairly wide so that items pasted are not obscured when
        # scorebox updated and becomes wider
        self.avoidBox = self.scoreBox.boundingRect().adjusted(-16, -16, 64, 24)
        # holds the path images uploaded from annotator
        self.tempImagePath = None

    def buildUnderLay(self):
        if self.underImage:
            log.debug("removing underImage")
            self.removeItem(self.underImage)
        if self.underRect:
            self.removeItem(self.underRect)
            log.debug("removing underRect")
        if self.overMask:
            self.removeItem(self.overMask)
            log.debug("removing overMask")

        # build pixmap and graphicsitemgroup.
        self.underImage = UnderlyingImages(self.src_img_data)
        # a margin that surrounds the scanned images, with size related to the
        # minimum dimensions of the images, but never smaller than 512 pixels
        margin_width = max(512, 0.20 * self.underImage.min_dimension)
        margin_rect = QRectF(self.underImage.boundingRect()).adjusted(
            -margin_width, -margin_width, margin_width, margin_width
        )
        self.underRect = UnderlyingRect(margin_rect)
        # TODO: the overmask has wrong z-value on rebuild (?)
        self.overMask = MaskingOverlay(margin_rect, self.underImage.boundingRect())
        self.addItem(self.underRect)
        self.addItem(self.underImage)
        self.addItem(self.overMask)

        if self.parent().is_experimental():
            self.build_page_hack_buttons()

        # Build scene rectangle to fit the image, and place image into it.
        self.setSceneRect(self.underImage.boundingRect())

    def remove_page_hack_buttons(self):
        for h in self._page_hack_buttons:
            self.removeItem(h)
            h.deleteLater()
        self._page_hack_buttons = []

    def build_page_hack_buttons(self):
        # TODO: Issue #2522 remove early return to enable this feature
        return

        def page_delete_func_factory(n):
            def page_delete():
                img = self.underImage.images[n]
                self.src_img_data.pop(n)
                br = img.mapRectToScene(img.boundingRect())
                log.debug(f"About to delete img {n}: left={br.left()} w={br.width()}")
                # shift existing annotations leftward
                loc = br.right()
                if n == len(self.underImage.images) - 1:
                    # special case when deleting right-most image
                    loc = br.left()
                stuff = self.find_items_right_of(loc)
                self.move_some_items(stuff, -br.width(), 0)
                # TODO: replace with emit signal (if needed)
                # self.parent().report_new_or_permuted_image_data(self.src_img_data)
                self.buildUnderLay()

            return page_delete

        def page_shift_func_factory(n, relative):
            def page_shift():
                d = self.src_img_data.pop(n)
                self.src_img_data.insert(n + relative, d)
                # self.parent().report_new_or_permuted_image_data(self.src_img_data)
                self.buildUnderLay()

            return page_shift

        def page_rotate_func_factory(n, degrees):
            def page_rotate():
                # get old page width and location, select rightward objects to shift
                img = self.underImage.images[n]
                br = img.mapRectToScene(img.boundingRect())
                loc = br.right()
                w = br.width()
                log.debug(f"About to rotate img {n} by {degrees}: right pt {loc} w={w}")
                stuff = self.find_items_right_of(loc)
                # do the rotation in metadata and rebuild
                self.src_img_data[n]["orientation"] += degrees
                # self.parent().report_new_or_permuted_image_data(self.src_img_data)
                self.buildUnderLay()
                # shift previously-selected rightward annotations by diff in widths
                img = self.underImage.images[n]
                br = img.mapRectToScene(img.boundingRect())
                log.debug(f"After rotation: old width {w} now {br.width()}")
                self.move_some_items(stuff, br.width() - w, 0)

            return page_rotate

        self.remove_page_hack_buttons()
        for n in range(len(self.underImage.images)):
            img = self.underImage.images[n]
            b = QToolButton(text=f"Page {n}")
            # b = QToolButton(text=f"\N{Page}")
            b.setStyleSheet("background-color: #ff6666")
            # parenting the menu inside the scene
            m = QMenu(b)
            # TODO: nicer to parent by Annotr but unsupported (?) and unpredictable
            # m = QMenu(self.parent())
            _ = m.addAction("Remove this page", page_delete_func_factory(n))
            if len(self.underImage.images) == 1:
                _.setEnabled(False)
                _.setToolTip("Cannot remove lone page")
            _ = m.addAction("Shift left", page_shift_func_factory(n, -1))
            if n == 0:
                _.setEnabled(False)
            _ = m.addAction("Shift right", page_shift_func_factory(n, 1))
            if n == len(self.underImage.images) - 1:
                _.setEnabled(False)
            m.addAction(
                "\N{Anticlockwise Open Circle Arrow} Rotate CCW",
                page_rotate_func_factory(n, -90),
            )
            m.addAction(
                "\N{Clockwise Open Circle Arrow} Rotate CW",
                page_rotate_func_factory(n, 90),
            )
            m.addAction("Flip", page_rotate_func_factory(n, 180))
            m.addSeparator()
            m.addAction("Find other pages...", self.parent().rearrangePages)
            b.setMenu(m)
            b.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            h = self.addWidget(b)
            h.setScale(1.8)
            br = img.mapRectToScene(img.boundingRect())
            wbr = h.mapRectToScene(h.boundingRect())
            # h.setPos(br.right() - wbr.width(), br.top() - wbr.height())
            # h.setPos(br.right() - wbr.width(), br.top())
            h.setPos(
                br.left() + br.width() / 2 - wbr.width() / 2,
                br.top() - wbr.height() / 2,
            )
            # h.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations)
            b.setToolTip(f"Page options for page {n}")
            self._page_hack_buttons.append(h)

    def getScore(self):
        return self.score

    def is_neutral_state(self) -> bool:
        """Has the mark has been changed from the unmarked state?

        No annotations is a neutral state.  Annotations that do not change the
        mark leave the scene in a neutral state.   Even neutral rubrics leave
        the scene in the neutral state.  But the use of any mark-changing
        annotation (currently non-neutral rubrics) will change the scene from
        neutral to non-neutral.

        Returns:
            True if the mark has been changed to a concrete value.
        """
        return self.getScore() is None

    def refreshStateAndScore(self):
        self.refreshScore()
        # after score and state are recomputed, we need to update a few things
        # the scorebox
        self.scoreBox.changeScore(self.score)
        # update the rubric-widget
        self.parent().rubric_widget.updateLegalityOfRubrics()
        # also update the marklabel in the annotator - same text as scorebox
        self.parent().refreshDisplayedMark(self.score)

        # update the ghostcomment if in rubric-mode.
        if self.mode == "rubric":
            self._updateGhost(self.current_rubric)

    def get_rubrics(self):
        """A list of the rubrics current used in the scene.

        Return:
            list: a list of dicts, one for each rubric that is on the page.

        TODO: we will be calling this function quite a lot: maybe its worth
        caching or something.
        """
        rubrics = []
        for X in self.items():
            # check if object has "saveable" attribute and it is set to true.
            if getattr(X, "saveable", False):
                if isinstance(X, RubricItem):
                    rubrics.append(X.as_rubric())
        return rubrics

    def refreshScore(self):
        """Compute the current score by adding up the rubric items on the page.

        Note that this assumes that the rubrics are consistent as per currentMarkingState
        """
        self.score = compute_score(self.get_rubrics(), self.maxMark)

    def get_src_img_data(self):
        return self.src_img_data

    def how_many_underlying_images_wide(self):
        """Count how many images wide the bottom layer is.

        Currently this is just the number of images (because we layout
        in one long row) but future revisions might support alternate
        layouts.
        """
        return len(self.src_img_data)

    def how_many_underlying_images_high(self):
        """How many images high is the bottom layer.

        Currently this is always 1 because we align the images in a
        single row but future revisions might support alternate layouts.
        """
        return 1

    def reset_scale_factor(self):
        self._scale = 1.0
        self._stuff_to_do_after_setting_scale()

    def get_scale_factor(self):
        return self._scale

    def set_scale_factor(self, scale):
        """The scale factor scales up or down all annotations."""
        self._scale = scale
        self._stuff_to_do_after_setting_scale()

    def increase_scale_factor(self, r: float = 1.1) -> None:
        """Scale up the annotations by 110%.

        Args:
            r: the multiplicative factor, defaults to 1.1.
        """
        self._scale *= r
        self._stuff_to_do_after_setting_scale()

    def decrease_scale_factor(self, r: float = 1.1) -> None:
        """Scale down the annotations by 110%.

        Args:
            r: the scale is multiplied by 1/r.
        """
        self.increase_scale_factor(1.0 / r)

    def _stuff_to_do_after_setting_scale(self):
        """Private method for tasks after changing scale.

        TODO: I'd like to move to a model where fontSize is constant
        and all things (line widths, fonts, etc) get multiplied by scale
        """
        self.fontSize = self._scale * AnnFontSizePts
        # TODO: don't like this 1.25 hardcoded
        font = QFont("Helvetica")
        font.setPixelSize(round(1.25 * self.fontSize))
        self.scoreBox.setFont(font)
        self.ghostItem.change_font_size(self.fontSize)

    def set_annotation_color(self, c):
        """Set the colour of annotations.

        Args:
            c (QColor/tuple): a QColor or an RGB triplet describing
                the new colour.
        """
        try:
            c = QColor(c)
        except TypeError:
            c = QColor.fromRgb(*c)
        style = {
            "annot_color": c,
            "pen_width": 2,
            # TODO: 64 hardcoded elsewhere
            "highlight_color": QColor(255, 255, 0, 64),
            "highlight_width": 50,
            # light highlight for backgrounds
            "box_tint": QColor(255, 255, 0, 16),
        }
        self.ink = QPen(style["annot_color"], style["pen_width"])
        self.lightBrush = QBrush(style["box_tint"])
        self.highlight = QPen(style["highlight_color"], style["highlight_width"])
        self.style = style
        for X in self.items():
            # check if object has "restyle" function and if so then use it to set the colour
            if getattr(X, "restyle", False):
                X.restyle(self.style)
        if self.scoreBox:
            self.scoreBox.update_style()

    def setToolMode(self, mode: str) -> None:
        """Sets the current toolMode.

        Args:
            mode: One of "rubric", "pan", "move" etc..

        Returns:
            None
        """
        # set focus so that shift/control change cursor
        self.views()[0].setFocus(Qt.FocusReason.TabFocusReason)

        self.mode = mode

        # To fix issues with changing mode mid-draw - eg #1540
        # trigger this
        self.stopMidDraw()

        # if current mode is not rubric, make sure the ghostcomment is hidden
        if self.mode != "rubric":
            self._hideGhost()
        else:
            # Careful, don't want it to appear at an old location
            gpt = QCursor.pos()  # global mouse pos
            vpt = self.views()[0].mapFromGlobal(gpt)  # mouse pos in view
            spt = self.views()[0].mapToScene(vpt)  # mouse pos in scene
            self.ghostItem.setPos(spt)
            self._exposeGhost()

        # if mode is "pan", allow the view to drag about, else turn it off
        if self.mode == "pan":
            self.views()[0].setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        else:
            self.views()[0].setDragMode(QGraphicsView.DragMode.NoDrag)

    def get_nonrubric_text_from_page(self):
        """Get the current text items and rubrics associated with this paper.

        Returns:
            list: strings from each bit of text.
        """
        texts = []
        for X in self.items():
            if isinstance(X, TextItem):
                # if item is in a rubric then its 'group' will be non-null
                # only keep those with group=None to keep non-rubric text
                if X.group() is None:
                    texts.append(X.toPlainText())
        return texts

    def get_rubric_ids(self):
        """Get the rubric IDs associated with this scene.

        Returns:
            list: of IDs.
        """
        rubrics = []
        for X in self.items():
            if isinstance(X, RubricItem):
                rubrics.append(X.rubricID)
        return rubrics

    def countComments(self) -> int:
        """Counts current text items and comments associated with the paper.

        Returns:
            Total number of comments associated with this paper.
        """
        count = 0
        for X in self.items():
            if type(X) is TextItem:
                count += 1
        return count

    def countRubrics(self) -> int:
        """Counts current rubrics (comments) associated with the paper.

        Returns:
            Total number of rubrics associated with this paper.
        """
        count = 0
        for X in self.items():
            if type(X) is RubricItem:
                count += 1
        return count

    def get_current_rubric_id(self):
        """Last-used or currently held rubric.

        Returns:
            int/str/None: the ID of the last-used or currently held
                rubric.  None probably means we never had one.
        """
        if not self.current_rubric:
            return None
        return self.current_rubric["id"]

    def reset_dirty(self):
        # TODO: what is the difference?
        # self.undoStack.resetClean()
        self.undoStack.setClean()

    def is_dirty(self) -> bool:
        """Has the scene had annotations modified since it was last clean?

        Note that annotations from a older session should not cause this
        to return true.  If you have "saved" annotations you should call
        :meth:`reset_dirty` to ensure this property.
        """
        return not self.undoStack.isClean()

    def hasAnnotations(self) -> bool:
        """Checks for pickleable annotations.

        Returns
            True if page scene has any pickle-able annotations.
            False otherwise.
        """
        for X in self.items():
            if getattr(X, "saveable", False):
                return True
        # no pickle-able items means no annotations.
        return False

    def getSaveableRectangle(self):
        # the rectangle is set to our current (potentially cropped) inner-rect of the masking
        br = self.overMask.mapRectToScene(self.overMask.inner_rect)
        # for context in cropped case, expand the crop-rect in each direction
        pad = max(128, 0.1 * min(br.height(), br.width()))
        br.adjust(-pad, -pad, pad, pad)
        # and then intersect that with the underlying-image rect
        br = br.intersected(self.underImage.boundingRect())

        # now potentially expand again for any annotations still outside
        for X in self.items():
            if getattr(X, "saveable", False):
                # now check it is inside the UnderlyingRect
                if X.collidesWithItem(
                    self.underRect, mode=Qt.ItemSelectionMode.ContainsItemShape
                ):
                    # add a little padding around things.
                    br = br.united(
                        X.mapRectToScene(X.boundingRect()).adjusted(-16, -16, 16, 16)
                    )
        return br

    def updateSceneRectangle(self):
        self.setSceneRect(self.getSaveableRectangle())
        self.update()

    def save(self, basename):
        """Save the annotated group-image.

        Args:
            basename (str/pathlib.Path): where to save, we will add a png
                or jpg extension to it.  If the file already exists, it
                will be overwritten.

        Returns:
            pathlib.Path: the file we just saved to, including jpg or png.
        """
        # don't want to render these, but should we restore them after?
        # TODO: or setVisible(False) instead of remove?
        self.remove_page_hack_buttons()

        self._hideGhost()

        # Get the width and height of the image
        br = self.getSaveableRectangle()
        self.setSceneRect(br)
        w = br.width()
        h = br.height()
        MINWIDTH = 1024  # subject to maxheight
        MAXWIDTH = 15999  # 16383 but for older imagemagick
        MAXHEIGHT = 8191
        MAX_PER_PAGE_WIDTH = 2000
        msg = []
        num_pages = self.how_many_underlying_images_wide()
        if w < MINWIDTH:
            r = (1.0 * w) / (1.0 * h)
            w = MINWIDTH
            h = w / r
            msg.append("Increasing bitmap width because of minimum width constraint")
            if h > MAXHEIGHT:
                h = MAXHEIGHT
                w = h * r
                msg.append("Constraining bitmap height by min width constraint")
        if w > num_pages * MAX_PER_PAGE_WIDTH:
            r = (1.0 * w) / (1.0 * h)
            w = num_pages * MAX_PER_PAGE_WIDTH
            h = w / r
            msg.append("Constraining bitmap width by maximum per page width")
        if w > MAXWIDTH:
            r = (1.0 * w) / (1.0 * h)
            w = MAXWIDTH
            h = w / r
            msg.append("Constraining bitmap width by overall maximum width")
        w = round(w)
        h = round(h)
        if msg:
            log.warning("{}: {}x{}".format(". ".join(msg), w, h))

        # Create an output pixmap and painter (to export it)
        oimg = QPixmap(w, h)
        exporter = QPainter(oimg)
        # Render the scene via the painter
        self.render(exporter)
        exporter.end()

        basename = Path(basename)
        pngname = basename.with_suffix(".png")
        jpgname = basename.with_suffix(".jpg")
        oimg.save(str(pngname))
        # Sadly no control over chroma subsampling which mucks up thin red lines
        # oimg.save(str(jpgname), quality=90)

        # im = PIL.Image.fromqpixmap(oimg)
        im = PIL.Image.open(pngname)
        im.convert("RGB").save(jpgname, quality=90, optimize=True, subsampling=0)

        jpgsize = jpgname.stat().st_size
        pngsize = pngname.stat().st_size
        log.debug("scene rendered: jpg/png sizes (%s, %s) bytes", jpgsize, pngsize)
        # For testing
        # if random.uniform(0, 1) < 0.5:
        if jpgsize < 0.9 * pngsize:
            pngname.unlink()
            return jpgname
        else:
            jpgname.unlink()
            return pngname

    def keyPressEvent(self, event):
        """Changes the focus or cursor based on key presses.

        Notes:
            Overrides parent method.
            Escape key removes focus from the scene.
            Changes the cursor in accordance with each tool's mousePress
            documentation.

        Args:
            event (QKeyEvent): The Key press event.

        Returns:
            None
        """
        # TODO: all this should somehow be an "alternative action" of the tool
        cursor = self.parent().cursor
        variableCursors = {
            "cross": (cursor["tick"], cursor["QMark"]),
            "line": (cursor["arrow"], cursor["DoubleArrow"]),
            "tick": (cursor["cross"], cursor["QMark"]),
            "box": (cursor["ellipse"], cursor["box"]),
            "pen": (cursor["Highlight"], cursor["DoubleArrow"]),
        }

        if self.mode in variableCursors:
            if event.key() == Qt.Key.Key_Shift:
                self.views()[0].setCursor(variableCursors.get(self.mode)[0])
            elif event.key() == Qt.Key.Key_Control:
                self.views()[0].setCursor(variableCursors.get(self.mode)[1])
            else:
                pass

        if event.key() == Qt.Key.Key_Escape:
            self.clearFocus()
            # also if in box,line,pen,rubric,text - stop mid-draw
            if self.mode in ["box", "line", "pen", "rubric", "text", "cross", "tick"]:
                self.stopMidDraw()
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """Changes cursors back to their standard cursor when keys are released.

        Args:
            event (QKeyEvent): the key release.

        Returns:
            None
        """
        variableCursorRelease = {
            "cross": self.parent().cursor["cross"],
            "line": self.parent().cursor["line"],
            "tick": self.parent().cursor["tick"],
            "box": self.parent().cursor["box"],
            "pen": self.parent().cursor["pen"],
        }
        if self.mode in variableCursorRelease:
            if self.views()[0].cursor() == variableCursorRelease.get(self.mode):
                pass
            else:
                self.views()[0].setCursor(variableCursorRelease.get(self.mode))
        else:
            pass

    def wheelEvent(self, event):
        if (
            QGuiApplication.queryKeyboardModifiers()
            == Qt.KeyboardModifier.ControlModifier
        ):
            s = mousewheel_delta_to_scale(event.delta())
            self.views()[0].scale(s, s)
            # sets the view rectangle and updates zoom-dropdown.
            self.views()[0].setZoomSelector(True)
            self.zoomFlag = 0
            event.accept()

    def mousePressEvent(self, event):
        """Call various tool functions depending on the mouse press location.

        Args:
            event (QMouseEvent): The mouse press event.

        Returns:
            None
        """
        # check if mouseclick inside the avoidBox
        if self.avoidBox.contains(event.scenePos()):
            return
        # if there is a visible ghost then check its bounding box avoids the scorebox(+boundaries)
        if self.ghostItem.isVisible():
            if self.avoidBox.intersects(
                self.ghostItem.mapRectToScene(self.ghostItem.boundingRect())
            ):
                return

        # Get the function name from the dictionary based on current mode.
        functionName = mousePress.get(self.mode, None)
        if functionName:
            # If you found a function, then call it.
            return getattr(self, functionName, None)(event)
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Call various tool functions depending on the mouse's location.

        Args:
            event (QMouseEvent): The mouse move event.

        Returns:
            None
        """
        functionName = mouseMove.get(self.mode, None)
        if functionName:
            return getattr(self, functionName, None)(event)
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # Similar to mouse-press but for mouse-release.
        functionName = mouseRelease.get(self.mode, None)
        if functionName:
            return getattr(self, functionName, None)(event)
        return super().mouseReleaseEvent(event)

    # Tool functions for press, move and release.
    # Depending on the tool different functions are called
    # Many (eg tick) just create a graphics item, others (eg line)
    # create a temp object (on press) which is changes (as mouse-moves)
    # and then destroyed (on release) and replaced with the
    # more permanent graphics item.

    def textUnderneathPoint(self, pt):
        """Check to see if any text-like object under point."""
        for under in self.items(pt):
            if (
                isinstance(under, DeltaItem)
                or isinstance(under, TextItem)
                or isinstance(under, RubricItem)
            ):
                return True
        return False

    def textUnderneathGhost(self):
        """Check to see if any text-like object under current ghost-text."""
        for under in self.ghostItem.collidingItems():
            if (
                isinstance(under, DeltaItem)
                or isinstance(under, TextItem)
                or isinstance(under, RubricItem)
            ):
                return True
        return False

    def boxStampPress(self, event, ghost_rect=None):
        # flag can be in 4 states
        # 0 = initial state - we aren't doing anything
        # 1 = box drawing started
        # 2 = box finished, path started
        # 3 = path finished, ready to stamp final object
        # 4 = error state - clean things up.

        if self.boxLineStampState == 0:
            # start the drag-box so (0->1)
            self.boxLineStampState = 1
            self.originPos = event.scenePos()
            self.currentPos = self.originPos
            self.boxItem = QGraphicsRectItem(
                QRectF(self.originPos, self.currentPos).normalized()
            )
            self.boxItem.setPen(self.ink)
            self.boxItem.setBrush(self.lightBrush)
            self.addItem(self.boxItem)
        elif self.boxLineStampState == 2:  # finish the connecting line
            if ghost_rect is None:
                ghost_rect = QRectF(
                    self.currentPos.x() - 16, self.currentPos.y() - 8, 16, 16
                )
            connectingPath = self.whichLineToDraw(
                ghost_rect,
                self.boxItem.mapRectToScene(self.boxItem.boundingRect()),
            )
            command = CommandPen(self, connectingPath)
            self.undoStack.push(command)
            self.removeItem(self.pathItem)
            self.boxLineStampState = 3  # get ready to stamp things.
        else:
            # this shouldn't happen, so (??->4)
            self.boxLineStampState = 4
        return

    def boxStampMove(self, event, ghost_rect=None):
        # flag can be in 4 states
        # 0 = initial state - we aren't doing anything
        # 1 = box drawing started
        # 2 = box finished, path started
        # 3 = path finished, ready to stamp final object
        # 4 = error state - clean things up.
        if self.boxLineStampState == 0:  # not doing anything, just moving mouse (0->0)
            return
        elif self.boxLineStampState == 1:  # mid box draw - keep drawing it. (1->1)
            self.currentPos = event.scenePos()
            if self.boxItem is None:
                # 2024-05: not convinced this None case can happen
                log.error("EEK: the boxItem was unexpectedly None, working around...")
                self.boxItem = QGraphicsRectItem()
                self.boxItem.setPen(self.ink)
                self.boxItem.setBrush(self.lightBrush)
                self.addItem(self.boxItem)
            self.boxItem.setRect(QRectF(self.originPos, self.currentPos).normalized())
            return
        elif (
            self.boxLineStampState == 2
        ):  # mid draw of connecting path - keep drawing it
            # update the connecting path
            self.currentPos = event.scenePos()
            if ghost_rect is None:
                ghost_rect = QRectF(
                    self.currentPos.x() - 16, self.currentPos.y() - 8, 16, 16
                )
            self.pathItem.setPath(
                self.whichLineToDraw(
                    ghost_rect,
                    self.boxItem.mapRectToScene(self.boxItem.boundingRect()),
                )
            )
        else:  # in some other state - should not happen, so (?->4)
            self.boxLineStampState = 4
        return

    def boxStampRelease(self, event):
        # flag can be in 4 states
        # 0 = initial state - we aren't doing anything
        # 1 = box drawing started
        # 2 = box finished, path started
        # 3 = path finished, ready to stamp final object
        # 4 = error state - clean things up.
        if self.boxLineStampState == 0:  # not in the middle of anything so do nothing.
            return
        elif (
            self.boxLineStampState == 1
        ):  # are mid-box draw, so time to finish it and move onto path-drawing.
            # start a macro - fix for #1961
            self.undoStack.beginMacro("Click-Drag composite object")

            # remove the temporary drawn box
            self.removeItem(self.boxItem)
            # make sure box is large enough
            if (
                self.boxItem.rect().width() < minimum_box_side_length
                or self.boxItem.rect().height() < minimum_box_side_length
            ):
                # is small box, so ignore it and draw no connecting path, just stamp final object
                self.boxLineStampState = 3
                return
            else:
                # push the drawn box onto undo stack
                command = CommandBox(self, self.boxItem.rect())
                self.undoStack.push(command)
                # now start drawing connecting path
                self.boxLineStampState = 2
                self.originPos = event.scenePos()
                self.currentPos = self.originPos
                self.pathItem = QGraphicsPathItem(QPainterPath(self.originPos))
                self.pathItem.setPen(self.ink)
                self.addItem(self.pathItem)
        else:  # we should not be here, so (?->4)
            self.boxLineStampState = 4

    def whichLineToDraw_init(self):
        witches = [
            which_horizontal_step,
            which_sticky_corners,
            which_classic_shortest_corner_side,
            which_centre_to_centre,
        ]
        self._witches = cycle(witches)
        self._whichLineToDraw = next(self._witches)

    def whichLineToDraw_next(self):
        self._whichLineToDraw = next(self._witches)
        print(f"Changing rubric-line to: {self._whichLineToDraw}")
        # TODO: can we generate a fake mouseMove event to force redraw?

    def whichLineToDraw(self, A, B):
        if A.intersects(B):
            # if boxes intersect then return a trivial path
            path = QPainterPath(A.topRight())
            path.lineTo(A.topRight())
            return path
        else:
            return self._whichLineToDraw(A, B)

    def stampCrossQMarkTick(self, event, cross=True):
        pt = event.scenePos()  # Grab the click's location and create command.
        if (event.button() == Qt.MouseButton.RightButton) or (
            QGuiApplication.queryKeyboardModifiers()
            == Qt.KeyboardModifier.ShiftModifier
        ):
            if cross:
                command = CommandTick(self, pt)
            else:
                command = CommandCross(self, pt)
        elif (event.button() == Qt.MouseButton.MiddleButton) or (
            QGuiApplication.queryKeyboardModifiers()
            == Qt.KeyboardModifier.ControlModifier
        ):
            command = CommandQMark(self, pt)
        else:
            if cross:
                command = CommandCross(self, pt)
            else:
                command = CommandTick(self, pt)
        self.undoStack.push(command)  # push onto the stack.

    def mousePressCross(self, event):
        """Selects the proper cross/?-mark/tick based on which mouse button/key combination.

        Notes:
            tick = right-click or shift+click.
            question mark = middle-click or control+click.
            cross = left-click or any combination other than the above.

        Args:
            event (QMouseEvent): the mouse press.

        Returns:
            None.
        """
        # use the boxStampPress function to update things
        self.boxStampPress(event)
        # only have to do something if in states 3 or 4
        if self.boxLineStampState == 3:  # means we are ready to stamp!
            self.stampCrossQMarkTick(event, cross=True)
        if self.boxLineStampState >= 3:  # stamp is done
            log.debug(
                f"flag = {self.boxLineStampState} so we must be finishing a click-drag cross: finalizing macro"
            )
            self.undoStack.endMacro()
            self.boxLineStampState = 0

    def mousePressTick(self, event):
        # use the boxStampPress function to update things
        self.boxStampPress(event)
        # only have to do something if in states 3 or 4
        if self.boxLineStampState == 3:  # means we are ready to stamp!
            self.stampCrossQMarkTick(event, cross=False)
        if self.boxLineStampState >= 3:  # stamp is done
            log.debug(
                f"flag = {self.boxLineStampState} so we must be finishing a click-drag tick: finalizing macro"
            )
            self.undoStack.endMacro()
            self.boxLineStampState = 0

    def mouseMoveCross(self, event):
        self.boxStampMove(event)
        if self.boxLineStampState >= 4:  # error has occurred
            log.debug(
                f"flag = {self.boxLineStampState} some sort of boxStamp error has occurred, so finish the macro"
            )
            self.boxLineStampState = 0
            self.undoStack.endMacro()

    def mouseMoveTick(self, event):
        self.boxStampMove(event)
        if self.boxLineStampState >= 4:  # error has occurred
            log.debug(
                f"flag = {self.boxLineStampState} some sort of boxStamp error has occurred, so finish the macro"
            )
            self.boxLineStampState = 0
            self.undoStack.endMacro()

    def mouseReleaseCross(self, event):
        # update things
        self.boxStampRelease(event)
        # only have to do something if in states 3 or 4
        if self.boxLineStampState == 3:  # means we are ready to stamp!
            self.stampCrossQMarkTick(event, cross=True)
        if self.boxLineStampState >= 3:  # stamp is done
            log.debug(
                f"flag = {self.boxLineStampState} so we must be finishing a click-drag cross: finalizing macro"
            )
            self.undoStack.endMacro()
            self.boxLineStampState = 0

    def mouseReleaseTick(self, event):
        # update things
        self.boxStampRelease(event)
        # only have to do something if in states 3 or 4
        if self.boxLineStampState == 3:  # means we are ready to stamp!
            self.stampCrossQMarkTick(event, cross=False)
        if self.boxLineStampState >= 3:  # stamp is done
            log.debug(
                f"flag = {self.boxLineStampState} so we must be finishing a click-drag cross: finalizing macro"
            )
            self.undoStack.endMacro()
            self.boxLineStampState = 0

    def mousePressRubric(self, event):
        """Mouse press while holding rubric tool.

        Usually this creates a rubric, an object consisting of a delta
        grade and an associated text item. If user drags then it
        instead starts the multi-stage creation of a box-line-rubric.
        If a box-line-rubric is in-progress, it continues to the next
        stage.

        Args:
            event (QMouseEvent): the given mouse click.

        Returns:
            None
        """
        # if delta not legal, then don't start
        if not self.isLegalRubric(self.current_rubric):
            return

        # check if anything underneath when trying to start/finish
        if self.boxLineStampState in [0, 2] and self.textUnderneathGhost():
            return

        # update state flag appropriately - but be careful of rubric-drag event
        if isinstance(event, QGraphicsSceneDragDropEvent):
            self.boxLineStampState = 3  # we just stamp things
        else:
            # pass in the bounding rect of the ghost text so can draw connecting path correctly
            self.boxStampPress(
                event,
                ghost_rect=self.ghostItem.mapRectToScene(self.ghostItem.boundingRect()),
            )

        if self.boxLineStampState == 3:  # time to stamp the rubric!
            pt = event.scenePos()  # grab the location of the mouse-click
            command = CommandRubric(self, pt, self.current_rubric)
            log.debug(
                "Making a Rubric: boxLineStampState is {}".format(
                    self.boxLineStampState
                )
            )
            self.undoStack.push(command)  # push the delta onto the undo stack.
            self.refreshStateAndScore()  # and now refresh the markingstate and score

        if self.boxLineStampState >= 3:
            log.debug(
                "boxLineStampState > 0 so we must be finishing a click-drag rubric: finalizing macro"
            )
            self.boxLineStampState = 0
            self.undoStack.endMacro()

    def mousePressMove(self, event):
        """Create closed hand cursor when move-tool is selected, otherwise does nothing.

        Notes:
            The actual moving of objects is handled by themselves since they
            know how to handle the ItemPositionChange signal as a move-command.

        Args:
            event (QMouseEvent): the mouse press.

        Returns:
            None
        """
        self.views()[0].setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)

    def mousePressPan(self, event):
        """While pan-tool selected changes the cursor to a closed hand, otherwise does not do much.

        Notes:
            Do not pass on event to superclass since we want to avoid
            selecting an object and moving that (fixes #834)

        Args:
            event (QMouseEvent): the mouse press.

        Returns:
            None
        """
        self.views()[0].setCursor(Qt.CursorShape.ClosedHandCursor)
        return

    def mousePressText(self, event):
        """Mouse press while holding text tool.

        Usually this creates a textobject, but if user drags then, it
        instead starts the multi-stage creation of a box-line-rubric.
        If a box-line-rubric is in-progress, it continues to the next
        stage.

        Args:
            event (QMouseEvent): the given mouse click.

        Returns:
            None
        """
        # Find the object under the click.
        # since there might be a line right under the point during stage2, offset the test point by a couple of pixels to the right.
        # note - chose to the right since when we start typing text it will extend rightwards
        # from the current point.
        under = self.itemAt(event.scenePos() + QPointF(2, 0), QTransform())
        # If something is there... (fixes bug reported by MattC)
        if under is not None:
            # If it is part of a group then do nothing
            if isinstance(under.group(), RubricItem):
                return
            # If it is a textitem then fire up the editor.
            if isinstance(under, TextItem):
                if (
                    self.boxLineStampState == 2
                ):  # make sure not trying to start text on top of text
                    return
                under.setTextInteractionFlags(
                    Qt.TextInteractionFlag.TextEditorInteraction
                )
                self.setFocusItem(under, Qt.FocusReason.MouseFocusReason)
                super().mousePressEvent(event)
                return
            # check if a textitem currently has focus and clear it.
            under = self.focusItem()
            if isinstance(under, TextItem):
                under.clearFocus()

        # now use the boxstamp code to update things
        self.boxStampPress(event)

        if self.boxLineStampState == 3:
            # Construct empty text object, give focus to start editor
            ept = event.scenePos()
            command = CommandText(self, ept, "")
            # move so centred under cursor   TODO: move into class!
            pt = ept - QPointF(0, command.blurb.boundingRect().height() / 2)
            command.blurb.setPos(pt)
            command.blurb.enable_interactive()
            command.blurb.setFocus()
            self.undoStack.push(command)

            log.debug(
                "boxLineStampState > 0 so we must be finishing a click-drag text: finalizing macro"
            )
            self.undoStack.endMacro()

    def mouseMoveText(self, event):
        """Handles mouse moving with a text.

        Args:
            event (QMouseEvent): the event of the mouse moving.

        Returns:
            None
        """
        self.boxStampMove(event)

    def mouseReleaseText(self, event):
        # if haven't started drawing, or are mid draw of line be careful of what is underneath
        # if there is text under the ghost then do not stamp anything - ignore the event.
        if self.textUnderneathPoint(event.scenePos()) and self.boxLineStampState in [
            0,
            2,
        ]:
            return

        self.boxStampRelease(event)

        if self.boxLineStampState == 3:
            # Construct empty text object, give focus to start editor
            pt = event.scenePos()
            command = CommandText(self, pt, "")
            # move so centred under cursor   TODO: move into class!
            pt -= QPointF(0, command.blurb.boundingRect().height() / 2)
            command.blurb.setPos(pt)
            command.blurb.enable_interactive()
            command.blurb.setFocus()
            self.undoStack.push(command)

        if self.boxLineStampState >= 3:  # stamp is done
            log.debug(
                f"flag = {self.boxLineStampState} so we must be finishing a click-drag text: Finalizing macro"
            )
            self.undoStack.endMacro()
            self.boxLineStampState = 0

    def mouseReleaseMove(self, event):
        """Handles mouse releases for move tool by setting cursor to an open hand.

        Args:
            event (QMouseEvent): given mouse release.

        Returns:
            None.
        """
        self.views()[0].setCursor(Qt.CursorShape.OpenHandCursor)
        super().mouseReleaseEvent(event)
        # refresh view after moving objects
        # EXPERIMENTAL: recompute bounding box in case you move an item outside the pages
        # self.updateSceneRectangle()
        # self.update()

    def mouseReleasePan(self, event):
        """Handles mouse releases for pan tool by setting cursor to an open hand.

        Args:
            event (QMouseEvent): given mouse release.

        Returns:
            None.
        """
        self.views()[0].setCursor(Qt.CursorShape.OpenHandCursor)
        super().mouseReleaseEvent(event)
        self.views()[0].setZoomSelector()

    def mousePressImage(self, event):
        """Adds the selected image at the location the mouse is pressed and shows a message box with instructions.

        Args:
            event (QMouseEvent): given mouse click.

        Returns:
            None
        """
        if self.tempImagePath is not None:
            imageFilePath = self.tempImagePath
            command = CommandImage(self, event.scenePos(), QImage(imageFilePath))
            self.undoStack.push(command)
            self.tempImagePath = None
            # set the mode back to move
            self.parent().toMoveMode()

            msg = QMessageBox(self.parent())
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Image Information")
            msg.setText(
                "You can double-click on an Image to modify its scale and border."
            )
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    def dragEnterEvent(self, e):
        """Handles drag/drop events."""
        if e.mimeData().hasFormat("text/plain"):
            # User has dragged in plain text from somewhere
            e.acceptProposedAction()
        elif e.mimeData().hasFormat(
            "application/x-qabstractitemmodeldatalist"
        ) or e.mimeData().hasFormat("application/x-qstandarditemmodeldatalist"):
            # User has dragged in a rubric from the rubric-list.
            e.setDropAction(Qt.DropAction.CopyAction)
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        """Handles drag and move events."""
        e.acceptProposedAction()

    def dropEvent(self, e):
        """Handles drop events."""
        # all drop events should copy
        # - even if user is trying to remove rubric from rubric-list make sure is copy-action.
        e.setDropAction(Qt.DropAction.CopyAction)

        if e.mimeData().hasFormat("text/plain"):
            # Simulate a rubric click.
            # TODO: cannot simulate a rubric, we have no ID: Issue #2417
            txt = e.mimeData().text()
            # self.rubricText = txt
            # self.rubricDelta = "0"
            # self.rubricKind = "neutral"
            # self.mousePressRubric(e)
            log.error(
                f"Issue #2417: Drag-drop gave plain text but no way to add: {txt}"
            )
        elif e.mimeData().hasFormat(
            "application/x-qabstractitemmodeldatalist"
        ) or e.mimeData().hasFormat("application/x-qstandarditemmodeldatalist"):
            # Simulate a rubric click.
            self.mousePressRubric(e)
            # User has dragged in a rubric from the rubric-list.
            pass
        else:
            pass
        # After the drop event make sure pageview has the focus.
        self.views()[0].setFocus(Qt.FocusReason.TabFocusReason)

    def latexAFragment(self, *args, **kwargs):
        """Latex a fragment of text."""
        return self.parent().latexAFragment(*args, **kwargs)

    def event(self, event):
        """A fix for misread touchpad events on macOS.

        Args:
            event (QEvent): A mouse event.

        Returns:
            (bool) True if the event is accepted, False otherwise.
        """
        if event.type() in [
            QEvent.Type.TouchBegin,
            QEvent.Type.TouchEnd,
            QEvent.Type.TouchUpdate,
            QEvent.Type.TouchCancel,
        ]:
            # ignore the event
            event.accept()
            return True
        else:
            return super().event(event)

    def _debug_printUndoStack(self):
        """A helper method for debugging the undoStack."""
        c = self.undoStack.count()
        for k in range(c):
            print(k, self.undoStack.text(k))

    def is_user_placed(self, item) -> bool:
        """Tell me if the user placed it or if its some autogen junk.

        Let's try to isolate this unpleasantness in one place.

        Returns:
            True if this is a user-generated object, False if not.
        """
        from plom.client.tools import (
            CrossItem,
            DeltaItem,
            ImageItem,
            TextItem,
            TickItem,
        )
        from plom.client.tools.ellipse import EllipseItem
        from plom.client.tools.highlight import HighlightItem
        from plom.client.tools.line import LineItem
        from plom.client.tools.arrow import ArrowItem, ArrowDoubleItem
        from plom.client.tools.pen import PenItem
        from plom.client.tools.penArrow import PenArrowItem
        from plom.client.tools.questionMark import QMarkItem

        if getattr(item, "saveable", None):
            return True
        if item in (
            CrossItem,
            DeltaItem,
            ImageItem,
            TextItem,
            TickItem,
            EllipseItem,
            HighlightItem,
            LineItem,
            ArrowItem,
            ArrowDoubleItem,
            PenItem,
            PenArrowItem,
            QMarkItem,
        ):
            return True
        # TODO more special cases?  I notice a naked QGraphicsLineItem used in elastic box...
        return False

    def find_items_right_of(self, x):
        keep = []
        log.debug(f"Searching for user-placed objects to the right of x={x}")
        for item in self.items():
            if not self.is_user_placed(item):
                log.debug(f"  nonuser: {item}")
                continue
            br = item.mapRectToScene(item.boundingRect())
            myx = br.left()
            if myx > x:
                log.debug(f"  found:   {item}: has x={myx} > {x}")
                keep.append(item)
            else:
                log.debug(f"  discard: {item}: has x={myx} <= {x}")
        return keep

    def move_some_items(self, I, dx, dy):
        """Translate some of the objects in the scene.

        Args:
            I (list): which objects to move.  TODO: not quite sure yet
                what is admissible here but we will try to filter out
                non-user-created stuff.
            dx (float): translation delta in the horizontal direction.
            dy (float): translation delta in the vertical direction.

        Wraps the movement of all objects in a compound undo item.
        """
        from plom.client.tools import CommandMoveItem

        log.debug(f"Shifting {len(I)} objects by ({dx}, {dy})")
        self.undoStack.beginMacro("Speak at once while taking turns")
        for item in I:
            if not self.is_user_placed(item):
                continue
            log.debug(f"got user-placed item {item}, shifting by ({dx}, {dy})")
            command = CommandMoveItem(item, QPointF(dx, dy))
            self.undoStack.push(command)
        self.undoStack.endMacro()

    def pickleSceneItems(self):
        """Pickles the saveable annotation items in the scene.

        Returns:
            (list[str]): a list containing all pickled elements.
        """
        lst = []
        for X in self.items():
            # check if object has "saveable" attribute and it is set to true.
            if getattr(X, "saveable", False):
                lst.append(X.pickle())
        return lst

    def unpickleSceneItems(self, lst):
        """Unpickles all items from the scene.

        Args:
            lst (list[list[str]]): a list containing lists of scene items'
                pickled information.

        Notes:
            Each pickled item type in lst is in a different format. Look in
            tools for more information.

        Returns:
            None, adds pickled items to the scene.

        Raises:
            ValueError: invalid pickle data.
        """
        # do this as a single undo macro.
        self.undoStack.beginMacro("Unpickling scene items")

        # clear all items from scene.
        for X in self.items():
            # X is a saveable object then it is user-created.
            # Hence it can be deleted, otherwise leave it.
            if getattr(X, "saveable", False):
                command = CommandDelete(self, X)
                self.undoStack.push(command)
        # now load up the new items
        for X in lst:
            # Special hack for legacy server data:
            if X[0] == "GroupDeltaText":
                log.info("Rewrote legacy GroupDeltaText %s as a Rubric", X[3])
                X[0] = "Rubric"
            CmdCls = globals().get("Command{}".format(X[0]), None)
            if CmdCls and getattr(CmdCls, "from_pickle", None):
                # TODO: use try-except here?
                self.undoStack.push(CmdCls.from_pickle(X, scene=self))
                continue
            log.error("Could not unpickle whatever this is:\n  {}".format(X))
            raise ValueError("Could not unpickle whatever this is:\n  {}".format(X))
        # now make sure focus is cleared from every item
        for X in self.items():
            X.clearFocus()
        # finish the macro
        self.undoStack.endMacro()

    def mousePressBox(self, event):
        """Handle mouse presses when box tool is selected.

        Notes:
            Creates a temp box which is updated as the mouse moves
            and replaced with a boxitem when the drawing is finished.
            If left-click then a highlight box will be drawn at finish,
            else if right-click or click+shift, an ellipse is drawn.

        Args:
            event (QMouseEvent): the mouse press event.

        Returns:
            None
        """
        if self.boxFlag != 0:
            # in middle of drawing a box, so ignore the new press
            return

        self.originPos = event.scenePos()
        self.currentPos = self.originPos
        # If left-click then a highlight box, else an ellipse.
        # Set a flag to tell the mouseReleaseBox function which.
        if (event.button() == Qt.MouseButton.RightButton) or (
            QGuiApplication.queryKeyboardModifiers()
            == Qt.KeyboardModifier.ShiftModifier
        ):
            self.boxFlag = 2
            self.ellipseItem = QGraphicsEllipseItem(
                QRectF(self.originPos.x(), self.originPos.y(), 0, 0)
            )
            self.ellipseItem.setPen(self.ink)
            self.ellipseItem.setBrush(self.lightBrush)
            self.addItem(self.ellipseItem)
        else:
            self.boxFlag = 1
            # Create a temp box item for animating the drawing as the
            # user moves the mouse.
            # Do not push command onto undoStack until drawing finished.
            self.boxItem = QGraphicsRectItem(
                QRectF(self.originPos, self.currentPos).normalized()
            )
            self.boxItem.setPen(self.ink)
            self.boxItem.setBrush(self.lightBrush)
            self.addItem(self.boxItem)

    def mouseMoveBox(self, event):
        """Update the size of the box as the mouse is moved.

        Notes:
            This animates the drawing of the box for the user.

        Args:
            event (QMouseEvent): the event of the mouse moving.

        Returns:
            None
        """
        self.currentPos = event.scenePos()
        if self.boxFlag == 2:
            if self.ellipseItem is None:
                self.ellipseItem = QGraphicsEllipseItem(
                    QRectF(self.originPos.x(), self.originPos.y(), 0, 0)
                )
            else:
                rx = abs(self.originPos.x() - self.currentPos.x())
                ry = abs(self.originPos.y() - self.currentPos.y())
                self.ellipseItem.setRect(
                    QRectF(
                        self.originPos.x() - rx, self.originPos.y() - ry, 2 * rx, 2 * ry
                    )
                )
        elif self.boxFlag == 1:
            if self.boxItem is None:
                # 2024-05: not convinced this None case can happen
                log.error("EEK: the boxItem was unexpectedly None, working around...")
                self.boxItem = QGraphicsRectItem()
                self.boxItem.setPen(self.ink)
                self.boxItem.setBrush(self.lightBrush)
                self.addItem(self.boxItem)
            self.boxItem.setRect(QRectF(self.originPos, self.currentPos).normalized())
        else:
            return

    def mouseReleaseBox(self, event):
        """Handle when the mouse is released after drawing a new box.

        Notes:
            Remove the temp boxitem (which was needed for animation)
            and create a command for either a highlighted box or opaque box
            depending on whether or not the boxflag was set.
            Push the resulting command onto the undo stack.

        Args:
            event (QMouseEvent): the given mouse release.

        Returns:
            None
        """
        if self.boxFlag == 0:
            return
        elif self.boxFlag == 1:
            self.removeItem(self.boxItem)
            # normalise the rectangle to have positive width/height
            nrect = self.boxItem.rect().normalized()
            # check if rect has some area - avoid tiny boxes
            if (
                nrect.width() > minimum_box_side_length
                and nrect.height() > minimum_box_side_length
            ):
                command = CommandBox(self, nrect)
                self.undoStack.push(command)
        else:
            self.removeItem(self.ellipseItem)
            # check if ellipse has some area (don't allow long/thin)
            if (
                self.ellipseItem.rect().width() > minimum_box_side_length
                and self.ellipseItem.rect().height() > minimum_box_side_length
            ):
                command = CommandEllipse(self, self.ellipseItem.rect())
                self.undoStack.push(command)

        self.boxFlag = 0

    def mousePressLine(self, event):
        """Handle the mouse press when using the line tool to draw a line.

        Notes:
            Creates a temp line which is updated as the mouse moves
            and replaced with a line or arrow when the drawing is finished.
            Single arrowhead = right click or click+shift
            Double arrowhead = middle click or click+control
            No Arrows = left click or any other combination.

        Args:
            event (QMouseEvent): the given mouse press.

        Returns:
            None
        """
        # Set arrow flag to tell mouseReleaseLine to draw line or arrow
        if self.arrowFlag != 0:
            # mid line draw so ignore press
            return
        if (event.button() == Qt.MouseButton.RightButton) or (
            QGuiApplication.queryKeyboardModifiers()
            == Qt.KeyboardModifier.ShiftModifier
        ):
            self.arrowFlag = 2
        elif (event.button() == Qt.MouseButton.MiddleButton) or (
            QGuiApplication.queryKeyboardModifiers()
            == Qt.KeyboardModifier.ControlModifier
        ):
            self.arrowFlag = 4
        else:
            self.arrowFlag = 1
        # Create a temp line which is updated as mouse moves.
        # Do not push command onto undoStack until drawing finished.
        self.originPos = event.scenePos()
        self.currentPos = self.originPos
        self.lineItem = QGraphicsLineItem(QLineF(self.originPos, self.currentPos))
        self.lineItem.setPen(self.ink)
        self.addItem(self.lineItem)

    def mouseMoveLine(self, event):
        """Update the length of the box as the mouse is moved.

        Notes:
            This animates the drawing of the line for the user.

        Args:
            event (QMouseEvent): the event of the mouse moving.

        Returns:
            None
        """
        if self.arrowFlag:
            self.currentPos = event.scenePos()
            self.lineItem.setLine(QLineF(self.originPos, self.currentPos))

    def mouseReleaseLine(self, event):
        """Handle when the mouse is released after drawing a new line.

        Notes:
            Remove the temp lineitem (which was needed for animation)
            and create a command for either a line, arrow or double arrow
            depending on whether or not the arrow flag was set.
            Push the resulting command onto the undo stack.

        Args:
            event (QMouseEvent): the given mouse release.

        Returns:
            None
        """
        if self.arrowFlag == 0:
            return
        elif self.arrowFlag == 1:
            command = CommandLine(self, self.originPos, self.currentPos)
        elif self.arrowFlag == 2:
            command = CommandArrow(self, self.originPos, self.currentPos)
        elif self.arrowFlag == 4:
            command = CommandArrowDouble(self, self.originPos, self.currentPos)
        else:
            raise RuntimeError(
                f"Tertium non datur: arrowFlag={self.arrowFlag} should not be possible"
            )
        self.arrowFlag = 0
        self.removeItem(self.lineItem)
        # don't add if too short
        if (self.originPos - self.currentPos).manhattanLength() > 24:
            self.undoStack.push(command)

    def mousePressPen(self, event):
        """Handle the mouse press when using the pen tool to draw.

        Notes:
            normal pen = left click.
            highlight pen = right click or click+shift.
            pen with double-arrowhead = middle click or click+control.

        Args:
            event (QMouseEvent): the associated mouse press.

        Returns:
            None
        """
        if self.penFlag != 0:
            # in middle of drawing a path, so ignore
            return

        self.originPos = event.scenePos()
        self.currentPos = self.originPos
        # create the path.
        self.path = QPainterPath()
        self.path.moveTo(self.originPos)
        self.path.lineTo(self.currentPos)
        self.pathItem = QGraphicsPathItem(self.path)
        # If left-click then setPen to the standard thin-red
        # Else set to the highlighter or pen with arrows.
        # set penFlag so correct object created on mouse-release
        # non-zero value so we don't add to path after mouse-release
        if (event.button() == Qt.MouseButton.RightButton) or (
            QGuiApplication.queryKeyboardModifiers()
            == Qt.KeyboardModifier.ShiftModifier
        ):
            self.pathItem.setPen(self.highlight)
            self.penFlag = 2
        elif (event.button() == Qt.MouseButton.MiddleButton) or (
            QGuiApplication.queryKeyboardModifiers()
            == Qt.KeyboardModifier.ControlModifier
        ):
            # middle button is pen-path with arrows at both ends
            self.pathItem.setPen(self.ink)
            self.penFlag = 4
        else:
            self.pathItem.setPen(self.ink)
            self.penFlag = 1
        # Note - command not pushed onto stack until path is finished on
        # mouse-release.
        self.addItem(self.pathItem)

    def mouseMovePen(self, event):
        """Update the pen-path as the mouse is moved.

        Notes:
            This animates the drawing for the user.

        Args:
            event (QMouseEvent): the event of the mouse moving.

        Returns:
            None
        """
        if self.penFlag:
            self.currentPos = event.scenePos()
            self.path.lineTo(self.currentPos)
            self.pathItem.setPath(self.path)
        # do not add to path when flag is zero.

    def mouseReleasePen(self, event):
        """Handle when the mouse is released after drawing.

        Notes:
            Remove the temp pen-path (which was needed for animation)
            and create a command for either the pen-path or highlight
            path depending on whether or not the highlight flag was set.
            Push the resulting command onto the undo stack

        Args:
            event (QMouseEvent): the given mouse release.

        Returns:
            None
        """
        if self.penFlag == 0:
            return
        elif self.penFlag == 1:
            if self.path.length() <= 1:  # path is very short, so add a little blob.
                self.path.lineTo(event.scenePos() + QPointF(2, 0))
                self.path.lineTo(event.scenePos() + QPointF(2, 2))
                self.path.lineTo(event.scenePos() + QPointF(0, 2))
                self.path.lineTo(event.scenePos())
            command = CommandPen(self, self.path)
        elif self.penFlag == 2:
            if self.path.length() <= 1:  # path is very short, so add a blob.
                self.path.lineTo(event.scenePos() + QPointF(4, 0))
                self.path.lineTo(event.scenePos() + QPointF(4, 4))
                self.path.lineTo(event.scenePos() + QPointF(0, 4))
                self.path.lineTo(event.scenePos())
            command = CommandHighlight(self, self.path)
        elif self.penFlag == 4:
            command = CommandPenArrow(self, self.path)
        else:
            raise RuntimeError(
                f"Tertium non datur: penFlag={self.penFlag} should not be possible"
            )
        self.penFlag = 0
        self.removeItem(self.pathItem)
        self.undoStack.push(command)
        # don't add if too short - check by boundingRect
        # TODO: decide threshold for pen annotation size
        # if (
        #     self.pathItem.boundingRect().height() + self.pathItem.boundingRect().width()
        #     > 8
        # ):
        #     self.undoStack.push(command)

    def mousePressZoom(self, event):
        """Handle the mouse press when drawing a zoom box.

        Notes:
            If right-click (or shift) then zoom-out, else - don't do much
            until release.

        Args:
            event (QMouseEvent): given mouse press.

        Returns:
            None
        """
        if self.zoomFlag:
            return

        if (event.button() == Qt.MouseButton.RightButton) or (
            QGuiApplication.queryKeyboardModifiers()
            == Qt.KeyboardModifier.ShiftModifier
        ):
            # sets the view rectangle and updates zoom-dropdown.
            self.views()[0].scale(0.8, 0.8)
            self.views()[0].centerOn(event.scenePos())
            self.views()[0].setZoomSelector(True)
            self.zoomFlag = 0
            return
        else:
            self.zoomFlag = 1

        self.originPos = event.scenePos()
        self.currentPos = self.originPos
        self.zoomBoxItem = QGraphicsRectItem(
            QRectF(self.originPos, self.currentPos).normalized()
        )
        self.zoomBoxItem.setPen(QColor("blue"))
        self.zoomBoxItem.setBrush(self.zoomBrush)
        self.addItem(self.zoomBoxItem)

    def mouseMoveZoom(self, event):
        """Update the size of the zoom box as the mouse is moved.

        Notes:
            This animates the drawing of the box for the user.

        Args:
            event (QMouseEvent): the event of the mouse moving.

        Returns:
            None
        """
        if self.zoomFlag:
            self.zoomFlag = 2  # drag started.
            self.currentPos = event.scenePos()
            if self.zoomBoxItem is None:
                # somehow missed the mouse-press (2024: not convinced this can happen)
                log.error("EEK: the zoombox was unexpectedly None, working around...")
                self.zoomBoxItem = QGraphicsRectItem()
                self.zoomBoxItem.setPen(self.ink)
                self.zoomBoxItem.setBrush(self.zoomBrush)
                self.addItem(self.zoomBoxItem)
            self.zoomBoxItem.setRect(
                QRectF(self.originPos, self.currentPos).normalized()
            )

    def mouseReleaseZoom(self, event):
        """Handle when the mouse is released after drawing a new zoom box.

        Notes: Either zoom-in a little (if zoombox small), else fit the
            zoombox in view. Delete the zoombox afterwards and set the zoomflag
            back to 0.

        Args:
            event (QMouseEvent): the given mouse release.

        Returns:
            None
        """
        if self.zoomFlag == 0:
            return

        # check to see if box is quite small (since very hard
        # to click button without moving a little)
        # if small then set flag to 1 and treat like a click
        # TODO: These thresholds are in physical units ("page pixels"?) so are effected by zoom
        # TODO: it would be much better to express them in (screen) pixels b/c they are a UI threshold
        if self.zoomBoxItem.rect().height() < 8 and self.zoomBoxItem.rect().width() < 8:
            self.zoomFlag = 1

        if self.zoomFlag == 1:
            self.views()[0].scale(1.25, 1.25)
            self.views()[0].centerOn(event.scenePos())

        elif self.zoomFlag == 2:
            self.views()[0].fitInView(
                self.zoomBoxItem, Qt.AspectRatioMode.KeepAspectRatio
            )

        # sets the view rectangle and updates zoom-dropdown.
        self.views()[0].setZoomSelector(True)
        # remove the box and put flag back.
        self.removeItem(self.zoomBoxItem)
        self.zoomFlag = 0

    def mousePressDelete(self, event):
        """Handle the mouse press when drawing a delete box.

        Notes:
            Nothing happens until button is released.

        Args:
            event (QMouseEvent): given mouse press.

        Returns:
            None
        """
        if self.deleteFlag:
            return

        self.deleteFlag = 1
        self.originPos = event.scenePos()
        self.currentPos = self.originPos
        self.delBoxItem = QGraphicsRectItem(
            QRectF(self.originPos, self.currentPos).normalized()
        )
        self.delBoxItem.setPen(QPen(QColor("red"), self.style["pen_width"]))
        self.delBoxItem.setBrush(self.deleteBrush)
        self.addItem(self.delBoxItem)

    def mouseMoveDelete(self, event):
        """Update the size of the delete box as the mouse is moved.

        Notes:
            This animates the drawing of the box for the user.

        Args:
            event (QMouseEvent): the event of the mouse moving.

        Returns:
            None
        """
        if self.deleteFlag:
            self.deleteFlag = 2  # drag started.
            self.currentPos = event.scenePos()
            if self.delBoxItem is None:
                # somehow missed the mouse-press (2024: not convinced this can happen)
                log.error("EEK: the delbox was unexpectedly None, working around...")
                self.delBoxItem = QGraphicsRectItem()
                self.delBoxItem.setPen(QPen(QColor("red"), self.style["pen_width"]))
                self.delBoxItem.setBrush(self.deleteBrush)
                self.addItem(self.delBoxItem)
            self.delBoxItem.setRect(
                QRectF(self.originPos, self.currentPos).normalized()
            )

    def deleteIfLegal(self, item):
        """Deletes the annotation item if that is a legal action.

        Notes:
            Can't delete the pageimage, scorebox, delete-box, ghostitem and
            its constituents, probably other things too.  You can delete
            annotations: those all have a "saveable" attribute.

        Args:
            item (QGraphicsItem): the item to possibly be deleted.

        Returns:
            None
        """
        if getattr(item, "saveable", False):  # we can only delete "saveable" items
            command = CommandDelete(self, item)
            self.undoStack.push(command)

    def mouseReleaseRubric(self, event):
        # if haven't started drawing, or are mid draw of line be careful of what is underneath
        # if there is text under the ghost then do not stamp anything - ignore the event.
        if self.textUnderneathGhost() and self.boxLineStampState in [0, 2]:
            return

        # update things
        self.boxStampRelease(event)
        # only have to do something if in states 3 or 4
        if self.boxLineStampState == 3:  # means is small box and we are ready to stamp!
            # if text under ghost then ignore this event
            if self.textUnderneathGhost():  # text under here - not safe to stamp
                self.undoStack.endMacro()
                self.undoStack.undo()
                self.boxLineStampState = 0
                return
            # small box, so just stamp the rubric
            command = CommandRubric(self, event.scenePos(), self.current_rubric)
            log.debug(
                "Making a Rubric: boxLineStampState is {}".format(
                    self.boxLineStampState
                )
            )
            # push the delta onto the undo stack.
            self.undoStack.push(command)
            self.refreshStateAndScore()  # and now refresh the markingstate and score

        if self.boxLineStampState >= 3:  # stamp is done
            # TODO: how to get here?  In testing 2022-03-01, Colin could not make this code run
            log.debug(
                f"flag = {self.boxLineStampState} so we must be finishing a click-drag rubric: finalizing macro"
            )
            self.undoStack.endMacro()
            self.boxLineStampState = 0

    def mouseReleaseDelete(self, event):
        """Handle when the mouse is released after drawing a new delete box.

        Notes:
             Remove the temp boxitem (which was needed for animation)
            and then delete all objects that lie within the box.
            Push the resulting commands onto the undo stack

        Args:
            event (QMouseEvent): the given mouse release.

        Returns:
            None
        """
        if self.deleteFlag == 0:
            return
        # check to see if box is quite small (since very hard
        # to click button without moving a little)
        # if small then set flag to 1 and treat like a click
        if self.delBoxItem.rect().height() < 8 and self.delBoxItem.rect().width() < 8:
            self.deleteFlag = 1

        if self.deleteFlag == 1:
            self.originPos = event.scenePos()
            # grab list of items in rectangle around click
            nearby = self.items(
                QRectF(self.originPos.x() - 5, self.originPos.y() - 5, 8, 8),
                mode=Qt.ItemSelectionMode.IntersectsItemShape,
                deviceTransform=QTransform(),
            )
            if len(nearby) == 0:
                return
            else:
                # delete the zeroth element of the list
                if nearby[0].group() is not None:  # object part of Rubric
                    self.deleteIfLegal(nearby[0].group())  # delete the group
                else:
                    self.deleteIfLegal(nearby[0])
        elif self.deleteFlag == 2:
            # check all items against the delete-box - this is a little clumsy, but works and there are not so many items typically.
            for X in self.items():
                # make sure is not background image or the scorebox, or the delbox itself.
                if X.collidesWithItem(
                    self.delBoxItem, mode=Qt.ItemSelectionMode.ContainsItemShape
                ):
                    if X.group() is None:
                        self.deleteIfLegal(X)
                    else:
                        pass  # is part of a group

        self.removeItem(self.delBoxItem)
        self.deleteFlag = 0  # put flag back.

    def hasAnyCrosses(self) -> bool:
        """Returns True if scene has any crosses, False otherwise."""
        for X in self.items():
            if isinstance(X, CrossItem):
                return True
        return False

    def hasOnlyCrosses(self) -> bool:
        """Returns True if scene has only crosses, False otherwise."""
        for X in self.items():
            if getattr(X, "saveable", None):
                if not isinstance(X, CrossItem):
                    return False
        return True

    def hasAnyComments(self) -> bool:
        """Returns True if scene has any rubrics or text items, False otherwise."""
        for X in self.items():
            if isinstance(X, (TextItem, RubricItem)):
                return True
        return False

    def hasAnyTicks(self) -> bool:
        """Returns True if scene has any ticks. False otherwise."""
        for X in self.items():
            if isinstance(X, TickItem):
                return True
        return False

    def hasOnlyTicks(self) -> bool:
        """Returns True if scene has only ticks, False otherwise."""
        for X in self.items():
            if getattr(X, "saveable", None):
                if not isinstance(X, TickItem):
                    return False
        return True

    def hasOnlyTicksCrossesDeltas(self) -> bool:
        """Checks if the image only has crosses, ticks or deltas.

        Returns:
            True if scene only has ticks/crosses/deltas, False otherwise.
        """
        for x in self.items():
            if getattr(x, "saveable", None):
                if isinstance(x, (TickItem, CrossItem)):
                    continue
                if isinstance(x, RubricItem):
                    # check if this is a delta-rubric
                    # TODO: see rubrics_list.py: rubric_is_naked_delta
                    if x.kind == "relative" and x.blurb.toPlainText() == ".":
                        continue
                return False  # otherwise
        return True  # only tick,cross or delta-rubrics

    def get_list_of_non_annotated_underimages(self) -> list[int]:
        """Which images in the scene are not yet annotated.

        Note these are indexed from zero.  Thinking of them as pages is
        potentially misleading: we are annotating a scene made of a list
        of images: which of those images are not yet annotated?
        """
        # TODO: Issue #3367: do nicer code without explicit N^2
        lst = []
        for n in range(len(self.underImage.images)):
            img = self.underImage.images[n]
            page_annotated = False
            for x in self.items():
                if self.is_user_placed(x) and x.collidesWithItem(img):
                    page_annotated = True
                    # no need to further check this img
                    break
            if not page_annotated:
                lst.append(n)
        return lst

    def itemWithinBounds(self, item) -> bool:
        """Check if given item is within the margins or not."""
        return item.collidesWithItem(
            self.underRect, mode=Qt.ItemSelectionMode.ContainsItemShape
        )

    def check_all_saveable_objects_inside(self) -> list:
        """Checks that all objects are within the boundary of the page.

        Returns:
            All annotation (saveable) objects that are outside
            of the boundaries of the margin box (annotable area).
            The list will be empty in the good case of no objects being
            outside.
        """
        out_objs = []
        for X in self.items():
            if getattr(X, "saveable", False):
                if not self.itemWithinBounds(X):
                    out_objs.append(X)
        return out_objs

    def _updateGhost(self, rubric: dict[str, Any]) -> None:
        """Updates the ghost object based on the delta and text.

        Args:
            rubric: we need its delta, its text and whether its legal.

        Returns:
            None
        """
        self.ghostItem.changeComment(
            rubric["display_delta"], rubric["text"], self.isLegalRubric(rubric)
        )

    def _exposeGhost(self) -> None:
        """Exposes the ghost object."""
        self.ghostItem.setVisible(True)

    def _hideGhost(self) -> None:
        """Hides the ghost object."""
        self.ghostItem.setVisible(False)

    def mouseMoveRubric(self, event):
        """Handles mouse moving with a rubric.

        Args:
            event (QMouseEvent): the event of the mouse moving.

        Returns:
            None
        """
        if not self.ghostItem.isVisible():
            self.ghostItem.setVisible(True)
        self.ghostItem.setPos(event.scenePos())

        # pass in the bounding rect of the ghost text so can draw connecting path correctly
        self.boxStampMove(
            event,
            ghost_rect=self.ghostItem.mapRectToScene(self.ghostItem.boundingRect()),
        )

    def setTheMark(self, newMark: int) -> None:
        """Sets the new mark/score for the paper.

        Args:
            newMark: the new mark/score for the paper.

        Returns:
            None
        """
        self.score = newMark
        self.scoreBox.changeScore(self.score)

    def undo(self):
        """Undoes a given action."""
        self.undoStack.undo()

    def redo(self):
        """Redoes a given action."""
        self.undoStack.redo()

    def isLegalRubric(self, rubric: dict[str, Any]) -> bool:
        """Is this rubric-type legal for the current scene, and does it move score below 0 or above maxMark?

        Args:
            rubric (dict): must have at least the keys "kind", "value",
                "display_delta", and "out_of".

        Returns:
            True if the delta is legal, False otherwise.
        """
        rubrics = self.get_rubrics()
        rubrics.append(rubric)

        try:
            compute_score(rubrics, self.maxMark)
        except ValueError:
            return False
        except PlomInconsistentRubric:
            return False
        return True

    def setCurrentRubric(self, rubric: dict[str, Any]) -> None:
        """Changes the new rubric for the paper based on the delta and text.

        This doesn't effect what is shown in the scene: its just a setter.
        To force an update, see ``setToolMode``, which you likely want to call
        after this method.

        Args:
            rubric (dict): must have at least the keys and values::
                - value (int):
                - out_of (int):
                - display_delta (str): a string displaying the value of the rubric.
                - text (str): the text in the rubric.
                - id (int): the id of the rubric.
                - kind (str): ``"absolute"``, ``"neutral"``, etc.

        Returns:
            None
        """
        self.current_rubric = rubric
        self._updateGhost(rubric)

    def stopMidDraw(self):
        # look at all the mid-draw flags and cancel accordingly.
        # the flags are arrowFlag, boxFlag, penFlag, boxLineStampState, zoomBox
        # note - only one should be non-zero at a given time
        log.debug("Flags = {}".format(self.__getFlags()))
        if self.arrowFlag > 0:  # midway through drawing a line
            self.arrowFlag = 0
            self.removeItem(self.lineItem)
        if self.penFlag > 0:  # midway through drawing a path
            self.penFlag = 0
            self.removeItem(self.pathItem)
        # box flag needs a little care since two possibilities mid-draw
        if self.boxFlag == 1:  # midway through drawing a box
            self.boxFlag = 0
            self.removeItem(self.boxItem)
        if self.boxFlag == 2:  # midway through drawing an ellipse
            self.boxFlag = 0
            self.removeItem(self.ellipseItem)
        # box-stamp flag needs care - uses undo-macro - need to clean that up
        # 1 = drawing the box
        # 2 = drawing the line
        # 3 = pasting the object - this should only be very briefly mid function.
        if self.boxLineStampState == 1:  # drawing the box
            self.removeItem(self.boxItem)
            self.boxLineStampState = 0
        if (
            self.boxLineStampState == 2
        ):  # undo-macro started, box drawn, mid draw of path
            self.removeItem(self.pathItem)
            self.undoStack.endMacro()
            self.undo()  # removes the drawn box
            self.boxLineStampState = 0
        if self.boxLineStampState == 3:
            # Should be very hard to reach here - end macro and undo
            self.undoStack.endMacro()
            self.undo()  # removes the drawn box

        # check if mid-zoom-box draw:
        if self.zoomFlag == 2:
            self.removeItem(self.zoomBoxItem)
            self.zoomFlag = 0

    def isDrawing(self):
        return any(flag > 0 for flag in self.__getFlags())

    def __getFlags(self):
        return [
            self.arrowFlag,
            self.boxFlag,
            self.penFlag,
            self.zoomFlag,
            self.boxLineStampState,
        ]

    # PAGE SCENE CROPPING STUFF
    def _crop_to_focus(self, crop_rect):
        # this is called by the actual command-redo.
        self.overMask.crop_to_focus(crop_rect)
        self.scoreBox.setPos(crop_rect.topLeft())
        self.avoidBox = self.scoreBox.boundingRect().adjusted(-16, -16, 64, 24)
        # set zoom to "fit-page"
        self.views()[0].zoomFitPage(update=True)

    def current_crop_rectangle_as_proportions(
        self,
    ) -> tuple[float, float, float, float]:
        """Return the crop rectangle as proportions of original image."""
        full_height = self.underImage.boundingRect().height()
        full_width = self.underImage.boundingRect().width()
        rect_in_pix = self.overMask.inner_rect

        rect_as_proportions = (
            rect_in_pix.x() / full_width,
            rect_in_pix.y() / full_height,
            rect_in_pix.width() / full_width,
            rect_in_pix.height() / full_height,
        )
        return rect_as_proportions

    def crop_from_plomfile(self, crop_dat):
        # crop dat = (x,y,w,h) as proportions of full image, so scale by underlying image width/height
        full_height = self.underImage.boundingRect().height()
        full_width = self.underImage.boundingRect().width()
        crop_rect = QRectF(
            crop_dat[0] * full_width,
            crop_dat[1] * full_height,
            crop_dat[2] * full_width,
            crop_dat[3] * full_height,
        )
        self.trigger_crop(crop_rect)

    def uncrop_underlying_images(self):
        self.trigger_crop(self.overMask.get_original_inner_rect())

    def trigger_crop(self, crop_rect):
        # make sure that the underlying crop-rectangle is normalised
        # also make sure that it is not larger than the original image - so use their intersection
        actual_crop = crop_rect.intersected(self.underImage.boundingRect()).normalized()
        # pass new crop rect, as well as current one (for undo)
        command = CommandCrop(self, actual_crop, self.overMask.inner_rect)
        self.undoStack.push(command)
        # now set mode to move.
        self.parent().toMoveMode()

    def mousePressCrop(self, event):
        """Handle the mouse press when drawing a crop box.

        Notes:
            Nothing happens until button is released.

        Args:
            event (QMouseEvent): given mouse press.

        Returns:
            None
        """
        if self.deleteFlag:
            return

        self.deleteFlag = 1
        self.originPos = event.scenePos()
        self.currentPos = self.originPos
        self.delBoxItem = QGraphicsRectItem(
            QRectF(self.originPos, self.currentPos).normalized()
        )
        self.delBoxItem.setPen(QPen(QColor("red"), self.style["pen_width"]))
        self.delBoxItem.setBrush(self.deleteBrush)
        self.addItem(self.delBoxItem)

    def mouseMoveCrop(self, event):
        """Update the size of the crop box as the mouse is moved.

        Notes:
            This animates the drawing of the box for the user.

        Args:
            event (QMouseEvent): the event of the mouse moving.

        Returns:
            None
        """
        if self.deleteFlag:
            self.deleteFlag = 2  # drag started.
            self.currentPos = event.scenePos()
            if self.delBoxItem is None:
                log.error("EEK: the delbox was unexpectedly None, working around...")
                # somehow missed the mouse-press (2024: not convinced this can happen)
                self.delBoxItem = QGraphicsRectItem()
                self.delBoxItem.setPen(QPen(QColor("red"), self.style["pen_width"]))
                self.delBoxItem.setBrush(self.deleteBrush)
                self.addItem(self.delBoxItem)
            self.delBoxItem.setRect(
                QRectF(self.originPos, self.currentPos).normalized()
            )

    def mouseReleaseCrop(self, event):
        """Handle when the mouse is released after drawing a new delete box.

        Notes:
            Remove the temp boxitem (which was needed for animation)
            and push the crop command onto the undo stack

        Args:
            event (QMouseEvent): the given mouse release.

        Returns:
            None
        """
        if self.deleteFlag == 0:
            return
        # check to see if box is quite small (since very hard
        # to click button without moving a little)

        # The box should have a minimum size related to the smaller dimension
        # of the collection of underlying images, but never smaller than 256
        minbox = max(256, 0.2 * self.underImage.min_dimension)

        # if small then set flag to 0 and return
        if (
            self.delBoxItem.rect().height() < minbox
            or self.delBoxItem.rect().width() < minbox
        ):
            self.removeItem(self.delBoxItem)
            self.deleteFlag = 0
        else:
            self.removeItem(self.delBoxItem)
            self.deleteFlag = 0  # put flag back.
            self.trigger_crop(self.delBoxItem.rect())
