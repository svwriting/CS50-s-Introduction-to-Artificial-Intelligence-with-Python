import csv
import sys
import calendar

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidences_=[]
    labels_=[]
    with open(filename,mode='r') as csvfile:
        shoppingReader=csv.reader(csvfile)
        for row in shoppingReader:
            evidences_.append(row[:17])
            labels_.append(1 if row[17]=="TRUE" else 0)
    for i in range(1,len(evidences_)):
        evidences_[i][0]=int(evidences_[i][0])
        evidences_[i][1]=float(evidences_[i][1])
        evidences_[i][2]=int(evidences_[i][2])
        evidences_[i][3]=float(evidences_[i][3])
        evidences_[i][4]=int(evidences_[i][4])
        evidences_[i][5]=float(evidences_[i][5])
        evidences_[i][6]=float(evidences_[i][6])
        evidences_[i][7]=float(evidences_[i][7])
        evidences_[i][8]=float(evidences_[i][8])
        evidences_[i][9]=float(evidences_[i][9])
        evidences_[i][10]=list(calendar.month_abbr).index(evidences_[i][10][0:3])-1
        evidences_[i][11]=int(evidences_[i][11])
        evidences_[i][12]=int(evidences_[i][12])
        evidences_[i][13]=int(evidences_[i][13])
        evidences_[i][14]=int(evidences_[i][14])
        evidences_[i][15]=1 if evidences_[i][15]=="Returning_Visitor" else 0
        evidences_[i][16]=1 if evidences_[i][16]=="TRUE" else 0
        #print(evidences_[i])
    evidences_=evidences_[1:]
    labels_=labels_[1:]
    #print(labels_)
    return evidences_,labels_
    raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    return KNeighborsClassifier(1).fit(evidence,labels)
    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positive_c, positive_n=0,0
    negative_c, negative_n=0,0
    for i in range(len(labels)):
        if labels[i]==1:
            if labels[i]==predictions[i]:
                positive_c+=1
            positive_n+=1
        else:
            if labels[i]==predictions[i]:
                negative_c+=1
            negative_n+=1
    #print(positive_c, positive_n,negative_c, negative_n)
    return positive_c/positive_n,negative_c/negative_n
    raise NotImplementedError


if __name__ == "__main__":
    main()
