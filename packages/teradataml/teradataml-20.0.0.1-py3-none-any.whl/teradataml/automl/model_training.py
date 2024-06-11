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
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import math
import pandas as pd
from itertools import product

# Teradata libraries
from teradataml.context import context as tdmlctx
from teradataml.dataframe.copy_to import copy_to_sql
from teradataml.dataframe.dataframe import DataFrame
from teradataml import execute_sql, get_connection
from teradataml import SVM, GLM, DecisionForest, XGBoost, GridSearch, KNN, RandomSearch
from teradataml.utils.validators import _Validators


class _ModelTraining:
    
    def __init__(self, 
                 data, 
                 target_column,
                 model_list,
                 verbose=0,
                 features=None,
                 task_type="Regression",
                 custom_data = None):
        """
        DESCRIPTION:
            Function initializes the data, target column, features and models
            for model training.
         
        PARAMETERS:  
            data:
                Required Argument.
                Specifies the dataset for model training phase.
                Types: teradataml Dataframe
            
            target_column:
                Required Argument.
                Specifies the target column present inside the dataset.
                Types: str
            
            model_list:
                Required Argument.
                Specifies the list of models to be used for model training.
                Types: list
                
            verbose:
                Optional Argument.
                Specifies the detailed execution steps based on verbose level.
                Default Value: 0
                Permitted Values: 
                    * 0: prints the progress bar and leaderboard
                    * 1: prints the execution steps of AutoML.
                    * 2: prints the intermediate data between the 
                         execution of each step of AutoML.
                Types: int
                
            features:
                Required Argument.
                Specifies the list of selected feature by rfe, lasso and pca
                respectively in this order.
                Types: list of list of strings (str)
                
            task_type:
                Required Argument.
                Specifies the task type for AutoML, whether to apply regresion 
                or classification on the provived dataset.
                Default Value: "Regression"
                Permitted Values: "Regression", "Classification"
                Types: str
                
            custom_data:
                Optional Argument.
                Specifies json object containing user customized input.
                Types: json object
        """
        self.data = data
        self.target_column = target_column
        self.model_list = model_list
        self.verbose = verbose
        self.features = (features[1], features[0], features[2])
        self.task_type = task_type
        self.custom_data = custom_data
        self.labels = self.data.drop_duplicate(self.target_column).size
        self.startify_col = None

    def model_training(self, 
                       auto=True,
                       max_runtime_secs=None,
                       stopping_metric=None, 
                       stopping_tolerance=0,
                       max_models=None 
                       ):
        """
        DESCRIPTION:
            Function to perform following tasks:-
                1. Generates the hyperparameters for different ML models.
                2. Performs hyperparameter tunning for different ML models in parallel.
                3. Displays the leaderboard of trained ML models.
         
        PARAMETERS:           
            auto:
                Optional Argument.
                Specifies whether to run data preparation in auto mode or custom mode.
                When set to True, runs automtically otherwise, it take user inputs.
                Default Value: True
                Types: boolean  
                
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
            pandas dataframes containing model information, leaderboard and target 
            column distinct count.     
        """
        self.stopping_metric = stopping_metric
        self.stopping_tolerance = stopping_tolerance
        self.max_runtime_secs = max_runtime_secs
        self.max_models = max_models
        
        self._display_heading(phase=3, progress_bar=self.progress_bar)
        self._display_msg(msg='Model Training started ...',
                          progress_bar=self.progress_bar,
                          show_data=True)
        # Generates the hyperparameters for different ML models
        parameters = self._generate_parameter()
        
        # handles customized hyperparameters
        if not auto:
            parameters = self._custom_hyperparameters(parameters)
        
        # Validates the upper limit of max_models based on total model combinations
        if self.max_models is not None:
            self._validate_upper_limit_for_max_models(parameters)
            
        if self.verbose == 2:
            self._display_hyperparameters(parameters)

        # Parallel execution of hpt
        trained_models_info = self._parallel_training(parameters)
        
        # Displaying leaderboard
        leader_board, models = self._display_leaderboard(trained_models_info)
        
        self._display_heading(phase=4,
                              progress_bar=self.progress_bar)
        self.progress_bar.update()
            
        return models, leader_board, self.labels
    
    def _get_model_param_space(self,
                               hyperparameters):
        """
        DESCRIPTION:
            Internal function to calculate the total number of models to be trained for specific model.
        
        PARAMETERS:
            hyperparameters:
                Required Argument.
                Specifies the hyperparameters availables for ML model.
                Types: list of dict
        
        RETURNS:
            int containing, total number of models available for training.
        """
        # Creating all possible combinations of hyperparameters
        all_combinations = list(product(*[v if isinstance(v, tuple) else [v] for v in hyperparameters.values()]))
        # Getting total number of models for each model model training function
        total_models = len(all_combinations)
        return total_models

    def _validate_upper_limit_for_max_models(self,
                                             hyperparameters_list):
        """
        DESCRIPTION:
            Internal function to validate the upper limit of max_models.
        
        PARAMETERS:
            hyperparameters_list:
                Required Argument.
                Specifies the hyperparameters for different ML models.
                Types: list of dict
        
        RETURNS:
            None
        
        RAISES:
            TeradataMlException, ValueError
        """
        model_param_space = 0
        for hyperparameter_dct in hyperparameters_list:
            # getting total number of models for each model
            total_models = self._get_model_param_space(hyperparameter_dct)
            model_param_space += total_models
            
        # Validating upper range for max_models 
        _Validators._validate_argument_range(self.max_models, "max_models", ubound=model_param_space, ubound_inclusive=True)
    
    def _display_hyperparameters(self,
                                 hyperparameters_list):
        """
        DESCRIPTION:
            Internal function to display the hyperparameters for different ML models.
         
        PARAMETERS:
            hyperparameters_list:
                Required Argument.
                Specifies the hyperparameters for different ML models.
                Types: list of dict
        
        RETURNS:
            None
        """	
        self._display_msg(msg="\nHyperparameters used for model training: ",
                          progress_bar = self.progress_bar,
                          show_data=True)
        print(" " *150, end='\r', flush=True)

        # Iterating over hyperparameters_list
        for hyperparameter_dct in hyperparameters_list:
            # Extracting hyperparameter and their value from hyperparameters dictionary
            for key, val in hyperparameter_dct.items():
                # Displaying hyperparameters
                print(f"{key} : {str(val)}")

            # Displaying total number of models for each model
            total_models = self._get_model_param_space(hyperparameter_dct)
            print(f"Total number of models for {hyperparameter_dct['name']} : {total_models}")
            print(f"--"*100+'\n')
    
    def _display_leaderboard(self, 
                             trained_models_info):
        """
        DESCRIPTION:
            Internal function to display the trainined ML models.
         
        PARAMETERS:
            trained_models_info:
                Required Argument.
                Specifies the trained models inforamtion to display.
                Types: pandas Dataframe
        
        RETURNS:
            pandas Dataframe.
        """	
        # Creating a copy to avoid use of same reference of memory
        if self.task_type != "Regression":
            sorted_model_df = trained_models_info.sort_values(by=['Micro-F1', 'Weighted-F1'], 
                                                ascending=[False, False]).reset_index(drop=True)
        else:
            sorted_model_df = trained_models_info.sort_values(by='R2-score', 
                                                ascending=False).reset_index(drop=True)
        
        # Adding rank to leaderboard
        sorted_model_df.insert(0, 'Rank', sorted_model_df.index + 1) 

        # Excluding the model object and model name from leaderboard
        leaderboard = sorted_model_df.drop(["model-obj","Name"], axis=1)
        # filtering the rows based on the max_models
        if self.max_models is not None:
            leaderboard = leaderboard[leaderboard["Rank"] <= self.max_models]
        
        self._display_msg(msg="Leaderboard",
                          progress_bar=self.progress_bar,
                          data=leaderboard,
                          show_data=True)
        
        return leaderboard, sorted_model_df

    def _update_hyperparameters(self,
                                existing_params, 
                                new_params):
        """
        DESCRIPTION:
            Function to update customized hyperparameters by performing addition or replacement 
            based on user input.

        PARAMETERS:  
            existing_params:
                Required Argument.
                Specifies the existing generated hyperparameters for specific model.
                Types: dict

            new_params:
                Required Argument.
                Specifies the newly passed hyperparameters from user input.
                Types: dict
                
        RETURNS:
            Updated dictionary containing hyperparameters for specific model.
        """
        # Iterating over new hyperparameters and performing required operation 
        # based on passed method ADD or REPLACE
        for feature, param_list in new_params.items():
            if feature in existing_params.keys():
                if param_list["Method"] == "ADD":
                    # Extending existing list
                    existing_params[feature] = list(existing_params[feature])
                    existing_params[feature].extend(param_list["Value"])
                    # Updating list with unique values.
                    existing_params[feature]=tuple(set(existing_params[feature]))
                elif param_list["Method"] == "REPLACE":
                    # Replacing with entirely new value
                    existing_params[feature] = tuple(param_list["Value"])
                else:
                    self._display_msg(inline_msg="Passed method is not valid.")
            else:
                self._display_msg(inline_msg="\nPassed model argument {} is not"
                                  "available for model {}. Skipping it."
                                  .format(feature,existing_params['name']))
                continue
            # Returning updated hyperparamter
        return existing_params

    def _custom_hyperparameters(self,
                                hyperparameters):
        """
        DESCRIPTION:
            Function to extract and update hyperaparameters from user input for model training.

        PARAMETERS:  
            hyperparameters:
                Required Argument.
                Specifies the existing generated hyperparameters for all models.
                Types: list
                
        RETURNS:
             Updated list of dictionaries containing hyperparameterd for all models.
        """
        self._display_msg(msg="\nStarting customized hyperparameter update ...",
                          progress_bar=self.progress_bar,
                          show_data=True)
        
        # Fetching user input for performing hyperparameter tuning 
        hyperparameter_tuning_input = self.custom_data.get("HyperparameterTuningIndicator", False) 
        if hyperparameter_tuning_input:
            # Extracting models and its corresponding hyperparameters details
            model_hyperparameters = self.custom_data.get("HyperparameterTuningParam", None)
            # Getting model index for mapping
            model_index_param = self.model_mapping
            # Checking hyperparameters passed by user and mapping them according to model
            if model_hyperparameters:
                for model_name, hyp_list in model_hyperparameters.items():
                    if model_name in list(model_index_param.keys()):
                        model_index = model_index_param[model_name]
                    else:
                        self._display_msg(inline_msg="\nPassed model {} is not available for training.".format(model_name))
                        continue
                    # Updating existing hyperparameters with customized hyperparameters as per user input
                    hyperparameters[model_index]=self._update_hyperparameters(hyperparameters[model_index],hyp_list)
                # Displaying it after update
                self._display_msg(inline_msg="\nCompleted customized hyperparameter update.",
                                 progress_bar=self.progress_bar)
            else:
                self._display_msg(inline_msg="No information provided for custom hyperparameters. AutoML will proceed with default values.",
                                 progress_bar=self.progress_bar)
        else:
            self._display_msg(inline_msg="\nSkipping customized hyperparameter tuning",
                             progress_bar=self.progress_bar)
        # Retunring updated hyperparameters for all models    
        return hyperparameters
    
    # Hyperparameter generation for XGBoost or Decision Forest
    def _get_tree_model_hyperparameters(self,
                                        num_rows, 
                                        num_cols,
                                        model_name):
        """
        DESCRIPTION:
            Internal function to generate hyperparameters for tree based model i.e., XGBoost or Decision Forest.
         
        PARAMETERS:
            num_rows:
                Required Argument.
                Specifies the number of rows in dataset.
                Types: int
                
            num_cols:
                Required Argument.
                Specifies the number of columns in dataset.
                Types: int

            model_name:
                Required Argument.
                Specifies which linear model is getting used for generating hyperparameters.
                Types: Str
                
        RETURNS:
            dict containing, hyperparameters for XGBoost or Decision Forest.
        """
        # Initializing hyperparameters based on default value
        min_impurity = [0.0]
        shrinkage_factor = [0.5]
        max_depth = [5]
        min_node_size = [1]
        iter_num = [10]
        num_trees = [-1]
        
        # Extending values for hyperparameters based on dataset size, i.e., number of rows and columns
        if num_rows < 1000 and num_cols < 10:
            min_impurity.extend([0.1])
            shrinkage_factor.extend([0.1, 0.2])
            max_depth.extend([6, 7, 8])
            min_node_size.extend([2])
            iter_num.extend([20])
            num_trees.extend([10, 20])
        elif num_rows < 10000 and num_cols < 15:
            min_impurity.extend([0.1, 0.2])
            shrinkage_factor.extend([0.1, 0.3])
            max_depth.extend([6, 8, 10])
            min_node_size.extend([2, 3])
            iter_num.extend([20, 30])
            num_trees.extend([20, 30])
        elif num_rows < 100000 and num_cols < 20:
            min_impurity.extend([0.2, 0.3])
            shrinkage_factor.extend([0.01, 0.1, 0.2])
            max_depth.extend([4, 6, 7])
            min_node_size.extend([3, 4])
            iter_num.extend([30, 40])
            num_trees.extend([30, 40])
        else:
            min_impurity.extend([0.1, 0.2, 0.3])
            shrinkage_factor.extend([0.01, 0.05, 0.1])
            max_depth.extend([3, 4, 7, 8])
            min_node_size.extend([2, 3, 4])
            iter_num.extend([20, 30, 40])
            num_trees.extend([20, 30, 40])

        # Hyperparameters for XGBoost model
        xgb_params = {
                'response_column': self.target_column,
                'name':'xgboost',
                'model_type': 'Regression',
                'column_sampling': (1, .6),
                'min_impurity': tuple(min_impurity),
                'lambda1': (0.01, 0.1, 1, 10),
                'shrinkage_factor': tuple(shrinkage_factor),
                'max_depth': tuple(max_depth),
                'min_node_size': tuple(min_node_size),
                'iter_num': tuple(iter_num),
                'seed':42
                }
        # Hyperparameters for Decision Forest model
        df_params = {
                'response_column': self.target_column, 
                'name': 'decision_forest',
                'tree_type': 'Regression',
                'min_impurity': tuple(min_impurity),
                'max_depth': tuple(max_depth),
                'min_node_size': tuple(min_node_size),
                'num_trees': tuple(num_trees),
                'seed':42
        }
        
        # Updating model type in case of classification
        if self.task_type == "Classification":
            xgb_params['model_type'] = 'Classification'
            df_params['tree_type'] = 'Classification'

        # Returning hyperparameters based on passed model
        if model_name == 'xgboost':
            return xgb_params
        elif model_name == 'decision_forest':
            return df_params
        else:
            return None

    # Hyperparameter generation for KNN
    def _get_knn_hyperparameters(self,
                                 num_rows=None, 
                                 num_cols=None):
        """
        DESCRIPTION:
            Internal function to generate hyperparameters for KNN.
         
        PARAMETERS:
            num_rows
                Required Argument.
                Specifies the number of rows in dataset.
                Types: int
                
            num_cols:
                Required Argument.
                Specifies the number of columns in dataset.
                Types: int
                
        RETURNS:
            dict containing, hyperparameters for KNN.
        """
        params = {
                'response_column': self.target_column,
                'name': 'knn',
                'model_type': 'Regression',
                'k': (3, 5, 6, 8, 10, 12),
                "id_column":"id",
                "voting_weight": 1.0
                }
        
        if self.task_type == "Classification":
            params['model_type'] = 'Classification'
    
        return params

    # Hyperparameter generation for SVM/GLM
    def _get_linear_model_hyperparameters(self,
                                          num_rows,
                                          num_cols,
                                          model_name):
        """
        DESCRIPTION:
            Internal function to generate hyperparameters for linear models i.e., SVM or GLM.
         
        PARAMETERS:               
            num_rows:
                Required Argument.
                Specifies the number of rows in dataset.
                Types: int
                
            num_cols:
                Required Argument.
                Specifies the number of columns in dataset.
                Types: int

            model_name:
                Required Argument.
                Specifies which tree model is getting used for generating hyperparameters.
                Types: Str
                
        RETURNS:
            dict containing, hyperparameters for SVM or GLM.
        """
        # Initializing hyperparameters based on default value
        iter_max = [300]
        batch_size = [10]
        
        # Extending values for hyperparameters based on dataset size i.e., number of rows and columns
        if num_rows < 1000 and num_cols < 10:
            iter_max.extend([100, 200])
            batch_size.extend([20, 40, 50])
        elif num_rows < 10000 and num_cols < 15:
            iter_max.extend([200, 400])
            batch_size.extend([50, 60, 80])
        elif num_rows < 100000 and num_cols < 20:
            iter_max.extend([400])
            batch_size.extend([100, 150])
        else:
            iter_max.extend([200, 400, 500])
            batch_size.extend([80, 100, 150])
            
        # Hyperparameters for SVM model    
        svm_params = { 
                'response_column': self.target_column,
                'name':'svm', 
                'model_type':'regression',
                'lambda1':(0.001, 0.02, 0.1),
                'alpha':(.15, .85),
                'tolerance':(0.001, 0.01),
                'learning_rate':('Invtime','Adaptive','constant'),
                'initial_eta' : (0.05, 0.1),
                'momentum':(0.65, 0.8, 0.95),
                'nesterov': True,
                'intercept': True,
                'iter_num_no_change':(5, 10, 50),
                'local_sgd_iterations ': (10, 20),
                'iter_max' : tuple(iter_max),
                'batch_size' : tuple(batch_size)
                }
        # Hyperparameters for GLM model
        glm_params={
                'response_column': self.target_column,
                'name': 'glm',
                'family': 'GAUSSIAN',
                'lambda1':(0.001, 0.02, 0.1),
                'alpha': (0.15, 0.85),
                'learning_rate': ('invtime', 'constant', 'adaptive'),
                'initial_eta': (0.05, 0.1),
                'momentum': (0.65, 0.8, 0.95),
                'iter_num_no_change':(5, 10, 50),
                'iter_max' : tuple(iter_max),
                'batch_size' : tuple(batch_size)
                }
        
        # Updating model type in case of classification    
        if self.task_type == "Classification":
            svm_params['model_type'] = 'Classification'
            svm_params['learning_rate'] =  'OPTIMAL'
            glm_params['family'] = 'BINOMIAL'
            glm_params['learning_rate'] =  'OPTIMAL'
        
        # Returning hyperparameters based on passed model    
        if model_name == 'svm':
            return svm_params
        elif model_name == 'glm':
            return glm_params
        else:
            return None

    def _generate_parameter(self):
        """
        DESCRIPTION:
            Internal function to generate hyperparameters for ML models.
                
        RETURNS:
            list containing, dict of hyperparameters for different ML models.
        """
        # list for storing hyperparameters
        parameters=[]
        # Index for model mapping
        model_index=0
        # Dictionary for mapping model with index
        self.model_mapping={}
        
        # Getting number of rows and columns
        num_rows = self.data.shape[0]
        num_cols = self.data.shape[1]
        
        # Updating model list for multi-class classification
        if self.task_type.casefold() == "classification" and self.labels > 2:
            for model in ['glm','svm']:
                if model in self.model_list:
                    self._display_msg(inline_msg="\nMulti-class classification is "
                                     "not supported by {} model. Skipping {} model."
                                     .format(model, model),
                                     progress_bar=self.progress_bar)
                    self.model_list.remove(model)
                    
        # Model functions mapping for hyperparameter generation           
        model_functions = {
            'decision_forest': self._get_tree_model_hyperparameters,
            'xgboost': self._get_tree_model_hyperparameters,
            'knn': self._get_knn_hyperparameters,
            'glm': self._get_linear_model_hyperparameters,
            'svm': self._get_linear_model_hyperparameters,
        }
        
        # Generating hyperparameters for each model
        if self.model_list:
            for model in self.model_list:
                self.model_mapping[model] = model_index
                if model == 'knn':
                    parameters.append(model_functions[model](num_rows, num_cols))
                else:
                    parameters.append(model_functions[model](num_rows, num_cols, model))
                model_index += 1
        else:
            raise ValueError("No model is selected for training.")

        return parameters
    
    def distribute_max_models(self):
        """
        DESCRIPTION:
            Internal function to distribute max_models across available model functions.
        
        RETURNS:
            dictionary containing max_models distribution and list of models to remove.
        """
        # Getting total number of models
        model_count=len(self.model_list)
        # Evenly distributing max_models across models
        base_assign = self.max_models // model_count
        # Creating list of max_models for each model
        distribution = [base_assign] * model_count
        
        # Calculating remaining models
        remaining_model_count = self.max_models % model_count
        if remaining_model_count:
            # distributing remaining model across models.
            # Starting from first model in list and distributing remaining models by 1 each.
            for i in range(remaining_model_count):
                distribution[i] += 1
        
        # Creating dictionary for model distribution
        model_distribution = dict(zip(self.model_list, distribution))
        # Getting list of models with 0 distribution and removing them from model list
        # While for model having distribution greater than 0, updating distribution with 
        # 1/3rd of original value as we are training with 3 different feature selection methods.
        models_to_remove = []
        for model in self.model_list:
            initial_count = model_distribution[model]          
            if initial_count == 0:
                models_to_remove.append(model)
            else:
                model_distribution[model] = math.ceil(initial_count / 3)
        
        return model_distribution, models_to_remove

    def _parallel_training(self, parameters):
        """
        DESCRIPTION:
            Internal function initiates the threadpool executor 
            for hyperparameter tunning of ML models.
         
        PARAMETERS:
             parameters:
                Required Argument.
                Specifies the hyperparamters for ML models.
                Types: list of dict

        RETURNS:
            Pandas DataFrame containing, trained models information.
        """ 

        # Hyperparameters for each model
        model_params = parameters[:min(len(parameters), 5)]
        self._display_msg(msg="\nPerforming hyperParameter tuning ...", progress_bar=self.progress_bar)

        # Defining training and testing data
        data_types = ['lasso', 'rfe', 'pca']
        trainng_datas = tuple(DataFrame(self.table_name_mapping[f'{data_type}_train']) for data_type in data_types)
        testing_datas = tuple(DataFrame(self.table_name_mapping[f'{data_type}_test']) for data_type in data_types)

        if self.stopping_metric is None:
            self.stopping_tolerance, self.stopping_metric = 1.0, 'MICRO-F1' \
                                    if self.is_classification_type() else 'R2'

        self.max_runtime_secs = self.max_runtime_secs/len(model_params) \
                                if self.max_runtime_secs is not None else None
                   
        if self.max_models is not None:
            # Getting model distribution and models to remove
            self.max_models_distribution, models_to_remove = self.distribute_max_models()
            # Removing model parameters with 0 distribution
            if len(models_to_remove):
                for model in models_to_remove:
                    model_params = [param for param in model_params if param['name'] != model]
                    # Updating progress bar as we are removing model
                    self.progress_bar.update()

        if self.is_classification_type():
            self.startify_col = self.target_column

        trained_models = []
        for param in model_params:
            result = self._hyperparameter_tunning(param, trainng_datas, testing_datas)
            trained_models.append(result)

        models_df = pd.concat(trained_models, ignore_index=True)

        # Score the model and combine the results into a single DataFrame
        trained_models_info = self._model_scoring(testing_datas, models_df)
        trained_models_info = trained_models_info.reset_index(drop=True)

        return trained_models_info
    
    def _model_scoring(self,
                       test_data,
                       model_info):
        """
        DESCRIPTION:
            Internal function generates the performance metrics for
            trained ML models using testing dataset.
         
        PARAMETERS:
            test_data
                Required Argument.
                Specifies the testing datasets
                Types: tuple of Teradataml DataFrame
            
            model_info
                Required Argument.
                Specifies the trained models information.
                Types: Pandas DataFrame
            
        RETURNS:
            Pandas DataFrame containing, trained models with their performance metrics.
        """ 
        self._display_msg(msg="Evaluating models performance ...",
                          progress_bar = self.progress_bar,
                          show_data=True)
        # Empty list for storing model performance metrics
        model_performance_data = []

        # Mapping feature selection methods to corresponding test data
        feature_selection_to_test_data = {"lasso": test_data[0], 
                                          "rfe": test_data[1], 
                                          "pca": test_data[2]}

        # Iterating over models 
        for index, model_row in model_info.iterrows():
            # Extracting model name, model id, feature selection method, and model object
            model_name, model_id, feature_selection, model_object = model_row['Name'], \
                model_row['Model-ID'], model_row['Feature-Selection'], model_row['obj']

            # Selecting test data based on feature selection method
            test_set = feature_selection_to_test_data[feature_selection]

            # Model evaluation
            if model_name == 'knn':
                performance_metrics = model_object.evaluate(test_data=test_set)
            else:
                eval_params = _ModelTraining._eval_params_generation(model_name, 
                                                                     self.target_column,
                                                                     self.task_type)
                performance_metrics = model_object.evaluate(newdata=test_set, **eval_params)

            # Extracting performance metrics
            if self.is_classification_type():
                # Classification
                # Extract performance metrics from the output data
                performance_metrics_list = [metric[2] for metric in performance_metrics.output_data.itertuples()]

                # Combine all the elements to form a new row
                new_row = [model_name, model_id, feature_selection] + performance_metrics_list + [model_object]
            else:
                # Regression
                regression_metrics = next(performance_metrics.result.itertuples())
                sample_size = test_set.select('id').size
                feature_count = len(test_set.columns) - 2
                r2_score = regression_metrics[8]
                adjusted_r2_score = 1 - ((1 - r2_score) * (sample_size - 1) / (sample_size - feature_count - 1))
                new_row = [model_name, model_id, feature_selection, regression_metrics[0], 
                           regression_metrics[1], regression_metrics[2], regression_metrics[5], 
                           regression_metrics[6], r2_score, adjusted_r2_score, model_object]

            model_performance_data.append(new_row)

        if self.is_classification_type():
            model_metrics_df = pd.DataFrame(model_performance_data, columns=['Name','Model-ID',
                                                        'Feature-Selection','Accuracy','Micro-Precision',
                                                        'Micro-Recall','Micro-F1',
                                                        'Macro-Precision','Macro-Recall',
                                                        'Macro-F1','Weighted-Precision',
                                                        'Weighted-Recall','Weighted-F1',
                                                        'model-obj'])
        else:
            model_metrics_df = pd.DataFrame(model_performance_data, columns=['Name', 'Model-ID',
                                                            'Feature-Selection',
                                                            'MAE', 'MSE', 'MSLE',
                                                            'RMSE', 'RMSLE',
                                                            'R2-score',
                                                            'Adjusted R2-score',       
                                                            'model-obj'])
        self._display_msg(msg="Evaluation completed.",
                          progress_bar = self.progress_bar,
                          show_data=True)

        return model_metrics_df
    
    def _hyperparameter_tunning(self,
                                model_param, 
                                train_data,
                                test_data):
        """
        DESCRIPTION:
            Internal function performs hyperparameter tuning on 
            ML models for regression/classification problems.
         
        PARAMETERS:
            model_param
                Required Argument.
                Specifies the eval_params argument for GridSearch.
                Types: dict
                
            train_data:
                Required Argument.
                Specifies the training datasets.
                Types: tuple of Teradataml DataFrame
            
            test_data
                Required Argument.
                Specifies the testing datasets
                Types: tuple of Teradataml DataFrame
            
        RETURNS:
            pandas DataFrame containing, trained models information.
        """ 
        # Mapping model names to functions
        model_to_func = {"glm": GLM, "svm": SVM, 
                         "xgboost": XGBoost, "decision_forest": DecisionForest, "knn": KNN}

        # Setting eval_params for hpt.
        eval_params = _ModelTraining._eval_params_generation(model_param['name'], 
                                                             self.target_column,
                                                             self.task_type)

        # Input columns for model
        model_param['input_columns'] = self.features

        self._display_msg(msg=model_param['name'], 
                          progress_bar=self.progress_bar,
                          show_data=True)
        
        # Defining test data for KNN
        if model_param['name'] == 'knn':
            model_param['test_data'] = test_data

        # Using RandomSearch for hyperparameter tunning when max_models is given.
        # Otherwise, using GridSearch for hyperparameter tunning.
        if self.max_models is not None:
            # Setting max_models for RandomSearch based on model name
            model_param['max_models'] = self.max_models_distribution[model_param['name']]
            # Defining RandomSearch with ML model based on Name, and max_models
            _obj = RandomSearch(func=model_to_func[model_param['name']],
                                params=model_param,
                                n_iter=model_param['max_models'])
        else:
            # Defining Gridsearch with ML model based on Name
            _obj = GridSearch(func=model_to_func[model_param['name']], 
                              params=model_param)
        
        if self.verbose > 0:
            print(" " *200, end='\r', flush=True)
            verbose = 1
        else:
            verbose = 0
            
        # Hyperparameter tunning
        if model_param['name'] == 'knn':
            _obj.fit(data=train_data, evaluation_metric=self.stopping_metric,
                    early_stop=self.stopping_tolerance, run_parallel=True, 
                    sample_seed=42, sample_id_column='id', discard_invalid_column_params=True,
                    stratify_column=self.startify_col,verbose=verbose, max_time=self.max_runtime_secs)
        else:
            _obj.fit(data=train_data, evaluation_metric=self.stopping_metric,
                    early_stop=self.stopping_tolerance, **eval_params, 
                    run_parallel=True, discard_invalid_column_params=True, sample_seed=42, 
                    sample_id_column='id',stratify_column=self.startify_col, verbose=verbose, max_time=self.max_runtime_secs)

        # Getting all passed models
        _df = _obj.model_stats.merge(_obj.models[_obj.models['STATUS']=='PASS'][['MODEL_ID', 'DATA_ID']], on='MODEL_ID', how='inner')
        # Creating mapping data ID to feature selection method
        data_id_to_method_map = {"DF_0": "lasso", "DF_1": "rfe", "DF_2": "pca"}
        
        # Mapping data ID to feature selection method
        _df['Feature-Selection'] = _df['DATA_ID'].map(data_id_to_method_map)
        # Getting model details
        _df['Name'] = model_param['name']
        _df['Model-ID'] = _df['MODEL_ID']
        _df['obj'] = _df['MODEL_ID'].apply(lambda x: _obj.get_model(x))
        
        # Extracting needed columns
        model_info = _df[["Name", "Model-ID", "Feature-Selection", "obj"]]
        
        self._display_msg(msg="-"*100,
                          progress_bar=self.progress_bar,
                          show_data=True)
        self.progress_bar.update()

        return model_info

    @staticmethod
    def _eval_params_generation(ml_name,
                                target_column,
                                task_type):
        """
        DESCRIPTION:
            Internal function generates the eval_params for 
            different ML models.
         
        PARAMETERS:
            ml_name
                Required Argument.
                Specifies the ML name for eval_params generation.
                Types: str

            target_column
                Required Argument.
                Specifies the target column.
                Types: str
            
            task_type:
                Required Argument.
                Specifies the task type for AutoML, whether to apply regresion 
                or classification on the provived dataset.
                Default Value: "Regression"
                Permitted Values: "Regression", "Classification"
                Types: str

        RETURNS:
            dict containing, eval_params for ML model.
        """ 
        # Setting the eval_params
        eval_params = {"id_column": "id",
                        "accumulate": target_column}

        # For Classification
        if task_type.lower() != "regression":
            if ml_name == 'xgboost':
                eval_params['model_type'] = 'Classification'
                eval_params['object_order_column'] = ['task_index', 'tree_num', 'iter','class_num', 'tree_order']
            else:
                if ml_name == 'glm':
                    eval_params['family'] = 'BINOMIAL'
                    
                eval_params['output_prob'] = True
        else:
        # For Regression
            if ml_name == 'xgboost':
                eval_params['model_type'] = 'Regression'
                eval_params['object_order_column'] = ['task_index', 'tree_num', 'iter', 'tree_order']
                
        return eval_params