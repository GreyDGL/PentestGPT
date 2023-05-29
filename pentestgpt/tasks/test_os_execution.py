# just a trial script to test the os module
import subprocess

# use sqlmap in the terminal

cmd = 'sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --batch --level=5 --risk=3'

# execute the command
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
output_str = ""
while True:
    output = p.stdout.readline()
    if output:
        print(output.decode("utf-8"), end="")
        output_str += output.decode("utf-8")
    if output == b"" and p.poll() is not None:
        print("------end of output------")
        break

print(output_str)
