import os
import sys
from list_model_exe_path import list_models_path

def set_model() -> None:
    """
    Reads available models, filters out not allowed models, and prompts the user to select a model.
        - Retrieves the list of models using the `list_models_path` variable.
        - Filters out disallowed models specified in a "not_allowed.txt" file located in the "info" folder.
        - Presents the allowed models and provides an option for the user to select one.
        - Saves the chosen model to a "model.txt" file in the "info" folder.

    Args:
        None

    Returns:
        None

    Notes:
        - If no command line argumnets then the default option is selected (index 0).
    """
    
    argv = sys.argv
    models = os.popen(list_models_path)
    
    
    parent_folder = os.path.dirname(os.path.dirname(list_models_path))

   
    info_folder = os.path.join(parent_folder, "info")

  
    not_allowed_models = [str(nmodel) for nmodel in open(os.path.join(info_folder,"not_allowed.txt"),"r").read().strip().split("\n")]
    
    allowed_models = []
    for line in models.read().strip().split("\n"):
       
        if line.strip().split(" ")[0] in not_allowed_models:
            
            continue
        
        allowed_models.append(line.split(" ")[0])
    

    d = {}
    print("Choose model: ")
    for i in range(len(allowed_models)):
        d[i] = allowed_models[i]
        print(f"{i} : {allowed_models[i]}")
   
    
    if len(argv) == 2:
        choose = 0
    else:
        choose = input("choose option: ")
    try:
        choose = int(choose)
        if choose < 0 or choose > max(d.keys()):
            choose = 0
    except Exception:
        choose = d.keys()[0]
    
    with open(os.path.join(info_folder,"model.txt"), "w") as file:
        file.write(allowed_models[choose])

   
if __name__ == "__main__":
    set_model()
