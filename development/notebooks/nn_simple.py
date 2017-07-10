from keras.layers import Conv2D, Activation, MaxPooling2D
from keras.layers import Input, Dense, Flatten
from keras.models import Model

def model(input_shape=(150,150,3)):
    # Input layer
    inputs = Input(shape=input_shape)

    # Hidden & output layers
    x = Conv2D(16, (3, 3), padding='same', name='conv1')(inputs)
    x = Activation('relu', name='conv1_act1')(x)
    x = MaxPooling2D(pool_size=(2, 2), padding='same', name='conv1_max')(x)

    x = Flatten(name='flatten')(x)
    x = Dense(32, name='dense1')(x)
    x = Activation('relu', name='dense1_act1')(x)

    predictions = Dense(2, activation='softmax', name='output')(x)

    return Model(inputs=inputs, outputs=predictions)