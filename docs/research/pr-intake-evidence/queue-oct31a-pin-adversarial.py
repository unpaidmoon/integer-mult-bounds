import hashlib,json,os,pathlib,subprocess,sys,tempfile
sys.path.insert(0,str(pathlib.Path('scripts').resolve()))
import check_pinned_edits as guard
records=[]
def fixture(root,newline=False):
 root.mkdir();env={**os.environ,'GIT_CONFIG_GLOBAL':os.devnull}
 for args in [('init','-q','-b','main'),('config','user.name','Fixture'),('config','user.email','fixture@example.invalid')]:subprocess.run(['git',*args],cwd=root,env=env,check=True,capture_output=True)
 name='research/pkg/line\nname.txt' if newline else 'research/pkg/a.txt';p=root/name;p.parent.mkdir(parents=True);p.write_bytes(b'old payload\n');(root/'pin.txt').write_text(hashlib.sha256(p.read_bytes()).hexdigest())
 subprocess.run(['git','add','.'],cwd=root,env=env,check=True,capture_output=True);subprocess.run(['git','commit','-qm','base'],cwd=root,env=env,check=True,capture_output=True);subprocess.run(['git','switch','-qc','candidate'],cwd=root,env=env,check=True,capture_output=True)
 return p
with tempfile.TemporaryDirectory() as tmp:
 base=pathlib.Path(tmp)
 for label,newline in [('ordinary_path',False),('newline_path',True)]:
  root=base/label;p=fixture(root,newline);p.write_bytes(b'new payload\n');subprocess.run(['git','add','.'],cwd=root,check=True,capture_output=True);subprocess.run(['git','commit','-qm','edit'],cwd=root,check=True,capture_output=True)
  try:r=guard.check(root,'main','HEAD');records.append(dict(case=label,expected_frozen_stale=1,report=r))
  except Exception as e:records.append(dict(case=label,expected_frozen_stale=1,error=repr(e)))
 root=base/'specified_root';p=fixture(root);p.write_bytes(b'new payload\n');subprocess.run(['git','add','.'],cwd=root,check=True,capture_output=True);subprocess.run(['git','commit','-qm','edit'],cwd=root,check=True,capture_output=True)
 other=base/'other_repo';fixture(other);old=os.environ.get('GIT_DIR');os.environ['GIT_DIR']=str(other/'.git')
 try:r=guard.check(root,'main','HEAD');records.append(dict(case='ambient_GIT_DIR_redirect',expected_frozen_stale=1,report=r))
 finally:
  if old is None:os.environ.pop('GIT_DIR',None)
  else:os.environ['GIT_DIR']=old
assert records[0]['report']['frozen_stale']==1
print(json.dumps(records,indent=2))
