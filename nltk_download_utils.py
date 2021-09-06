import subprocess
cmd = ["python", "-m", "textblob.download_corpora"]
subprocess.run(cmd,shell=True)
print("Working")
