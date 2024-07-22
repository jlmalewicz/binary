import matplotlib.pyplot as plt

mycolors = {'brp': ['blue', 'red', 'purple'],
            'cold': ['#96C3CE', '#82D173', '#4C6663'],
            'warm': ['#EFC11A', '#FF8966', '#63372C'],
            'magma': ['#FF8762', '#862984','#160f3b'],
            'pastel': ['#2B768E', '#1AAD85','#DA674D'],
            'primary': ['#FFBB19', '#E81034','#3209C2']}
ii = 0
fig = plt.figure(figsize=(10, 3), dpi=100)

for key in mycolors:
    plt.vlines(x=[ii,ii+1,ii+2], ymin=0, ymax=1, colors=mycolors[key], linewidth=20)
    plt.text(x=ii+1, y=1.3, s=key, ha='center', va='top')
    ii+=4

plt.axis('off')
plt.ylim(0,1.7)
plt.show()