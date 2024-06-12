import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

def load_and_prepare_data():
    data_path = pkg_resources.resource_filename('my_toyota_package', 'data/ToyotaCorolla.csv')
    toyotaCorolla_df = pd.read_csv(data_path).iloc[:1000,:]
    toyotaCorolla_df = toyotaCorolla_df.rename(columns={'Age_08_04': 'Age', 'Quarterly_Tax': 'Tax'})

    predictors = ['Age', 'KM', 'Fuel_Type', 'HP', 'Met_Color', 'Automatic', 'CC', 
                  'Doors', 'Tax', 'Weight']
    outcome = 'Price'

    X = pd.get_dummies(toyotaCorolla_df[predictors], drop_first=True)
    y = toyotaCorolla_df[outcome]

    train_X, valid_X, train_y, valid_y = train_test_split(X, y, test_size=0.4, random_state=1)

    return train_X, valid_X, train_y, valid_y

def optimize_decision_tree(train_X, train_y):
    param_grid = {
        'max_depth': [5, 10, 15, 20, 25], 
        'min_impurity_decrease': [0, 0.001, 0.005, 0.01], 
        'min_samples_split': [10, 20, 30, 40, 50], 
    }
    gridSearch = GridSearchCV(DecisionTreeRegressor(), param_grid, cv=5, n_jobs=-1)
    gridSearch.fit(train_X, train_y)
    return gridSearch.best_params_

def train_decision_tree(train_X, train_y, params):
    regTree = DecisionTreeRegressor(**params)
    regTree.fit(train_X, train_y)
    return regTree

def evaluate_model(model, valid_X, valid_y):
    predictions = model.predict(valid_X)
    mse = mean_squared_error(valid_y, predictions)
    return mse

def main():
    train_X, valid_X, train_y, valid_y = load_and_prepare_data()
    params = optimize_decision_tree(train_X, train_y)
    model = train_decision_tree(train_X, train_y, params)
    mse = evaluate_model(model, valid_X, valid_y)
    print('Mean Squared Error:', mse)

if __name__ == "__main__":
    main()
