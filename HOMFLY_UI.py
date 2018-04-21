from PySide import QtGui, QtCore
from Polynomials import *
from HOMFLYcalculator import *
import sys
from fractions import Fraction


class HOMFLYWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.calcFraction = Fraction(1, 2)
        self.prevConstructedFraction = Fraction(0, 1)
        self.isCanCalculate = True
        self.minP = -20
        self.maxP = 20
        self.maxQ = 20
        self.LoadImages()
        self.setupUI(self)

    def LoadImages(self):
        self.iReader = QtGui.QImageReader()
        self.iReader.setScaledSize(QtCore.QSize(70, 156))
        self.iReader.setFileName("images\\ap.png")
        self.imageAP = self.iReader.read()
        self.iReader.setFileName("images\\am.png")
        self.imageAM = self.iReader.read()
        self.iReader.setFileName("images\\bp.png")
        self.imageBP = self.iReader.read()
        self.iReader.setFileName("images\\bm.png")
        self.imageBM = self.iReader.read()
        self.iReader.setScaledSize(QtCore.QSize(40, 156))
        self.iReader.setFileName("images\\l1.png")
        self.imageL1 = self.iReader.read()
        self.iReader.setFileName("images\\r1.png")
        self.imageR1 = self.iReader.read()
        self.iReader.setScaledSize(QtCore.QSize(60, 156))
        self.iReader.setFileName("images\\r2.png")
        self.imageR2 = self.iReader.read()

    def BuildKnotPicture(self, fraction):
        if (not fraction == None) and ((not self.prevConstructedFraction.numerator == fraction.numerator) or (not self.prevConstructedFraction.denominator == fraction.denominator)):
            e = ExtFraction()
            e.SetFraction(fraction.numerator, fraction.denominator)
            self.prevConstructedFraction = Fraction(fraction)
            # self.answerLabel.clear()
            self.answerOutText.clear()

            for i in reversed(range(0, self.knotLayout.count())):
                w = self.knotLayout.itemAt(i)
                wid = w.widget()
                if not wid == None:
                    self.knotLayout.removeItem(w)
                    wid.setParent(None)
                else:
                    self.knotLayout.removeItem(w)

            sLabel = QtGui.QLabel()
            self.knotLayout.addWidget(sLabel)

            if e.IsCorrect():
                des = e.GetPartialDenominators()
                if len(des) > 0:
                    i = 0
                    # draw start
                    l = QtGui.QLabel()
                    l.setPixmap(QtGui.QPixmap(self.imageL1))
                    self.knotLayout.addWidget(l)
                    for d in des:
                        if i % 2 == 0:  # Draw A part
                            if d > 0:  # positive
                                for j in range(0, d):
                                    l = QtGui.QLabel()
                                    l.setPixmap(QtGui.QPixmap(self.imageAP))
                                    self.knotLayout.addWidget(l)
                            elif d < 0:  # negative
                                for j in range(0, abs(d)):
                                    l = QtGui.QLabel()
                                    l.setPixmap(QtGui.QPixmap(self.imageAM))
                                    self.knotLayout.addWidget(l)
                        else:  # Draw B part
                            if d > 0:  # positive
                                for j in range(0, d):
                                    l = QtGui.QLabel()
                                    l.setPixmap(QtGui.QPixmap(self.imageBP))
                                    self.knotLayout.addWidget(l)
                            elif d < 0:  # negative
                                for j in range(0, abs(d)):
                                    l = QtGui.QLabel()
                                    l.setPixmap(QtGui.QPixmap(self.imageBM))
                                    self.knotLayout.addWidget(l)
                        i = i + 1
                    # Draw end
                    if i % 2 == 0:
                        l = QtGui.QLabel()
                        l.setPixmap(QtGui.QPixmap(self.imageR2))
                        self.knotLayout.addWidget(l)
                    else:
                        l = QtGui.QLabel()
                        l.setPixmap(QtGui.QPixmap(self.imageR1))
                        self.knotLayout.addWidget(l)

            else:
                self.warnLabel = QtGui.QLabel()
                self.warnLabel.setStyleSheet("QLabel {padding: 20}")
                self.warnLabel.setText("I can not build the knot :(")
                self.knotLayout.addWidget(self.warnLabel)
            eLabel = QtGui.QLabel()
            self.knotLayout.addWidget(eLabel)
            self.knotLayout.setStretchFactor(sLabel, 1)
            self.knotLayout.setStretchFactor(eLabel, 1)

    def centerize(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2,
                  (screen.height()-size.height())/2 - 40)

    def setStyle(self):
        # self.answerLabel.setStyleSheet(
            # "QLabel {background-color: #404040; color: #fff; padding: 10}")
        self.answerShadow = QtGui.QGraphicsDropShadowEffect(self)
        self.answerShadow.setBlurRadius(8)
        self.answerShadow.setOffset(4, 4)
        self.answerShadow.setColor(QtGui.QColor(24, 24, 24, 128))
        # self.answerLabel.setGraphicsEffect(self.answerShadow)

        self.setStyleSheet("""QWidget#centralWidget {background-color: #272727}

                                QLabel {color: #CCC}

                                QSlider:groove {
                                    background: #202020;
                                }
                                QSlider:handle {
                                    background: #404040;
                                    width: 10px;
                                }


                                QComboBox QAbstractItemView {
                                    border: 0px solid #404040;
                                    selection-background-color: #303030;
                                    color: #CCC;
                                    background-color: #404040;
                                }


                                QComboBox {
                                    border: 0px solid gray;
                                    border-radius: 3px;
                                    padding: 3px 0px 3px 3px;
                                    min-width: 6em;
                                }

                                QComboBox:!editable, QComboBox::drop-down:editable {
                                    background: #404040;
                                    color: #CCC;
                                }

                                QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                                    background: #404040;
                                    color: #CCC;
                                }

                                QComboBox:on {
                                    padding-top: 3px;
                                    padding-left: 3px;
                                }

                                QComboBox::drop-down {
                                    border-left-width: 0px;
                                }

                                QPushButton { 
                                                background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
                                                    stop: 0 #222222,
                                                    stop: 1 #222222 );
                                                border: 3;
                                                border-radius: 6px;
                                                color: #CCC;}

                                QPushButton:hover { 
                                                    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
                                                    stop: 0 #222222,
                                                    stop: 1 #202020); }

                                QPushButton:pressed { 
                                                        background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
                                                    stop: 0 #202020,
                                                    stop: 1 #222222); }

                                QLineEdit { border: 2px solid #404040;
                                            border-radius: 5px;
                                            background: #404040;
                                            selection-background-color: darkgray;
                                            color: #CCC}

                                QMenuBar {
                                            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                                              stop:0 #404040, stop:1 #353535);}

                                QMenuBar::item {
                                    spacing: 3px;
                                    padding: 1px 4px;
                                    background: transparent;
                                    color: #CCC}

                                QMenuBar::item:selected {
                                    background: #353535;}

                                QMenuBar::item:pressed {
                                    background: #353535;}

                                QStatusBar {
                                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                                              stop:0 #404040, stop:1 #353535);
                                    color: #CCC;}
""")

    def Calculate(self):
        # self.answerLabel.clear()
        if abs(self.calcFraction.numerator) == abs(self.calcFraction.denominator):
            print(
                "I can not calculate polynomial for trivial knot. Try to understand, what are you doing.")
        else:
            if self.isCanCalculate:
                self.isCanCalculate = False
                calc = HOMFLYCalculator()
                res = calc.CalculateOnce(self.calcFraction)
                s = res.toString()
                self.answerOutText.setText(s)
                self.isCanCalculate = True

    def GetFractionFromSet(self, array):
        x = Fraction(0, 1)
        isSkip = False
        for i in reversed(range(0, len(array))):
            if not isSkip:
                s = Fraction(array[i], 1) + x
                if s.numerator == 0:
                    x = Fraction(0, 1)
                    isSkip = True
                else:
                    x = 1 / s
            else:
                isSkip = False

        return x

    def sliderMouseReleaseEvent(self, event):
        self.BuildKnotPicture(self.calcFraction)
        # self.Resize()

    def SetFractionValue(self, p, q):

        if q == 0:
            q = 1

        if abs(p) > q:
            if p < 0:
                p = -1 * q
            else:
                p = q

        f = Fraction(p, q)
        self.i2TextLabel.setAlignment(QtCore.Qt.AlignCenter)

        if f.numerator*f.denominator % 2 == 1 and not f.denominator == 1:
            if f.numerator > 0:
                self.calcFraction = Fraction(
                    f.numerator-f.denominator, f.denominator)
            else:
                self.calcFraction = Fraction(
                    f.numerator+f.denominator, f.denominator)
        else:
            self.calcFraction = Fraction(f.numerator, f.denominator)

        self.i2TextValue = "p/q = " + str(self.calcFraction)
        self.i2TextLabel.setText(self.i2TextValue)

    def OnChangeI2LineEdit(self, text):
        symbols = text.split(" ")
        sequence = []
        for s in symbols:
            if len(s) > 0:
                isNegative = False
                if s[0] == "-":
                    s2 = s[1:]
                    isNegative = True
                else:
                    s2 = s
                if s2.isdigit() and len(s2) > 0:
                    sequence.append(-1 * int(s2) if isNegative else int(s2))

        if len(sequence) > 0:
            f = self.GetFractionFromSet(sequence)
        else:
            f = Fraction(1, 1)
        self.SetFractionValue(f.numerator, f.denominator)
        self.BuildKnotPicture(self.calcFraction)
        # self.Resize()

    def ChangePSlider(self, v):
        self.i1PValue.setText(str(v))
        self.SetFractionValue(self.i1PSlider.value(), self.i1QSlider.value())

    def ChangeQSlider(self, v):
        self.i1QValue.setText(str(v))
        self.SetFractionValue(self.i1PSlider.value(), self.i1QSlider.value())

    def buildIMBox(self):
        # clear all widgets
        if not self.i1PLabel == None:
            self.imboxL.removeWidget(self.i1PLabel)
            self.i1PLabel.setParent(None)
        if not self.i1QLabel == None:
            self.imboxL.removeWidget(self.i1QLabel)
            self.i1QLabel.setParent(None)
        if not self.i2Label == None:
            self.imboxL.removeWidget(self.i2Label)
            self.i2Label.setParent(None)

        if not self.i1PSlider == None:
            self.imboxL.removeWidget(self.i1PSlider)
            self.i1PSlider.setParent(None)
        if not self.i1QSlider == None:
            self.imboxL.removeWidget(self.i1QSlider)
            self.i1QSlider.setParent(None)

        if not self.i1PValue == None:
            self.imboxL.removeWidget(self.i1PValue)
            self.i1PValue.setParent(None)
        if not self.i1QValue == None:
            self.imboxL.removeWidget(self.i1QValue)
            self.i1QValue.setParent(None)

        if not self.i2LineEdit == None:
            self.imboxL.removeWidget(self.i2LineEdit)
            self.i2LineEdit.setParent(None)
        if not self.i2TextLabel == None:
            self.imboxL.removeWidget(self.i2TextLabel)
            self.i2TextLabel.setParent(None)

        if self.IMComboBox.currentIndex() == 0:
            self.i1PLabel = QtGui.QLabel()
            self.i1PLabel.setText("p")
            self.i1PLabel.setFont(self.labelFont)
            self.i1PLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.i1QLabel = QtGui.QLabel()
            self.i1QLabel.setText("q")
            self.i1QLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.i1QLabel.setFont(self.labelFont)
            self.imboxL.addWidget(self.i1PLabel, 0, 0, 1, 1)
            self.imboxL.addWidget(self.i1QLabel, 1, 0, 1, 1)
            self.i1PSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
            self.i1PSlider.setMinimum(self.minP)
            self.i1PSlider.setMaximum(self.maxP)
            self.i1QSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
            self.i1QSlider.setMinimum(1)
            self.i1QSlider.setMaximum(self.maxQ)
            # self.i1PSlider.setFixedSize(300, 25)
            self.i1PSlider.setValue(1)
            self.i1QSlider.setValue(2)
            self.connect(self.i1PSlider, QtCore.SIGNAL(
                "valueChanged(int)"), self.ChangePSlider)
            self.connect(self.i1QSlider, QtCore.SIGNAL(
                "valueChanged(int)"), self.ChangeQSlider)
            self.i1PSlider.mouseReleaseEvent = self.sliderMouseReleaseEvent
            self.i1QSlider.mouseReleaseEvent = self.sliderMouseReleaseEvent

            self.imboxL.addWidget(self.i1PSlider, 0, 1, 1, 1)
            self.imboxL.addWidget(self.i1QSlider, 1, 1, 1, 1)
            self.i1PValue = QtGui.QLabel()
            self.i1PValue.setText("")
            self.i1PValue.setFont(self.labelFont)
            self.i1QValue = QtGui.QLabel()
            self.i1QValue.setText("")
            self.i1PValue.setFont(self.labelFont)
            self.imboxL.addWidget(self.i1PValue, 0, 2, 1, 1)
            self.imboxL.addWidget(self.i1QValue, 1, 2, 1, 1)

            self.i2TextLabel = QtGui.QLabel()
            self.i2TextLabel.setFont(self.labelFont)
            self.imboxL.addWidget(self.i2TextLabel, 0, 3, 2, 1)
            self.ChangePSlider(self.i1PSlider.value())
            self.ChangeQSlider(self.i1QSlider.value())

            self.imboxL.setRowMinimumHeight(0, 25)
            self.imboxL.setRowMinimumHeight(1, 25)

        elif self.IMComboBox.currentIndex() == 1:
            self.i2Label = QtGui.QLabel()
            self.i2Label.setText("D:")
            self.i2Label.setAlignment(QtCore.Qt.AlignCenter)
            self.i2Label.setFont(self.labelFont)
            self.imboxL.addWidget(self.i2Label, 0, 0, 2, 1)
            self.i2LineEdit = QtGui.QLineEdit()
            self.i2LineEdit.setFont(self.inputFont)
            self.imboxL.addWidget(self.i2LineEdit, 0, 1, 2, 1)
            self.i2LineEdit.textChanged[str].connect(self.OnChangeI2LineEdit)

            self.i2TextLabel = QtGui.QLabel()
            self.i2TextLabel.setFont(self.labelFont)
            self.imboxL.addWidget(self.i2TextLabel, 0, 3, 2, 1)
            self.OnChangeI2LineEdit("")
            self.i2TextLabel.setText(self.i2TextValue)
            self.imboxL.setRowMinimumHeight(0, 25)
        else:
            pass

        # self.answerLabel.clear()
        if self.IMComboBox.currentIndex() == 0:
            self.SetFractionValue(self.i1PSlider.value(),
                                  self.i1QSlider.value())
        else:
            self.calcFraction = Fraction(1, 1)
        self.BuildKnotPicture(self.calcFraction)

    def setupUI(self, MainWindow):
        self.setWindowTitle("HOMFLY polynomial calculator")
        self.setWindowIcon(QtGui.QIcon('images\\icon.png'))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.centralwidget.setObjectName("centralWidget")
        self.mainGrid = QtGui.QGridLayout(self.centralwidget)

        self.labelFont = QtGui.QFont()
        self.labelFont.setFamily("Tahoma")
        self.labelFont.setPointSize(10)
        self.labelFont.setWeight(0)
        self.labelFont.setItalic(False)
        self.labelFont.setBold(False)

        self.ccboxFont = QtGui.QFont()
        self.ccboxFont.setFamily("Tahoma")
        self.ccboxFont.setPointSize(14)
        self.ccboxFont.setWeight(0)
        self.ccboxFont.setItalic(False)
        self.ccboxFont.setBold(False)

        self.inputFont = QtGui.QFont()
        self.inputFont.setFamily("Tahoma")
        self.inputFont.setPointSize(15)
        self.inputFont.setWeight(50)
        self.inputFont.setItalic(False)
        self.inputFont.setBold(False)

        self.IMTitle = QtGui.QLabel()
        self.IMTitle.setText("Input method:")
        self.IMTitle.setFont(self.labelFont)
        self.mainGrid.addWidget(self.IMTitle, 0, 0, 1, 1)

        self.IMComboBox = QtGui.QComboBox()
        self.IMComboBox.addItem("Fraction p/q")
        self.IMComboBox.addItem("Array of denominators")
        self.IMComboBox.setFont(self.labelFont)
        self.IMComboBox.activated.connect(self.buildIMBox)
        self.mainGrid.addWidget(self.IMComboBox, 1, 0, 1, 1)
        self.mainGrid.setRowMinimumHeight(0, 10)
        self.mainGrid.setRowMinimumHeight(1, 25)

        self.imboxL = QtGui.QGridLayout()
        self.imboxL.setColumnMinimumWidth(1, 250)
        self.imboxL.setColumnMinimumWidth(0, 25)
        self.imboxL.setColumnMinimumWidth(2, 15)
        self.imboxL.setColumnMinimumWidth(3, 75)
        self.i1PLabel = None
        self.i1QLabel = None
        self.i1PSlider = None
        self.i1QSlider = None
        self.i1PValue = None
        self.i1QValue = None
        self.i2Label = None
        self.i2LineEdit = None
        self.i2TextLabel = None
        self.i2TextValue = ""
        self.warnLabel = None

        # self.answerLabel = QtGui.QLabel()
        self.answerOutText = QtGui.QLineEdit()

        self.knotLayout = QtGui.QHBoxLayout()
        self.knotLayout.setSpacing(0)
        self.mainGrid.addLayout(self.knotLayout, 4, 0, 1, 1)
        self.mainGrid.addLayout(self.imboxL, 2, 0, 1, 1)

        self.buildIMBox()

        self.calcButton = QtGui.QPushButton("Calculate HOMFLY")
        self.calcButton.setMinimumHeight(40)
        self.connect(self.calcButton, QtCore.SIGNAL(
            "clicked()"), self.Calculate)
        self.mainGrid.addWidget(self.calcButton, 3, 0, 1, 1)
        self.mainGrid.setRowMinimumHeight(3, 45)

        # self.answerLabel.setAlignment(QtCore.Qt.AlignCenter)
        # self.answerLabel.setMinimumHeight(50)
        # self.mainGrid.addWidget(self.answerLabel, 5, 0, 1, 1)
        # self.answerOutText.setMinimumHeight(50)
        font = self.answerOutText.font()
        font.setPointSize(18)
        self.answerOutText.setFont(font)
        self.answerOutText.setAlignment(QtCore.Qt.AlignCenter)
        self.mainGrid.addWidget(self.answerOutText, 5, 0, 1, 1)

        self.mainGrid.setRowStretch(4, 1)

        self.setLayout(self.mainGrid)
        MainWindow.setCentralWidget(self.centralwidget)
        self.centerize()
        self.setStyle()


def main():
    app = QtGui.QApplication(sys.argv)
    window = HOMFLYWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
