import json

from yplib.index import *
from yplib.http_util import *
import pymysql
import adbc_driver_manager
import adbc_driver_flightsql.dbapi as flight_sql

import threading

# 创建一个线程本地存储对象
thread_local = threading.local()


# 有关数据库操作的类
def get_connect(database=None, user=None, password=None, charset='utf8mb4', port=3306, host=None):
    return pymysql.connect(database=database, user=user, password=password, charset=charset, port=port, host=host)


def get_connect_from_config(db_config='stock_db', database=None, user=None, password=None, charset=None, port=None, host=None):
    config_db = get_config_data(db_config)
    database = database if database is not None else config_db['database']
    user = user if user is not None else config_db['user']
    host = host if host is not None else config_db['host']
    password = password if password is not None else config_db['password']
    port = port if port is not None else config_db['port'] if 'port' in config_db else 3306
    charset = charset if charset is not None else config_db['charset'] if 'charset' in config_db else 'utf8mb4'
    return get_connect(database=database, user=user, password=password, charset=charset, port=port, host=host)


# 执行 sql 语句, 并且提交, 默认值提交的了
def exec_sql(sql='', db_conn=None, db_config='stock_db', commit=True, is_log=False, database=None):
    db_cursor = None
    try:
        db_conn = db_conn if db_conn is not None else get_connect_from_config(db_config, database=database)
        if sql is None or sql == '':
            if is_log:
                to_log_file("db_conn is None or sql is None or sql == '', so return")
            return
        db_cursor = db_conn.cursor()
        if isinstance(sql, list) or isinstance(sql, set):
            for s in sql:
                if is_log:
                    to_log_file(s)
                db_cursor.execute(s)
        else:
            if is_log:
                to_log_file(sql)
            db_cursor.execute(str(sql))
        if commit:
            db_conn.commit()
    finally:
        if db_cursor is not None:
            db_cursor.close()
        if db_conn is not None:
            db_conn.close()


def get_doris_conn(db_config='doris'):
    config_db = get_config_data(db_config)
    my_uri = config_db['uri']
    my_db_kwargs = {
        adbc_driver_manager.DatabaseOptions.USERNAME.value: config_db['username'],
        adbc_driver_manager.DatabaseOptions.PASSWORD.value: config_db['password'],
    }
    conn = flight_sql.connect(uri=my_uri, db_kwargs=my_db_kwargs, autocommit=True)
    return conn


# 执行 sql 语句, 并且提交, 默认值提交的了
def exec_doris_sql(sql='', db_config='wh_doris', database='mx_risk'):
    exec_sql(sql, db_config=db_config, database=database)
    # conn = get_doris_conn(db_config)
    # cursor = conn.cursor()
    # cursor.execute(sql)
    # cursor.close()
    # conn.close()


def get_data_from_doris(sql='', db_config='doris'):
    if not hasattr(thread_local, 'conn_doris'):
        thread_local.conn_doris = get_doris_conn(db_config)
    conn_doris = thread_local.conn_doris
    cursor = conn_doris.cursor()
    cursor.execute(sql)
    arrow_data = cursor.fetchallarrow()
    dataframe = arrow_data.to_pandas()
    json_data = dataframe.to_json(orient='records', date_format='iso')
    return json.loads(json_data)


def get_data_line_one_from_doris(sql='', db_config='doris'):
    data_list = get_data_from_doris(sql, db_config=db_config)
    if len(data_list):
        return list(data_list[0].values())
    return None


# 执行 sql 语句, 不提交
def exec_sql_un_commit(sql='', db_conn=None, database=None):
    exec_sql(sql=sql, db_conn=db_conn, commit=False, database=database)


# 执行 sql 获得 数据
def get_data_from_sql(sql='', db_conn=None, db_config='stock_db', is_log=False, database=None):
    db_cursor = None
    try:
        db_conn = db_conn if db_conn is not None else get_connect_from_config(db_config, database=database)
        if sql is None or sql == '':
            if is_log:
                to_log_file("db_conn is None or sql is None or sql == '', so return")
            return
        db_cursor = db_conn.cursor()
        if is_log:
            to_log_file(sql)
        db_cursor.execute(str(sql))
        data = db_cursor.fetchall()
    finally:
        if db_cursor is not None:
            db_cursor.close()
        if db_conn is not None:
            db_conn.close()
    return data


# table_name, column_name_list, type_list, comment_list, column_name_type_comment_list, info_list
def get_table_sql(file_path):
    table_list = []
    r_list = []
    # 普通文件的解析
    d_list = open(file_path, 'r', encoding='utf-8').readlines()
    # 一个 table 的语句
    table_one = []
    is_start = False
    is_end = False
    for i in range(len(d_list)):
        line = d_list[i].strip()
        if line.lower().startswith('CREATE TABLE `'.lower()) and not is_start:
            is_start = True
        if line.lower().endswith(';'.lower()) and not is_end:
            is_end = True
        if is_start:
            table_one.append(line)
        if is_end:
            if len(table_one):
                table_list.append(table_one)
            table_one = []
            is_start = False
            is_end = False
    # 所有的表结构
    for one_table in table_list:
        # table_name, column_name_list, type_list, comment_list, column_name_type_comment_list, info_list
        table_one_list = ['', [], [], [], [], []]
        # 遍历这个表的,解析出这个表结构数据
        for one_sql in one_table:
            # 表名称
            if one_sql.lower().startswith('CREATE TABLE `'.lower()):
                name_match = re.search(r"CREATE TABLE `(\w+)", one_sql)
                if name_match:
                    table_name = name_match.group(1)
                    # 例如 : analyze_report_loan_tmp
                    # 0 : table_name
                    table_one_list[0] = table_name
            else:
                # 列名称
                one_sql = one_sql.strip()
                if one_sql.startswith('`'):
                    column_match = re.search(r"`(\w+)", one_sql)
                    if column_match:
                        column_name = column_match.group(1)
                        # 1 : column_name
                        table_one_list[1].append(column_name)
                        # 例如 : [order_id]
                        c_list = one_sql.split(' ')
                        column_type = c_list[1]
                        # 2 : column_type
                        table_one_list[2].append(column_type)
                        comment = ''
                        comment_index = -1
                        for i in range(len(c_list)):
                            c = c_list[i]
                            if c.lower() == 'COMMENT'.lower():
                                comment_index = i
                        if comment_index != -1:
                            comment = re.findall(r"'(.+?)'", ''.join(c_list[comment_index + 1:]))[0]
                        comment = comment.strip()
                        if not len(comment) and column_name.lower() == 'id':
                            comment = 'id'
                        # 3 : comment
                        table_one_list[3].append(comment)
                        table_one_list[4].append([column_name, column_type, comment])
        table_one_list[5] = one_table
        r_list.append(table_one_list)
    return r_list


# country, table_name_list
def get_country_table(file_path):
    r_list = []
    need_list = to_list_from_txt_with_blank_line(file_path)
    for table_country_list in need_list:
        country = table_country_list[0]
        r_name_list = []
        # 所有的 table_name
        table_name_list = table_country_list[1:]
        # to_log_file(country)
        for table_name in table_name_list:
            table_name = table_name.strip()
            # 脱敏字段
            desense_column_list = []
            is_log = False
            max_id = -1
            is_done = False
            sp_list = [' ', '\t']
            for sp_o in sp_list:
                if sp_o in table_name:
                    b_n_list = table_name.split(sp_o)
                    table_name = b_n_list[0]
                    desense_temp_list = b_n_list[1:]
                    for o_d in desense_temp_list:
                        # 每个 脱敏字段处理一下, 去掉 \t, 等字段
                        for o_r in sp_list:
                            o_d = o_d.replace(o_r, '')
                        if not len(o_d):
                            continue
                        if o_d.startswith('['):
                            o_d = o_d[1:-1]
                        # 是控制字段,
                        if o_d.startswith('--'):
                            o_d = o_d.replace('--', '')
                            # 是否是log,
                            if o_d.lower() == 'log':
                                is_log = True
                            # 是否完成
                            if o_d.lower() == 'done':
                                is_done = True
                            # 是id
                            if o_d.lower().startswith('max_id='):
                                max_id = to_int(o_d.lower()[len('max_id='):])
                        else:
                            desense_column_list = o_d.split(',')
            if not is_done:
                r_name_list.append([table_name, desense_column_list, is_log, max_id])
        r_list.append([country, r_name_list])
    return r_list


# SHOW TABLES; -- 查询所有的表
def do_query(instance_name='merlion-risk-prod', db_name='rsk_admin', sql_content='select * from tb_company limit 100;'):
    csrf_token, session_id = do_get_token()
    cookie = {'csrftoken': csrf_token, 'sessionid': session_id}
    headers = {'X-Csrftoken': csrf_token}
    form_data = {'instance_name': instance_name, 'db_name': db_name, 'sql_content': sql_content, 'limit_num': '0'}
    url = get_config_data('archery_username_password')['url']
    r_json = do_post(url + '/query/', is_form_data=True, headers=headers, cookie=cookie, data=form_data, r_json=True)
    if r_json['status'] != 0:
        to_log_file(r_json)
        return
    rows = r_json['data']['rows']
    column_list = r_json['data']['column_list']
    r_list = []
    for one_rows in rows:
        obj_one = {}
        for i in range(len(one_rows)):
            obj_one[column_list[i]] = one_rows[i]
        r_list.append(obj_one)
    return r_list


def show_create_table(instance_name='ksm-wh', db_name='mx_risk', table_name='tb_model_log'):
    r_list = do_query(instance_name=instance_name, db_name=db_name, sql_content='show create table `{}`;'.format(table_name))
    table_sql = r_list[0]['Create Table']
    table_sql = table_sql if table_sql.endswith(';') else table_sql + ';'
    return table_sql


def do_get_token():
    do_check_token()
    token_json = get_config_data('csrf_token')
    return token_json['csrf_token'], token_json['session_id']


#
def do_check_token():
    token_json = get_config_data('csrf_token')
    if 'time' not in token_json or int(to_datetime().timestamp()) - int(token_json['time']) > 60 * 20:
        do_get_token_from_login()


def do_get_token_from_login():
    user_obj = get_config_data('archery_username_password')
    url = user_obj['url']
    # get 一下,获得 token
    response = do_get_response(url + '/login/')
    csrf_token = next(filter(lambda s: s.split('=')[0].lower() == 'csrftoken', response.headers['Set-Cookie'].split('; '))).split('=')[1]
    cookie = {'csrftoken': csrf_token}
    headers = {'X-Csrftoken': csrf_token}
    form_data = {
        'username': user_obj['username'],
        'password': user_obj['password']
    }
    response = do_post_response(url + '/authenticate/', is_form_data=True, headers=headers, cookie=cookie, data=form_data)
    same_site = next(filter(lambda s: s.split('=')[0].lower() == 'SameSite'.lower(), response.headers['Set-Cookie'].split('; ')))
    session_id = same_site.split(', ')[1].split('=')[1]
    r_obj = {}
    r_obj['csrf_token'] = csrf_token
    r_obj['session_id'] = session_id
    r_obj['time'] = int(to_datetime().timestamp())
    set_config_data('csrf_token', r_obj)
    return csrf_token, session_id
