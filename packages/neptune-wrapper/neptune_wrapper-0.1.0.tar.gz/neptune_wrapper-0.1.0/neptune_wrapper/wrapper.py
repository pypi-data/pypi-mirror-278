# Description: Wrapper for Neptune experiment tracking client
# we aim to track the following parameters:
# data version, env, code, hyperameters, preprocessing parameters, metrics,
# results, figures, model_checkpoints
#
# version 1.0.4

import os
import neptune
from .utils import Params

class NeptuneWrapper():

    def __init__(self, projectName=None, api='', dataDir = '', params = None,
                 sourceFiles = ['environment.yml',
                                'requirements.txt',
                                'model.py',
                                'run.py'], **kwargs):
        self.projectName = projectName
        self.api = api
        if os.name == 'posix':
            self.dataDir = str(dataDir)
        elif os.name == 'nt':
            self.dataDir = f'file://{dataDir}'
        self.params = params
        self.sourceFiles = sourceFiles

        for key, value in kwargs.items():
            self.__dict__[key] = value

    def transform_params_in_dict(self):
        def get_non_callable_attributes(object):
            return [a for a in dir(object) if not a.startswith('__')
                    and not callable(getattr(object, a))]

        paramsAttr = get_non_callable_attributes(self.params)
        paramsDict = {a: getattr(self.params, a) for a in paramsAttr}
        return paramsDict

    def create_run(self, mode='async'):
        self.run = neptune.init_run(project=self.projectName, api_token=self.api,
                                    source_files=self.sourceFiles,
                                    capture_hardware_metrics=True,
                                    mode=mode)
        self.run['dataset'].track_files(self.dataDir)
        if self.params is not None:
            if type(self.params) is Params:
                self.run['parameters'] = self.transform_params_in_dict()
            elif type(self.params) is dict:
                self.run['parameters'] = self.params
            else:
                raise TypeError('Params should be either Params or dict')

    def log_parameters(self, paramName, paramValue, firstLevel = ''):
        self.run[f'{firstLevel}/{paramName}'] = paramValue

    def log_artifact(self, fileName, filePath, firstLevel=''):
        self.run[f'{firstLevel}/{fileName}'].upload(filePath)

    def stop_run(self):
        self.run.stop()

    def get_tensorflow_keras_callback(self, level='training'):
        from neptune.integrations.tensorflow_keras import NeptuneCallback
        return NeptuneCallback(run=self.run[level])
    
    def get_pytorch_callback(self, model):
        from neptune_pytorch import NeptuneLogger
        npt_logger = NeptuneLogger(run=self.run,
                                   model=model,
                                   log_freq=1)
        return npt_logger