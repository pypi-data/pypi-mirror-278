def insert_data_in_df(worksheet, dataframe):
    # Insert header
    worksheet.Range(
        worksheet.Cells(1, 1), worksheet.Cells(1, dataframe.columns.shape[0])
    ).Value = dataframe.columns
    dataframe = dataframe.fillna(0)
    worksheet.Range(
        worksheet.Cells(2, 1),
        worksheet.Cells(dataframe.shape[0] + 1, dataframe.shape[1]),
    ).Value = dataframe.values
