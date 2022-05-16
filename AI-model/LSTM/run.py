__author__ = "Jakob Aungiers"
__copyright__ = "Jakob Aungiers 2018"
__version__ = "2.0.0"
__license__ = "MIT"

import os
import json
import time
import math
import matplotlib.pyplot as plt
from core.data_processor import DataLoader
from core.model import Model
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

def plot_results(predicted_data, true_data):
    fig = plt.figure(facecolor='white') 
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data', color = 'black', linewidth= 1.7)
    plt.plot(predicted_data, label='Prediction', color = 'lime', linewidth= 1.7, linestyle='dashdot')
    plt.legend(frameon = False, loc='upper right',fontsize='small')
    plt.show()


def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
	# Pad the list of predictions to shift it in the graph to it's correct start
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
        plt.legend()
    plt.show()


def main():
    configs = json.load(open('config.json', 'rb'))
    if not os.path.exists(configs['model']['save_dir']): os.makedirs(configs['model']['save_dir'])

    data = DataLoader(
        os.path.join('data', configs['data']['filename']),
        configs['data']['train_test_split'],
        configs['data']['columns']
    )
    print(data)
    model = Model()
    model.build_model(configs)
    x, y = data.get_train_data(
        seq_len=configs['data']['sequence_length'],
        normalise=configs['data']['normalise']
    )

    '''
	# in-memory training
    model.train(
		x,
		y,
		epochs = configs['training']['epochs'],
		batch_size = configs['training']['batch_size'],
		save_dir = configs['model']['save_dir']
	)
    '''
    # out-of memory generative training
    steps_per_epoch = math.ceil((data.len_train - configs['data']['sequence_length']) / configs['training']['batch_size'])
    model.train_generator(
        data_gen=data.generate_train_batch(
            seq_len=configs['data']['sequence_length'],
            batch_size=configs['training']['batch_size'],
            normalise=configs['data']['normalise']
        ),
        epochs=configs['training']['epochs'],
        batch_size=configs['training']['batch_size'],
        steps_per_epoch=steps_per_epoch,
        save_dir=configs['model']['save_dir']
    )
    
    x_test, y_test = data.get_test_data(
        seq_len=configs['data']['sequence_length'],
        normalise=configs['data']['normalise']
    )

    #predictions_multiseq = model.predict_sequences_multiple(x_test, configs['data']['sequence_length'], configs['data']['sequence_length'])
    #predictions_fullseq = model.predict_sequence_full(x_test, configs['data']['sequence_length'])
    predictions_t = model.predict_point_by_point(x)
    predictions_pointbypoint = model.predict_point_by_point(x_test)

    print("Mean Absolute Error : " + str(mean_absolute_error(predictions_t, y)))
    print("Mean Squared Error : " + str(mean_squared_error(predictions_t, y)))
    print("RMSE : " + str(mean_squared_error(predictions_t, y)** 0.5))
    print("r2_score : " + str(r2_score(predictions_t, y)))
    
    #plot_results_multiple(predictions_multiseq, y_test, configs['data']['sequence_length'])
    #plot_results(predictions_fullseq, y_test)
    plot_results(predictions_pointbypoint[300:500], y_test[300:500])
    print("Mean Absolute Error : " + str(mean_absolute_error(predictions_pointbypoint, y_test)))
    print("Mean Squared Error : " + str(mean_squared_error(predictions_pointbypoint, y_test)))
    print("RMSE : " + str(mean_squared_error(predictions_pointbypoint, y_test)** 0.5))
    print("r2_score : " + str(r2_score(predictions_pointbypoint, y_test)))


if __name__ == '__main__':
    main()