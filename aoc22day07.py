import warnings

class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.Parent = parent
        self.children = []
        self.totalFileSize = 0 # total size of files contained directly in this directory
        self.size = 0

def addContentsToDirectory(lines, i, dir):
    addContents = True
    if (len(dir.children) > 0 or dir.totalFileSize > 0):
        warnings.warn("Directory already processed.")
        addContents = False
    
    while (i < len(lines) and lines[i][0] != '$'):
        if (not addContents):
            pass
        elif (lines[i][0] == 'd'): # child directory
            childName = lines[i].split()[1]
            dir.children.append(Directory(childName, dir))
        else: # file
            fileSize = int(lines[i].split()[0])
            dir.totalFileSize += fileSize
        i += 1
    
    return i

def buildDirectoryTree(lines):
    root = Directory('/')
    current = root
    i = 1
    while (i < len(lines)):
        line = lines[i].strip()
        if (line == "$ ls"):
            i = addContentsToDirectory(lines, i+1, current) - 1
        elif (line == "$ cd .."):
            current = current.Parent
        elif (line[0:4] == "$ cd"):
            childName = line.split()[2]
            for child in current.children:
                if child.name == childName:
                    current = child
                    break
        else:
            raise Exception("Unexpected command " + line)
        i += 1
    return root

def populateDirSizes(dir):
    dir.size = dir.totalFileSize
    for child in dir.children:
        dir.size += populateDirSizes(child)
    return dir.size

def findDirsOfMaxSize(dirs, rootDir, maxSize):
    if (rootDir.size <= maxSize):
        dirs.append(rootDir)
    for child in rootDir.children:
        findDirsOfMaxSize(dirs, child, maxSize)

def findSmallestDirOfMinSize(rootDir, minSize, currentSmallest=None):
    if (rootDir.size >= minSize):
        if (currentSmallest == None or rootDir.size < currentSmallest.size):
            currentSmallest = rootDir
    for child in rootDir.children:
        currentSmallest = findSmallestDirOfMinSize(child, minSize, currentSmallest)
    return currentSmallest

file = open('day7input.txt', 'r')
lines = file.readlines()
rootDir = buildDirectoryTree(lines)
populateDirSizes(rootDir)
dirs = []
findDirsOfMaxSize(dirs, rootDir, 100000)

print("Part 1 Answer = " + str(sum(d.size for d in dirs)))

unusedSpace = 70000000 - rootDir.size
needSpace = 30000000 - unusedSpace

dir = findSmallestDirOfMinSize(rootDir, needSpace)
print("Part 2 Answer = " + str(dir.size))