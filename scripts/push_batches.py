import os, subprocess
os.chdir('/home/claude/psych-online-web-port-claude'); os.environ['GIT_TERMINAL_PROMPT']='0'
root='PsychOnline-Web/assets'
units=[]
for d in sorted(os.listdir(root)):
    p=os.path.join(root,d)
    if os.path.isdir(p) and d in ('songs','shared'):
        units += [os.path.join(p,x) for x in sorted(os.listdir(p))]
    else: units.append(p)
def size(p):
    if os.path.isfile(p): return os.path.getsize(p)
    return sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk(p) for f in fs)
batches=[];cur=[];cs=0
for u in units:
    s=size(u)
    if cur and cs+s>90e6: batches.append(cur);cur=[];cs=0
    cur.append(u);cs+=s
if cur: batches.append(cur)
for i,b in enumerate(batches):
    subprocess.run(['git','add']+b,check=True)
    subprocess.run(['git','commit','-qm',f'Add web build assets {i+1}/{len(batches)}'],check=True)
    for t in range(3):
        r=subprocess.run(['git','push','origin','main'],capture_output=True,text=True)
        print(i+1,len(batches),r.returncode,r.stderr[-150:],flush=True)
        if r.returncode==0: break
print('DONE',flush=True)
