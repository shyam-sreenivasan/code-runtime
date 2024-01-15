
import time
import os
import psutil

def timedfunction(func, *args, **kwargs):
    start_time = int(time.time())
    result = func(*args, **kwargs)
    end_time = int(time.time())
    return (end_time - start_time), result

def format_path(path):
    return path.replace("\\", "/")

def get_next_id(i=0):
    while True:
        i += 1
        yield i 

def get_projects(project_root):
    projects = []
    for item in os.listdir(project_root):
        if os.path.isdir(os.path.join(project_root, item)):
            projects.append(item)
    return projects

def get_project_tree(name, parent, ignore_files=None):
    if ignore_files is None:
        ignore_files = []
    id_generator = get_next_id()
    path_map = []
    
    def get_sub_tree(item, parent):
        for igf in ignore_files:
            if igf in item:
                return None
            
        full_path = format_path(os.path.join(parent, item))
        _id = next(id_generator)
        path_map.append({
            "id": _id,
            "path": full_path
        })
        final_item = {
            "id": _id,
            "name": item,
            "isFolder": True,
            "items": []
        }
            
        if os.path.isfile(full_path):
           final_item["isFolder"] = False
           return final_item
        
        items = []
        for _item in os.listdir(full_path):
            sub_tree = get_sub_tree(_item, full_path)
            if sub_tree is not None:
                items.append(sub_tree)
        final_item["items"] = items
        return final_item
    return get_sub_tree(name, parent), path_map

def find_process_by_port(port):
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.info['connections']:
                if conn.status == psutil.CONN_LISTEN and conn.laddr.port == port:
                    return psutil.Process(proc.pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None