#!/usr/bin/env python3

import numpy as np
from sklearn import preprocessing, linear_model
from sklearn.metrics import mean_squared_error, r2_score


def main():
    nba_data = np.genfromtxt('training.csv', delimiter=',')

    # Shuffle data to avoid overfitting.
    np.random.shuffle(nba_data)

    nba_X = nba_data[:, 0:-1]
    nba_y = nba_data[:, -1]

    # Standardize X so that mean value is 0 and deviation is 1.
    nba_std_X = preprocessing.scale(nba_X)

    test_size = round(0.05 * len(nba_y))

    # Split the data into training/testing sets
    nba_X_train = nba_std_X[:-test_size]
    nba_X_test = nba_std_X[-test_size:]

    # Split the targets into training/testing sets
    nba_y_train = nba_y[:-test_size]
    nba_y_test = nba_y[-test_size:]

    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(nba_X_train, nba_y_train)

    # Make predictions using the testing set
    nba_y_pred = regr.predict(nba_X_test)

    nba_dummy = nba_X[-test_size:, 0] + nba_X[-test_size:, 14]

    print("Mean squared error: %.2f" % mean_squared_error(nba_y_test, nba_y_pred))
    print("Dummy Mean squared error: %.2f" % mean_squared_error(nba_y_test, nba_dummy))
    print('Variance score: %.2f' % r2_score(nba_y_test, nba_y_pred))


if __name__ == '__main__':
    main()
