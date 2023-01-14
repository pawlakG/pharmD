#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
eToxPred: 
Read SMILES data and estimate the SAscorea and Tox-score

@author: Limeng Pu
"""

from __future__ import division

import sys

# add folder contains the modules to the path
sys.path.insert(0,'SAscore') # input the path to the "SAscore" folder here
sys.path.insert(0,'toxicity') # input the path to the "toxicity" folder here

import argparse

import pybel

import pickle
import theano
import numpy as np
from theano.gof import graph
from sa_dbn import DBN

from sklearn.externals import joblib

def argdet():
    if len(sys.argv) == 1:
        print('Need input file!')
        exit()
    if len(sys.argv) == 3:
        args = myargs()
        return args
    if len(sys.argv) == 5:
        args = myargs()
        return args
    else:
        print('Cannot recognize the inputs!')
        exit()

def myargs():
    parser = argparse.ArgumentParser()                                              
    parser.add_argument('--input', '-i', required = True, help = 'input filename')
    parser.add_argument('--output', '-o', required = False, help = 'output filename')
    args = parser.parse_args()
    return args

def write2file(filename, ids, predicted_values, proba):
    ids = np.array(ids)
    ids = np.reshape(ids,(ids.shape[0],1))
    proba = np.reshape(proba,(len(proba),1))
    sa_filename = filename + '_sa.txt'
    sa_data = np.concatenate((ids,predicted_values),axis = 1)
    with open(sa_filename, 'w') as sa_output_file:
        np.savetxt(sa_filename, sa_data, delimiter = ' ', fmt = '%s')
    sa_output_file.close()
    tox_filename = filename + '_tox.txt'
    tox_data = np.concatenate((ids, proba),axis = 1)
    with open(tox_filename, 'w') as tox_output_file:
        np.savetxt(tox_filename, tox_data, delimiter = ' ', fmt = '%s')
    tox_output_file.close()
        
# load the data from a .sdf file
def bits2string(x):
    fp_string = '0'*1024
    fp_list = list(fp_string)
    for item in x:
        fp_list[item-1] = '1'
    fp_string=''.join(reversed(fp_list)) #reverse bit order to match openbabel output
    return fp_string

def load_data(filename):
    fps = []
    ids = []
    for mol in pybel.readfile('smi', filename):
        mol.addh()
        temp_smiles = mol.write('smi')
        smiles = pybel.readstring('smi',temp_smiles)
        mol_id = mol.title
        fp_bits = smiles.calcfp().bits
        fp_string = bits2string(fp_bits)
        # convert the data from string to a numpy matrix
        X = np.array(list(fp_string),dtype=float)
        fps.append(X)
        ids.append(mol_id)
    fps = np.asarray(fps)
    return fps,ids

# define the prediction function
def predict(X_test, sa_model = 'sa_trained_model.pkl', tox_model = 'tox_trained_model.pkl'):
    # load the saved model
    with open(sa_model, 'rb') as in_strm:
        regressor = pickle.load(in_strm)
    in_strm.close()
    y_pred = regressor.linearLayer.y_pred
    # find the input to theano graph
    inputs = graph.inputs([y_pred])
    # select only x
    inputs = [item for item in inputs if item.name == 'x']
    # compile a predictor function
    predict_model = theano.function(
        inputs=inputs,
        outputs=y_pred)
    X_test = X_test.astype(np.float32)
    predicted_values = predict_model(X_test)
    predicted_values = np.asarray(predicted_values)
    predicted_values = np.reshape(predicted_values,(len(predicted_values),1))
    xtree = joblib.load(tox_model)
    proba = xtree.predict_proba(X_test)[:,1]
    print('Prediction done!')
    return predicted_values,proba

if __name__ == "__main__":
    args = argdet()
    X, ids = load_data(args.input)
    predicted_values,proba = predict(X,'SA_trained_model_cpu.pkl','Tox_trained_model.pkl') # if cuda is not installed, use the trained_model_cpu
    write2file(args.output, ids, predicted_values, proba)
