import subprocess
import sys
import setup_util
from os.path import expanduser
import os
import getpass

home = expanduser("~")

def start(args):
  setup_util.replace_text("kelp/app.pl", "localhost", ""+ args.database_host +"")
  setup_util.replace_text("kelp/nginx.conf", "USR", getpass.getuser())
  setup_util.replace_text("kelp/nginx.conf", "server unix:.*\/FrameworkBenchmarks", "server unix:" + home + "/FrameworkBenchmarks")

  try:
    subprocess.Popen("plackup -E production -s Starman --workers=" + str(args.max_threads) + " -l " + home + "/FrameworkBenchmarks/kelp/frameworks-benchmark.sock -a ./app.pl", shell=True, cwd="kelp")
    subprocess.check_call("sudo /usr/local/nginx/sbin/nginx -c " + home + "/FrameworkBenchmarks/kelp/nginx.conf", shell=True)
    return 0
  except subprocess.CalledProcessError:
    return 1
def stop():
  try:
    subprocess.call("sudo /usr/local/nginx/sbin/nginx -s stop", shell=True)
    p = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
      if 'plackup' in line:
        pid = int(line.split(None, 2)[1])
        os.kill(pid, 9)
    return 0
  except subprocess.CalledProcessError:
    return 1
