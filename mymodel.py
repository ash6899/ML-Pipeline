from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
from keras.datasets import fashion_mnist
from keras.utils import np_utils
import keras
import sys
import os
from keras.utils.vis_utils import plot_model
sys.stdin=open('/root/input.txt','r')
(x_train, y_train), (x_test, y_test)  = fashion_mnist.load_data()
img_rows = x_train[0].shape[0]
img_cols = x_train[1].shape[0]
x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]
num_pixels = x_train.shape[1] * x_train.shape[2]
model = Sequential()
convlayers = int(sys.stdin.readline())
first_layer_nfilter = int(sys.stdin.readline())
first_layer_kernel_size = int(sys.stdin.readline())
first_layer_pool_size = int(sys.stdin.readline())
model.add(Conv2D(first_layer_nfilter, (first_layer_kernel_size, first_layer_kernel_size),
                 padding = "same", 
                 input_shape = input_shape))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size = (first_layer_pool_size, first_layer_pool_size)))
for i in range(1,convlayers):
	nfilters = int(sys.stdin.readline())
	kernel_size = int(sys.stdin.readline())
	pool_size = int(sys.stdin.readline())
	model.add(Conv2D(nfilters, (kernel_size, kernel_size),padding = "same"))
	model.add(Activation("relu"))
	model.add(MaxPooling2D(pool_size = (pool_size, pool_size)))
model.add(Flatten())
fc_input = int(sys.stdin.readline())
for i in range(0,fc_input):
	no_neurons = int(sys.stdin.readline())
	model.add(Dense(no_neurons))
	model.add(Activation("relu"))
model.add(Dense(num_classes))
model.add(Activation("softmax"))
model.compile(loss = 'categorical_crossentropy',
              optimizer = keras.optimizers.Adadelta(),
              metrics = ['accuracy'])
print(model.summary())
batch_size = 64
epochs = 5
history = model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_data=(x_test, y_test),
          shuffle=True)
model.save("/root/fashion-mnist.h5")
scores = model.evaluate(x_test, y_test, verbose=1)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])
accuracy_file = open('/root/accuracy.txt','w')
accuracy_file.write(str(scores[1]))
accuracy_file.close()
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
host_address = "khandelwalyash6899@gmail.com"
host_pass = EMAILPASSWORD
guest_address = "yashkhandelwal2017@gmail.com"
subject = "Regarding Info of your model "
content = '''Hello, 
				Developer this is an email regarding your model.
				Congratulations on your success.
			THANK YOU ...'''+'\n Its accuracy is  '+ str(scores[1])
message = MIMEMultipart()
message['From'] = host_address
message['To'] = guest_address
message['Subject'] = subject
message.attach(MIMEText(content, 'plain'))
session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls()
session.login(host_address, host_pass)
text = message.as_string()
session.sendmail(host_address, guest_address  , text)
session.quit()
print('Successfully sent your mail')
