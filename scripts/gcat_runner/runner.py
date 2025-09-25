#! /usr/bin/env python

import os
import datetime
import subprocess
import stat

class Runner(object):
    def __init__(self, singularity_script, qsub_option, log_dir, without_sync):
        self.qsub_option = qsub_option
        self.singularity_script = os.path.abspath(singularity_script)
        self.jobname = os.path.basename(self.singularity_script).replace(".sh", "").replace("singularity_", "")
        self.log_dir = log_dir
        self.without_sync = without_sync

    def task_exec(self):
        pass

class Drmaa_runner(Runner):
    def task_exec(self):
        import drmaa
    
        s = drmaa.Session()
        s.initialize()
         
        jt = s.createJobTemplate()
        jt.jobName = self.jobname
        jt.outputPath = ':' + self.log_dir
        jt.errorPath = ':' + self.log_dir
        jt.nativeSpecification = self.qsub_option
        jt.remoteCommand = self.singularity_script
        os.chmod(self.singularity_script, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP)

        returncode = 0
        returnflag = True

        jobid = s.runJob(jt)
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        print ("Your job has been submitted with id: " + jobid + " at Date/Time: " + date)
        if not self.without_sync:
            retval = s.wait(jobid, drmaa.Session.TIMEOUT_WAIT_FOREVER)
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            print ("Job: " + str(retval.jobId) + ' finished with status: ' + str(retval.hasExited) + ' and exit status: ' + str(retval.exitStatus) + " at Date/Time: " + date)
            returncode = retval.exitStatus
            returnflag = retval.hasExited

        s.deleteJobTemplate(jt)
        s.exit()

        if returncode != 0 or not returnflag: 
            raise RuntimeError("Job: " + str(retval.jobId)  + ' failed at Date/Time: ' + date)

class Qsub_runner(Runner):
    def task_exec(self):
        if self.without_sync:
            qsub_commands = ['qsub', '-N', self.jobname]
        else:
            qsub_commands = ['qsub', '-sync', 'yes', '-N', self.jobname]

        #if self.max_task != 0:
        #    qsub_commands.extend(['-t', '1-'+str(self.max_task)+':1'])

        qsub_options = []
        if type(self.qsub_option) == type(""):
            qsub_options += self.qsub_option.split(' ')
            if '' in qsub_options:
                qsub_options.remove('')
        if len(qsub_options) > 0:
            qsub_commands += qsub_options

        returncode = subprocess.call(qsub_commands + [
            "-o", self.log_dir,
            "-e", self.log_dir,
            self.singularity_script
        ])

        if returncode != 0: 
            raise RuntimeError("The batch job failed.")

class Slurm_runner(Runner):
    def task_exec(self):
        if self.without_sync:
            qsub_commands = ['sbatch']
        else:
            qsub_commands = ['sbatch', '--wait']

        qsub_options = []
        if type(self.qsub_option) == type(""):
            qsub_options += self.qsub_option.split(' ')
            if '' in qsub_options:
                qsub_options.remove('')
        if len(qsub_options) > 0:
            qsub_commands += qsub_options

        log_o_path = "%s/%s.o" % (self.log_dir, self.jobname) + "%j"
        log_e_path = "%s/%s.e" % (self.log_dir, self.jobname) + "%j"

        returncode = subprocess.call(qsub_commands + [
            "-o", log_o_path, 
            "-e", log_e_path, 
            "-J", self.jobname,
            self.singularity_script
        ])

        if returncode != 0: 
            raise RuntimeError("The batch job failed.")

class Bash_runner(Runner):
    def task_exec(self):
        bash_commands = ['bash']
        qsub_options = []
        if len(qsub_options) > 0:
            bash_commands = bash_commands + qsub_options

        now = datetime.datetime.now()
        date = now.strftime("%Y%m%d-%H%M%S")
        log_file = "%s/%s.%s" % (self.log_dir, os.path.splitext(os.path.basename(self.singularity_script))[0], date)
        returncode = -1
        with open(log_file, "w") as f:
            returncode = subprocess.call(bash_commands + [
                self.singularity_script
            ], stdout=f, stderr=f)
        if returncode != 0: 
            raise RuntimeError("The batch job failed.")

class Openpbs_runner(Runner):
    def task_exec(self):
        qsub_commands = ['qsub', '-Wblock=true', '-N', self.jobname]

        qsub_options = []
        if type(self.qsub_option) == type(""):
            qsub_options += self.qsub_option.split(' ')
            if '' in qsub_options:
                qsub_options.remove('')
        if len(qsub_options) > 0:
            qsub_commands += qsub_options

        now = datetime.datetime.now()
        date = now.strftime("%Y%m%d-%H%M%S")
        log_o_path = "%s/%s.o%s" % (self.log_dir, self.jobname, date)
        log_e_path = "%s/%s.e%s" % (self.log_dir, self.jobname, date)

        print(" ".join(qsub_commands + [
            "-o", log_o_path,
            "-e", log_e_path,
            self.singularity_script
        ]))
        returncode = subprocess.call(qsub_commands + [
            "-o", log_o_path,
            "-e", log_e_path,
            self.singularity_script
        ])

        if returncode != 0: 
            raise RuntimeError("The batch job failed.")

def main(args):
    import yaml
    conf = yaml.safe_load(open(args.conf))
    if args.interval > 0:
        import time
        import random
        time.sleep(int(args.interval*random.random())) 

    if conf["runner"] == "qsub":
        runner = Qsub_runner(args.script, conf["qsub_option"], conf["log_dir"], args.without_sync)
    elif conf["runner"] == "slurm":
        runner = Slurm_runner(args.script, conf["qsub_option"], conf["log_dir"], args.without_sync)
    elif conf["runner"] == "bash":
        runner = Bash_runner(args.script, conf["qsub_option"], conf["log_dir"], args.without_sync)
    elif conf["runner"] == "openpbs":
        runner = Openpbs_runner(args.script, conf["qsub_option"], conf["log_dir"], args.without_sync)
    else:
        runner = Drmaa_runner(args.script, conf["qsub_option"], conf["log_dir"], args.without_sync)
    runner.task_exec()
