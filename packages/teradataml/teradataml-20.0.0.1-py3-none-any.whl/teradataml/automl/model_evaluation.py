# ################################################################## 
# 
# Copyright 2024 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Sweta Shaw
# Email Id: Sweta.Shaw@Teradata.com
# 
# Secondary Owner: Akhil Bisht
# Email Id: AKHIL.BISHT@Teradata.com
# 
# Version: 1.1
# Function Version: 1.0
# ##################################################################

# Python libraries
import time

# Teradata libraries
from teradataml.dataframe.dataframe import DataFrame
from teradataml.automl.model_training import _ModelTraining


class _ModelEvaluator:
    
    def __init__(self, 
                 df=None, 
                 target_column=None, 
                 task_type=None):
        """
        DESCRIPTION:
            Function initializes the data, target column, features and models
            for model evaluation.
         
        PARAMETERS:  
            df:
                Required Argument.
                Specifies the model information.
                Types: teradataml Dataframe
            
            target_column:
                Required Argument.
                Specifies the target column present inside the dataset.
                Types: str
                
            task_type:
                Required Argument.
                Specifies the task type for AutoML, whether to apply regresion OR classification
                on the provived dataset.
                Default Value: "Regression"
                Permitted Values: "Regression", "Classification"
                Types: str

        """
        self.model_info = df
        self.target_column = target_column
        self.task_type = task_type
        
    def model_evaluation(self, rank, table_name_mapping, test_data_ind = False, target_column_ind = False):
        """
        DESCRIPTION:
            Function performs the model evaluation on the specified rank in leaderborad.
         
        PARAMETERS:  
            rank:
                Required Argument.
                Specifies the position of ML model for evaluation.
                Types: int
                        
            table_name_mapping:
                Required Argument.
                Specifies the mapping of train,test table names.
                Types: dict
            
            test_data_ind:
                Optional Argument.
                Specifies whether test data is present or not.
                Default Value: False
                Types: bool
            
            target_column_ind:
                Optional Argument.
                Specifies whether target column is present in the dataset or not.
                Default Value: False
                
        RETURNS:
            tuple containing, performance metrics and predicitions of specified rank ML model.
             
        """
        # Setting test data indicator and target column indicator
        self.test_data_ind = test_data_ind
        self.target_column_ind = target_column_ind
        self.table_name_mapping = table_name_mapping
        
        # Return predictions only if test data is present and target column is not present
        return self._evaluator(rank)

    def _evaluator(self,
                   rank):
        """
        DESCRIPTION:
            Internal Function runs evaluator function for specified rank ML model
            based on regression/classification problem.
         
        PARAMETERS:  
            rank:
                Required Argument.
                Specifies the position(rank) of ML model for evaluation.
                Types: int
                
        RETURNS:
            tuple containing, performance metrics and predictions of ML model.
             
        """
        # Extracting model using rank
        model = self.model_info.loc[rank]
        
        # Defining eval_params 
        eval_params = _ModelTraining._eval_params_generation(model['Name'],
                                                             self.target_column,
                                                             self.task_type)
        
        # Test Data
        test = DataFrame(self.table_name_mapping['{}_test'.format(model['Feature-Selection'])])

        # Getting test data from table
        if not self.test_data_ind:
            # Test Data
            test = DataFrame(self.table_name_mapping['{}_test'.format(model['Feature-Selection'])])
        else:
            test = DataFrame(self.table_name_mapping['{}_new_test'.format(model['Feature-Selection'])])

        print("\nFollowing model is being used for generating prediction :")
        print("Model ID :", model['Model-ID'],
              "\nFeature Selection Method :",model['Feature-Selection'])

        # Evaluation and predictions 
        if model['Name'] == 'knn':
            metrics = model['model-obj'].evaluate(test_data=test)
            pred = model['model-obj'].predict(test_data=test)
        else:
            # Return predictions only if test data is present and target column is not present
            if self.test_data_ind and not self.target_column_ind:
                eval_params.pop("accumulate")
                pred = model['model-obj'].predict(newdata=test, **eval_params)
                return pred
            # Return both metrics and predictions for all other cases
            metrics = model['model-obj'].evaluate(newdata=test, **eval_params)
            pred = model['model-obj'].predict(newdata=test, **eval_params)
        
        return (metrics, pred)