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
import json
import numpy as np
from sklearn.metrics import confusion_matrix
import time

# Teradata libraries
from teradataml.dataframe.copy_to import copy_to_sql
from teradataml import ColumnExpression
from teradataml.dataframe.dataframe import DataFrame
from teradataml.utils.validators import _Validators
from teradataml import ROC
from teradataml.common.utils import UtilFuncs
from teradataml.utils.dtypes import _Dtypes
from teradataml.common.utils import UtilFuncs
from teradataml import TeradataMlException
from teradataml.common.messages import Messages, MessageCodes
from teradatasqlalchemy.telemetry.queryband import collect_queryband

# AutoML Internal libraries
from teradataml.automl.data_preparation import _DataPreparation
from teradataml.automl.feature_engineering import _FeatureEngineering
from teradataml.automl.feature_exploration import _FeatureExplore, _is_terminal
from teradataml.automl.model_evaluation import _ModelEvaluator
from teradataml.automl.model_training import _ModelTraining
from teradataml.automl.data_transformation import _DataTransformation
from teradataml.automl.custom_json_utils import _GenerateCustomJson


class AutoML:
    
    def __init__(self,
                 task_type = "Default",
                 include = None,
                 exclude = None,
                 verbose = 0,
                 max_runtime_secs = None,
                 stopping_metric = None, 
                 stopping_tolerance = None,
                 max_models = None,
                 custom_config_file = None):
        """
        DESCRIPTION:
            AutoML (Automated Machine Learning) is an approach that automates the process 
            of building, training, and validating machine learning models. It involves 
            various algorithms to automate various aspects of the machine learning workflow, 
            such as data preparation, feature engineering, model selection, hyperparameter
            tuning, and model deployment. It aims to simplify the process of building 
            machine learning models, by automating some of the more time-consuming 
            and labor-intensive tasks involved in the process.
            
            AutoML is designed to handle both regression and classification (binary and 
            multiclass) tasks. User can specify the task type whether to apply
            regression OR classification algorithm on the provided dataset. By default, AutoML 
            decides the task type.
            
            AutoML by default, trains using all model algorithms applicable for the 
            task type problem. For example, "glm" and "svm" does not support multi-class 
            classification problem. Thus, only 3 models are available to train in case 
            of multi-class classification problem, by default. While for regression and 
            binary classification problem, all 5 models i.e., "glm", "svm", "knn", 
            "decision_forest", "xgboost" are available to train by default.
            
            AutoML provides functionality to use specific model algorithms for training.
            User can provide either include or exclude model. In case of include, 
            only specified models are trained while for exclude, all models except 
            specified model are trained.
            
            AutoML also provides an option to customize the processes within feature
            engineering, data preparation and model training phases. User can customize
            the processes by passing the JSON file path in case of custom run. It also 
            supports early stopping of model training based on stopping metrics,
            maximum running time and maximum models to be trained.
         
        PARAMETERS:  
            task_type:
                Optional Argument.
                Specifies the task type for AutoML, whether to apply regression OR classification
                on the provided dataset. If user wants AutoML to decide the task type automatically, 
                then it should be set to "Default".
                Default Value: "Default"
                Permitted Values: "Regression", "Classification", "Default"
                Types: str
            
            include:
                Optional Argument.
                Specifies the model algorithms to be used for model training phase.
                By default, all 5 models are used for training for regression and binary
                classification problem, while only 3 models are used for multi-class.
                Permitted Values: "glm", "svm", "knn", "decision_forest", "xgboost"
                Types: str OR list of str
                    
            
            exclude:
                Optional Argument.
                Specifies the model algorithms to be excluded from model training phase.
                No model is excluded by default. 
                Permitted Values: "glm", "svm", "knn", "decision_forest", "xgboost"
                Types: str OR list of str
            
            verbose:
                Optional Argument.
                Specifies the detailed execution steps based on verbose level.
                Default Value: 0
                Permitted Values: 
                    * 0: prints the progress bar and leaderboard
                    * 1: prints the execution steps of AutoML.
                    * 2: prints the intermediate data between the execution of each step of AutoML.
                Types: int
                
            max_runtime_secs:
                Optional Argument.
                Specifies the time limit in seconds for model training.
                Types: int
                
            stopping_metric:
                Required, when "stopping_tolerance" is set, otherwise optional.
                Specifies the stopping metrics for stopping tolerance in model training.
                Permitted Values: 
                    * For task_type "Regression": "R2", "MAE", "MSE", "MSLE", 
                                                  "RMSE", "RMSLE"
                    * For task_type "Classification": 'MICRO-F1','MACRO-F1',
                                                      'MICRO-RECALL','MACRO-RECALL',
                                                      'MICRO-PRECISION', 'MACRO-PRECISION',
                                                      'WEIGHTED-PRECISION','WEIGHTED-RECALL',
                                                      'WEIGHTED-F1', 'ACCURACY'
                Types: str

            stopping_tolerance:
                Required, when "stopping_metric" is set, otherwise optional.
                Specifies the stopping tolerance for stopping metrics in model training.
                Types: float
            
            max_models:
                Optional Argument.
                Specifies the maximum number of models to be trained.
                Types: int
                
            custom_config_file:
                Optional Argument.
                Specifies the path of JSON file in case of custom run.
                Types: str
                
        RETURNS:
            Instance of AutoML.
    
        RAISES:
            TeradataMlException, TypeError, ValueError
        
        EXAMPLES:
            # Notes:
            #     1. Get the connection to Vantage to execute the function.
            #     2. One must import the required functions mentioned in
            #        the example from teradataml.
            #     3. Function raises error if not supported on the Vantage
            #        user is connected to.

            # Load the example data.
            >>> load_example_data("GLMPredict", ["admissions_test", "admissions_train"])
            >>> load_example_data("decisionforestpredict", ["housing_train", "housing_test"])
            >>> load_example_data("teradataml", "iris_input")
    
            # Create teradataml DataFrames.
            >>> admissions_train = DataFrame.from_table("admissions_train")
            >>> admissions_test = DataFrame.from_table("admissions_test")
            >>> housing_train = DataFrame.from_table("housing_train")
            >>> housing_test = DataFrame.from_table("housing_test")
            >>> iris_input = DataFrame.from_table("iris_input")
            
            # Example 1: Run AutoML for classification problem.
            # Scenario: Predict whether a student will be admitted to a university
            #           based on different factors. Run AutoML to get the best 
            #           performing model out of available models.
           
            # Create an instance of AutoML.
            >>> automl_obj = AutoML(task_type="Classification")

            # Fit the data.
            >>> automl_obj.fit(admissions_train, "admitted")

            # Run predict with best performing model.
            >>> prediction = automl_obj.predict()
            >>> prediction
            
            # Run predict for new test data with best performing model.
            >>> prediction = automl_obj.predict(admissions_test)
            >>> prediction
            
            # Run predict for new test data with second best performing model.
            >>> prediction = automl_obj.predict(admissions_test, rank=2)
            >>> prediction 

            # Display leaderboard.
            >>> automl_obj.leaderboard()

            # Display best performing model.
            >>> automl_obj.leader()

            # Example 2 : Run AutoML for regression problem.
            # Scenario : Predict the price of house based on different factors.
            #            Run AutoML to get the best performing model using custom
            #            configuration file to customize different processes of
            #            AutoML Run. Use include to specify "xgbooost" and
            #            "decision_forset" models to be used for training.  
            
            # Generate custom JSON file
            >>> AutoML.generate_custom_config("custom_housing")           

            # Create instance of AutoML.
            >>> automl_obj = AutoML(task_type="Regression",
            >>>                     verbose=1,
            >>>                     include=["decision_forest", "xgboost"], 
            >>>                     custom_config_file="custom_housing.json")
            # Fit the data.
            >>> automl_obj.fit(housing_train, "price")

            # Run predict with best performing model.
            >>> prediction = automl_obj.predict()
            >>> prediction
            
            # Run predict for new test data with best performing model.
            >>> prediction = automl_obj.predict(housing_test)
            >>> prediction
            
            # Run predict for new test data with second best performing model.
            >>> prediction = automl_obj.predict(housing_test, rank=2)
            >>> prediction 

            # Display leaderboard.
            >>> automl_obj.leaderboard()
  
            # Display best performing model.
            >>> automl_obj.leader()

            # Example 3 : Run AutoML for multiclass classification problem.
            # Scenario : Predict the species of iris flower based on different
            #            factors. Use custom configuration file to customize 
            #            different processes of AutoML Run to get the best
            #            performing model out of available models.
            
            # Generate custom JSON file
            >>> AutoML.generate_custom_config()

            # Create instance of AutoML.
            >>> automl_obj = AutoML(verbose=2, 
            >>>                     exclude="xgboost",
            >>>                     custom_config_file="custom.json")
            # Fit the data.
            >>> automl_obj.fit(iris_input, iris_input.species)
 
            # Run predict with best performing model.
            >>> prediction = automl_obj.predict()
            >>> prediction

            # Run predict with second best performing model.
            >>> prediction = automl_obj.predict(rank=2)
            >>> prediction

            # Display leaderboard.
            >>> automl_obj.leaderboard()
 
            # Display best performing model.
            >>> automl_obj.leader()
 
            # Example 4 : Run AutoML for regression problem with early stopping metric and tolerance.
            # Scenario : Predict the price of house based on different factors. 
            #            Use custom configuration file to customize different 
            #            processes of AutoML Run. Define performance threshold
            #            to acquire for the available models, and terminate training 
            #            upon meeting the stipulated performance criteria.
            
            # Generate custom JSON file
            >>> AutoML.generate_custom_config("custom_housing")

            # Create instance of AutoML.
            >>> automl_obj = AutoML(verbose=2, 
            >>>                     exclude="xgboost",
            >>>                     stopping_metric="R2",
            >>>                     stopping_tolerance=0.7,
            >>>                     max_models=10,
            >>>                     custom_config_file="custom_housing.json")
            # Fit the data.
            >>> automl_obj.fit(housing_train, "price")
 
            # Run predict with best performing model.
            >>> prediction = automl_obj.predict()
            >>> prediction

            # Display leaderboard.
            >>> automl_obj.leaderboard()

            # Example 5 : Run AutoML for regression problem with maximum runtime.
            # Scenario : Predict the species of iris flower based on different factors.
            #            Run AutoML to get the best performing model in specified time.

            # Create instance of AutoML.
            >>> automl_obj = AutoML(verbose=2, 
            >>>                     exclude="xgboost",
            >>>                     max_runtime_secs=500,
            >>>                     max_models=3)
            # Fit the data.
            >>> automl_obj.fit(iris_input, iris_input.species)
 
            # Run predict with best performing model.
            >>> prediction = automl_obj.predict()
            >>> prediction

            # Run predict with second best performing model.
            >>> prediction = automl_obj.predict(rank=2)
            >>> prediction

            # Display leaderboard.
            >>> automl_obj.leaderboard()
 
            # Display best performing model.
            >>> automl_obj.leader()     
        """
        # Appending arguments to list for validation
        arg_info_matrix = []
        arg_info_matrix.append(["task_type", task_type, True, (str), True, ["Regression", "Classification", "Default"]])
        arg_info_matrix.append(["include", include, True, (str, list), True, ["glm", "svm", "knn", 
                                                                              "decision_forest", "xgboost"]])
        arg_info_matrix.append(["exclude", exclude, True, (str, list), True, ["glm", "svm", "knn", 
                                                                              "decision_forest", "xgboost"]])
        arg_info_matrix.append(["verbose", verbose, True, (int), True, [0,1,2]])
        arg_info_matrix.append(["max_runtime_secs", max_runtime_secs, True, (int, float)])
        arg_info_matrix.append(["stopping_metric", stopping_metric, True, (str), True, ["R2", 'MAE', 
                                                                                        'MSE', 'MSLE',
                                                                                        'RMSE', 'RMSLE',
                                                                                        'MICRO-F1','MACRO-F1',
                                                                                        'MICRO-RECALL','MACRO-RECALL',
                                                                                        'MICRO-PRECISION', 'MACRO-PRECISION',
                                                                                        'WEIGHTED-PRECISION','WEIGHTED-RECALL',
                                                                                        'WEIGHTED-F1', 'ACCURACY']])
        arg_info_matrix.append(["stopping_tolerance", stopping_tolerance, True, (float, int)])
        arg_info_matrix.append(["max_models", max_models, True, (int)])
        arg_info_matrix.append(["custom_config_file", custom_config_file, True, (str), True])
        

        # Validate argument types
        _Validators._validate_function_arguments(arg_info_matrix)
        # Either include or exclude can be used.
        if include is not None or exclude is not None:
            _Validators._validate_mutually_exclusive_arguments(include, "include", exclude, "exclude")
        # Validate mutually inclusive arguments
        _Validators._validate_mutually_inclusive_arguments(stopping_metric, "stopping_metric", stopping_tolerance, "stopping_tolerance")
        # Validate lower range for max_models
        _Validators._validate_argument_range(max_models, "max_models", lbound=1, lbound_inclusive=True)
        
        custom_data = None
        self.auto = True
        # Validate custom file
        if custom_config_file:
            # Performing validation
            _Validators._validate_file_exists(custom_config_file)
            _Validators._validate_file_extension(custom_config_file, "json")
            _Validators._check_empty_file(custom_config_file)
            # Setting auto to False
            self.auto = False
            # Loading file
            with open(custom_config_file, 'r') as json_file:
                custom_data = json.load(json_file)

        # Initializing class variables
        self.data = None
        self.target_column = None
        self.custom_data = custom_data
        self.task_type = task_type
        self.include_model = include
        self.exclude_model = exclude
        self.verbose = verbose
        self.max_runtime_secs = max_runtime_secs
        self.stopping_metric = stopping_metric
        self.stopping_tolerance = stopping_tolerance
        self.max_models = max_models
        self.model_list = ['decision_forest', 'xgboost', 'knn', 'svm', 'glm']
        self.is_classification_type = lambda: self.task_type.upper() == 'CLASSIFICATION'
        self._is_fit_called = False 
        
    @collect_queryband(queryband="AutoML_fit")    
    def fit(self,
            data,
            target_column):
        """
        DESCRIPTION:
            Function triggers the AutoML run. It is designed to handle both 
            regression and classification tasks depending on the specified "task_type".
            
        PARAMETERS:
            data:
                Required Argument.
                Specifies the input teradataml DataFrame.
                Types: teradataml Dataframe
            
            target_column:
                Required Argument.
                Specifies target column of dataset.
                Types: str or ColumnExpression

        RETURNS:
            None

        RAISES:
            TeradataMlException, TypeError, ValueError
            
        EXAMPLES:
            # Create an instance of the AutoML called "automl_obj" 
            # by referring "AutoML() or AutoRegressor() or AutoClassifier()" method.
            # Perform fit() operation on the "automl_obj".

            # Example 1: Passing column expression for target column.
            >>> automl_obj.fit(data = housing_train, target_col = housing_train.price)
                                    
            # Example 2: Passing name of target column.
            >>> automl_obj.fit(data = housing_train, target_col = "price") 
        """

        self._is_fit_called = True
        # Checking if target column is of type ColumnExpression
        if isinstance(target_column, ColumnExpression):
            target_column = target_column.name
        
        # Appending fit arguments to list for validation
        arg_info_fit_matrix = []
        arg_info_fit_matrix.append(["data", data, False, (DataFrame), True])
        arg_info_fit_matrix.append(["target_column", target_column, False, (str), True])

        # Validate argument types
        _Validators._validate_function_arguments(arg_info_fit_matrix)
        
        # Initializing class variables
        self.data = data
        self.target_column = target_column
        
        # Checking if include model list is present
        if self.include_model:
            # Converting to list if passed as string
            self.include_model = UtilFuncs._as_list(self.include_model)
            # Updating model list based on include list
            self.model_list = list(set(self.include_model))
            self.model_list = [model.lower() for model in self.model_list]

        # Checking if exclude model list is present
        if self.exclude_model:
            # Converting to list if passed as string
            self.exclude_model = UtilFuncs._as_list(self.exclude_model)
            # Updating model list based on exclude list
            self.model_list = list(set(self.model_list) - set(self.exclude_model))
            self.model_list = [model.lower() for model in self.model_list]
        
        # Checking if target column is present in data
        _Validators._validate_dataframe_has_argument_columns(self.target_column, "target_column", self.data, "df")
            
        # Handling default task type        
        if self.task_type.casefold() == "default":
            # if target column is having distinct values less than or equal to 20, 
            # then it will be mapped to classification problem else regression problem
            if self.data.drop_duplicate(self.target_column).size <= 20:
                print("\nTask type is set to Classification as target column "
                    "is having distinct values less than or equal to 20.")
                self.task_type = "Classification"
            else:
                print("\nTask type is set to Regression as target column is "
                    "having distinct values greater than 20.")
                self.task_type = "Regression"
        
        if self.is_classification_type():
            if self.stopping_metric is not None:
                permitted_values = ["MICRO-F1", "MACRO-F1", 
                                    "MICRO-RECALL", "MACRO-RECALL",
                                    "MICRO-PRECISION", "MACRO-PRECISION", 
                                    "WEIGHTED-PRECISION", "WEIGHTED-RECALL", 
                                    "WEIGHTED-F1", "ACCURACY"]
                _Validators._validate_permitted_values(self.stopping_metric, permitted_values, "stopping_metric")
        else:
            if self.stopping_metric is not None:
                permitted_values = ["R2", 'MAE', 'MSE', 'MSLE','RMSE', 'RMSLE']
                _Validators._validate_permitted_values(self.stopping_metric, permitted_values, "stopping_metric")

        if not self.is_classification_type():
            _Validators._validate_column_type(self.data, self.target_column, 'target_column', 
                                              expected_types=UtilFuncs()._get_numeric_datatypes())
        
        # Displaying received custom input
        if self.custom_data:
            print("\nReceived below input for customization : ")
            print(json.dumps(self.custom_data, indent=4))
        
        # Classification probelm
        task_cls = _Classification
        cls_method = "_classification"
        
        # Regression problem
        if self.task_type.casefold() == "regression":
            task_cls = _Regression
            cls_method = "_regression"

        # Running AutoML
        clf = task_cls(self.data, self.target_column, self.custom_data)
        
        self.model_info, self.leader_board, self.target_count, self.target_label, \
            self.data_transformation_params, self.table_name_mapping = getattr(clf, cls_method)(    
                                                                    model_list = self.model_list,
                                                                    auto = self.auto,
                                                                    verbose = self.verbose,
                                                                    max_runtime_secs = self.max_runtime_secs, 
                                                                    stopping_metric = self.stopping_metric, 
                                                                    stopping_tolerance = self.stopping_tolerance,
                                                                    max_models = self.max_models)

        # Model Evaluation Phase
        self.m_evaluator = _ModelEvaluator(self.model_info, 
                                           self.target_column,
                                           self.task_type)
      
    @collect_queryband(queryband="AutoML_predict")  
    def predict(self,
                data = None,
                rank = 1):
        """
        DESCRIPTION:
            Function generates prediction on either default test data or any other data 
            using model rank in leaderboard and displays performance metrics 
            of the specified model.
            
            If test data contains target column, then it displays both prediction 
            and performance metrics, otherwise displays only prediction.

        PARAMETERS:
            data:
                Optional Argument.
                Specifies the dataset on which prediction and performance
                metrices needs to be generated using model rank in leaderboard.
                When "data" is not specified default test data is used. Default 
                test data is the dataset generated at the time of training.
                Types: teradataml DataFrame

            rank:
                Optional Argument.
                Specifies the rank of the model in the leaderboard to be used for prediction.
                Default Value: 1
                Types: int
                
        RETURNS:
            Pandas DataFrame with predictions.

        RAISES:
            TeradataMlException, TypeError, ValueError

        EXAMPLES:
            # Create an instance of the AutoML called "automl_obj" 
            # by referring "AutoML() or AutoRegressor() or AutoClassifier()" method.
            # Perform fit() operation on the "automl_obj".
            # Perform predict() operation on the "automl_obj".
            
            # Example 1: Run predict with best performing model.
            >>> prediction = automl_obj.predict()
            >>> prediction
            
            # Example 2: Run predict with second best performing model.
            >>> prediction = automl_obj.predict(rank=2)
            >>> prediction
            
            # Example 3: Run predict for new test data with best performing model.
            >>> prediction = automl_obj.predict(admissions_test)
            >>> prediction
            
            # Example 4: Run predict for new test data with second best performing model.
            >>> prediction = automl_obj.predict(admissions_test, rank=2)
            >>> prediction
        """
        if not self._is_fit_called:
            # raise ValueError("fit() method must be called before generating prediction.")
            err = Messages.get_message(MessageCodes.FUNC_EXECUTION_FAILED,
                                       "'predict' method", \
                                       "'fit' method must be called before" \
                                       " running predict.")
            raise TeradataMlException(err, MessageCodes.EXECUTION_FAILED)
        # Appending predict arguments to list for validation.
        arg_info_pred_matrix = []
        arg_info_pred_matrix.append(["data", data, True, (DataFrame), True])
        arg_info_pred_matrix.append(["rank", rank, True, (int), True])

        # Validate argument types
        _Validators._validate_function_arguments(arg_info_pred_matrix)
        # Validate range for model rank
        _Validators._validate_argument_range(rank, "rank", lbound=1, 
                                             ubound=self.leader_board.Rank.max(),
                                             lbound_inclusive=True, ubound_inclusive=True)
        
        # Setting test data indicator to default value, i.e., False.
        self.test_data_ind = False
        # Setting target column indicator to default value, i.e., False.
        self.target_column_ind = False
        # Model Evaluation using rank-1 [rank starts from 0 in leaderboard]
        rank = rank-1
        
        # Checking if there is test data provided or not.
        # If no, then model will generate predicion on default test data.
        # If yes, then at first data transformation will happen then prediction will be generated.
        if data is None:
            metrics, pred = self.m_evaluator.model_evaluation(rank = rank,
                                                              table_name_mapping=self.table_name_mapping)
        else:
            # Setting test data indicator to True
            self.test_data_ind = True
            # Setting indicator to True if target column exists
            if self.target_column in data.columns:
                self.target_column_ind = True
        
            # Data Transformation Phase
            data_transform_instance = _DataTransformation(data = data,
                                                          data_transformation_params = \
                                                          self.data_transformation_params,
                                                          auto = self.auto,
                                                          verbose = self.verbose,
                                                          target_column_ind = self.target_column_ind,
                                                          table_name_mapping=self.table_name_mapping)
            
            self.table_name_mapping = data_transform_instance.data_transformation()
            
            # Checking for target column presence in passed test data.
            # If present, then both prediction and evaluation metrics will be generated.
            # If not present, then only prediction will be generated.
            if self.target_column_ind:
                metrics, pred = self.m_evaluator.model_evaluation(rank = rank, 
                                                                  test_data_ind = \
                                                                  self.test_data_ind, 
                                                                  target_column_ind = \
                                                                  self.target_column_ind,
                                                                  table_name_mapping=self.table_name_mapping)
            else:
                pred = self.m_evaluator.model_evaluation(rank = rank,
                                                         test_data_ind = \
                                                         self.test_data_ind,
                                                         table_name_mapping=self.table_name_mapping)
        # Checking if problem type is classification and target label is present.
        if self.is_classification_type() and self.target_label is not None:
            # Displaying target column labels
            tar_dct = {}
            print('\nTarget Column Mapping:')
            # Iterating rows
            for row in self.target_label.result.itertuples():
                # Retrieving the category names of encoded target column
                # row[1] contains the orginal name of cateogry
                # row[2] contains the encoded value
                if row[1] != 'TD_CATEGORY_COUNT':
                    tar_dct[row[1]] = row[2]
                    
            for key, value in tar_dct.items():
                print(f"{key}: {value}")
            
        print("\nPrediction : ")
        print(pred.result)
        
        # Showing performance metrics if there is no test data
        # Or if target column is present in test data.
        if not self.test_data_ind or self.target_column_ind:
            print("\nPerformance Metrics : ")
            print(metrics.result)
        
            prediction_column = 'prediction' if 'prediction' in pred.result.columns else 'Prediction'

            # Displaying confusion matrix and ROC-AUC for classification problem
            if self.is_classification_type():
                print_data = lambda data: print(data) if _is_terminal() else display(data)
                # Displaying ROC-AUC for binary classification
                if self.target_count == 2:
                    fit_params = {
                        "probability_column" : prediction_column,
                        "observation_column" : self.target_column,
                        "positive_class" : "1",
                        "data" : pred.result
                    }
                    # Fitting ROC
                    roc_out = ROC(**fit_params)
                    print("\nROC-AUC : ")
                    print_data(roc_out.result)
                    print_data(roc_out.output_data)
                
                # Displaying confusion matrix for binary and multiclass classification
                prediction_df=pred.result.to_pandas()
                target_col = self.target_column
                print("\nConfusion Matrix : ")
                print_data(confusion_matrix(prediction_df[target_col], prediction_df[prediction_column]))
                
        # Returning prediction
        return pred.result    
    
    @collect_queryband(queryband="AutoML_leaderboard")
    def leaderboard(self):
        """
        DESCRIPTION:
            Function displays leaderboard.

        RETURNS:
            Pandas DataFrame with Leaderboard information.

        RAISES:
            TeradataMlException.

        EXAMPLES:
            # Create an instance of the AutoML called "automl_obj" 
            # by referring "AutoML() or AutoRegressor() or AutoClassifier()" method.
            # Perform fit() operation on the "automl_obj".
            # Generate leaderboard using leaderboard() method on "automl_obj".
            >>> automl_obj.leaderboard()
        """
        if not self._is_fit_called:
            # raise ValueError("fit() method must be called before generating leaderboard.")
            err = Messages.get_message(MessageCodes.FUNC_EXECUTION_FAILED,
                                       "'leaderboard' method", \
                                       "'fit' method must be called before" \
                                       " generating leaderboard.")
            raise TeradataMlException(err, MessageCodes.EXECUTION_FAILED)
        return self.leader_board
        
    @collect_queryband(queryband="AutoML_leader")    
    def leader(self):
        """
        DESCRIPTION:
            Function displays best performing model.
            
        RETURNS:
            None

        RAISES:
            TeradataMlException.

        EXAMPLES:
            # Create an instance of the AutoML called "automl_obj" 
            # by referring "AutoML() or AutoRegressor() or AutoClassifier()" method.
            # Perform fit() operation on the "automl_obj".
            # Generate leaderboard using leaderboard() method on "automl_obj".
            # Display best performing model using leader() method on "automl_obj".
            >>> automl_obj.leader()   
        """
        if not self._is_fit_called:
            # raise ValueError("fit() method must be called before generating leader.")
            err = Messages.get_message(MessageCodes.FUNC_EXECUTION_FAILED,
                                       "'leader' method", \
                                       "'fit' method must be called before" \
                                       " generating leader.")
            raise TeradataMlException(err, MessageCodes.EXECUTION_FAILED)
        record = self.leader_board
        if not _is_terminal():
            display(record[record['Rank'] == 1])
        else:
            print(record[record['Rank'] == 1])
    
    @staticmethod
    def generate_custom_config(file_name = "custom"):
        """
        DESCRIPTION:
            Function generates custom JSON file containing user customized input under current 
            working directory which can be used for AutoML execution.
        
        PARAMETERS:
            file_name:
                Optional Argument.
                Specifies the name of the file to be generated. Do not pass the file name
                with extension. Extension '.json' is automatically added to specified file name.
                Default Value: "custom"
                Types: str
        
        RETURNS:
            None 
        
        EXAMPLES:
            # Import either of AutoML or AutoClassifier or AutoRegressor from teradataml.
            # As per requirement, generate json file using generate_custom_config() method.
            
            # Generate a default file named "custom.json" file using either of below options.
            >>> AutoML.generate_custom_config()
            or
            >>> AutoClassifier.generate_custom_config()
            or 
            >>> AutoRegressor.generate_custom_config()
            # The above code will generate "custom.json" file under the current working directory.
            
            # Generate different file name using "file_name" argument.
            >>> AutoML.generate_custom_config("titanic_custom")
            or
            >>> AutoClassifier.generate_custom_config("titanic_custom")
            or
            >>> AutoRegressor.generate_custom_config("housing_custom")
            # The above code will generate "titanic_custom.json" file under the current working directory.
                
        """
        # Intializing class
        generator = _GenerateCustomJson()
        # Generating custom JSON data
        data = generator._generate_custom_json()
        # Converting to JSON
        custom_json = json.dumps(data, indent=4)
        # Save JSON data to the specified file
        json_file = f"{file_name}.json"
        with open(json_file, 'w') as file:
            file.write(custom_json)
        print(f"\n'{json_file}' file is generated successfully under the current working directory.")


class _Regression(_FeatureExplore, _FeatureEngineering, _DataPreparation, _ModelTraining):
  
    def __init__(self, 
                 data, 
                 target_column,
                 custom_data = None):
        """
        DESCRIPTION:
            Function initializes the data, target column for Regression.
         
        PARAMETERS:  
            data:
                Required Argument.
                Specifies the input teradataml Dataframe.
                Types: teradataml Dataframe
            
            target_column:
                Required Argument.
                Specifies the name of the target column in "data".
                Types: str
            
            custom_data:
                Optional Argument.
                Specifies json object containing user customized input.
                Types: json object
        """
        self.data = data
        self.target_column = target_column
        self.custom_data = custom_data
        
        
    def _regression(self,
                    model_list = None, 
                    auto = False,
                    verbose = 0,
                    max_runtime_secs = None,
                    stopping_metric = None, 
                    stopping_tolerance = None,
                    max_models = None):
        """
        DESCRIPTION:
            Interal Function runs Regression.
         
        PARAMETERS:  
            auto:
                Optional Argument.
                Specifies whether to run AutoML in custom mode or auto mode.
                When set to False, runs in custom mode. Otherwise, by default runs in auto mode.
                Types: bool
                
            verbose:
                Optional Argument.
                Specifies the detailed execution steps based on verbose level.
                Default Value: 0
                Permitted Values: 
                    * 0: prints the progress bar and leaderboard
                    * 1: prints the execution steps of AutoML.
                    * 2: prints the intermediate data between the execution of each step of AutoML.
                Types: int
                
            max_runtime_secs:
                Optional Argument.
                Specifies the time limit in seconds for model training.
                Types: int
                
            stopping_metric:
                Required, when "stopping_tolerance" is set, otherwise optional.
                Specifies the stopping mertics for stopping tolerance in model training.
                Types: str

            stopping_tolerance:
                Required, when "stopping_metric" is set, otherwise optional.
                Specifies the stopping tolerance for stopping metrics in model training.
                Types: float
            
            max_models:
                Optional Argument.
                Specifies the maximum number of models to be trained.
                Types: int
        
        RETURNS:
            a tuple containing, model information and leaderboard.   
        """
        # Feature Exploration Phase
        _FeatureExplore.__init__(self, 
                                 data = self.data, 
                                 target_column = self.target_column,
                                 verbose=verbose)
        if verbose > 0:
            self._exploration()
        # Feature Engineering Phase
        _FeatureEngineering.__init__(self, 
                                     data = self.data, 
                                     target_column = self.target_column,
                                     model_list = model_list,
                                     verbose = verbose,
                                     custom_data = self.custom_data)
        # Start time
        start_time = time.time()
        data, excluded_columns, target_label, data_transformation_params = self.feature_engineering(auto)
        
        # Data preparation Phase
        _DataPreparation.__init__(self, 
                                  data = self.data, 
                                  target_column = self.target_column, 
                                  verbose = verbose,
                                  excluded_columns = excluded_columns,
                                  custom_data = self.custom_data,
                                  data_transform_dict = data_transformation_params)
        features, data_transformation_params = self.data_preparation(auto)

        # Calculating max_runtime_secs for model training by,
        # subtracting the time taken for feature engineering and data preparation
        max_runtime_secs = max_runtime_secs - (time.time() - start_time) \
                                if max_runtime_secs is not None else None
        
        # Setting max_runtime_secs to 60 seconds if it is less than 0
        max_runtime_secs = 60 if max_runtime_secs is not None and \
                                            max_runtime_secs < 0 else max_runtime_secs
        
        # Model Training
        _ModelTraining.__init__(self, 
                                data = self.data, 
                                target_column = self.target_column,
                                model_list = model_list, 
                                verbose = verbose,
                                features = features,
                                task_type = "Regression",
                                custom_data = self.custom_data)
        models_info, leaderboard, target_count = self.model_training(auto = auto,
                                                        max_runtime_secs = max_runtime_secs, 
                                                        stopping_metric = stopping_metric, 
                                                        stopping_tolerance = stopping_tolerance,
                                                        max_models = max_models)

        return (models_info, leaderboard, target_count, target_label, data_transformation_params, self.table_name_mapping)
            
class _Classification(_FeatureExplore, _FeatureEngineering, _DataPreparation, _ModelTraining):

    def __init__(self, 
                 data, 
                 target_column,
                 custom_data = None):
        """
        DESCRIPTION:
            Function initializes the data, target column for Classification.
         
        PARAMETERS:  
            data:
                Required Argument.
                Specifies the input teradataml Dataframe.
                Types: teradataml Dataframe
            
            target_column:
                Required Argument.
                Specifies the name of the target column in "data".
                Types: str
            
            custom_data:
                Optional Argument.
                Specifies json object containing user customized input.
                Types: json object
        """
        self.data = data
        self.target_column = target_column
        self.custom_data = custom_data

    def _classification(self,
                        model_list = None,
                        auto = False,
                        verbose = 0,
                        max_runtime_secs = None,
                        stopping_metric = None, 
                        stopping_tolerance = None,
                        max_models = None):
        """
        DESCRIPTION:
            Interal Function runs Classification.
         
        PARAMETERS:  
            auto:
                Optional Argument.
                Specifies whether to run AutoML in custom mode or auto mode.
                When set to False, runs in custom mode. Otherwise, by default runs in auto mode.
                Types: bool
                
            verbose:
                Optional Argument.
                Specifies the detailed execution steps based on verbose level.
                Default Value: 0
                Permitted Values: 
                    * 0: prints the progress bar and leaderboard
                    * 1: prints the execution steps of AutoML.
                    * 2: prints the intermediate data between the execution of each step of AutoML.
                Types: int
                
            max_runtime_secs:
                Optional Argument.
                Specifies the time limit in seconds for model training.
                Types: int
                
            stopping_metric:
                Required, when "stopping_tolerance" is set, otherwise optional.
	            Specifies the stopping mertics for stopping tolerance in model training.
                Types: str

            stopping_tolerance:
                Required, when "stopping_metric" is set, otherwise optional.
	            Specifies the stopping tolerance for stopping metrics in model training.
                Types: float
            
            max_models:
                Optional Argument.
                Specifies the maximum number of models to be trained.
                Types: int
        
        RETURNS:
            a tuple containing, model information and leaderboard.
        """
        
        
        # Feature Exploration Phase
        _FeatureExplore.__init__(self, 
                                     data = self.data, 
                                     target_column = self.target_column,
                                     verbose=verbose)
        if verbose > 0:
            self._exploration()
        # Feature Engineeting Phase
        _FeatureEngineering.__init__(self, 
                                     data = self.data, 
                                     target_column = self.target_column,
                                     model_list = model_list,
                                     verbose = verbose,
                                     task_type = "Classification",
                                     custom_data = self.custom_data)
        # Start time
        start_time = time.time()
        data, excluded_columns, target_label, data_transformation_params = self.feature_engineering(auto)
        # Data Preparation Phase
        _DataPreparation.__init__(self, 
                                  data = self.data, 
                                  target_column = self.target_column, 
                                  verbose = verbose,
                                  excluded_columns = excluded_columns, 
                                  custom_data = self.custom_data,
                                  data_transform_dict = data_transformation_params,
                                  task_type = "Classification")
        features, data_transformation_params = self.data_preparation(auto)

        # Calculating max_runtime_secs for model training by,
        # subtracting the time taken for feature engineering and data preparation
        max_runtime_secs = max_runtime_secs - (time.time() - start_time) \
                                if max_runtime_secs is not None else None
        
        # Setting max_runtime_secs to 60 seconds if it is less than 0
        max_runtime_secs = 60 if max_runtime_secs is not None and \
                                            max_runtime_secs < 0 else max_runtime_secs

        # Model training
        _ModelTraining.__init__(self, 
                                data = self.data, 
                                target_column = self.target_column,
                                model_list = model_list, 
                                verbose = verbose,
                                features = features, 
                                task_type = "Classification",
                                custom_data = self.custom_data)
        models_info, leaderboard, target_count = self.model_training(auto = auto,
                                                        max_runtime_secs = max_runtime_secs, 
                                                        stopping_metric = stopping_metric, 
                                                        stopping_tolerance = stopping_tolerance,
                                                        max_models = max_models)

        return (models_info, leaderboard, target_count, target_label, data_transformation_params, self.table_name_mapping)
  
    def _target_column_details(self): 
        """
        DESCRIPTION:
            Internal function displays the target column distribution of Target column/ Response column.
        """       
        # If data visualization libraries are available
        if self._check_visualization_libraries() and not _is_terminal():
            import matplotlib.pyplot as plt
            import seaborn as sns
            self._display_msg(msg='\nTarget Column Distribution:',
                              show_data=True)
            plt.figure(figsize=(6, 6))
            # Ploting a histogram for target column
            sns.countplot(data=self.data.select([self.target_column]).to_pandas(), x=self.target_column)
            plt.show()

    def _check_data_imbalance(self, 
                              data=None):
        """
        DESCRIPTION:
            Internal function calculate and checks the imbalance in dataset.
        
        PARAMETERS:
            data:
                Required Argument.
                Specifies the input teradataml DataFrame.
                Types: teradataml Dataframe
        
        RETURNS:
            bool, True if imbalance dataset detected, Otherwise False.
        """
        self._display_msg(msg="\nChecking imbalance data ...",
                          progress_bar=self.progress_bar)
        # Calculate the distribution of classes in the target column
        class_dist = data[self.target_column].value_counts().values

        # Find the minimum count of data points among the classes
        min_ct = np.min(class_dist)

        # Find the maximum count of data points among the classes
        max_ct = np.max(class_dist)

        # Calculate the imbalance ratio(minimum count to maximum count)
        imb_ratio = min_ct / max_ct

        # Check if the imbalance ratio less than the threshold of 0.4
        if imb_ratio < 0.4:
            self._display_msg(msg="Imbalance Found.",
                              progress_bar=self.progress_bar)
            return True

        self._display_msg(msg="Imbalance Not Found.",
                          progress_bar=self.progress_bar)
        return False
    
    def _set_custom_sampling(self):
        """
        DESCRIPTION:
            Function to handle customized data sampling for imbalance dataset.
        """
        # Fetching user input for data sampling
        data_imbalance_input = self.custom_data.get("DataImbalanceIndicator", False) 
        if data_imbalance_input:
            # Extracting method for performing data sampling
            handling_method = self.custom_data.get("DataImbalanceMethod", None)
            if handling_method == 'SMOTE':
                self._data_sampling_method = "SMOTE"
            elif handling_method == 'NearMiss':
                self._data_sampling_method = "NearMiss"
            else:
                self._display_msg(inline_msg="Provided method for data imbalance is not supported. AutoML will Proceed with default option.",
                                  progress_bar=self.progress_bar)
        else:
            self._display_msg(inline_msg="No information provided for performing customized imbalanced dataset sampling. AutoML will Proceed with default option.",
                              progress_bar=self.progress_bar)
    
    def _data_sampling(self, 
                       data):
        """
        DESCRIPTION:
            Function to handle data imbalance in dataset using sampling techniques 
            in case of classification.
            
        PARAMETERS:
            data:
                Required Argument.
                Specifies the input teradataml DataFrame.
                Types: pandas Dataframe.

        RETURNS:
            Teradataml dataframe after handling data imbalance.
        """
        self._display_msg(msg="\nStarting data imbalance handling ...",
                          progress_bar=self.progress_bar,
                          show_data=True)

        # Importing required libraries
        from imblearn.over_sampling import SMOTE
        from imblearn.under_sampling import NearMiss
        
        st = time.time()
        self._display_msg(msg=f"\nBalancing the data using {self._data_sampling_method}...",
                          progress_bar=self.progress_bar,
                          show_data=True)
        # Performing data sampling
        try:
            # Fetching the minimum target column label count and 
            # accordingly setting the number of neighbors for the sampler
            min_label_count = min(data[self.target_column].value_counts())
            if self._data_sampling_method == 'SMOTE':
                n_neighbors = min(5, min_label_count - 1)
                sampling_method = SMOTE(k_neighbors=n_neighbors, random_state=42)
            else:
                n_neighbors = min(3, min_label_count)
                sampling_method = NearMiss(version=1, n_neighbors=n_neighbors)
            
            # Fitting on dataset
            xt, yt = sampling_method.fit_resample(data.drop(columns=[self.target_column], axis=1), 
                                                    data[self.target_column])
            
            # Merging the balanced dataset with target column
            balanced_df = (xt.reset_index().merge(yt.reset_index(), on="index")) 
            balanced_df.drop(columns=['index', 'id'], axis=1, inplace=True)
            balanced_df = balanced_df.reset_index().rename(columns={'index': 'id'})
            
            et = time.time()
            self._display_msg(msg=f"Handled imbalanced dataset using {self._data_sampling_method}: {et - st:.2f} sec",
                                progress_bar=self.progress_bar,
                                show_data=True)
        except:
            self._display_msg(msg=f"Balancing using {self._data_sampling_method} Failed!!",
                              progress_bar=self.progress_bar,
                              show_data=True)
            # Returning original data if the data sampler fails
            return data
        
        self._display_msg(msg="Completed data imbalance handling.",
                          progress_bar=self.progress_bar,
                          show_data=True)
        # Returning balanced dataframe
        return balanced_df

class AutoRegressor(AutoML):
    
    def __init__(self,
                 include = None,
                 exclude = None,
                 verbose=0,
                 max_runtime_secs=None,
                 stopping_metric=None, 
                 stopping_tolerance=None,
                 max_models=None,
                 custom_config_file=None
                ):
        """
        DESCRIPTION:
            AutoRegressor is a special purpose AutoML feature to run regression specific tasks.
         
        PARAMETERS:
            include:
                Optional Argument.
                Specifies the model algorithms to be used for model training phase.
                By default, all 5 models are used for training for regression and binary
                classification problem, while only 3 models are used for multi-class.
                Permitted Values: "glm", "svm", "knn", "decision_forest", "xgboost"
                Types: str OR list of str
            
            exclude:
                Optional Argument.
                Specifies the model algorithms to be excluded from model training phase.
                No model is excluded by default.
                Permitted Values: "glm", "svm", "knn", "decision_forest", "xgboost"
                Types: str OR list of str
                    
            verbose:
                Optional Argument.
                Specifies the detailed execution steps based on verbose level.
                Default Value: 0
                Permitted Values: 
                    * 0: prints the progress bar and leaderboard
                    * 1: prints the execution steps of AutoML.
                    * 2: prints the intermediate data between the execution of each step of AutoML.
                Types: int
                
            max_runtime_secs:
                Optional Argument.
                Specifies the time limit in seconds for model training.
                Types: int
                
            stopping_metric:
                Required, when "stopping_tolerance" is set, otherwise optional.
                Specifies the stopping mertics for stopping tolerance in model training.
                Permitted Values: 
                    * For task_type "Regression": "R2", "MAE", "MSE", "MSLE", 
                                                  "RMSE", "RMSLE"
                    * For task_type "Classification": 'MICRO-F1','MACRO-F1',
                                                      'MICRO-RECALL','MACRO-RECALL',
                                                      'MICRO-PRECISION', 'MACRO-PRECISION',
                                                      'WEIGHTED-PRECISION','WEIGHTED-RECALL',
                                                      'WEIGHTED-F1', 'ACCURACY'
                Types: str

            stopping_tolerance:
                Required, when "stopping_metric" is set, otherwise optional.
                Specifies the stopping tolerance for stopping metrics in model training.
                Types: float
            
            max_models:
                Optional Argument.
                Specifies the maximum number of models to be trained.
                Types: int
                
            custom_config_file:
                Optional Argument.
                Specifies the path of JSON file in case of custom run.
                Types: str
                
        RETURNS:
            Instance of AutoRegressor.
    
        RAISES:
            TeradataMlException, TypeError, ValueError
            
        EXAMPLES:
            # Notes:
            #     1. Get the connection to Vantage to execute the function.
            #     2. One must import the required functions mentioned in
            #        the example from teradataml.
            #     3. Function will raise error if not supported on the Vantage
            #        user is connected to.

            # Load the example data.
            >>> load_example_data("decisionforestpredict", ["housing_train", "housing_test"])
    
            # Create teradataml DataFrame object.
            >>> housing_train = DataFrame.from_table("housing_train")
            
            # Example 1 : Run AutoRegressor using default options.
            # Scenario : Predict the price of house based on different factors.
           
            # Create instance of AutoRegressor.
            >>> automl_obj = AutoRegressor()

            # Fit the data.
            >>> automl_obj.fit(housing_train, "price")

            # Predict using best performing model.
            >>> prediction = automl_obj.predict()
            >>> prediction
            
            # Run predict for new test data with best performing model.
            >>> prediction = automl_obj.predict(housing_test)
            >>> prediction
            
            # Run predict for new test data with second best performing model.
            >>> prediction = automl_obj.predict(housing_test, rank=2)
            >>> prediction

            # Display leaderboard.
            >>> automl_obj.leaderboard()

            # Display best performing model.
            >>> automl_obj.leader()

            # Example 2 : Run AutoRegressor for regression problem with early stopping metric and tolerance.
            # Scenario : Predict the price of house based on different factors.
            #            Use custom configuration file to customize different 
            #            processes of AutoML Run. Define performance threshold
            #            to acquire for the available models, and terminate training 
            #            upon meeting the stipulated performance criteria.
            
            # Generate custom configuration file.
            >>> AutoRegressor.generate_custom_config("custom_housing")

            # Create instance of AutoRegressor.
            >>> automl_obj = AutoRegressor(verbose=2,
            >>>                            exclude="xgboost",
            >>>                            stopping_metric="R2",
            >>>                            stopping_tolerance=0.7,
            >>>                            max_models=10,
            >>>                            custom_config_file="custom_housing.json")
            # Fit the data.
            >>> automl_obj.fit(housing_train, "price")
 
            # Run predict with best performing model.
            >>> prediction = automl_obj.predict()
            >>> prediction

            # Display leaderboard.
            >>> automl_obj.leaderboard()

            # Example 3 : Run AutoRegressor for regression problem with maximum runtime.
            # Scenario : Predict the price of house based on different factors.
            #            Run AutoML to get the best performing model in specified time.

            # Create instance of AutoRegressor.
            >>> automl_obj = AutoRegressor(verbose=2, 
            >>>                            exclude="xgboost",
            >>>                            max_runtime_secs=500)
            # Fit the data.
            >>> automl_obj.fit(housing_train, "price")
 
            # Run predict with best performing model.
            >>> prediction = automl_obj.predict()
            >>> prediction

            # Run predict with second best performing model.
            >>> prediction = automl_obj.predict(rank=2)
            >>> prediction

            # Display leaderboard.
            >>> automl_obj.leaderboard()
 
            # Display best performing model.
            >>> automl_obj.leader()  
        """
        self.verbose = verbose
        self.max_runtime_secs = max_runtime_secs
        self.stopping_metric = stopping_metric
        self.stopping_tolerance = stopping_tolerance
        self.max_models = max_models
        self.custom_config_file = custom_config_file
        self.task_type = "Regression"
        self.include = include
        self.exclude = exclude
        
        super(AutoRegressor, self).__init__(task_type=self.task_type,
                                            include = self.include,
                                            exclude = self.exclude,
                                            verbose=self.verbose,
                                            max_runtime_secs=self.max_runtime_secs,
                                            stopping_metric=self.stopping_metric, 
                                            stopping_tolerance=self.stopping_tolerance,
                                            max_models=self.max_models,
                                            custom_config_file=self.custom_config_file)        
class AutoClassifier(AutoML):
        
    def __init__(self,
                include = None,
                exclude = None,
                verbose=0,
                max_runtime_secs=None,
                stopping_metric=None, 
                stopping_tolerance=None,
                max_models=None,
                custom_config_file=None
                ):
        """
        DESCRIPTION:
            AutoClassifier is a special purpose AutoML feature to run classification specific tasks.
            
        PARAMETERS:  
            include:
                Optional Argument.
                Specifies the model algorithms to be used for model training phase.
                By default, all 5 models are used for training for regression and binary
                classification problem, while only 3 models are used for multi-class.
                Permitted Values: "glm", "svm", "knn", "decision_forest", "xgboost"
                Types: str OR list of str  
            
            exclude:
                Optional Argument.
                Specifies the model algorithms to be excluded from model training phase.
                No model is excluded by default. 
                Permitted Values: "glm", "svm", "knn", "decision_forest", "xgboost"
                Types: str OR list of str
                    
            verbose:
                Optional Argument.
                Specifies the detailed execution steps based on verbose level.
                Default Value: 0
                Permitted Values: 
                    * 0: prints the progress bar and leaderboard
                    * 1: prints the execution steps of AutoML.
                    * 2: prints the intermediate data between the execution of each step of AutoML.
                Types: int
                
            max_runtime_secs:
                Optional Argument.
                Specifies the time limit in seconds for model training.
                Types: int
                
            stopping_metric:
                Required, when "stopping_tolerance" is set, otherwise optional.
                Specifies the stopping mertics for stopping tolerance in model training.
                Permitted Values: 
                    * For task_type "Regression": "R2", "MAE", "MSE", "MSLE", 
                                                  "RMSE", "RMSLE"
                    * For task_type "Classification": 'MICRO-F1','MACRO-F1',
                                                      'MICRO-RECALL','MACRO-RECALL',
                                                      'MICRO-PRECISION', 'MACRO-PRECISION',
                                                      'WEIGHTED-PRECISION','WEIGHTED-RECALL',
                                                      'WEIGHTED-F1', 'ACCURACY'
                Types: str

            stopping_tolerance:
                Required, when "stopping_metric" is set, otherwise optional.
                Specifies the stopping tolerance for stopping metrics in model training.
                Types: float
            
            max_models:
                Optional Argument.
                Specifies the maximum number of models to be trained.
                Types: int
                
            custom_config_file:
                Optional Argument.
                Specifies the path of json file in case of custom run.
                Types: str
                
        RETURNS:
            Instance of AutoClassifier.
    
        RAISES:
            TeradataMlException, TypeError, ValueError
            
        EXAMPLES:    
            # Notes:
            #     1. Get the connection to Vantage to execute the function.
            #     2. One must import the required functions mentioned in
            #        the example from teradataml.
            #     3. Function will raise error if not supported on the Vantage
            #        user is connected to.

            # Load the example data.
            >>> load_example_data("teradataml", ["titanic", "iris_input"])
            >>> load_example_data("GLMPredict", ["admissions_test", "admissions_train"])
            
            # Create teradataml DataFrame object.
            >>> admissions_train = DataFrame.from_table("admissions_train")
            >>> titanic = DataFrame.from_table("titanic")
            >>> iris_input = DataFrame.from_table("iris_input")
            >>> admissions_test = DataFrame.from_table("admissions_test")
            
            # Example 1 : Run AutoClassifier for binary classification problem
            # Scenario : Predict whether a student will be admitted to a university
            #            based on different factors. Run AutoML to get the best performing model
            #            out of available models.
            
            # Create instance of AutoClassifier..
            >>> automl_obj = AutoClassifier()

            # Fit the data.
            >>> automl_obj.fit(admissions_train, "admitted")

            # Predict using best performing model.
            >>> prediction = automl_obj.predict()
            >>> prediction
            
            # Run predict for new test data with best performing model.
            >>> prediction = automl_obj.predict(admissions_test)
            >>> prediction
            
            # Run predict for new test data with second best performing model.
            >>> prediction = automl_obj.predict(admissions_test, rank=2)
            >>> prediction

            # Display leaderboard.
            >>> automl_obj.leaderboard()

            # Display best performing model.
            >>> automl_obj.leader()

            # Example 2 : Run AutoClassifier for binary classification.
            # Scenario : Predict whether passenger aboard the RMS Titanic survived
            #            or not based on differect factors. Run AutoML to get the 
            #            best performing model out of available models. Use custom
            #            configuration file to customize different processes of
            #            AutoML Run. 
            
            # Generate custom configuration file.
            >>> AutoClassifier.generate_custom_config("custom_titanic")
            
            # Create instance of AutoClassifier.
            >>> automl_obj = AutoClassifier(verbose=2, 
            >>>                             custom_config_file="custom_titanic.json")
            # Fit the data.
            >>> automl_obj.fit(titanic, titanic.survived)
 
            # Run predict with best performing model.
            >>> prediction = automl_obj.predict()
            >>> prediction

            # Run predict with second best performing model.
            >>> prediction = automl_obj.predict(rank=2)
            >>> prediction

            # Display leaderboard.
            >>> automl_obj.leaderboard()
 
            # Display best performing model.
            >>> automl_obj.leader()

            # Example 3 : Run AutoClassifier for multiclass classification problem.
            # Scenario : Predict the species of iris flower based on different factors.
            #            Run AutoML to get the best performing model out of available 
            #            models. Use custom configuration file to customize different 
            #            processes of AutoML Run.
            
            # Generate custom configuration file.
            >>> AutoClassifier.generate_custom_config("custom_iris")
            
            # Create instance of AutoClassifier.
            >>> automl_obj = AutoClassifier(verbose=1, 
            >>>                             custom_config_file="custom_iris.json")
            # Fit the data.
            >>> automl_obj.fit(iris_input, "species")

            # Predict using best performing model.
            >>> prediction = automl_obj.predict()
            >>> prediction

            # Display leaderboard.
            >>> automl_obj.leaderboard()
  
            # Display best performing model.
            >>> automl_obj.leader()

            # Example 4 : Run AutoClassifier for classification problem with stopping metric and tolerance.
            # Scenario : Predict whether passenger aboard the RMS Titanic survived
            #            or not based on differect factors. Use custom configuration 
            #            file to customize different processes of AutoML Run. Define
            #            performance threshold to acquire for the available models, and 
            #            terminate training upon meeting the stipulated performance criteria.
            
            # Generate custom configuration file.
            >>> AutoClassifier.generate_custom_config("custom_titanic")

            # Create instance of AutoClassifier.
            >>> automl_obj = AutoClassifier(verbose=2, 
            >>>                             exclude="xgboost",
            >>>                             stopping_metric="MICRO-F1",
            >>>                             stopping_tolerance=0.7,
            >>>                             max_models=8
            >>>                             custom_config_file="custom_titanic.json")
            # Fit the data.
            >>> automl_obj.fit(titanic, titanic.survived)
 
            # Run predict with best performing model.
            >>> prediction = automl_obj.predict()
            >>> prediction

            # Display leaderboard.
            >>> automl_obj.leaderboard()

            # Example 5 : Run AutoClassifier for classification problem with maximum runtime.
            # Scenario : Predict the species of iris flower based on different factors.
            #            Run AutoML to get the best performing model in specified time.

            # Create instance of AutoClassifier.
            >>> automl_obj = AutoClassifier(verbose=2, 
            >>>                             exclude="xgboost",
            >>>                             max_runtime_secs=500)
            >>>                             max_models=3)
            # Fit the data.
            >>> automl_obj.fit(iris_input, iris_input.species)
 
            # Run predict with best performing model.
            >>> prediction = automl_obj.predict()
            >>> prediction

            # Run predict with second best performing model.
            >>> prediction = automl_obj.predict(rank=2)
            >>> prediction

            # Display leaderboard.
            >>> automl_obj.leaderboard()
 
            # Display best performing model.
            >>> automl_obj.leader()     
        """
        self.verbose = verbose
        self.max_runtime_secs = max_runtime_secs
        self.stopping_metric = stopping_metric
        self.stopping_tolerance = stopping_tolerance
        self.max_models = max_models
        self.custom_config_file = custom_config_file
        self.task_type = "Classification"
        self.include = include
        self.exclude = exclude
        
        super(AutoClassifier, self).__init__(task_type=self.task_type,
                                            include = self.include,
                                            exclude = self.exclude,
                                            verbose=self.verbose,
                                            max_runtime_secs=self.max_runtime_secs,
                                            stopping_metric=self.stopping_metric, 
                                            stopping_tolerance=self.stopping_tolerance,
                                            max_models=self.max_models,
                                            custom_config_file=self.custom_config_file)