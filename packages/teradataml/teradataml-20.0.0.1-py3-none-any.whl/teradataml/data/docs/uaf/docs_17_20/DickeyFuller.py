def DickeyFuller(data=None, data_filter_expr=None, algorithm=None, 
                 max_lags=None, drift_trend_formula=None, 
                 **generic_arguments):
    """
    DESCRIPTION:
        The DickeyFuller() function tests for the presence of one or more
        unit roots in a series to determine if the series is non-stationary.
        When a series contains unit roots, it is non-stationary. When a series
        contains no unit roots, whether the series is stationary is based on
        other factors.

        The following procedure is an example of how to use DickeyFuller() function:
            * Run regression tests.
            * Determine the algorithm for Dickey Fuller statistic data.
            * Run DickeyFuller() function using the algorithm.
            * (Result shows series contains unit roots) Use DIFF() and
              SeasonalNormalize() functions to remove unit roots.


    PARAMETERS:
        data:
            Required Argument.
            Speciifes a single logical-runtime series as an input.
            Types: TDSeries

        data_filter_expr:
            Optional Argument.
            Specifies the filter expression for "data".
            Types: ColumnExpression

        algorithm:
            Required Argument.
            Specifies the type of regression that is run for the test.
            Permitted Values:
                * NONE: Random walk
                * DRIFT: Random walk with drift
                * TREND: Random walk with linear trend
                * DRIFTNTREND: Random walk with drift and trend
                * FORMULA: Random walk with selected drift, trend and
                           auxiliary lags
            Types: str

        max_lags:
            Optional Argument.
            Specifies the maximum number of lags to use with the regression
            equation.
            Types: int

        drift_trend_formula:
            Optional Argument.
            Specifies the formula used to represent the drift and trend portions
            of the regression.
            Note:
                * Valid only when "algorithm" is set to 'formula'.
            Types: str

        **generic_arguments:
            Specifies the generic keyword arguments of UAF functions.
            Below are the generic keyword arguments:
                persist:
                    Optional Argument.
                    Specifies whether to persist the results of the
                    function in a table or not. When set to True,
                    results are persisted in a table; otherwise,
                    results are garbage collected at the end of the
                    session.
                    Note that, when UAF function is executed, an 
                    analytic result table (ART) is created.
                    Default Value: False
                    Types: bool

                volatile:
                    Optional Argument.
                    Specifies whether to put the results of the
                    function in a volatile ART or not. When set to
                    True, results are stored in a volatile ART,
                    otherwise not.
                    Default Value: False
                    Types: bool

                output_table_name:
                    Optional Argument.
                    Specifies the name of the table to store results. 
                    If not specified, a unique table name is internally 
                    generated.
                    Types: str

                output_db_name:
                    Optional Argument.
                    Specifies the name of the database to create output 
                    table into. If not specified, table is created into 
                    database specified by the user at the time of context 
                    creation or configuration parameter. Argument is ignored,
                    if "output_table_name" is not specified.
                    Types: str


    RETURNS:
        Instance of DickeyFuller.
        Output teradataml DataFrames can be accessed using attribute 
        references, such as DickeyFuller_obj.<attribute_name>.
        Output teradataml DataFrame attribute name is:
            1. result


    RAISES:
        TeradataMlException, TypeError, ValueError


    EXAMPLES:
        # Notes:
        #     1. Get the connection to Vantage to execute the function.
        #     2. One must import the required functions mentioned in
        #        the example from teradataml.
        #     3. Function will raise error if not supported on the Vantage
        #        user is connected to.

        # Check the list of available UAF analytic functions.
        display_analytic_functions(type="UAF")

        # Load the example data.
        load_example_data("uaf","timeseriesdatasetsd4")

        # Create teradataml DataFrame object.
        df = DataFrame.from_table("timeseriesdatasetsd4")

        # Create teradataml TDSeries object.
        data_series_df = TDSeries(data=df,
                                  id="dataset_id",
                                  row_index="seqno",
                                  row_index_style= "SEQUENCE",
                                  payload_field="magnitude",
                                  payload_content="REAL")

        # Example 1 : Determine whether the series is non-stationary by testing
        #             for the presence of the unit roots using random walk with
        #             linear trend for regression.
        uaf_out = DickeyFuller(data=data_series_df,
                               algorithm='TREND')

        # Print the result DataFrame.
        print(uaf_out.result)
    
    """
    