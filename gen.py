def ph_curve(x):
    return np.exp(-(x-6.5)**2*0.85) + np.exp(-(x-8.5)**2*0.4) + 0.01*(x-7.5)
fig, ax = plt.subplots()
x = np.random.normal(7.5, 3.5, 1000)

data = np.maximum(0,0.1+ph_curve(x) + np.random.normal(0,0.01,len(x)) + ph_curve(x)**2*np.random.normal(0,0.04,len(x))+np.random.normal(0,0.01,len(x))*(x-7.5)**2*0.2)
ax.scatter(x, data, s=2)

np.savetxt("data/ph_data.csv", np.array([x, data]).T, delimiter=",")