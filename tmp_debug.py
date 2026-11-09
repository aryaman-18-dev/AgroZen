from pathlib import Path
import time
r=Path('.'); ignored={'.git','.venv','node_modules','__pycache__','instance','logs','tmp'}
t=time.time(); all=list(r.rglob('*')); print('all',len(all),time.time()-t,flush=True)
f=[p for p in all if p.is_file() and not any(part in ignored for part in p.parts) and p.parts[0]!='PROJECT_DOCUMENTATION'];print('f',len(f),time.time()-t,flush=True)
