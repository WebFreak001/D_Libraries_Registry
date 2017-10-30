import github3
import os
from sys import argv
import hashlib as h

with open('README.md', 'rb') as f:
    original = h.sha1(f.read()).hexdigest()
g = github3.login(argv[1], argv[2])
print(g)
os.system('git pull origin master')
with open('README.md', 'rb') as f:
    # confront shasum because if no modifications in upstream just exit
    new = h.sha1(f.read()).hexdigest()

if new == original and len(argv) == 3:
    print ("no changes")
    exit(0)

excp = {
    'Netflix/vectorflow': 'Vectorflow is a minimalist neural network library optimized for sparse data and single machine environments.',
    'libmir/vectorflow':  'Mir implementation: Vectorflow is a minimalist neural network library optimized for sparse data and single machine environments.'
}

def get_from_exception_list(auth, proj):
    return excp[auth + "/" + proj]

def get_desc_and_update(author, proj):
    print("Updating description for:", author, proj)
    repo = g.repository(author, proj).to_json()
    return repo['description'], repo['pushed_at'][:repo['pushed_at'].find('T')]

with open('README.md', 'r') as f:
    data = f.readlines()

with open('README.md.tmp', 'w') as f:
    for line in data:
        if len(line) > 10 and line[2] == '[' and line[-3] == '|':
            div = '|'
            lastDiv = line.rfind(div)
            penDiv = line.rfind(div, 0, lastDiv)
            tmpLst = line.replace(')', '/').split('/')
            author, proj = tmpLst[3], tmpLst[4]
            # try:
            desc, upd = get_desc_and_update(author, proj)
            # except:
                # continue
            if desc == None:
                desc = get_from_exception_list (author, proj)
            if upd == None:
                upd = "Unknown"
            # print (desc,author, proj)
            lineToWrite = line[:penDiv + 1] + upd + '|' + desc + '\n'
        else:
            lineToWrite = line
        f.write(lineToWrite)

os.system ('mv README.md.tmp README.md')
os.system('git add README.md')
os.system('git commit -m "bot autoupdate"')
os.system('git push origin master')
