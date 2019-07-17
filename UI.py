# coding:utf-8
import os,time

from PIL import Image
from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import qtawesome
import random

from reportlab.pdfgen import canvas

from PyQt5.Qt import *
from PyQt5.QtCore import *
from check import check
rundice = check()


class MainUi(QtWidgets.QMainWindow):
    global maxFlag;
    maxFlag = True;
    global name
    global image1
    image1 = ["1", "2"]
    global image2
    image2 = ["1", "2"]
    global file2
    global ifConnect
    ifConnect = False

    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 600)

        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        # 窗口背景透明
        #self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)  # 去除缝隙
        self.init_left_ui()
        self.init_right_ui()
        self.setWindowIcon(QIcon('./res/3n.png'))
        self._bottom_rect = [QPoint(x, y) for x in range(1, self.width())
                             for y in range(0, 100)]
        self.m_flag = False

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

        reply = QMessageBox.question(self, '退出',
                                     "您即将关闭软件。确定继续吗？", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def collect(self,gtpath,predpath):
        a = random.randint(0,2)

        if a == 0:

            return 1,None,None
        elif a == 1:
            return 2,None,None
        else:
            return 3,None,None



    def warningEvent(self):
        #stat, gt, pred = rundice.collect(image1[1], image2[1])
        stat, gt, pred = self.collect(image1[1], image2[1])
        if stat == 0:
            print(rundice.evaluate(gt, pred))
            self.right_bar_widget_open_input.setText(str(rundice.evaluate(gt, pred)))
            return


        if stat == 1:


            QMessageBox.warning(self, '对应图像数目不匹配',
                                     "对应图像数目不匹配，请重新选择！", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.Yes)
            return




        elif stat == 2:
            QMessageBox.warning(self, '对应图像命名不匹配',
                                        "对应图像命名不匹配，请重新选择！", QMessageBox.Yes |
                                        QMessageBox.No, QMessageBox.Yes)
            return



        elif stat == 3:
            QMessageBox.warning(self, '对应图像形状不匹配',
                                        "对应图像形状不匹配，请重新选择！", QMessageBox.Yes |
                                        QMessageBox.No, QMessageBox.Yes)
            return









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
        self.left_label_3 = QtWidgets.QPushButton(qtawesome.icon('fa.phone', color='white'), "帮助")
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

        self.left_button_9 = QLabel("@betav1.02", self)

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

    def init_right_ui(self):
        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.right_title = QCheckBox("ISICDM挑战赛专用软件", self)
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





        self.open_icon = QCheckBox('选取文件生成结果', self)  # 单选按钮
        # self.open_icon = QtWidgets.QLabel(chr(0xf115) + ' ' + '打开文件  ')
        # self.open_icon.setFont(qtawesome.font('fa', 14))
        # self.open_icon.setFont(QFont("Microsoft YaHei"))

        self.right_bar_widget_open_input = QtWidgets.QLineEdit()
        self.right_bar_widget_open_input.setPlaceholderText("点击开始计算按钮夹生成结果")
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



        # self.id_icon = QtWidgets.QLabel(chr(0xf11c) + ' ' + '填写ID(选填)  ')
        # self.id_icon.setFont(qtawesome.font('fa', 14))

        # self.right_layout.addWidget(self.right_bar_widget1, 1, 0, 1, 9)  # 合起来

        # 选择文件
        self.right_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.folder', color='black'), "选择pre文件夹")
        self.right_layout.addWidget(self.right_button_1, 7, 0, 1, 3)
        self.right_button_1.clicked.connect(self.getdirectory1)
        # 选择文件夹
        self.right_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.folder', color='black'), "选择groundtruth文件夹")
        self.right_layout.addWidget(self.right_button_2, 8, 0, 1, 3)
        self.right_button_2.clicked.connect(self.getdirectory2)

        self.start = QtWidgets.QPushButton(qtawesome.icon('fa.play', color='black'), "开始计算")
        self.right_layout.addWidget(self.start, 9, 0, 1, 3)
        self.start.clicked.connect(self.warningEvent)

        # 进度条文字
        txt = ""









        # 进度条
        self.pbar = QProgressBar(self)

        self.pbar.setToolTip("任务处理进度条")
        self.right_layout.addWidget(self.pbar, 11, 0, 1, 9)

        self.right_message2 = QLabel(self)
        pixmap = QPixmap('./res/4.jpg')
        self.right_message2.setScaledContents(True)
        self.right_message2.setPixmap(pixmap)
        self.right_layout.addWidget(self.right_message2, 1, 0, 1, 9)

        self.right_message1 = QLabel("联系人：唐晓颖\n联系电话：13922156126", self)

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



        self.right_bar_widget_open_input.setStyleSheet(  # 选择文件栏
            '''QLineEdit{
            font-family:"Microsoft YaHei";
                    border:1px solid gray;
                    width:500px;
                    border-radius:10px;
                    padding:2px 4px;
            }


            ''')

        self.pbar.setStyleSheet(  # 进度条
            '''QProgressBar{ 
            font-family:"Microsoft YaHei";
               border:1px solid gray;
               width:300px;
               border-radius:10px;
               padding:2px 4px;
               text-align: center; 
            }
               QProgressBar::chunk {
               background-color: #8A2BE2;

    }
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
        #self.rb1.hide()
        #self.rb.hide()
        self.pbar.hide()
        #self.id_icon.hide()
        #self.right_bar_widget_id_input.hide()
        self.right_bar_widget_open_input.hide()
        self.right_button_1.hide()
        self.right_button_2.hide()
        #self.proc.hide()
        self.right_title.hide()


    def showmessage2(self):
        self.start.hide()
        self.right_message2.show()
        self.right_message1.hide()
        self.open_icon.hide()
        #self.rb1.hide()
        #self.rb.hide()
        self.pbar.hide()
        #self.id_icon.hide()
        #self.right_bar_widget_id_input.hide()
        self.right_bar_widget_open_input.hide()
        self.right_button_1.hide()
        self.right_button_2.hide()
        #self.proc.hide()
        self.right_title.hide()


    def showright(self):
        self.right_message2.hide()
        self.right_message1.hide()
        self.open_icon.show()
        #self.rb1.show()
        #self.rb.show()
        self.pbar.show()
        #self.id_icon.show()
        #self.right_bar_widget_id_input.show()
        self.right_bar_widget_open_input.show()
        self.right_button_1.show()
        self.right_button_2.show()
        #self.proc.show()
        self.start.show()
        self.right_title.show()

    def getdirectory1(self):
        directory1 = ""
        f = open('./path/origin1.txt')
        lastpath1 = str(f.read())
        print(f.read())
        f.close()

        directory1 = QFileDialog.getExistingDirectory(self, "选取文件夹", lastpath1)  # 起始路径
        if (directory1 != ""):
            # print(directory1)
            #self.right_bar_widget_open_input.setText( directory1)

            f = open('./path/origin1.txt', 'wb+')
            f.truncate()
            f.close()

            f = open('./path/origin1.txt', 'a')
            f.write(directory1)
            f.close()
            global image1
            image1[0] = 'dir'
            image1[1] = directory1
            print(image1)

    def getdirectory2(self):
        directory2 = ""
        f = open('./path/origin2.txt')
        lastpath2 = str(f.read())
        print(f.read())
        f.close()

        directory2 = QFileDialog.getExistingDirectory(self, "选取文件夹", lastpath2)  # 起始路径
        if (directory2 != ""):
            # print(directory1)
            #self.right_bar_widget_open_input.setText( directory1)

            f = open('./path/origin2.txt', 'wb+')
            f.truncate()
            f.close()

            f = open('./path/origin2.txt', 'a')
            f.write(directory2)
            f.close()
            global image2
            image2[0] = 'dir'
            image2[1] = directory2
            print(image2)





    def mousePressEvent(self, event):
        self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
        self.m_flag=False
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



def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
