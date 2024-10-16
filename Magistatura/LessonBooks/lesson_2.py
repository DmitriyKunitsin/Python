import matplotlib.pyplot as plt
from Adaline import AdalineGD

def main():
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,4))
    ada1 = AdalineGD(n_iter=10, 0.01).fit(X,y)

if __name__ == '__main__':
    main()