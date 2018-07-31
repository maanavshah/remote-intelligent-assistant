import matplotlib.pyplot as plt

def calc_accuracy():
	print("inside")
	count = 0
	total = 0
	with open("/home/maanav/REIA/src/user.txt", "r") as mssr_file:
		for line in mssr_file:
			print("total"+str(total)+"\n")
			total = total + 1
			print("word :"+line.split(' ', 1)[0])
			if line.split(' ', 1)[0] == "correctly":
				count = count + 1
				print("correct :"+str(count)+"\n") 
		accuracy = (count)/total
		accuracy = accuracy * 100
		print("Accuracy :"+str(accuracy))
		create_chart(count,total)

def create_chart(correct, total):
	labels = 'Correct', 'Incorrect'
	sizes = [correct, total-correct]
	colors = ['green', 'red']
	explode = (0.1, 0)  # explode 1st slice
	# Plot
	plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
	plt.axis('equal')
	plt.show()

print("Specifying accuracy.......")
calc_accuracy()
