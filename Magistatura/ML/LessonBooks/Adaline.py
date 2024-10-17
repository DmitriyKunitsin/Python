import numpy as np




class AdalineGD (object):
    '''Классификатор на основе адаптивного линейного нейрона
    
    Параметры
    _ _ _ _ _ _ _ _ _ _
    eta : float
        Скорость обучения (между 0.0 и 1.0)
    n_iter : int
        Начальное значение генератора случайных чисел 
        для инициализации случайными весами.

    Атрибуты
    _ _ _ _ _ _ _ _ _ _ 
    w_ : одномерный массив
        Веса после подгонки.
    cost_ : список
        Значение функции издержек на основе суммы квадратов
        в каждой эпохе
    '''
    def __init__(self, eta=0.01, n_iter=50, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state
    def fit(self, X, y):
        '''Подгоняет к обучающим данным
        
        Параметры
        _ _ _ _ _ _ _ _ _ _
        X : (подобен массиву), форма = [n_examples, n_features]
            Обучающие векторы, где n_examples - колличество образцов,
            n_features - колличество признаков.
        y : подобен массиву, форма = [n_examples]
            Целеые значения.

        Возвращает
        _ _ _ _ _ _ _ _ _ _ 
        self : object
        '''
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=1 + X.shape[1])
        self.cost_ = []

        for i in range(self.n_iter):
            net_input = self.net_input(X)
            output = self.activation(net_input)
            errors = (y - output)
            self.w_[1:] += self.eta * X.T.dot(errors)
            self.w_[0] += self.eta * errors.sum()
            cost = (errors**2).sum() / 2.0
            self.cost_.append(cost)
        return self
    
    def net_input(self, X):
        '''Вычисляет общий вход'''
        return np.dot(X, self.w_[1:]) + self.w_[0]
    
    def activation(self, X):
        """Вычисляет линейную активацию""" 
        return X
    def predict(self, X):
        '''Возвращает метку класса после единичного шага'''
        return np.where(self.activation(self.net_input(X)) >= 0.0, 1, -1)
