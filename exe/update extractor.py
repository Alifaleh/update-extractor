import os
import easygui
import shutil

welcome='''
#################################################
###---=| welcome to Update-Extractor Beta|=---###
#####---------------------------------------#####
#######-------=| BY:Ali A.Falih |=--------#######
#####---------------------------------------#####
###---=| Email:Alifalih783783@gmail.com |=---####
#################################################
'''

print(welcome)

def get_tree_files(root):
    files_tree_list=[]
    for root, dirs, files in os.walk(root):
        for f in files:
            files_tree_list.append(os.path.join(root, f))
    for i,f in enumerate(files_tree_list):
        files_tree_list[i]=f.split("/")[-1]
    return files_tree_list

def get_tree_folders(root):
    folders_tree_list=[]
    for root, dirs, files in os.walk(root):
        for d in dirs:
            folders_tree_list.append(os.path.join(root, d))
    for i,f in enumerate(folders_tree_list):
        folders_tree_list[i]=f.split("/")[-1]
    return folders_tree_list



def get_roots():
    old_path = easygui.diropenbox(title="Old version folder")
    new_path = easygui.diropenbox(title="New version folder")

    old_path_l = old_path.split("\\")
    old_path = ""
    for p in old_path_l:
        old_path = old_path + p + "/"

    new_path_l = new_path.split("\\")
    new_path = ""
    for p in new_path_l:
        new_path = new_path + p + "/"

    return old_path,new_path


def get_update_info(old_path,new_path):
    print("[+] Scanning files, please wait as it may take\n    a long time based on the file size.\n")
    ofil = get_tree_files(old_path)
    nfil = get_tree_files(new_path)

    ofol = get_tree_folders(old_path)
    nfol = get_tree_folders(new_path)

    folders2add = []
    folders2delete = []
    folders2stay = []
    files2add = []
    files2delete = []
    files2update = []

    for f in nfol:
        if f not in ofol:
            folders2add.append(f)

    print("[+] Folders to add: ("+str(len(folders2add))+").")
    for f in ofol:
        if f not in nfol:
            folders2delete.append(f)
    print("[+] Folders to delete: (" + str(len(folders2delete)) + ").")
    for f in ofol:
        if f in nfol:
            folders2stay.append(f)
    print("[+] Folders to stay: (" + str(len(folders2stay)) + ").")
    for f in nfil:
        if f not in ofil:
            files2add.append(f)
    print("[+] Files to add: (" + str(len(files2add)) + ").")
    for f in ofil:
        if f not in nfil:
            files2delete.append(f)
    print("[+] Files to delete: (" + str(len(files2delete)) + ").")
    files_update_chk_l = []
    for f in nfil:
        if f not in files2add:
            files_update_chk_l.append(f)

    for f in files_update_chk_l:
        file = open(old_path + f, mode="rb")
        of = file.read()
        file.close()
        file = open(new_path + f, mode="rb")
        nf = file.read()
        file.close()
        if of != nf:
            files2update.append(f)
    print("[+] Files to update: (" + str(len(files2update)) + ").\n")
    print("[+] Scan completed successfully.\n")
    return folders2add,folders2delete,folders2stay,files2add,files2delete,files2update

def extract_update(folders2add,folders2delete,folders2stay,files2add,files2delete,files2update):
    print("[+] starting update files extraction.")
    try:
        os.mkdir(os.getcwd() + "/" + old_path.split("/")[-2])
    except:
        pass

    for f in folders2stay:
        try:
            os.mkdir(os.getcwd() + "/" + old_path.split("/")[-2] + "/" + f)
        except:
            pass

    for f in folders2add:
        try:
            os.mkdir(os.getcwd() + "/" + old_path.split("/")[-2] + "/" + f)
        except:
            pass

    for f in files2add:
        try:
            shutil.copyfile(new_path + f, os.getcwd() + "/" + old_path.split("/")[-2] + "/" + f)
        except:
            pass

    for f in files2update:
        try:
            shutil.copyfile(new_path + f, os.getcwd() + "/" + old_path.split("/")[-2] + "/" + f)
        except:
            pass

try:
    old_path,new_path=get_roots()

    folders2add,folders2delete,folders2stay,files2add,files2delete,files2update=get_update_info(old_path,new_path)

    extract_update(folders2add,folders2delete,folders2stay,files2add,files2delete,files2update)
    print("\n[+]Extraction completed successfully.")
    input("\nPress Enter to exit....")
except Exception as e:
    file=open("errors.log","w", encoding="utf8")
    file.write(str(e))
    file.close()
    print("\n[-]Something went wrong.")
    input("Press Enter to exit....")
