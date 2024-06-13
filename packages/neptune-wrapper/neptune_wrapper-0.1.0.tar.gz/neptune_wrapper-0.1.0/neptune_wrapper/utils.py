import pathlib

# Version 1.0.7
class Params:
    def __init__(self, **kwargs):

        """ Parameters for Keras Implementation of your ANN. Add as many parameters
        as you want as optional keyword arguments.
        They intended to pass in parameters argument of your model class and be
        used like that: model.params.paramName
        I added some parameters as an example:

        chans           : number of channels and time points in the EEG data;
                          default: 8
        wdur            : duration of the analyzed window in seconds; default: 1
        samplingRate    : sampling rate of the EEG data in Hz; default: 250

        """

        for key, value in kwargs.items():
            self.__dict__[key] = value

    def add_parameters(self, **kwargs):

        for key, value in kwargs.items():
            self.__dict__[key] = value


######### AUXILIARY default net class functions #########
def manage_folders(nameModel='defaultnet', dirModel=None, dirLog=None,
                   dirResult=None):
    """ This function creates folders supporting the current instance of the
    model.

    Inputs:

    nameModel       : str, name of the model to be used in the folder name
    dirModel        : path, to save the weights of the model
                        default - 'net_modelX' in the current folder
    dirLogs         : path, path to save the tensorboard log and other logs;
                        default=None
    dirResults:     : path, to save the results; default - 'net_results'
                        in the current folder

    Outputs:

    dirModel        : path, to save the weights of the model
    dirLogs         : path, to save the tensorboard log and other logs
    dirResults:     : path, to save the results
    """

    folders = []
    # Model weights
    dirModel = name_output_folder(folder=dirModel, nameModel=nameModel,
                                  typeFolder='model')
    folders.append(dirModel)
    # Model log
    dirLog = name_output_folder(folder=dirLog, nameModel=nameModel,
                                typeFolder='log')
    folders.append(dirLog)
    # Model results
    dirResult = name_output_folder(folder=dirResult, nameModel=nameModel,
                                   typeFolder='results')
    folders.append(dirResult)

    # Create folders
    for folder in folders:
        if not pathlib.Path(folder).is_dir():
            pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

    return dirModel, dirLog, dirResult


def name_output_folder(folder=None, nameModel='', typeFolder='model'):
    """ This function creates a folder name to save the artefacts of the current
    instance of the model.

    Inputs:

    folder          : path, either to act as a output folder or None to create
                      a new folder matching the name of the model and the type
                      of the artefact
    nameModel       : str, name of the model to be used in the folder name
    typeFolder      : path, type of the artefacts to include in the folder name

    Outputs:

    folderOut       : path, if folder is None, it creates a new folder matching
                      the following pattern 'nameModel_typeFolderX' where X is
                      the number of the folder in the current directory. Otherwise,
                      it returns the folder path.

    """
    curFolder = pathlib.Path().absolute()
    if folder is None:
        searchedPattern = f'{nameModel.lower()}_{typeFolder}'
        if searchedPattern == '_':
            raise ValueError('Please provide a name for the model')
        else:
            if not list(curFolder.glob( f'{searchedPattern}*')):
                folderOut = curFolder.joinpath(searchedPattern)
            else:
                n = find_dir_number(curFolder, searchedPattern) + 1
                folderOut = curFolder.joinpath(f'{searchedPattern}{n}')
    else:
        folderOut = curFolder.joinpath(folder)

    return str(folderOut)

def find_dir_number(path, searchedPattern):
    """ This function finds the folder number in the current directory.
    Searches for the pattern 'searchedPatternX' where X is the number
    of the folder in the current directory and returns the maximum number X.
    Im case of no match, returns 0.

    Inputs:

    folder          : path, where to look for the model folder
    searchedPattern : str, start of the folder name; a number is expected after
                      the pattern in the name of the folder

    Outputs:

    num             : int, maximum number of the folder in the current directory
    """
    if type(path) == str: # compatibility
        path = pathlib.Path(path)

    numbersEncountered = [0] # if no folder is found, return 0
    for filepath in path.glob('*'):
        if filepath.is_dir():
            name = filepath.stem
            if name.startswith(searchedPattern):
                try:
                    numbersEncountered.append(int(name[len(searchedPattern):]))
                except ValueError:
                    if name[len(searchedPattern):] != '':
                        print(f'Not a number detected after the pattern '
                              f'{searchedPattern} during {find_dir_number.__name__}() use')
    return max(numbersEncountered)