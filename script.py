import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras import layers, models
from tensorflow.keras.applications import VGG16
from tensorflow.keras.optimizers import Adam

dataset, info = tfds.load('cats_vs_dogs', with_info=True, as_supervised=True)
full_train_dataset = dataset['train']

split = 0.8
train_size = int(split * info.splits['train'].num_examples)
validation_size = info.splits['train'].num_examples - train_size

train_dataset = full_train_dataset.take(train_size)
validation_dataset = full_train_dataset.skip(train_size)

def preprocess(image, label):
    image = tf.image.resize(image, (150, 150))
    image = image / 255.0
    return image, label

train_dataset = train_dataset.map(preprocess).batch(32).prefetch(tf.data.AUTOTUNE)
validation_dataset = validation_dataset.map(preprocess).batch(32).prefetch(tf.data.AUTOTUNE)

base_model = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=0.0001),
    metrics=['accuracy']
)

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=1
)

loss, accuracy = model.evaluate(validation_dataset)
print(f'Loss: {loss}, Accuracy: {accuracy}')

model.save('transfer_learning_cats_vs_dogs.h5')