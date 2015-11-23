__author__ = 'pierregagliardi'
import pandas as pd
import re

def retrieve_title(name):
    m = re.search(', ([A-Za-z ]+).', name)
    return m.group(1)

def numeric_title(title):
    titles={
        ('Ms','Mme', 'Mlle'):0,
        ('Capt', 'Don', 'Major', 'Sir'): 1,
        ('Dona', 'Lady', 'the Countess', 'Jonkheer'): 2,
        ('Col'):3,
        ('Dr'):4,
        ('Master'):5,
        ('Miss'):6,
        ('Mr'):7,
        ('Mrs'):8,
        ('Rev'):9
    }
    for (key,value) in titles.iteritems():
        if title in key:
            return value
            break

def feature_engineering(path):
 # Open up the csv file in to a Python object
 df = pd.read_csv(path, header=0)

 #Gender in numeric
 df['Gender'] = df['Sex'].map( {'female': 0, 'male': 1} ).astype(int)

 #Add column of titles
 df['Title']=df['Name'].map(retrieve_title)

 #Complete missing age values
 titles = df['Title'].unique()
 df['AgeFill'] = df['Age']
 df['FamilySize'] = df['SibSp'] + df['Parch']
 for title in titles:
  print(df[df['Title']==title]['Age'].mean())
  df.loc[ (df.Age.isnull()) & (df.Title == title),'AgeFill'] = df[df['Title']==title]['Age'].mean()

 df.loc[df['Embarked'].isnull(),'Embarked']='C'

 df.loc[ (df.Age.isnull()) & (df.Title == title),'AgeFill'] = df[df['Title']==title]['Age'].mean()
 df['Embarked_numeric'] = df['Embarked'].map( {'C': 0, 'S': 1, 'Q':2} ).astype(int)
 df['Title_numeric'] = df['Title'].map( numeric_title ).astype(int)
 df.loc[:,'AgeFill']=(df['AgeFill']-df['AgeFill'].mean())/df['AgeFill'].std()
 df.loc[:,'Fare']=(df['Fare']-df['Fare'].mean())/df['Fare'].std()
 print(df.head())

 df_survived=df['Survived']
 Y=df_survived.values
 df_numeric= df.drop(['Survived','Name', 'Sex', 'Ticket', 'Cabin', 'Embarked','Title'], axis=1).values
 X=df_numeric
 return (X,Y)
