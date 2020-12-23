# Twomes Analysis Pipeline

## Introduction

The goal of the Twomes Analysis Pipeline is to find a good estimate for the model parameters that cause the building to lose and gain heat. Armed with better insight into the values of these parameters for their home, their heating installations and their comfort desires, home owners may be able to achieve a reduction in ![CO2](https://render.githubusercontent.com/render/math?math=CO_%7B2%7D)-emission more effectively and more efficiently. The analysis pipeline is part of the [TFF project Twomes](https://www.windesheim.nl/onderzoek/lectoraten/energietransitie#accordeon-37345-37346), see the illustration below.

![Twomes Overview](/docs/images/twomes-overview.png)

## Reading guide

This document is built with a topdown structure. It starts with an abstract view of the model and ends with concrete design requirements based on the model equations. Please make yourself familiar with the [terminology](#terminology) used by the model. These terms are used without further explanation throughout the document.

For developers, see the [technical documentation](/docs/technical-documentation.ipynb).

## Inverse grey-box model

A simple inverse grey-box model is used to predict the model parameters of a specific building, its heating installation and the occupants’ comfort needs. Since the measured data is time-based, meaning the output of each timestamp influences the next input, finding model parameters from measured data analytically is hard. Multiple models, varying in complexity, will be published, starting with the simplest model. After a model has proven itself, model parameters may be 'split' into more detailed versions. Using simple, coarse models for inverse grey-box modelling tends to provide a more reliable fit, but provide less detailed information. More complex, refined models may provide more details and insight in, e.g. what to adjust to reduce energy loss, but run the risk of overfitting.

The complete analysis pipeline is shown below, consisting of multiple loops. Each loop is individually described in [loops](#loops).

![Full model](/docs/images/model.png)

### Terminology

- **Measured data** is time series data related to heat balance. It is the monitoring / observed data of all measurement devices combined with the weather data. Two types of measured data are distinguished.
    - **Measured input data** is time series input data for the model. This data can only change over time and is not dependent on model parameters. However, in combination with the model parameters, it influences the calculated data, the output of the model.
    - **Measured comparison data** is the time series multidimensional curve that the output of the model must be fitted to. This data has the same datatype as the calculated output data. It includes data such as indoor temperature and energy usage.
- **Model parameters** are constant parameters that do not change over time. These parameters are unknown. The grey-box model is used inversely to estimate these values by fitting the calculated curve to the measured curve by tweaking these model parameters. Some model parameters can be calculated analytically. Reducing the number of model parameters that must be found using curve-fitting makes fitting the other model parameters easier. These model parameters can be divided into three categories.
	- **Building parameters**, e.g. specific heat loss, thermal inertia, effective thermal mass, effective solar aperture.
	- **Installation parameters**
		- **Installation hardware parameters**, e.g. maximum heating power, net heating system efficiency.
		- **Installation settings parameters**, e.g. heating system supply temperature setting, thermostat program settings.
	- **Comfort needs parameters**, behaviour-related parameters, e.g. home occupancy patterns and desired temperatures when occupants are home.
- **Calculated output data** is the output of the model defined as a time series multidimensional curve. This output must be tweaked by manipulating the model parameters until it optimally fits the curve of the measured comparison data. 

### Loops

The Twomes Analysis Pipeline consists of three primary loops: the inner loop, the fitting loop and the outer loop.

**Inner loop, making a curve**. This loop iterates over short time intervals (*dt*). The model uses recent time series input data and time-independent model parameters to calculate time series output data. Some output is also an input for the next step in this loop, e.g. the indoor temperature is used as output and new input.

![Inner loop](/docs/images/model-inner-loop.png)

**Fitting loop, fitting a curve**. Let the curve-fitting algorithm change the model parameters; after each inner loop, calculate a measure of 'fit' between the curve determined by calculated time series data of the inner loop and the curve determined by the measured times series data.

![Fitting loop](/docs/images/model-fitting-loop.png)

**Outer loop, run model periodically**. Regularly repeat curve fitting to determine changes/trends in model parameters. These may be considered time-independent in the measurement period of the model but in fact, change over time as well. See [Input and model parameters](#Input-and-model-parameters) for more information.

![Outer loop](/docs/images/model-outer-loop.png)

After learning the model parameters, they can be altered to simulate a new outcome to predict the effectiveness of interventions, e.g.:
	
	- Applying a specific insulation method.
	- Changing the installation hardware of the heating system (e.g., replacing a gas-fired boiler by a hybrid heat pump).  
	- Changing the installation settings (e.g. reducing the supply temperature). 
	- Changing comfort needs (e.g. work at home more often or lowering the temperature setting in the morning). 

### Input and model parameters

As mentioned before, model parameters are considered to be time-independent, meaning their values are constant during the inner loop and are adjusted in the fitting loop to fit the curve of the measured comparison data. However, when running the outer loop, the best estimates for the model parameters found may vary gradually over time. Therefore, it is important to choose the right timeframe in the fitting loop. Choose too few measuring points, and the found values will be statistically insignificant. Choose too many, and the found values will be spread out too much because in reality the parameters change gradually over time.

Some model parameters, such as the the thermal inertia of the building, can be calculated analytically. The Twomes Analysis Pipeline must allow for such parameters to be calculated analytically, and thus fixed during curve fitting. The spread of the distribution of all calculations in a given period tells the accuracy of this parameter. If the spread of such parameters is too high, the measurement period may be too large meaning the model parameter may not be reliable.

Lastly, the model must be adaptable to missing input parameters and periods where data is completely missing. Some residences may not have some of the required measurement devices to measure all input data. If so, these measured input parameters must be convertible to a model parameter making it possible to use the same model fitting by tweaking these parameters or simply ignoring them. Normally, these parameters are time-based, but this will no longer be the case for the given period to reduce unnecessary complexity in the model. This concept must also work the other way around, meaning a model parameter must be convertible to a measured time series input for the model (or locked as mentioned in the paragraph above).
