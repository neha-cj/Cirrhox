import tensorflow as tf
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load base model
base = DenseNet121(include_top=False, input_shape=(224, 224, 3), weights="imagenet")
x = GlobalAveragePooling2D()(base.output)
output = Dense(1, activation="sigmoid")(x)

model = Model(inputs=base.input, outputs=output)

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_gen = datagen.flow_from_directory(
    "../../datasets/ultrasound/",
    target_size=(224, 224),
    batch_size=16,
    class_mode="binary",
    subset="training"
)

val_gen = datagen.flow_from_directory(
    "../../datasets/ultrasound/",
    target_size=(224, 224),
    batch_size=16,
    class_mode="binary",
    subset="validation"
)

model.fit(train_gen, validation_data=val_gen, epochs=5)

model.save("../models/densenet_model.h5")

print("DenseNet saved!")
