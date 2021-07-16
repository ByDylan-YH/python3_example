import sql_metadata


# 去掉注释
def clean(sql_str):
    # remove the /* */ comments
    q = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", sql_str)
    # remove whole line -- and # comments
    lines = [line for line in q.splitlines() if not re.match("^\s*(--|#)", line)]
    # remove trailing -- and # comments
    q = " ".join([re.split("--|#", line)[0] for line in lines])
    q = ' '.join(q.split())
    return q


if __name__ == '__main__':
    sql = """
    select init_date,fund_account,money_type,stock_code,stock_type,exchange_type,current_amount,correct_amount
    from  hive_cleandb.t_mid_clean_datastock_extend_hv 
    where money_type=0 and part_init_date>initDate and part_init_date<=endDate
    and current_amount+correct_amount>0
    """
    parser_result = sql_metadata.Parser(sql)
    print(parser_result.columns)
    print(parser_result.tables)
    print(parser_result.columns_dict)
    print(parser_result.tables_aliases)
