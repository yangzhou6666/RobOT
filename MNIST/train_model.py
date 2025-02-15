from tensorflow import keras
import tensorflow as tf
import numpy as np


gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)
        

def Lenet5():
    input_tensor = keras.layers.Input(shape=(28, 28, 1))
    
    x = keras.layers.Convolution2D(6, (5, 5), activation='relu', padding='same', name='block1_conv1')(input_tensor)
    x = keras.layers.MaxPooling2D(pool_size=(2, 2), name='block1_pool1')(x)

    x = keras.layers.Convolution2D(16, (5, 5), activation='relu', padding='same', name='block2_conv1')(x)
    x = keras.layers.MaxPooling2D(pool_size=(2, 2), name='block2_pool1')(x)
    
    x = keras.layers.Flatten(name='flatten')(x)
    x = keras.layers.Dense(120, activation='relu', name='fc1')(x)
    x = keras.layers.Dense(84, activation='relu', name='fc2')(x)
    x = keras.layers.Dense(10, name='before_softmax')(x)
    x = keras.layers.Activation('softmax', name='redictions')(x)
    
    return keras.models.Model(input_tensor, x)


def load_mnist(path="./mnist.npz"):
    f = np.load(path)
    x_train, y_train = f['x_train'], f['y_train']
    x_test, y_test = f['x_test'], f['y_test']
    f.close()

    x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
    x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)

    x_train = x_train.astype('float32') / 255.
    x_test = x_test.astype('float32') / 255.

    y_train = keras.utils.to_categorical(y_train, 10)
    y_test = keras.utils.to_categorical(y_test, 10)
    
    return x_train, x_test, y_train, y_test


path = "./mnist.npz"
x_train, x_test, y_train, y_test = load_mnist(path)


lenet5 = Lenet5()
lenet5.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
lenet5.fit(x_train, y_train, epochs=10, batch_size=64)

lenet5.evaluate(x_test, y_test)

lenet5.save("./Lenet5_mnist.h5")


