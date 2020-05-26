data_file = open('/root/data.txt','r')
input_file = open('/root/input.txt','r')
accuracy_file = open('/root/accuracy.txt','r')

data = data_file.read()
data = data.split('\n')
old_accuracy = float(data[0])		  
layer = int(data[1])		                     
line = int(data[2])		                    
cp_line = line % 3			  
entered_data = int(data[3])		  3

old_data = int(data[4])		 
index_fc = int(data[5])		  
new_accuracy = float(accuracy_file.read()) 			  
inputs = input_file.read()
inputs = inputs.split('\n')
if new_accuracy > old_accuracy and new_accuracy - old_accuracy >= 0.00001 :
	old_accuracy = new_accuracy
	if layer == 1:
		if cp_line == 1:
			entered_data = entered_data * 2
		else :
			entered_data += 1	 
	else :
		entered_data += 100		 
	inputs[line] = str(entered_data)	  							

else:
	
	if layer == 1 :							
		if cp_line == 1 :						

			if entered_data//2 == old_data :

				inputs = inputs[0:line]
				inputs.append('1') 				
				layer = 2					
				index_fc = line    				
				inputs.append('100')				
				old_data = 100			
				entered_data = 100			
				line = line + 1				
				inputs[0] = str(int(inputs[0]) - 1)		
				
				inputs[line] = str(entered_data//2)	
				line = line + 1				
				entered_data = 3			
				old_data = 2				
				inputs[line] = str(entered_data)	
		elif cp_line == 2:

			
			inputs[line] = str(entered_data - 1)		
			line = line + 1				
			entered_data = 3				
			old_data = 2				
			inputs[line] = str(entered_data)	 
		
		elif cp_line == 0:

			inputs[line] = str(entered_data - 1)		
			line = line + 1				
			old_data = int(inputs[line - 3])			
			entered_data = old_data * 2			 
			inputs[0] = str(int(inputs[0]) + 1) 		
			inputs = inputs[0:line]			
			inputs.append(str(entered_data))		
			inputs.append('2')
			inputs.append('2')
			inputs.append('0')
			index_fc = line + 3				
	else:
		

		noOfLayers = int(inputs[index_fc])+1		                  
		inputs[index_fc]=str(noOfLayers)			
		entered_data -= 64					
		old_data = entered_data				
		inputs[line] = str(entered_data)			
		line += 1						
		inputs.append(str(entered_data))			 


data_file.close()
input_file.close()


data_file = open('/root/data.txt','w')
input_file = open('/root/input.txt','w')

data_file_data = str(old_accuracy) + '\n' + str(layer) + '\n' + str(line) + '\n' + str(entered_data) + '\n' + str(old_data) + '\n' + str(index_fc)

data_file.write(data_file_data)						

data_file.close()

input_file_data = '\n'.join(inputs)

input_file.write(input_file_data)					

input_file.close()