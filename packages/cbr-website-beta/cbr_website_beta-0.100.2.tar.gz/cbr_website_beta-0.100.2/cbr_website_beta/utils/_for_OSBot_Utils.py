from osbot_utils.utils.Files import folder_name, parent_folder


def convert_paths_into_folder_dict(data_set):
    def insert_into_dict(d, parts):
        if len(parts) == 1:
            if "files" not in d:
                d["files"] = {}
            d["files"][parts[0]] = None  # Or some default value
        else:
            head, *tail = parts
            if head not in d:
                d[head] = {}
            insert_into_dict(d[head], tail)

    folder_dict = {}

    for item in data_set:
        parts = item.split('/')
        insert_into_dict(folder_dict, parts)

    return folder_dict

def parent_folder_name(target):
    return folder_name(parent_folder(target))