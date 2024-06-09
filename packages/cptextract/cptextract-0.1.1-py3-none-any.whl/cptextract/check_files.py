from cptextract.load_files import CPT_import

def consolidate_class_data(auto_delete):
    """complies class to dictionay and removes duplicate 
    CPT_Import class instances due to the different file extensions in the process.
    ags files takes precedance.

    Parameters
    ----------
    auto_delete : booleon
        true or false

    Returns
    -------
    dict
        a dictionary with key:value pairs of CPT ID and matching CPT_Import class instance
    """
    CPT_unique = set()
    dict2 = {}
    #auto_delete = True
    i_to_delete = []
    for i in range(len(CPT_import.all)):
        
        IDkey = CPT_import.all[i].CPT_ID
        x = CPT_import.all[i]

        if IDkey not in CPT_unique: 
            dict2[IDkey] = x
            CPT_unique.add(IDkey)
        else:
            # the order of perference is ags then xlsx where duplicate files exist
            if x.file_extension == ".ags":
                dict2[IDkey] = x

            else:
                if auto_delete:
                    i_to_delete.append(CPT_import.all[i])
                else:
                    msg = f"\n{x.CPT_ID} {x.file_extension} not imported!"
                    x.add_msg(msg = msg, msg_type = 'e')
                    
                pass

    # removes duplicates
    for j in range(len(i_to_delete)):
        for i in range(len(CPT_import.all)):
            if CPT_import.all[i] == i_to_delete[j]:
                del CPT_import.all[i]
                break

    if len(CPT_import.all) == len(dict2.keys()):
        print(f"{len(i_to_delete)} duplicates removed")   
        print(f"{len(CPT_import.all)} unique CPTs available for import!")
    else:
        print("Duplicates have not been removed. Class instances may not match dictionary")
        #raise Exception("Duplicaates have not been removed. Mismatch number of CPTs available for import")
    
    return dict2