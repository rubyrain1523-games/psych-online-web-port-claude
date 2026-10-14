import os, sys, json
root = sys.argv[1]
files, dirs = {}, {}
for dp, dn, fn in os.walk(root):
    rel = os.path.relpath(dp, root).replace('\\', '/')
    rel = '' if rel == '.' else rel
    dirs[rel] = sorted(dn + fn)
    for f in fn:
        p = (rel + '/' + f) if rel else f
        files[p] = os.path.getsize(os.path.join(dp, f))
    for d in dn:
        p = (rel + '/' + d) if rel else d
        dirs.setdefault(p, [])
json.dump({'files': files, 'dirs': dirs}, open(os.path.join(root, 'vfs_manifest.json'), 'w'))
print(len(files), 'files', len(dirs), 'dirs')
