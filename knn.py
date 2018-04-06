import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import random

def distance(p1, p2):
	"""To find the distance between given two points"""
	return np.sqrt(np.sum(np.power(p2 - p1, 2)))

p1 = np.array([2,5])
p2 = np.array([6,4])

#print(distance(p1,p2))

def majority_vote(votes):
	"""Function that returns the majority vote in given sequence. If more than one key have the equal majority then the winner is picked randomly"""
	vote_count = {}
	winners = []
	for vote in votes:
		if vote in vote_count:
			vote_count[vote] += 1
		else:
			vote_count[vote] = 1
			
	max_vote = max(vote_count.values())
	
	for vote, count in vote_count.items():
		if count == max_vote:
			winners.append(vote)
			
	return random.choice(winners)
	
votes = [1,2,3,3,2,1,2,2,3,3]
#print(majority_vote(votes))

def find_nearest_neighbors(p,points,k=5):
	"""Function to find the k nearest neighbors for the given point p among points"""
	distances = np.zeros(points.shape[0])
	for i in range(len(distances)):
		distances[i] = distance(p,points[i])
	ind = np.argsort(distances)
	return ind[:k]

def knn_predict(p,points,outcomes,k=5):
	"""Function to predict and classify the given point p"""
	ind = find_nearest_neighbors(p,points,k)
	return majority_vote(outcomes[ind])
	
points = np.array([[1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]])
p = np.array([1,1])
outcomes = np.array([0,0,0,0,1,1,1,1,1])
#print(knn_predict(p,points,outcomes,k=2)) 
#plt.plot(points[:,0],points[:,1],"ro")
#plt.plot(point[0],point[1],"bo")
#plt.axis([0.5,3.5,0.5,3.5])
#plt.show()

def generate_synth_data(n=50):
	"""Generate observations and outcomes """
	points = np.concatenate((ss.norm(0,1).rvs((n,2)),ss.norm(1,1).rvs((n,2))),axis=0)
	outcomes = np.concatenate((np.repeat(0,n),np.repeat(1,n)))
	return (points,outcomes)
	
n = 20
(points,outcomes) = generate_synth_data(n)
#plt.figure()
#plt.plot(points[:n,0],points[:n,1],"ro")
#plt.plot(points[n:,0],points[n:,1],"bo")
#plt.savefig("bivariate.pdf")

def make_prediction_grid(predictors, outcomes, limits, h, k):
	"""Classify all points in the prediction grid"""
	(x_min, x_max, y_min, y_max) = limits
	xs = np.arange(x_min, x_max, h)
	ys = np.arange(y_min, y_max, h)
	xx, yy = np.meshgrid(xs, ys)
	
	prediction_grid = np.zeros(xx.shape,dtype = int)
	for i,x in enumerate(xs):
		for j,y in enumerate(ys):
			p = np.array([x,y])
			prediction_grid[j,i] = knn_predict(p, predictors, outcomes, k)
	return (xx, yy, prediction_grid)

	
def plot_prediction_grid (xx, yy, prediction_grid, filename):
    """ Plot KNN predictions for every point on the grid."""
    from matplotlib.colors import ListedColormap
    background_colormap = ListedColormap (["hotpink","lightskyblue", "yellowgreen"])
    observation_colormap = ListedColormap (["red","blue","green"])
    plt.figure(figsize =(10,10))
    plt.pcolormesh(xx, yy, prediction_grid, cmap = background_colormap, alpha = 0.5)
    plt.scatter(predictors[:,0], predictors [:,1], c = outcomes, cmap = observation_colormap, s = 50)
    plt.xlabel('Variable 1'); plt.ylabel('Variable 2')
    plt.xticks(()); plt.yticks(())
    plt.xlim (np.min(xx), np.max(xx))
    plt.ylim (np.min(yy), np.max(yy))
    plt.savefig(filename)
	
(predictors,outcomes) = generate_synth_data()
#k=50; limits = (-3,4,-3,4); h= 0.1; filename = "prediction_grid_50"
#(xx, yy, prediction_grid) = make_prediction_grid(predictors, outcomes, limits, h,k)
#plot_prediction_grid(xx, yy, prediction_grid, filename)

from sklearn import datasets
iris = datasets.load_iris()
predictors = iris.data[:,0:2]
outcomes = iris.target
#plt.plot(predictors[outcomes==0][:,0],predictors[outcomes==0][:,1],"ro")
#plt.plot(predictors[outcomes==1][:,0],predictors[outcomes==1][:,1],"go")
#plt.plot(predictors[outcomes==2][:,0],predictors[outcomes==2][:,1],"bo")

#k=5; limits = (4,8,1.5,4.5); h= 0.1; filename = "iris_predict_grid.pdf"
#(xx, yy, prediction_grid) = make_prediction_grid(predictors, outcomes, limits, h,k)
#plot_prediction_grid(xx, yy, prediction_grid, filename)


from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 5)
knn.fit(predictors,outcomes)
sk_predictions = knn.predict(predictors)

my_predictions = np.array([knn_predict(p,predictors,outcomes,5) for p in predictors])

print(100*np.mean(sk_predictions == my_predictions))
print(100*np.mean(sk_predictions == outcomes))
print(100*np.mean(my_predictions == outcomes))