import librosa
import matplotlib.pyplot as plt
import pandas as pd
import librosa.display
import numpy as np
from PIL import Image
import matplotlib
import tensorflow as tf
import random
import json
from tensorflow.keras.models import model_from_json
import os

### define functions
def detect_barking(path_to_file):
    try:
        y, sr = librosa.load(path_to_file)
        print('File reading was successful')
        #print(type(y))
        #print(type(sr))
    except Exception as e:
        print('Following error occured: \n')
        print(f'{e}')
        return

    matplotlib.use('Agg')
    
    input_wave = pd.DataFrame(y)
    input_wave.reset_index(inplace=True)
    input_wave = input_wave.rename(columns={'index':'t',0:'f'})
    input_wave['t'] = input_wave['t']/sr # --> sr == number of points per second
    input_wave = input_wave.loc[input_wave['t']<=1.000]
    y = input_wave['f'].values

    
    S_full, phase = librosa.magphase(librosa.stft(y))
    fig, ax = plt.subplots(figsize=(16,8))
    img = librosa.display.specshow(librosa.amplitude_to_db(S_full, ref=np.max),y_axis='log',x_axis='time', sr=sr, ax=ax)
    plt.axis('off')
    fig.canvas.draw()

    image = Image.frombytes('RGB', fig.canvas.get_width_height(),fig.canvas.tostring_rgb())
    
    new_image = image.resize((100, 100))
    np_img = np.array([np.array(new_image)])

    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_json_path = os.path.join(current_dir, 'model', 'model.json')
    model_h5_path = os.path.join(current_dir, 'model', 'model.h5')

    # load json and create model
    json_file = open(model_json_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(model_h5_path)

    prediction = loaded_model.predict(np_img)
    prediction = prediction.round()

    if (prediction[0][0] == 1.0) & (prediction[0][1] == 0.0):
        bark = 0
    elif (prediction[0][0] == 0.0) & (prediction[0][1] == 1.0):
        bark = 1
    else:
        bark = -1

    if bark == 1:### TODO: resolve nan cases
        return_stmnt = [{'type':'bark', 'ts':0},
                        {'type':'howl', 'ts':0}]
    else:
        return_stmnt = {}

    return json.dumps(return_stmnt)