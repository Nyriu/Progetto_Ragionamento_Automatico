##################################################
# Globali
##################################################
from datetime import timedelta
#MAIN_DIR="./" # TODO mettere in testa ad altri path

# Inputs ####################
INPUT_DIR    = "inputs/"
INPUT_PREFIX = "input_"
INPUT_EXT    = ".in"

INPUT_MZN_DIR    = "inputs_mzn/"
INPUT_MZN_PREFIX = INPUT_PREFIX
INPUT_MZN_EXT    = ".dzn"

INPUT_LP_DIR    = "inputs_lp/"
INPUT_LP_PREFIX = INPUT_PREFIX
INPUT_LP_EXT    = ".lp"

# Outputs ####################
OUTPUT_DIR    = "outputs/"
OUTPUT_PREFIX = "output_"
OUTPUT_EXT    = ".json"

OUTPUT_MZN_DIR    = "outputs_mzn/"
OUTPUT_MZN_PREFIX = OUTPUT_PREFIX
OUTPUT_MZN_EXT    = OUTPUT_EXT

OUTPUT_LP_DIR    = "outputs_lp/"
OUTPUT_LP_PREFIX = OUTPUT_PREFIX
OUTPUT_LP_EXT    = OUTPUT_EXT



# TIMEOUT = timedelta(minutes=5) # TODO
TIMEOUT = timedelta(minutes=2)


# Batches ####################
BATCH_ROOT_DIR   = "batches/"
BATCH_DIR_PREFIX = "batch_"

BATCH_COMPONENTS = [
        ".*[.]mzn",
        ".*[.]lp",
        #INPUT_DIR,
        INPUT_MZN_DIR,
        INPUT_LP_DIR,

        #OUTPUT_DIR,
        OUTPUT_MZN_DIR,
        OUTPUT_LP_DIR,

        ".*[.]png", ".*[.]jpg", ".*[.]jpeg"
        ]



# Pretty print dell'Output
SYMBOLS = {
        "empty"        : "--",
        "malato"       : "-M",
        "malati"       : "MM",
        "positivo"     : "-P",
        "positivi"     : "PP",
        "osservazione" : "-O",
        "quarantena"   : "-Q",
        "quaranteni"   : "QQ"
        }


