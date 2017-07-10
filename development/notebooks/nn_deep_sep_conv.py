from keras.layers import Conv2D, Activation, SeparableConvolution2D, BatchNormalization
from keras.layers import Input, Dense, Flatten, Dropout, MaxPooling2D
from keras.models import Model

def model(input_shape=(150,150,3)):
    # Input layer
    inputs = Input(shape=input_shape)

    # Hidden & output layers
    x = Conv2D(32, (3, 3), padding='same')(inputs)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2), padding='same')(x)
    
    x = SeparableConvolution2D(64, (3, 3), padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2), padding='same')(x)

    x = Flatten()(x)
    x = Dropout(0.5)(x)
    x = Dense(128)(x)
    x = Activation('relu')(x)

    predictions = Dense(2, activation='softmax')(x)

    return Model(inputs=inputs, outputs=predictions)