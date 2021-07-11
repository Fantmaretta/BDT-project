from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from filter_evaluation import *
from sklearn.model_selection import train_test_split


# TODO scegliere modello -> predire quantita di pioggia? accuratezza? oppure probabilità che piova? -> qualli variabili usare?
# TODO quale modello usare? regressione? se abbiamo classi? regressione logistca ok solo su due classi

#Logistic Regression / SVC
def regression(X_list_scores, y_list_labels, list_labels_ok):
    '''Given a list of scores of features and a list of labels for the candidates (0/1) as returned by
    calculate_scores_labels method in filter_builder.py, it computes LogisticRegression on them and returns the
    coefficientes of the regression, that represent the weights of the filters (features), old and predicted labels,
    predict_proba'''
    lr = LogisticRegression(solver='lbfgs', max_iter=1000, random_state=42, class_weight='balanced')
    #lr = SVC(kernel='linear')
    lr.fit(np.array(X_list_scores), np.array(y_list_labels))
    predicted_labels = lr.predict(X_list_scores)
    predict_proba = lr.predict_proba(X_list_scores)
    coef = lr.coef_
    print("list scores before", X_list_scores)
    print("list labels before", y_list_labels)
    #print("new predicted labels", predicted_labels)
    #print("coef", lr.coef_)
    print("predict_proba", predict_proba.tolist())
    #print("regression score", lr.score(np.array(list_scores_labels[0]), np.array(list_scores_labels[1])))
    print("regression score y predicted labels / labels ok", lr.score(np.array(X_list_scores), np.array(list_labels_ok)))
    #print("regression score y data /labels ok", lr.score(np.array(predicted_labels), np.array(list_labels_ok)))
    zip_label = list(zip(*[y_list_labels, predicted_labels, list_labels_ok]))
    print("zip labels before, predicted, right", zip_label)
    return [zip_label, coef, predict_proba, predicted_labels]










# With training and test
def regression_1(X_train, y_train, X_test, y_test):
    '''Given a list of scores of features and a list of labels for the candidates (0/1) as returned by
    calculate_scores_labels method in filter_builder.py, it computes LogisticRegression on them and returns the
    coefficientes of the regrssion, that represent the weights of the filters (features)'''
    lr = LogisticRegression(solver='lbfgs', max_iter=1000, random_state=42, class_weight='balanced')
    #lr = SVC(kernel='linear')
    lr.fit(np.array(X_train), np.array(y_train))
    y_pred = lr.predict(X_test)
    print("accuracy score", accuracy_score(y_test, y_pred))
    coef = lr.coef_
    print("X_train", X_train)
    print("y_train", y_train)
    print("X_train", X_test)
    print("y_train", y_test)
    print("coef", lr.coef_)
    print("y_pred", y_pred)
    #print("regression score", lr.score(np.array(list_scores_labels[0]), np.array(list_scores_labels[1])))
    #print("zip labels before and later", list(zip(list_scores_labels[1], predicted_labels)))
    '''lr.fit(np.array(list_scores_labels[0]), np.array(list_scores_labels[1]))
    predicted_labels_2 = lr.predict(list_scores_labels[0])
    print("list scores_2", list_scores_labels[0])
    print("list labels_2", list_scores_labels[1])
    print("coef_2", lr.coef_)
    print("new predicted labels_2", predicted_labels_2)
    print("regression score_2", lr.score(np.array(list_scores_labels[0]), np.array(list_scores_labels[1])))
    print("zip labels before and later_2", list(zip(list_scores_labels[1], predicted_labels_2)))'''
    return coef




#Decision Tree
def regression_2(list_scores_labels):
    '''Given a list of scores of features and a list of labels for the candidates (0/1) as returned by
    calculate_scores_labels method in filter_builder.py, it computes LogisticRegression on them and returns the
    coefficientes of the regrssion, that represent the weights of the filters (features)'''
    lr = DecisionTreeClassifier(random_state=0)
    lr.fit(np.array(list_scores_labels[0]), np.array(list_scores_labels[1]))
    predicted_labels = lr.predict(list_scores_labels[0])
    print("list scores", list_scores_labels[0])
    print("list labels", list_scores_labels[1])
    print("new predicted labels", predicted_labels)
    print("regression score", lr.score(np.array(list_scores_labels[0]), np.array(list_scores_labels[1])))
    print("zip labels before and later", list(zip(list_scores_labels[1], predicted_labels)))
    return 0