from keras.layers import Input, Dense, Flatten
from keras.models import Model

def model(input_shape=(150,150,3)):
    # Input layer
    inputs = Input(shape=input_shape)

    # Hidden & output layers
    x = Dense(32, activation='relu')(inputs)
    x = Dense(32, activation='relu')(x)
    x = Flatten()(x)
    predictions = Dense(2, activation='softmax')(x)

    return Model(inputs=inputs, outputs=predictions)
   