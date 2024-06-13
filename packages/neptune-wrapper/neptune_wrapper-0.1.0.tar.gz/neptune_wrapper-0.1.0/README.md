<!-- ========================== -->

[![neptune_wrapper CI](https://github.com/bryzgalovdm/neptune_wrapper/actions/workflows/unit-test.yml/badge.svg)](https://github.com/bryzgalovdm/neptune_wrapper/actions/workflows/unit-test.yml)
[![Coverage Status](https://raw.githubusercontent.com/bryzgalovdm/neptune_wrapper/python-coverage-comment-action-data/badge.svg)](https://raw.githubusercontent.com/bryzgalovdm/neptune_wrapper/python-coverage-comment-action-data/badge.svg)
![GitHub contributors](https://img.shields.io/github/contributors/bryzgalovdm/neptune_wrapper)

# Introduction
This is a wrapper for Neptune.AI experiment tracking. It allows to easily log the 
parameters, metrics and results of the ML experiments in a structured way. It is made to
provide OS-independent, more intuitive way to use Neptune.AI tracking in your code.

To be perfectly honest, I use it also as a way to learn how to create a package and
publish it on PyPi.

# Installation
```
pip install neptune-wrapper
```

# Basics of machine learning experiment tracking

When looking for optimal architecture or hyperparameters, very soon you will find 
yourself with dozens of slighly different folders, results and artefacts. To find
the good run or the clue to impromevements becomes very hard. This is where experiment 
tracking comes in handy. It allows you to keep track of all the experiments you run,
and to easily compare them.

## What do we track?
We aim to track as much as possible, namely:
* dataset version
* code version
* environment
* logs
* preprocessing parameters
* hyperparameters
* metrics during training
* results of training
* model_weights
* artefacts (e.g. plots, images, etc.)

## How do we track?
There are several third-party libraries that make the tracking easy. For nearly exhaustive list (2023), 
please this page [here](https://neptune.ai/blog/best-ml-experiment-tracking-tools). We 
use [Neptune.AI](https://neptune.ai/product/experiment-tracking). NeptuneAI has a
wrapper that records the experiments parameters and metrics in a structured way, and
sends them to the NeptuneAI server. The server then allows you to browse the experiments, and to compare them. For full documentation, please see [here](https://docs.neptune.ai/).

## How do I start tracking?
To start tracking, you need to create a NeptuneAI account [here](https://app.neptune.ai/register).
Then, once you are logged in, you can create a new project - name it as you wish.

Voilà! To start logging experiments in your new project, you needed:
* to have an account name (gotten when registered)
* to have a project name (gotten when created a new project)
* to have a token (assigned to you when registered)

To start the tracking in your code, you need to (WARNING: this is not full code but a snippet):
### Tensorflow
```
from neptune_wrapper.wrapper import NeptuneWrapper
from src.networks.net import VanillaNet
from src.tracking.neptune_config import API
...

# Define the parameters
projectName = 'vanillaTest' # Name of the project created in Neptune account
username = 'jdoe'
net = VanillaNet(*params)
neptuneTracker = NeptuneWrapper(projectName=f'{username}/{projectName}', api=API,
                                dataDir='filesToTrack', params=params,
                                sourceFiles=['main.py'])
neptuneTracker.create_run()
neptuneCallback = neptuneTracker.get_tensorflow_keras_callback()

...

# Run the training
net.compile()
history = net.train(trainData, trainLabels, 10, valSplit=0.2,
                           callbacksToAdd=neptuneCallback)
                           
# Log some more things
metricsToTrack = ['loss', 'accuracy', 'val_loss', 'val_accuracy']
for metricName in metricsToTrack:
neptuneTracker.log_parameters(metricName, history.history[metricName],
                              firstLevel='train')
neptuneTracker.stop_run()                                                       
```
### Pytorch
```
from neptune_wrapper import NeptuneTracker
from src.networks.net import VanillaNet
from src.tracking.neptune_config import API

# Define the parameters
projectName = 'vanillaTest' # Name of the project created in Neptune account
username = 'jdoe'
NeptuneTracker = NeptuneWrapper(projectName=f'{username}/{projectName}', api=API,
                                dataDir='filesToTrack', params=params,
                                sourceFiles=['main.py'])
neptuneTracker.create_run()
pytorchLogger = neptuneTracker.get_pytorch_logger(model=net)

net = VanillaNet(*params)
net.to(device)
for epoch in range(nepochs):
    train_loss, n, start = 0.0, 0, time.time()
    for X, y in train_loader:
        X = X.to(device).long()
        y = y.to(device).long()
        X_hat = net(X.float(), y)

        l = net.loss(X.float(), X_hat).to(device)
        optimizer.zero_grad()
        l.backward()
        optimizer.step()

        train_loss += l.cpu().item()
        n += X.shape[0]

    train_loss /= n
    print('epoch %d, train loss %.4f , time %.1f sec'
        % (epoch, train_loss, time.time() - start))
    losses["train_loss"].append(train_loss)

    # Log
    NeptuneTracker.run[pytorchLogger.base_namespace]["training/loss"].append(train_loss)
    
neptuneTracker.stop_run()
```

Experiment will appear in your project web page. You can then browse the experiment and 
compare it with other experiments. You can also download the experiment files, and
reproduce the experiment.

**For full demonstration of Neptune.AI capabilities, please see or run [test_file](../../tests/neptune_wrapper_tests.py).
(Note that this is not a unittest test instance!!!)** 

## Tips
* To avoid entering name of your project and API token every time you run the code,
you can create a file called 'config.py' in `src/tracking` folder and take the info
from there. It could take the following form:
```
API = 'WRkcmVzcyI...'
USER_NAME = user

def get_project_name(project):
    return f'{USER_NAME}/{project}'
```
* If you work at Windows computer, beware of the path length limit (260 characters). Neptune
creates a folder to cache at each run with around 100 characters in the home folder of its
entrypoint. If you have a long path before the entrypoint, you might get an error. To avoid
this, you can place this repo closer to root.
* If synchronization with Neptune servers failed, you can still sync the experiment post-factum.
To do so, you need to run the following command in the folder of your source script (make
sure you are in the virtual environment with neptune):
```
neptune sync
```
Note that this is a shell command, not python command.
