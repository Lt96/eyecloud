# coding:utf-8
import os
import traceback

from PIL import Image
from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import qtawesome
from PyQt5.QtWidgets import QCheckBox, QProgressBar, QFileDialog, QSpacerItem
from reportlab.pdfgen import canvas
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import *

from FundusAnalysis import FundusAnalysis

CONFIG_PATH = './config.json'
exts = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG']


o1 = open('./res/path/origin1.txt', 'wb+')
o1.truncate()
o1.close()

o2 = open('./res/path/origin2.txt', 'wb+')
o2.truncate()
o2.close()

s1 = open('./res/path/start1.txt', 'wb+')
s1.truncate()
s1.close()

s2 = open('./res/path/start2.txt', 'wb+')
s2.truncate()
s2.close()


class AnalysisThread(QtCore.QThread):
    #  通过类成员对象定义信号对象
    signal_bar = pyqtSignal(int)
    signal_txt = pyqtSignal(str)

    def __init__(self, fundusAnalysis, images, save_paths, va, ids, button):
        super(AnalysisThread, self).__init__()
        self.fundusAnalysis = fundusAnalysis
        self.images = images
        self.save_paths = save_paths
        self.va = va
        self.ids = ids
        self.button = button

    def run(self):
        self.button.setEnabled(False)
        self.fundusAnalysis.initial(self.callback_txt)
        self.fundusAnalysis.analysis(
            self.images,
            self.save_paths,
            self.callback_pbar,
            self.callback_txt,
            self.va,
            self.ids
        )
        self.button.setEnabled(True)

    def callback_pbar(self, msg):
        self.signal_bar.emit(msg)

    def callback_txt(self, msg):
        self.signal_txt.emit(msg)


class MainUi(QtWidgets.QMainWindow):
    global maxFlag
    maxFlag = True
    global name
    global image1
    image1 = ["1", "2"]
    global file2
    global ifConnect
    ifConnect = False

    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 720)

        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        # 窗口背景透明
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)  # 去除缝隙
        self.init_left_ui()
        self.init_right_ui()
        self.setWindowIcon(QIcon('./res/3n.png'))
        self._bottom_rect = [QPoint(x, y) for x in range(1, self.width())
                             for y in range(0, 100)]
        self.m_flag = False
        self.fundusAnalysis = FundusAnalysis(CONFIG_PATH)

    def maxMin(self):
        global maxFlag
        desktop = QDesktopWidget()

        rect = desktop.screenGeometry(0)  # 获取第一个显示器的分辨率
        if (maxFlag):
            self.setGeometry(QtCore.QRect(0, 0, desktop.geometry().width(), desktop.geometry().height()))
            # self.setFixedSize(QSize( desktop.geometry().width(),desktop.geometry().height()))
            self.setFixedSize(rect.width(), rect.height())

            maxFlag = False
            print(maxFlag)
        else:

            self.setGeometry(QtCore.QRect(desktop.geometry().width() / 5, desktop.geometry().height() / 5, 1000, 720))
            self.setFixedSize(QSize(1000, 720))
            maxFlag = True
            print(maxFlag)

    def closeEvent(self, event):

        reply = QMessageBox(QMessageBox.Question, self.tr('退出'),
                            self.tr("您即将关闭软件，确定继续吗？"), QMessageBox.NoButton, self)
        yr_btn = reply.addButton(self.tr("是"), QMessageBox.YesRole)
        reply.addButton(self.tr("否"), QMessageBox.NoRole)
        reply.exec_()

        if reply.clickedButton() == yr_btn:
            event.accept()
        else:
            event.ignore()

    def warning(self,event):
        warn = QMessageBox.warning(self,'警告',"出现错误，请选择需要诊断的图片或者文件夹",QMessageBox.Yes,
                                   QMessageBox.Yes)
        if warn == QMessageBox.Yes:
            event.ignore()

    def init_left_ui(self):
        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格
        self.main_layout.addWidget(self.left_widget, 0, 0, 10, 2)  # 左侧部件在第0行第0列，占12行2列
        self.left_close = QtWidgets.QPushButton(qtawesome.icon('fa.times', color='gray'), "")  # 关闭按钮

        self.left_mini = QtWidgets.QPushButton(qtawesome.icon('fa.minus', color='gray'), "")  # 最小化按钮
        self.left_close.clicked.connect(self.close)
        self.left_mini.clicked.connect(self.showMinimized)

        self.left_label_1 = QtWidgets.QPushButton(qtawesome.icon('fa.book', color='white'), "项目")
        self.left_label_1.setObjectName('left_label')
        self.left_label_1.clicked.connect(self.showmessage2)

        self.left_label_2 = QtWidgets.QPushButton(qtawesome.icon('fa.tasks', color='white'), "任务中心")
        self.left_label_2.setObjectName('left_label')
        self.left_label_2.clicked.connect(self.showright)
        self.left_label_3 = QtWidgets.QPushButton(qtawesome.icon('fa.at', color='white'), "帮助")
        self.left_label_3.setObjectName('left_label')
        self.left_label_3.clicked.connect(self.showmessage1)
        self.left_layout.addWidget(self.left_mini, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 0, 1, 1)

        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 3, 0, 1, 3)

        # blank
        self.left_button_1 = QLabel("", self)

        self.left_button_2 = QLabel("", self)
        self.left_button_3 = QLabel("", self)
        self.left_button_4 = QLabel("", self)
        self.left_button_5 = QLabel("", self)
        self.left_button_6 = QLabel("", self)

        self.left_button_9 = QLabel(self)
        self.left_button_9.setText("<a href='https://shimo.im/docs/bQeGWqF6C30WBVAU/' style='color:white'>Betav1.3.0</a>")
        self.left_button_9.setOpenExternalLinks(True)  # 允许访问超链接
        self.left_button_9.linkHovered.connect(self.link_hovered)  # 针对链接光标略过
        self.left_button_9.linkActivated.connect(self.link_clicked)  # 针对链接点击事件

        self.left_button_9.setStyleSheet(
            '''
            QLabel{
            border-width:0;
                border-style:outset;
                font-family:"Microsoft YaHei";
                font-size:10px;
                color:white;

            }
            '''
        )

        # 空白
        self.left_layout.addWidget(self.left_button_1, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_4, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_5, 8, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_6, 9, 0, 1, 3)

        self.left_layout.addWidget(self.left_button_9, 10, 0, 1, 3)

        # 左侧按钮
        self.left_close.setFixedSize(16, 16)  # 设置关闭按钮的大小

        self.left_mini.setFixedSize(16, 16)  # 设置最小化按钮大小
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')

        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.left_label_1.setStyleSheet(  # left1
            '''
            QPushButton{
                font-family:"Microsoft YaHei";
                border:none;
                color:white;
                font-size:15px;
                height:50px;
                padding-left:10px;
                padding-right:10px;
                text-align:left;
            }
            QPushButton:hover{
                color:black;
                border:1px solid #F3F3F5;
                border-radius:10px;
                background:LightGray;
            }
        ''')

        self.left_label_2.setStyleSheet(  # left2
            '''
            QPushButton{
            font-family:"Microsoft YaHei";
                border:none;
                color:white;
                font-size:15px;
                height:50px;
                padding-left:10px;
                padding-right:10px;
                text-align:left;
            }
            QPushButton:hover{
                color:black;
                border:1px solid #F3F3F5;
                border-radius:10px;
                background:LightGray;
            }
        ''')

        self.left_label_3.setStyleSheet(  # left3
            '''
            QPushButton{
                font-family:"Microsoft YaHei";
                border:none;
                color:white;
                font-size:15px;
                height:50px;
                padding-left:10px;
                padding-right:10px;
                text-align:left;
            }
            QPushButton:hover{
                color:black;
                border:1px solid #F3F3F5;
                border-radius:10px;
                background:LightGray;
            }
        ''')

        # 左侧菜单
        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
            QWidget#left_widget{
                background:gray;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;}
        ''')

    def link_hovered(self):

        print("光标滑过版本号")

    def link_clicked(self):

        print("点击访问查看更新")

    def init_right_ui(self):
        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.right_title = QCheckBox("AIforEye智能辅助诊断系统", self)
        self.right_layout.addWidget(self.right_title, 1, 0, 1, 3)

        self.right_title.setStyleSheet(
            '''
            QCheckBox{
                font-family:"Microsoft YaHei";
                spacing: 2px;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border:none;
                color:black;



    } QCheckBox::indicator {
    width: 40px;
    height: 30px;
    } QCheckBox::indicator:unchecked {
    image: url(./res/3n.png);

    }
    } QCheckBox::indicator:unchecked:pressed {
    image: url(./res/3n.png);

    } 
    QCheckBox::indicator:checked{
    image: url(./res/3n.png);}
    QCheckBox::indicator:checked:pressed {
    image: url(./res/3n.png);}


            '''

        )

        self.main_layout.addWidget(self.right_widget, 0, 3, 10, 10)  # 右侧部件在第0行第3列，占12行10列

        self.id_icon = QCheckBox('填写病人ID（选填）', self)  # 单选按钮

        self.right_layout.addWidget(self.id_icon, 2, 0, 1, 1)

        self.id_icon.setStyleSheet(
            '''
            QCheckBox{
                font-family:"Microsoft YaHei";
                spacing: 2px;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border:none;
                color:black;



    } QCheckBox::indicator {
    width: 40px;
    height: 30px;
    } QCheckBox::indicator:unchecked {
    image: url(./res/input.png);

    }
    } QCheckBox::indicator:unchecked:pressed {
    image: url(./res/input.png);

    } 
    QCheckBox::indicator:checked{
    image: url(./res/input.png);}
    QCheckBox::indicator:checked:pressed {
    image: url(./res/input.png);}


            '''

        )

        self.right_bar_widget_id_input = QtWidgets.QLineEdit()
        self.right_bar_widget_id_input.setPlaceholderText("请在此填入病人ID")
        regExp = QRegExp('^[1-9]\d{1,30}$')

        self.right_bar_widget_id_input.setValidator(QRegExpValidator(regExp, self))

        # self.right_layout.addWidget(self.id_icon, 2, 0, 1, 1)  # icon

        self.right_layout.addWidget(self.right_bar_widget_id_input, 3, 0, 1, 9)  # 输入栏

        self.open_icon = QCheckBox('打开文件 (DR诊断目前仅限于50DX散瞳照)', self)  # 单选按钮
        # self.open_icon = QtWidgets.QLabel(chr(0xf115) + ' ' + '打开文件  ')
        # self.open_icon.setFont(qtawesome.font('fa', 14))
        # self.open_icon.setFont(QFont("Microsoft YaHei"))

        self.right_bar_widget_open_input = QtWidgets.QLineEdit()
        self.right_bar_widget_open_input.setPlaceholderText("点击按钮选择图片或文件夹生成源路径")
        self.right_bar_widget_open_input.setEnabled(False)

        self.right_layout.addWidget(self.open_icon, 4, 0, 1, 3)  # icon
        self.right_layout.addWidget(self.right_bar_widget_open_input, 5, 0, 1, 9)  # 输入栏

        self.open_icon.setStyleSheet(
            '''
            QCheckBox{
                font-family:"Microsoft YaHei";
                spacing: 2px;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border:none;
                color:black;



    } QCheckBox::indicator {
    width: 40px;
    height: 30px;
    } QCheckBox::indicator:unchecked {
    image: url(./res/open.png);

    }
    } QCheckBox::indicator:unchecked:pressed {
    image: url(./res/open.png);

    } 
    QCheckBox::indicator:checked{
    image: url(./res/open.png);}
    QCheckBox::indicator:checked:pressed {
    image: url(./res/open.png);}


            '''

        )

        # checkbox
        self.rb = QCheckBox('血管分析', self)  # 单选按钮
        self.rb.toggled.connect(self.setConnect)

        self.rb.setToolTip("可选择是否进行血管分析")
        self.right_layout.addWidget(self.rb, 6, 0, 1, 2)

        self.rb1 = QCheckBox('DR诊断', self)
        # self.rb1.setFont(qtawesome.font('fa', 14))

        self.rb1.setToolTip("默认进行DR诊断")
        self.right_layout.addWidget(self.rb1, 6, 2, 1, 2)

        # self.id_icon = QtWidgets.QLabel(chr(0xf11c) + ' ' + '填写ID(选填)  ')
        # self.id_icon.setFont(qtawesome.font('fa', 14))

        # self.right_layout.addWidget(self.right_bar_widget1, 1, 0, 1, 9)  # 合起来

        # 选择文件
        self.right_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.picture-o', color='black'), "选择图片")
        self.right_layout.addWidget(self.right_button_1, 7, 0, 1, 2)
        self.right_button_1.clicked.connect(self.gitfilename)
        # 选择文件夹
        self.right_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.folder', color='black'), "选择文件夹")
        self.right_layout.addWidget(self.right_button_2, 8, 0, 1, 2)
        self.right_button_2.clicked.connect(self.getdirectory)

        self.start = QtWidgets.QPushButton(qtawesome.icon('fa.play', color='black'), "选择保存路径并开始")
        self.right_layout.addWidget(self.start, 9, 0, 1, 2)
        self.start.clicked.connect(self.main)

        # 进度条文字
        txt = ""
        # self.proc = QtWidgets.QLabel(chr(0xf110) + ' ' + '任务进度：' + '' + txt)
        self.proc = QCheckBox('任务进度：' + '' + txt, self)  # 单选按钮
        # self.proc.setFont(qtawesome.font('fa', 12))
        self.right_layout.addWidget(self.proc, 10, 0, 1, 9)

        self.proc.setStyleSheet(
            '''
            QCheckBox{
                font-family:"Microsoft YaHei";
                spacing: 2px;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border:none;
                color:black;



    } QCheckBox::indicator {
    width: 40px;
    height: 30px;
    } QCheckBox::indicator:unchecked {
    image: url(./res/loading.png);

    }
    } QCheckBox::indicator:unchecked:pressed {
    image: url(./res/loading.png);

    } 
    QCheckBox::indicator:checked{
    image: url(./res/loading.png);}
    QCheckBox::indicator:checked:pressed {
    image: url(./res/loading.png);}


            '''

        )

        # 进度条
        self.pbar = QProgressBar(self)

        self.pbar.setToolTip("任务处理进度条")
        self.right_layout.addWidget(self.pbar, 11, 0, 1, 9)

        self.right_message2 = QLabel(self)
        pixmap = QPixmap('./res/4.jpg')
        self.right_message2.setScaledContents(True)
        self.right_message2.setPixmap(pixmap)
        self.right_layout.addWidget(self.right_message2, 1, 0, 1, 9)

        self.right_message1 = QLabel("邮箱: tangxy@sustc.edu.cn\n"
                                     "地址: 广东省深圳市南山区南方科技大学\n"
                                     "合作单位: 中山大学中山眼科中心\n", self)

        self.right_message1.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.right_layout.addWidget(self.right_message1, 1, 0, 1, 3)  # 输入栏

        self.right_message1.setStyleSheet(
            '''
                QLabel{

                border-width:0;
                border-style:outset;
                font-family:"Microsoft YaHei";
                font-size:20px;
                height:50px;
                padding-left:0px;
                padding-right:10px;
                text-align:left;

                }

            ''')

        # self.right_message2 = QtWidgets.QTextBrowser()
        # self.right_message2.setText("概况")  # 概况
        # self.right_layout.addWidget(self.right_message2, 0, 0, 1, 9)

        self.right_bar_widget_id_input.setStyleSheet(  # 输入id栏
            '''QLineEdit{
                    font-family:"Microsoft YaHei";
                    border:1px solid gray;
                    width:300px;
                    border-radius:10px;
                    padding:2px 4px;
            }''')

        self.right_bar_widget_open_input.setStyleSheet(  # 选择文件栏
            '''QLineEdit{
            font-family:"Microsoft YaHei";
                    border:1px solid gray;
                    width:300px;
                    border-radius:10px;
                    padding:2px 4px;
            }


            ''')

        self.pbar.setStyleSheet(  # 进度条
            '''QProgressBar{ 
            font-family:"Microsoft YaHei";
               border:1px solid gray;

               border-radius:10px;
               padding:2px 4px;
               text-align: center; 
            }
               QProgressBar::chunk {


               border-radius:10px;
               background:#696969



    }
            ''')

        # background:qlineargradient(spread:pad,x1:0,y1:0,x2:1,y2:0,stop:0 red,stop:1 blue)

        self.rb.setStyleSheet(
            '''
            QCheckBox{
                font-family:"Microsoft YaHei";
                spacing: 2px;
                color: white;
                font-size:14px;

                border:none;
                color:black;



} QCheckBox::indicator {
    width: 40px;
    height: 20px;
} QCheckBox::indicator:unchecked {
    image: url(./res/off1.png);}

QCheckBox::indicator:unchecked:hover {
image: url(./res/off1-hover.png);
}


} QCheckBox::indicator:unchecked:pressed {
    image: url(./res/off1.png);

} 
QCheckBox::indicator:checked{
    image: url(./res/on1.png);}
QCheckBox::indicator:checked:hover {
image: url(./res/on1-hover.png);
}
QCheckBox::indicator:checked:pressed {
    image: url(./res/on1.png);}


            '''

        )

        self.rb1.setStyleSheet(  # DR
            '''
            QCheckBox{
                font-family:"Microsoft YaHei";
                spacing: 2px;
                color: white;
                font-size: 14px;

                border:none;
                color:black;



    } QCheckBox::indicator {
    width: 40px;
    height: 20px;
    } QCheckBox::indicator:unchecked {
    image: url(./res/true.png);

    }
    } QCheckBox::indicator:unchecked:pressed {
    image: url(./res/true.png);

    } 
    QCheckBox::indicator:checked{
    image: url(./res/true.png);}
    QCheckBox::indicator:checked:pressed {
    image: url(./res/true.png);}


            ''')

        self.right_button_1.setStyleSheet(  # 选择图片
            '''
            QPushButton{
            font-family:"Microsoft YaHei";
                border:1px solid #F3F3F5;
                border-radius:10px;
                border:none;
                color:black;
                background:lavender;

                font-size:14px;
                height:40px;
                padding-left:10px;
                padding-right:10px;
                text-align:left;
            }
            QPushButton:hover{
                color:black;
                border:1px solid #F3F3F5;
                border-radius:10px;
                background:gainsboro ;
            }
        ''')
        self.right_button_2.setStyleSheet(  # 选择文件夹
            '''
            QPushButton{
            font-family:"Microsoft YaHei";
                border:1px solid #F3F3F5;
                border-radius:10px;
                border:none;
                color:black;
                background:lavender;

                font-size:14px;
                height:40px;
                padding-left:10px;
                padding-right:10px;
                text-align:left;
            }
            QPushButton:hover{
                color:black;
                border:1px solid #F3F3F5;
                border-radius:10px;
                background:gainsboro ;
            }
        ''')

        self.right_widget.setStyleSheet(  # 右边大框
            '''
            QWidget#right_widget{
            font-family:"Microsoft YaHei";
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')
        self.start.setStyleSheet(  # 开始任务
            '''
            QPushButton{
            font-family:"Microsoft YaHei";
                border:1px solid #F3F3F5;
                border-radius:10px;
                border:none;
                color:black;
                background:lavender;

                font-size:14px;
                height:40px;
                padding-left:10px;
                padding-right:10px;
                text-align:left;
            }
            QPushButton:hover{
                color:black;
                border:1px solid #F3F3F5;
                border-radius:10px;
                background:gainsboro ;
            }
        ''')
        self.right_message1.hide()
        self.right_message2.hide()

    def showmessage1(self):
        self.start.hide()
        self.right_message1.show()
        self.right_message2.hide()
        self.open_icon.hide()
        self.rb1.hide()
        self.rb.hide()
        self.pbar.hide()
        self.id_icon.hide()
        self.right_bar_widget_id_input.hide()
        self.right_bar_widget_open_input.hide()
        self.right_button_1.hide()
        self.right_button_2.hide()
        self.proc.hide()
        self.right_title.hide()

    def showmessage2(self):
        self.start.hide()
        self.right_message2.show()
        self.right_message1.hide()
        self.open_icon.hide()
        self.rb1.hide()
        self.rb.hide()
        self.pbar.hide()
        self.id_icon.hide()
        self.right_bar_widget_id_input.hide()
        self.right_bar_widget_open_input.hide()
        self.right_button_1.hide()
        self.right_button_2.hide()
        self.proc.hide()
        self.right_title.hide()

    def showright(self):
        self.right_message2.hide()
        self.right_message1.hide()
        self.open_icon.show()
        self.rb1.show()
        self.rb.show()
        self.pbar.show()
        self.id_icon.show()
        self.right_bar_widget_id_input.show()
        self.right_bar_widget_open_input.show()
        self.right_button_1.show()
        self.right_button_2.show()
        self.proc.show()
        self.start.show()
        self.right_title.show()

    def setConnect(self):
        global ifConnect
        if (ifConnect):
            ifConnect = False
        else:
            ifConnect = True
        print(ifConnect)

    def printl(self):
        self.pbar.setValue(0)
        global image1

        self.right_bar_widget_open_input.setEnabled(False)

        if image1[0] == "dir":
            f = open("./res/path/start1.txt")
            lastpath13 = str(f.read())
            print(f.read())
            f.close()
            filename = QFileDialog.getSaveFileName(self, 'save file', lastpath13)
            print(filename)
            f = open('./res/path/start1.txt', 'wb+')
            f.truncate()
            f.close()

            f = open('./res/path/start1.txt', 'a')
            f.write(filename[0])
            f.close()
            if filename[0] != "":
                self.dirPDF(image1[1], filename[0])
        elif image1[0] == "f":
            f = open("./res/path/start2.txt")
            lastpath23 = str(f.read())
            print(f.read())
            f.close()
            filename = QFileDialog.getSaveFileName(self, 'save file', lastpath23, '(*.pdf)')
            print(filename)
            f = open('./res/path/start2.txt', 'wb+')
            f.truncate()
            f.close()

            f = open('./res/path/start2.txt', 'a')
            f.write(filename[0])
            f.close()
            if filename[0] != "":
                self.pbar.setValue(100)
                self.pic2pdf(image1[1], filename[0])
        else:
            print("null")

        self.right_bar_widget_id_input.clear()

    def dirPDF(self, input_path, output_path):  # 转文件夹
        self.pbar.setValue(0)
        print("start")
        print(input_path)
        print(output_path)
        # 获取输入文件夹中的所有文件/夹，并改变工作空间
        files = os.listdir(input_path)
        os.chdir(input_path)
        # 判断输出文件夹是否存在，不存在则创建
        if (not os.path.exists(output_path)):
            os.makedirs(output_path)
        count = 0
        for file in files:
            if (os.path.isfile(file)):
                count += 1
        now = 0
        for file in files:
            # 判断是否为文件，文件夹不操作
            if (os.path.isfile(file)):
                now += 1
                self.pbar.setValue(now / count * 100)
                # 用.隔开文件名获取图片处理
                point = file.rfind('.')
                rightpart = file[point:]
                leftpart = file[:point]
                print(rightpart)
                if (rightpart == '.jpg' or rightpart == '.png'):
                    #     img = Image.open(file)
                    #     width = int(img.size[0] * 2)
                    #     height = int(img.size[1] * 2)
                    #     img = img.resize((width, height), Image.ANTIALIAS)
                    print(os.path.join(output_path, "New_" + file))
                    #     img.save(os.path.join(output_path, "New_" + file))
                    self.pic2pdf(file, os.path.join(output_path, "New_" + leftpart + ".pdf"))
        self.pbar.setValue(100)

    def pic2pdf(self, img, filePdf):  # 将一张图片转为pdf
        print(1)
        # 读取图片，确保按文件名排序
        print(img)
        imgdoc = Image.open(img)  # 打开图片
        x = imgdoc.size[0]
        y = imgdoc.size[1]
        c = canvas.Canvas(filePdf, [x + 100, y + 100])  # 使用图片创建单页的 PDF
        print(imgdoc.size)
        c.drawImage(img, 50, 0, x, y)
        c.drawString(20, y + 5, filePdf)
        c.showPage()
        c.save()

    def gitfilename(self):
        f = open('./res/path/origin1.txt')
        lastpath = str(f.read())
        print(f.read())
        f.close()

        filename = QFileDialog.getOpenFileName(self, "选择文件", lastpath, "Image (*.jpg);;Image(*.png)")  # 这个地方弹出窗口

        if (filename != ""):
            self.right_bar_widget_open_input.setText(filename[0])
            f = open('./res/path/origin1.txt', 'wb+')
            f.truncate()
            f.close()

            f = open('./res/path/origin1.txt', 'a')
            f.write(filename[0])
            f.close()

            global image1
            #  file1+=['ID: '+self.IDmessage.text()]
            image1[0] = "f"
            image1[1] = filename[0]
            print(filename[0])

    def getdirectory(self):
        directory1 = ""
        f = open('./res/path/origin2.txt')
        lastpath = str(f.read())
        print(f.read())
        f.close()

        directory1 = QFileDialog.getExistingDirectory(self, "选取文件夹", lastpath)  # 起始路径
        if (directory1 != ""):
            # print(directory1)
            self.right_bar_widget_open_input.setText(directory1)

            f = open('./res/path/origin2.txt', 'wb+')
            f.truncate()
            f.close()

            f = open('./res/path/origin2.txt', 'a')
            f.write(directory1)
            f.close()
            global image1
            image1[0] = 'dir'
            image1[1] = directory1
            print(image1)

    def mousePressEvent(self, event):
        self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
        self.m_flag = False
        if event.button() == Qt.LeftButton and self.m_Position in self._bottom_rect:
            self.m_flag = True
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):

        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置

            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):

        self.m_flag = False

        self.setCursor(QCursor(Qt.ArrowCursor))

    def main(self):
        self.right_bar_widget_id_input.setEnabled(False)
        self.pbar.setValue(0)

        global image1
        if (image1 == []):
            print("null")
        else:
            if (image1[0] == "dir"):
                with open("./res/path/start1.txt") as f:
                    lastpath13 = str(f.read())
                    save_directory = QFileDialog.getExistingDirectory(self, "诊断报告保存路径", lastpath13)

                if save_directory:
                    with open('./res/path/start1.txt', 'wb+') as f:
                        f.truncate()

                    with open('./res/path/start1.txt', 'a') as f:
                        f.write(save_directory)

                if not save_directory:
                    return
                images = os.listdir(image1[1])
                images = [
                    os.path.join(image1[1], image) for image in images
                    if os.path.splitext(image)[1] in exts
                ]
                ids = [
                    os.path.splitext(os.path.split(image)[1])[0]
                    for image in images
                ]
                save_paths = [
                    os.path.join(save_directory, id_ + '.pdf')
                    for id_ in ids
                ]
                self.thread = AnalysisThread(
                    self.fundusAnalysis,
                    images,
                    save_paths,
                    ifConnect,
                    ids,
                    self.start)
                self.thread.signal_bar.connect(self.callback_pbar)
                self.thread.signal_txt.connect(self.callback_proc)
                self.thread.finished.connect(self.thread.quit)
                self.thread.finished.connect(self.thread.deleteLater)
                self.thread.start()

            if (image1[0] == "f"):
                with open("./res/path/start2.txt") as f:
                    lastpath23 = str(f.read())
                    filename, _ = QFileDialog.getSaveFileName(self, '诊断报告保存路径', lastpath23, '(*.pdf)')

                if filename:
                    with open('./res/path/start2.txt', 'wb+') as f:
                        f.truncate()

                    with open('./res/path/start2.txt', 'a') as f:
                        f.write(filename)

                if not filename:
                    return
                # (self, 'save file', '/','(*.png);;(*.jpg);;(*.pdf)')
                #  img = Image.open(image1[1])
                #  width = int(img.size[0] * 2)
                #  height = int(img.size[1] * 2)
                #  img = img.resize((width, height), Image.ANTIALIAS)
                #  print(filename)
                #  dir=os.path.join(os.path.dirname(filename[0]),  os.path.basename(filename[0]))
                #  print(dir)
                #  print(filename[0])
                # img.save(filename[0])
                id_ = self.right_bar_widget_id_input.text()
                if not id_:
                    name = os.path.split(image1[1])[1]
                    id_ = os.path.splitext(name)[0]
                self.thread = AnalysisThread(
                    self.fundusAnalysis,
                    [image1[1]],
                    [filename],
                    ifConnect,
                    [id_],
                    self.start
                )
                self.thread.signal_bar.connect(self.callback_pbar)
                self.thread.signal_txt.connect(self.callback_proc)
                self.thread.finished.connect(self.thread.quit)
                self.thread.finished.connect(self.thread.deleteLater)
                self.thread.start()

        self.right_bar_widget_id_input.clear()
        self.right_bar_widget_id_input.setEnabled(True)

    def callback_pbar(self, value):
        self.pbar.setValue(value)

    def callback_proc(self, txt):
        self.proc.setText(txt)


def my_errors(exc_type, exc_value, tb):
    file = open('./error.log', 'w')
    traceback.print_exception(exc_type, exc_value, tb, file=file)
    file.close()
    print(exc_type, exc_value)
    sys.exit(1)


sys.excepthook = my_errors

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())
