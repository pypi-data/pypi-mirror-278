def GoldfeldQuandt(data=None, data_filter_expr=None, 
                   orig_regr_paramcnt=None, weights=False, formula=None, 
                   algorithm=None, start_idx=None, omit=None, 
                   significance_level=None, test="GREATER",
                   **generic_arguments):
    """
    DESCRIPTION:
        The GoldfeldQuandt() function is a statistical test to determine
        a regression model with the Best Linear Unbiased Estimator (BLUE).
        The test checks for homoscedasticity (constant variance) in
        regression analyses.


    PARAMETERS:
        data:
            Required Argument.
            Specifies an input time series to be tested for
            heteroscedasticity. The "row_axis" determines
            the order of TDSeries data.
            Types: TDSeries

        data_filter_expr:
            Optional Argument.
            Specifies the filter expression for "data".
            Types: ColumnExpression

        orig_regr_paramcnt:
            Required Argument.
            Specifies the number of responses and explanatory variables
            present in the original regression.
            Types: int

        weights:
            Optional Argument.
            Specifies whether the last series found in the payload
            is to be interpreted as a series of weights that can
            be used to perform a weighted least squares regression
            solution. When set to True, the last series is interpreted
            as series of weights, otherwise not.
            Default Value: False
            Types: bool

        formula:
            Required Argument.
            Specifies the formula used in the regression operation.
            The name of the response variable must always be Y,
            and the name of the explanatory variable must always be X1.
            For example, "Y = B0 + B1 * X1".
            Notes:
                * The "formula" argument must be specified along with the 
                  "algorithm" argument.
                * Use the following link to refer the formula rules:
                  "https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Teradata-VantageTM-Unbounded-Array-Framework-Time-Series-Reference-17.20/Mathematic-Operators-and-Functions/Formula-Rules"
            Types: str

        algorithm:
            Required Argument.
            Specifies the algorithm used for the regression.
            Permitted Values:
                1. QR: QR decomposition is used for the regression.
                2. PSI: pseudo-inverse based on singular value
                   decomposition (SVD) is used to solve the regression.
            Types: str

        start_idx:
            Optional Argument.
            Specifies the split-point index for the function. 
            When argument is:
                * less than 1.0, then the split-point index is calculated as:
                    split_point_index = start_idx * N
                    Where, 'N' is the total number of sample rows.
                * greater than 1.0, then "start_idx" is the split-point index.
                * not specified, then split-point index is calculate as:
                    start_idx = (N - omit) / 2
                    Where, 'N' is the total number of entries in the data series.
            Types: float

        omit:
            Required Argument.
            Specifies the number of central sample values to omit when
            forming the two test groups. 
            When argument is:
                * less than 1.0, then the number of samples to be omitted is
                  calculated as:
                    omit_sample_count = omit * N
                    Where 'N' is the total number of entries in the data series
                * greater than 1.0, then "omit" is interpreted as number of 
                  central points to omit.
            Types: float

        significance_level:
            Required Argument.
            Specifies the significance level for the test.
            Types: float

        test:
            Optional Argument.
            Specifies the test method for Goldfeld-Quandt test 
            statistic computation and hypothesis evaluation.
            Permitted Values:
                * GREATER: If the Goldfeld-Quandt test-statistic is less
                           than the higher critical value, the null hypothesis
                           is accepted, and there is no evidence of
                           heteroscedastic variance.
                           If the Goldfeld-Quandt test statistic is greater
                           than or equal to the critical value, then the null 
                           hypothesis is rejected, and there is evidence of 
                           heteroscedastic variance.
                * LESS: If the Goldfeld-Quandt test-statistic is greater than
                        the lower critical value, the null hypothesis is accepted,
                        and there is no evidence of heteroscedastic variance.
                        If the Goldfeld-Quandt test statistic is less than or
                        equal to than the critical value, then the null hypothesis
                        is rejected, and there is evidence of heteroscedastic
                        variance.
                * TWOSIDED: If the Goldfeld-Quandt test-statistic is greater than
                            the lower tail critical value and less than the higher
                            tail critical value, the null hypothesis is accepted,
                            and there is no evidence of heteroscedastic variance.
                            If the Goldfeld-Quandt test statistic is less than or
                            equal to the lower tail critical value or greater than
                            or equal to the high tail critical value, then the
                            null hypothesis is rejected, and there is evidence
                            of heteroscedastic variance.
            Default Value: GREATER
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
        Instance of GoldfeldQuandt.
        Output teradataml DataFrames can be accessed using attribute 
        references, such as GoldfeldQuandt_obj.<attribute_name>.
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
        load_example_data("uaf", ["gq_t1"])

        # Create teradataml DataFrame object.
        data = DataFrame.from_table("gq_t1")

        # Example 1: Execute the GoldfeldQuandt() function on TDSeries input
        #            to check for homoscedasticity in regression analyses.
        # Create teradataml TDSeries object.
        data_series_df = TDSeries(data=data,
                                 id="series_id",
                                 row_index="row_i",
                                 row_index_style="SEQUENCE",
                                 payload_field=["y1", "x1"],
                                 payload_content="MULTIVAR_REAL")

        # Execute GoldfeldQuandt for TDGenSeries.
        uaf_out = GoldfeldQuandt(data=data_series_df,
                                 formula="Y = B0 + B1*X1",
                                 omit=2.0,
                                 significance_level=0.05,
                                 orig_regr_paramcnt=2,
                                 algorithm="QR")

        # Print the result DataFrame.
        print(uaf_out.result)
    
    """
    