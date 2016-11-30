import sys, os, time
from subprocess import Popen, list2cmdline
import ConfigParser
scriptDirectory = os.path.dirname(os.path.realpath(__file__))
_confile = "mobi-coop.conf"

# initialize the config parser
conf = ConfigParser.ConfigParser()
confFile = os.path.join(scriptDirectory,_confile)
conf.read(confFile)

repeat = conf.getint("iteration","repeat")

def exec_commands(cmds):
    ''' Exec commands in parallel in multiple process '''
    if not cmds: return # empty list

    def done(p):
        return p.poll() is not None
    def success(p):
        return p.returncode == 0
    def fail():
        sys.exit(1)

    max_task = 8
    processes = []
    while True:
        while cmds and len(processes) < max_task:
            task = cmds.pop()
            print list2cmdline(task)
            processes.append(Popen(task))

        for p in processes:
            if done(p):
                if success(p):
                    processes.remove(p)
                else:
                    fail()

        if not processes and not cmds:
            break
        else:
            time.sleep(0.5)

if __name__ == "__main__":
    commands = []
    for i in xrange(repeat):
        commands.append(['python','main.py',str(i)])

    exec_commands(commands)