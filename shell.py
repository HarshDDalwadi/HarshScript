import harshScript

while True:
	text = input("harshScript >>> ")
	result, error = harshScript.run('<stdin>', text)
	if error: print(error.as_string())
	else: print(result)