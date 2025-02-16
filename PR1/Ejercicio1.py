import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
#cargando el dataset de diabetes que incorpora sklearn.
diabetes = datasets.load_diabetes()
#usamos solo una caracteristica
diabetes_x = diabetes.data[:,np.newaxis,2]
#dividimos el dato ente entrenamiento y validación o test.
#esto es algo recurrente cuando hacemos aprendizaje máquina.

diabetes_x_train = diabetes_x[:-20] # Todos menos los 20 ultimos.

diabetes_x_test = diabetes_x[-20:] # desde el puesto 10 empezanod por le final hasta el final

# luego cogemos las clases para obtener los valores esperados.
diabetes_y_train = diabetes.target[:-20]
diabetes_y_test = diabetes.target[-20:]

#creamos la regresión lineal:
linearreg = linear_model.LinearRegression()
linearreg.fit(diabetes_x_train, diabetes_y_train)

#Comprobamos la capacidad de predicción
diabetes_y_pred = linearreg.predict(diabetes_x_test)
print("Mostramos los valores obtenidos por la regresión lineal")
print('Coeficientes: \n', linearreg.coef_)
print("MSE: %.2f"
      % mean_squared_error(diabetes_y_test, diabetes_y_pred))
print('R2: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred)) #coeficiente de regresión.
