import os
import pickle


def run_or_get_pkl(filename, func):
    """
    If the filename is not found, runs the function and saves a pickle to the
    filename ( but this has been commented out for submission)
    :return the output of the function
    """
    if not os.path.isfile(filename):
        # with open(filename, "wb") as file:
        #     mat = func()
        #     # pickle.dump(mat, file, protocol=pickle.HIGHEST_PROTOCOL)
        #     return mat
        return func()
    else:
        return pickle.load(open(filename, "rb"))
