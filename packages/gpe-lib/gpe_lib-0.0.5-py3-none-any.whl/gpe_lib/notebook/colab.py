# gpe_lib/notebook/colab/__init__.py
# --- IMPORTS ---------------------------------------------------------------
import os
from google.colab import output, files

# --- DECLARATIONS ----------------------------------------------------------

# --- FUNCTIONS -------------------------------------------------------------
def settings():
    import matplotlib.pyplot as plt
    plt.rcParams["figure.figsize"] = (3,3)
    plt.rcParams["legend.title_fontsize"] = "small"
    # output.enable_custom_widget_manager()
    
# --- COMMANDS --------------------------------------------------------------
settings()

# try:
#     os.system("pip install ipympl")
#     import ipympl
# except: pass
