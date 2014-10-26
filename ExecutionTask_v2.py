import subprocess

from javax.swing import SwingWorker, JOptionPane

    
def execute(GUI, command,OutDir,ErrorCollector ):
    GUI.console.append("Executing the command: " +command+"\n")
    GUI.pm.setIndeterminate(True)
    GUI.RunBtn.enabled=False
    p = subprocess.Popen(command,stderr=subprocess.PIPE, shell=True)
    err=p.communicate()
    GUI.console.append(str(err[1]))
    ErrorCollector.append(str(err[1]))
    command_make="cd "+OutDir+" ; make -j30"
    p_make = subprocess.Popen(command_make,stderr=subprocess.PIPE, shell=True)
    err_make=p_make.communicate()
    GUI.console.append(str(err_make[1]))
    ErrorCollector.append(str(err_make[1]))

class Task(SwingWorker):
    def __init__(self,gui,iters,sampleSheet,InputDir,OutputDir,lanes):
        self.gui=gui
        self.iteration=iters
        self.sampleData=sampleSheet
        self.Input=InputDir
        self.Out=OutputDir
        self.laneNum=lanes
        
        print len(self.iteration)
    
    def doInBackground(self):
        
        ErrorCollector=[]
        
        if self.iteration[0]:
            print self.Out
            self.gui.console.append("Running Iteration...01_0M_NY...Creating directories\n")
            OutDir=self.Out+"/01_0M_NY"
            command="perl /usr/local/bin/configureBclToFastq.pl --input-dir "+self.Input+" --output-dir "+OutDir+" --with-failed-reads --sample-sheet "+self.sampleData+" --fastq-cluster-count 0 --tiles s_["+self.laneNum+"]"
            print command
            execute(self.gui, command, OutDir,ErrorCollector)
            
        if self.iteration[1]:
            OutDir=self.Out+"/02_0M_N"
            self.gui.console.append("Running Iteration...02_0M_N...Creating directories\n")
            command="perl /usr/local/bin/configureBclToFastq.pl --input-dir "+self.Input+" --output-dir "+OutDir+" --sample-sheet "+self.sampleData+" --fastq-cluster-count 0 --tiles s_["+self.laneNum+"]"
            print command
            execute(self.gui, command, OutDir,ErrorCollector)
        
        if self.iteration[2]:
            OutDir=self.Out+"/03_1M_NY"
            self.gui.console.append("Running Iteration...03_1M_NY...Creating directories\n")
            command="perl /usr/local/bin/configureBclToFastq.pl --input-dir "+self.Input+" --output-dir "+OutDir+" --mismatches 1 --with-failed-reads --sample-sheet "+self.sampleData+" --fastq-cluster-count 0 --tiles s_["+self.laneNum+"]"
            print command
            execute(self.gui, command, OutDir,ErrorCollector)
            
        if self.iteration[3]:
            OutDir=self.Out+"/04_1M_N"
            self.gui.console.append("Running Iteration...04_1M_N...Creating directories\n")
            command="perl /usr/local/bin/configureBclToFastq.pl --input-dir "+self.Input+" --output-dir "+OutDir+" --mismatches 1 --sample-sheet "+self.sampleData+" --fastq-cluster-count 0 --tiles s_["+self.laneNum+"]"
            print command
            execute(self.gui, command, OutDir,ErrorCollector)
        
        if not ErrorCollector=="":
            JOptionPane.showMessageDialog(self.gui.f,"\n".join(ErrorCollector));
        elif not self.iteration[0] and not self.iteration[1] and not self.iteration[2] and not self.iteration[3]:
            JOptionPane.showMessageDialog(self.gui.f,"Nothing is selected")
        else:
            JOptionPane.showMessageDialog(self.gui.f,"Completed Successfully");
            

    def done(self):
        self.gui.RunBtn.enabled=True
        self.gui.pm.setIndeterminate(False)
        
