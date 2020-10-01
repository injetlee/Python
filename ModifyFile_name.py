import os
dir = os.getcwd()
subdir = os.listdir(dir)
for i in subdir:
    path = os.path.join(dir, i)
    if os.path.isdir(path):
        end_dir = os.listdir(path)
        for i in range(len(end_dir)):
            newname = end_dir[i][0:50]
            os.rename(os.path.join(path, end_dir[
                      i]), os.path.join(path, newname))
