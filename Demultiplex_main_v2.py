import ExecutionTask_v2 as ET

from java.awt import BorderLayout, GridLayout
from java.lang import Runnable
from javax.swing import JFrame, SwingUtilities, JButton, JFileChooser, JTextArea, \
    JPanel, JTextField, JCheckBox, JScrollPane, JProgressBar


def FolderChooser(JFrame):
    chooseFolder = JFileChooser()
    chooseFolder.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
    chooseFolder.showOpenDialog(JFrame)
    return chooseFolder.selectedFile
        
def FileChooser(JFrame):
    chooseFile = JFileChooser()
    chooseFile.showOpenDialog(JFrame)
    return chooseFile.selectedFile

class DemultiplexGUI(Runnable):

    global SampleSheet
    
    def __init__(self):

        self.f = JFrame("Demultiplex the data")
        self.f.setSize(1250, 1000)
        self.f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        
        #Progress Monitor
        self.pm=JProgressBar(100,100)
        
        #Lane Area
        self.LaneAre=JPanel()
        self.lane1=JCheckBox("Lane 1", True)
        self.lane2=JCheckBox("Lane 2", True)
        self.lane3=JCheckBox("Lane 3", True)
        self.lane4=JCheckBox("Lane 4", True)
        self.lane5=JCheckBox("Lane 5", True)
        self.lane6=JCheckBox("Lane 6", True)
        self.lane7=JCheckBox("Lane 7", True)
        self.lane8=JCheckBox("Lane 8", True)
        self.LaneAre.add(self.lane1)
        self.LaneAre.add(self.lane2)
        self.LaneAre.add(self.lane3)
        self.LaneAre.add(self.lane4)
        self.LaneAre.add(self.lane5)
        self.LaneAre.add(self.lane6)
        self.LaneAre.add(self.lane7)
        self.LaneAre.add(self.lane8)
        
        self.txtArea = JPanel(GridLayout(15,0))
        #self.txtArea.setPreferredSize(Dimension(150, 150))
        self.textAreaForSheet = JTextField(30)
        self.textAreaInputForFolder = JTextField(30)
        self.textAreaOutPutFolder= JTextField(30)
        self.txtArea.add(self.textAreaForSheet)
        self.txtArea.add(self.textAreaInputForFolder)
        self.txtArea.add(self.textAreaOutPutFolder)
        self.txtArea.add(self.LaneAre)
        
        self.buttonArea = JPanel(GridLayout(15,0))
        #self.buttonArea.setPreferredSize(Dimension(150, 150))
        self.sampleSheetBtn = JButton("SampleSheet", actionPerformed=self.onClickSample)
        self.runOutPutFolder = JButton("RUN Folder",actionPerformed=self.onClickRun)
        self.DemultiplexOutPutFolder = JButton("Output Folder",actionPerformed=self.onClickOut)
        self.buttonArea.add(self.sampleSheetBtn)
        self.buttonArea.add(self.runOutPutFolder)
        self.buttonArea.add(self.DemultiplexOutPutFolder)
        
        self.CheckBox = JPanel(GridLayout(15,0))
        #self.buttonArea.setPreferredSize(Dimension(150, 150))
        self.Iter1 = JCheckBox("01_0M_NY", True,)
        self.Iter2 = JCheckBox("02_0M_N", True,)
        self.Iter3 = JCheckBox("03_1M_NY", True,)
        self.Iter4 = JCheckBox("04_1M_N", True,)
        
        self.CheckBox.add(self.Iter1)
        self.CheckBox.add(self.Iter2)
        self.CheckBox.add(self.Iter3)
        self.CheckBox.add(self.Iter4)

        self.ExecutePanel = JPanel()
        self.console=JTextArea(20,100)
        
        self.sp = JScrollPane(self.console);
        self.RunBtn = JButton("Demultiplex",actionPerformed= self.performDemultiplex)
        self.CanBtn = JButton("Cancel",actionPerformed= self.CancelJob)

        self.ExecutePanel.add(self.RunBtn)
        self.ExecutePanel.add(self.CanBtn)
        self.ExecutePanel.add(self.sp, BorderLayout.CENTER)

        self.f.add(self.txtArea, BorderLayout.CENTER)
        self.f.add(self.buttonArea, BorderLayout.WEST)
        self.f.add(self.CheckBox, BorderLayout.EAST)
        self.f.add(self.ExecutePanel, BorderLayout.NORTH)
        self.f.add(self.pm,BorderLayout.SOUTH)
        
    def run(self):
        self.f.setVisible(True)

    def onClickRun(self,event=""):
        self.DirName= FolderChooser(self.f)
        self.textAreaInputForFolder.setText(str(self.DirName))

    def onClickOut(self,event=""):
        self.OutDirName= FolderChooser(self.f)
        self.textAreaOutPutFolder.setText(str(self.OutDirName))
    
    def onClickSample(self,event):
        self.sampleSheet=FileChooser(self.f)
        self.textAreaForSheet.setText(str(self.sampleSheet))
        
    def performDemultiplex(self,event):
        NumberOfIterations=[self.Iter1.selected,self.Iter2.selected,self.Iter3.selected,self.Iter4.selected]
        LaneNumber=[self.lane1.selected,self.lane2.selected,self.lane3.selected,self.lane4.selected,self.lane5.selected,self.lane6.selected,self.lane7.selected,self.lane8.selected]
        selectedLanes = [str(i+1) for i, x in enumerate(LaneNumber) if x==True]
        lanes=','.join(selectedLanes)
        print LaneNumber,selectedLanes,lanes, lanes
        self.task = ET.Task(self,NumberOfIterations,str(self.sampleSheet),str(self.DirName),str(self.OutDirName), lanes)
        self.task.execute()

    def CancelJob(self,event):
        self.task.cancel(True)
        
if __name__ == "__main__":
    SwingUtilities.invokeLater(DemultiplexGUI())

        
        
