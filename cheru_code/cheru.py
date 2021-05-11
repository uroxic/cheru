#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""切噜语（ちぇる語, Language Cheru）转换

定义:
    W_cheru = '切' ^ `CHERU_SET`+
    切噜词均以'切'开头，可用字符集为`CHERU_SET`

    L_cheru = {W_cheru ∪ `\\W`}*
    切噜语由切噜词与标点符号连接而成
"""

import re
import sys
import ctypes
import cheruresource
from itertools import zip_longest
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

CHERU_SET = '切卟叮咧哔唎啪啰啵嘭噜噼巴拉蹦铃'
CHERU_DIC = {c: i for i, c in enumerate(CHERU_SET)}
ENCODING = 'gb18030'
rex_split = re.compile(r'\b', re.U)
rex_word = re.compile(r'^\w+$', re.U)
rex_cheru_word: re.Pattern = re.compile(rf'切[{CHERU_SET}]+', re.U)


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def word2cheru(w: str) -> str:
    c = ['切']
    for b in w.encode(ENCODING):
        c.append(CHERU_SET[b & 0xf])
        c.append(CHERU_SET[(b >> 4) & 0xf])
    return ''.join(c)


def cheru2word(c: str) -> str:
    if not c[0] == '切' or len(c) < 2:
        return c
    b = []
    for b1, b2 in grouper(c[1:], 2, '切'):
        x = CHERU_DIC.get(b2, 0)
        x = x << 4 | CHERU_DIC.get(b1, 0)
        b.append(x)
    return bytes(b).decode(ENCODING, 'replace')


def str2cheru(s: str) -> str:
    c = []
    for w in rex_split.split(s):
        if rex_word.search(w):
            w = word2cheru(w)
        c.append(w)
    return ''.join(c)


def cheru2str(c: str) -> str:
    return rex_cheru_word.sub(lambda w: cheru2word(w.group()), c)
    # s = []
    # for w in rex_split.split(c):
    #     if rex_word.search(w):
    #         w = cheru2word(w)
    #     s.append(w)
    # return ''.join(s)


def cherulize(ss):
    if (ss[:4] == '切噜一下'):
        s = ss[4:]
        return ('切噜～♪ ' + str2cheru(s))
    else:
        return ('切噜～♪ ' + str2cheru(ss))


def decherulize(ss):
    if (ss[:4] == '切噜～♪'):
        s = ss[4:]
        return ('你的切噜噜是：\n' + cheru2str(s))
    else:
        return ('切不动勒切噜噜...')


class MainUi(QMainWindow):

    def __init__(self):
        super().__init__()
        self.BtnList = {}
        self.TextEditList = {}
        self.initUI()  # 界面绘制交给InitUi方法

    def initUI(self):
        self.desktop = QApplication.desktop()
        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        self.dpi = ctypes.windll.gdi32.GetDeviceCaps(
            ctypes.windll.user32.GetDC(0), 88)
        self.ratio = self.dpi/96
        self.height = int(self.ratio*self.screenRect.width()*21/80+0.5)
        self.width = int(self.ratio*self.screenRect.width()*7/15+0.5)
        self.unit = int(self.ratio*self.screenRect.width()/240+0.5)

        font = QFont()
        font.setPointSize(int(1.5*self.unit/self.ratio+0.5))

        self.main_widget = QWidget()  # 创建窗口主部件
        self.main_widget.setObjectName("MainWindow")
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.main_widget.setStyleSheet(
            "QWidget#MainWindow{border-image:url(:/cheru.png);}")
        self.setWindowOpacity(0.85)  # 设置窗口透明度
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setStyleSheet(
            ''' QWidget{color:#232C51; background:rgba(255,255,255,192); border:1px solid darkGray; border-radius:'''+str(self.unit)+'''px;}''')

        close = QPushButton("")  # 关闭按钮
        large = QPushButton("")  # 空白按钮
        mini = QPushButton("")  # 最小化按钮
        close.setFixedSize(2*self.unit, 2*self.unit)
        large.setFixedSize(2*self.unit, 2*self.unit)
        mini.setFixedSize(2*self.unit, 2*self.unit)
        close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:'''+str(self.unit)+'''px;}QPushButton:hover{background:red;}''')
        large.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:'''+str(self.unit)+'''px;}QPushButton:hover{background:#F7C604;}''')
        mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:'''+str(self.unit)+'''px;}QPushButton:hover{background:#0DDF0D;}''')
        close.clicked.connect(QCoreApplication.instance().quit)
        mini.clicked.connect(self.showMinimized)
        large.clicked.connect(self.windowCtl)

        title0 = QLabel('                        切噜～♪                        ')
        title1 = QLabel('input:')
        title2 = QLabel('output:')
        title0.setFont(font)
        title1.setFont(font)
        title2.setFont(font)
        title1.setFixedSize(8*self.unit, int(2.25*self.unit+0.5))
        title2.setFixedSize(8*self.unit, int(2.25*self.unit+0.5))

        text1 = QTextEdit()
        text2 = QTextEdit()
        self.TextEditList['text1'] = text1
        self.TextEditList['text2'] = text2
        text1.setStyleSheet(
            '''QTextEdit{border:1px solid gray; border-radius:'''+str(self.unit)+'''px; padding:2px 4px;}''')
        text2.setStyleSheet(
            '''QTextEdit{border:1px solid gray; border-radius:'''+str(self.unit)+'''px; padding:2px 4px;}''')
        text1.setFont(font)
        text2.setFont(font)

        text1.setPlainText('使用 \'切噜一下 \' 开始切噜噜, \'切噜～♪ \' 翻译切噜噜')

        btn1 = QPushButton(" 切噜一下 ", self)
        btn2 = QPushButton(" 切噜～♪ ", self)
        self.BtnList['btn1'] = btn1
        self.BtnList['btn2'] = btn2
        btn1.setStyleSheet('''QPushButton{border:1px solid darkGray;height:'''+str(3*self.unit)+'''px;width:'''+str(10*self.unit)+'''px;}
                               QPushButton:hover{border:1px solid darkGray; border-radius:'''+str(self.unit)+'''px; background:rgba(211,211,211,192);}''')
        btn2.setStyleSheet('''QPushButton{border:1px solid darkGray;height:'''+str(3*self.unit)+'''px;width:'''+str(10*self.unit)+'''px;}
                               QPushButton:hover{border:1px solid darkGray; border-radius:'''+str(self.unit)+'''px; background:rgba(211,211,211,192);}''')
        btn1.setFont(font)
        btn2.setFont(font)

        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        hbox0 = QHBoxLayout()
        hbox0.addWidget(title1)
        hbox0.addStretch(1)
        hbox0.addWidget(title0)
        hbox0.addStretch(1)
        hbox0.addWidget(mini)
        hbox0.addWidget(large)
        hbox0.addWidget(close)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(title2)
        hbox1.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(5)
        hbox2.addWidget(btn1)
        hbox2.addStretch(1)
        hbox2.addWidget(btn2)
        hbox2.addStretch(5)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox0)
        vbox.addWidget(text1)
        vbox.addLayout(hbox1)
        vbox.addWidget(text2)
        vbox.addLayout(hbox2)

        self.main_widget.setLayout(vbox)
        # 设置窗口的位置和大小
        self.setGeometry(200, 200, self.width, self.height)
        # 设置窗口的标题
        self.setWindowTitle('cheru')
        # 设置窗口的图标，引用cheruresource的wcheru.ico图片
        self.setWindowIcon(QIcon(':/cheru.ico'))

    def buttonClicked(self):
        sender = self.sender()
        if(sender == self.BtnList['btn1']):
            self.TextEditList['text2'].setPlainText(
                cherulize(self.TextEditList['text1'].toPlainText()))
        if(sender == self.BtnList['btn2']):
            self.TextEditList['text2'].setPlainText(
                decherulize(self.TextEditList['text1'].toPlainText()))

    def windowCtl(self):
        if(self.isMaximized()):
            self.showNormal()
        else:
            self.showMaximized()

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None


if __name__ == '__main__':
    # 创建应用程序和对象
    ctypes.windll.user32.SetProcessDPIAware()
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    mui = MainUi()
    mui.show()
    sys.exit(app.exec_())
