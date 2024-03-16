from PySide2.QtCore import Qt
from PySide2.QtWidgets import *
import os


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.nodes = {}
        self.search_path = ''
        # Parent Layout
        self.layout = QVBoxLayout()

        # Child layouts
        self.uplyt1 = QHBoxLayout()
        self.uplyt2 = QHBoxLayout()
        self.midlyt = QHBoxLayout()
        self.lowlyt = QHBoxLayout()

        # Buttons
        button = QPushButton("Select Marked")
        button.clicked.connect(self.select)
        button1 = QPushButton('Select All')
        button1.clicked.connect(self.selectAll)
        button2 = QPushButton('Browse')
        button2.clicked.connect(self.browse)
        button3 = QPushButton('Search')
        button3.clicked.connect(self.search)

        self.view = QListWidget()
        self.view2 = QListWidget()
        self.miss = QListWidget()
        self.miss.addItem("Missing Files:")
        self.label = QListWidget()
        self.label.addItem("Path you chose:")

        # structure
        self.uplyt1.addWidget(button1)
        self.uplyt1.addWidget(self.view)
        self.uplyt2.addWidget(button)
        self.uplyt2.addWidget(self.view2)
        self.midlyt.addWidget(button2)
        self.midlyt.addWidget(self.label)
        self.lowlyt.addWidget(button3)
        self.lowlyt.addWidget(self.miss)

        # Layout Setup
        self.layout.addLayout(self.uplyt1)
        self.layout.addLayout(self.uplyt2)
        self.layout.addLayout(self.midlyt)
        self.layout.addLayout(self.lowlyt)

        self.setLayout(self.layout)
        self.setParent(hou.ui.mainQtWindow(), Qt.Window)
        self.resize(800, 600)

    def selectAll(self):
        self.view.clear()
        self.obj_list = list(hou.node("/").allSubChildren())
        for i in range(len(self.obj_list)):
            try:
                self.nodes[self.obj_list[i].name()] = self.obj_list[i].evalParm('file').replace('\\', '/')
            except:
                pass

        QMessageBox.about(self, "Selected", f"you selected {len(self.nodes)}")
        self.view.addItems(self.nodes)
        self.view2.clear()

    def select(self):
        self.view2.clear()
        self.nodes.clear()
        self.obj_list = list(hou.selectedNodes())
        for i in range(len(self.obj_list)):
            try:
                self.nodes[self.obj_list[i].name()] = self.obj_list[i].evalParm('file').replace('\\', '/')
            except:
                pass

        QMessageBox.about(self, "Selected", f"you selected {len(self.nodes)}")
        self.view2.addItems(self.nodes)
        self.view.clear()

    def browse(self):
        self.search_path = QFileDialog.getExistingDirectory(caption='Select a folder')
        self.label.addItem(self.search_path)

    def finder(self, file):
        for root, dirs, files in os.walk(self.search_path):
            if file in files:
                x = os.path.join(root, file)
                x = x.replace('\\', '/')
                return x

    def search(self):
        path = ''
        self.miss.clear()

        lost = []
        found = []

        for nodeName, filePath in self.nodes.items():
            file = filePath.split("/")[-1]
            if not os.path.isfile(filePath):
                path = self.finder(file)

            if not path:
                lost.append(nodeName)

            else:
                for i in range(len(self.obj_list)):
                    if self.obj_list[i].name() == nodeName:
                        if hip in path:
                            path = path.replace(hip, "$HIP")
                        elif job in path:
                            path = path.replace(job, "$JOB")
                        elif prj in path:
                            path = path.replace(prj, "$PRJ")

                        try:
                            if path:
                                self.obj_list[i].parm('file').set(path)
                        except:
                            pass

                        del self.obj_list[i]
                        found.append(nodeName)
                        break

        for i in found:
            del self.nodes[i]

        if lost is not []:
            QMessageBox.about(self, "Lost Files:",
                              f'{lost} \n browse now in another place \n "note": the missing nodes are already selected')
            self.miss.addItem("Missing Files:")
            self.miss.addItems(lost)
            self.view.clear()
            self.view2.clear()
            self.label.clear()
            self.label.addItem("Path you chose:")
        else:
            QMessageBox.about(self, "done", "done")
            self.label.clear()
            self.label.addItem("Path you chose:")


dlg = App()
dlg.show()
