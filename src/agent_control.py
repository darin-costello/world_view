#!/usr/bin/python

import sys, rospy
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from sphero_swarm_node.msg import SpheroTwist
from mm_apriltags_tracker.msg import april_tag_pos
from geometry_msgs.msg import Pose2D


APRILTAG = 6
TBOT = 32

class AgentControl(QtGui.QWidget):
    def __init__(self):
        super(QtGui.QWidget, self).__init__()
        width = 500 #TODO change to query param
        height = 500 #TODO change to query param
        self.saveNum = 0
        self.resize(width, height)
        self.initUI()
        self.leader = -1
        rospy.init_node("world_view", anonymous = True)
        self.tagLocSub = rospy.Subscriber('/april_tag_pos', april_tag_pos, self.tagPosCallback)
        self.blackPen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        self.bluePen = QtGui.QPen(QtCore.Qt.blue, 2, QtCore.Qt.SolidLine)
        self.agentMap = {}


    def initUI(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.createPNGAction = QAction("Create Map", self)

        self.createPNGAction.triggered.connect(self.createPNG)
        self.addAction(self.createPNGAction)
        self.createPNGAction.setShortcuts([QKeySequence(Qt.CTRL + Qt.Key_P)])
        self.setPalette(p)
        self.show()


    def createPNG(self):
        self.update()
        p = QPixmap.grabWindow(self.winId())
        p.save("save%d.png" % self.saveNum, "png")
        self.saveNum += 1


    def tagPosCallback(self, msg):
        for i in range(0, len(msg.id)):
            self.agentMap[msg.id[i]] = msg.pose[i]
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter();
        painter.begin(self)
        for key, value in self.agentMap.iteritems():

            rect = QRect(value.x - APRILTAG/2, value.y - APRILTAG/2, APRILTAG, APRILTAG)
            painter.setBrush(Qt.black)
            if(key == 0):
                painter.setBrush(Qt.blue)
            painter.drawRect(rect)
        painter.end()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = AgentControl()
    w.show()
    sys.exit(app.exec_())
