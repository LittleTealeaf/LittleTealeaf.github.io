import os, shutil

dir_gen_src = os.path.join('.','src','gen')
dir_gen_public = os.path.join('.','public','gen')


def delete_directory_if_exists(dir):
    if os.path.exists(dir) and os.path.isdir(dir):
        print("Deleted Directory: " + dir)
        shutil.rmtree(dir)

delete_directory_if_exists(dir_gen_public)
delete_directory_if_exists(dir_gen_src)

def resource_src(name):
    "returns the path for a file with the provided name in the src generated directory"
    return os.path.join(dir_gen_src,name)

def resource_public(name):
    "returns the path for a file with the provided name in the public generated directory"
    return os.path.join(dir_gen_public,name)