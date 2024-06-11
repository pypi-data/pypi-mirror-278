# import necessary modules
import logging


from peliqan.client import WritebackClient, BackendServiceClient, DBClient, SFTPClient, PeliqanTrinoDBClient
from peliqan.exceptions import PeliqanClientException
from peliqan.utils import empty, _retry_get_resource_status

# get logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False

# get log handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)

# set log format
formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s %(message)s")

# set format to log handler
sh.setFormatter(formatter)

# add handler to logger
logger.addHandler(sh)


class BasePeliqanClient:
    """
    This base class wraps all operations we want to expose to our internal and external clients.
    """

    def __init__(self, jwt, backend_url):
        self.JWT = jwt
        self.BACKEND_URL = backend_url
        self.DW_ID = None
        """
        Id of the Peliqan provisioned data warehouse.
        """
        self.__service_client__ = BackendServiceClient(jwt, backend_url)

    def find_resource(self, resource_type, resource_id=None, resource_name=None, **kwargs):
        """

           :param resource_type: can be connection/database/table.
           :param resource_id: id of the resource.
           :param resource_name: name of the resource.
           :param kwargs: additional kwargs can also be passed.
           :return: resource details as a dict.
        """
        return self.__service_client__.find_resource(resource_type, resource_id, resource_name, **kwargs)

    # todo allow user to set a PK column for the query (or update the guessed PK)
    def load_table(self, db_name='', schema_name='', table_name='', query='',
                   df=False, fillna_with=None, fillnat_with=None,
                   enable_python_types=True, enable_datetime_as_string=True, tz='UTC'):

        trino_db = self.trinoconnect()
        return trino_db.fetch(db_name=db_name, schema_name=schema_name, table_name=table_name,
                              query=query, df=df,
                              fillna_with=fillna_with, fillnat_with=fillnat_with,
                              enable_python_types=enable_python_types,
                              enable_datetime_as_string=enable_datetime_as_string, tz=tz)

    # todo: make it easier to find table & field ids in UI
    def update_cell(self, row_pk, value, schema_id=None, schema_name=None, table_id=None, table_name=None,
                    field_id=None, field_name=None):
        if row_pk is empty:
            raise PeliqanClientException("'row_pk' must be provided.")

        # BACKEND_URL and JWT are prepended to the generated script,
        # see create_script() --> transform_script() in peliqan/convert_raw_script.py
        base_url = f"{self.BACKEND_URL}/api/database/rows/table/%s/"

        if not schema_id and not schema_name:
            raise PeliqanClientException("schema_id or schema_name must be provided as kwargs")

        if not table_id and not table_name:
            raise PeliqanClientException("table_id or table_name must be provided as kwargs")
        elif not table_id and table_name:
            # only do this if table_id is not provided
            table_id = self.__service_client__.get_cached_results('table', table_name, 'table_id')

        if not table_id:
            lookup_data = self.find_resource(
                'table',
                resource_id=table_id, resource_name=table_name,
                schema_id=schema_id, schema_name=schema_name,
                field_id=field_id, field_name=field_name
            )
            table_id = lookup_data['table_id']

        # # prioritise field id
        if field_id:
            lookup_data = self.find_resource(
                'table',
                resource_id=table_id, resource_name=table_name,
                schema_id=schema_id, schema_name=schema_name,
                field_id=field_id, field_name=field_name
            )
            field_name = lookup_data['table_id']['field_name']

        if not field_name:
            raise PeliqanClientException("field_id or field_name must be provided as kwargs")

        # set the final url
        if isinstance(table_id, int):
            raise PeliqanClientException("table_id could not be resolved, please check provided arguments.")

        # set table_id to base url
        url = base_url % table_id

        data = {
            'pk': row_pk,
            'data': {
                field_name: value
            }
        }
        return self.__service_client__.update_record(url, data)

    def get_refresh_connection_status(self, connection_name=None, connection_id=None, task_id=''):
        base_url = f"{self.BACKEND_URL}/api/servers/%s/syncdb/status/"

        return self.__service_client__.get_refresh_resource_task_status(
            resource_type='connection',
            refresh_baseurl=base_url,
            resource_name=connection_name,
            resource_id=connection_id,
            task_id=task_id
        )

    def get_refresh_database_status(self, connection_name=None, database_name=None, database_id=None, task_id=''):
        base_url = f"{self.BACKEND_URL}/api/applications/%s/syncdb/status/"
        return self.__service_client__.get_refresh_resource_task_status(
            resource_type='database',
            refresh_baseurl=base_url,
            resource_name=database_name,
            resource_id=database_id,
            task_id=task_id,
            connection_name=connection_name
        )

    def get_refresh_schema_status(self, connection_name=None, database_name=None, schema_name=None, schema_id=None,
                                  task_id=''):
        base_url = f"{self.BACKEND_URL}/api/database/schemas/%s/syncdb/status/"
        return self.__service_client__.get_refresh_resource_task_status(
            resource_type='schema',
            refresh_baseurl=base_url,
            resource_name=schema_name,
            resource_id=schema_id,
            task_id=task_id,
            connection_name=connection_name,
            database_name=database_name
        )

    def get_refresh_table_status(self, connection_name=None, database_name=None, schema_name=None, table_name=None,
                                 table_id=None, task_id=''):
        base_url = f"{self.BACKEND_URL}/api/database/tables/%s/syncdb/status/"
        return self.__service_client__.get_refresh_resource_task_status(
            resource_type='table',
            refresh_baseurl=base_url,
            resource_name=table_name,
            resource_id=table_id,
            task_id=task_id,
            connection_name=connection_name,
            database_name=database_name,
            schema_name=schema_name
        )



    def _refresh_connection(self, base_url, connection_id, connection_name, is_async):
        response = self.__service_client__.refresh_resource(
            resource_type='connection',
            refresh_baseurl=base_url,
            resource_name=connection_name,
            resource_id=connection_id
        )

        if not is_async:
            response = _retry_get_resource_status(
                lambda: self.get_refresh_connection_status(
                    connection_name=connection_name,
                    connection_id=connection_id,
                    task_id=response.get('task_id'))
            )

        return response

    def run_pipeline(self, connection_name=None, connection_id=None, tables=None, is_async=True):
        if not isinstance(tables, (list, tuple, type(None))):
            tables = [tables]

        tables = ','.join(table for table in tables) if tables else ""
        pipeline = "true"

        base_url = (
            f"{self.BACKEND_URL}/api/servers/%s/syncdb/?pipeline={pipeline}&tables={tables}"
        )

        return self._refresh_connection(base_url, connection_id, connection_name, is_async)

    def refresh_connection(
        self,
        connection_name=None,
        connection_id=None,
        is_async=True,
    ):

        base_url = (
            f"{self.BACKEND_URL}/api/servers/%s/syncdb/"
        )

        return self._refresh_connection(base_url, connection_id, connection_name, is_async)

    def refresh_database(self, connection_name=None, database_name=None, database_id=None, is_async=True):
        base_url = f"{self.BACKEND_URL}/api/applications/%s/syncdb/"
        response = self.__service_client__.refresh_resource(resource_type='database', refresh_baseurl=base_url,
                                                            resource_name=database_name, resource_id=database_id,
                                                            connection_name=connection_name)

        if not is_async:
            response = _retry_get_resource_status(
                lambda: self.get_refresh_database_status(connection_name=connection_name, database_name=database_name,
                                                         database_id=database_id, task_id=response.get('task_id'))
            )

        return response

    def refresh_schema(self, connection_name=None, database_name=None, schema_name=None, schema_id=None, is_async=True):

        base_url = f"{self.BACKEND_URL}/api/database/schemas/%s/syncdb/"
        response = self.__service_client__.refresh_resource(resource_type='schema', refresh_baseurl=base_url,
                                                            resource_name=schema_name, resource_id=schema_id,
                                                            database_name=database_name,
                                                            connection_name=connection_name)

        if not is_async:
            response = _retry_get_resource_status(
                lambda: self.get_refresh_schema_status(connection_name=connection_name, database_name=database_name,
                                                       schema_name=schema_name, schema_id=schema_id,
                                                       task_id=response.get('task_id'))
            )

        return response

    def refresh_table(self, connection_name=None, database_name=None, schema_name=None,
                      table_name=None, table_id=None, is_async=True):

        base_url = f"{self.BACKEND_URL}/api/database/tables/%s/syncdb/"
        response = self.__service_client__.refresh_resource(resource_type='table', refresh_baseurl=base_url,
                                                            resource_name=table_name, resource_id=table_id,
                                                            database_name=database_name, schema_name=schema_name,
                                                            connection_name=connection_name)

        if not is_async:
            response = _retry_get_resource_status(
                lambda: self.get_refresh_table_status(connection_name=connection_name, database_name=database_name,
                                                      schema_name=schema_name, table_name=table_name, table_id=table_id,
                                                      task_id=response.get('task_id'))
            )

        return response

    def connect(self, connection=None):
        """
        :param connection: name of the Connection added in Peliqan under Admin > Connections.
        Or a dict with connection properties (credentials etc.).
        """
        if not connection:
            raise PeliqanClientException("connection must be set.")
        connector = WritebackClient(connection, self.JWT, self.BACKEND_URL)
        return connector

    def dbconnect(self, connection=None):
        """
        :param connection: name of the Connection added in Peliqan under Admin > Connections.
        Or a dict with connection properties (credentials etc.).
        """
        if not connection:
            raise PeliqanClientException("connection must be set.")
        connector = DBClient(connection, self.JWT, self.BACKEND_URL)
        return connector

    def trinoconnect(self):
        return PeliqanTrinoDBClient(None, self.JWT, self.BACKEND_URL)

    def sftpconnect(self, connection=None):
        """
        :param connection: name of the Connection added in Peliqan under Admin > Connections.
        Or a dict with connection properties (credentials etc.).
        """
        if not connection:
            raise PeliqanClientException("connection must be set.")
        connector = SFTPClient(connection, self.JWT, self.BACKEND_URL)
        return connector

    def _validate_and_lookup_table(self, table_id, table_name):
        if not table_id and not table_name:
            raise PeliqanClientException("table_id or table_name must be provided as kwargs")
        elif not table_id and table_name:
            # only do this if table_id is not provided
            table_id = self.__service_client__.get_cached_results('table', table_name, 'table_id')

        if not table_id:
            lookup_data = self.find_resource('table', resource_id=table_id, resource_name=table_name)
            table_id = lookup_data['table_id']

        if type(table_id) != int:
            raise PeliqanClientException("table_id could not be resolved, please check provided arguments.")

        return table_id

    def _validate_writeback_status(self, writeback_status):
        error = False
        if type(writeback_status) == list:
            writeback_status_str = ''
            for w in writeback_status:
                w_status = w.upper()
                if w_status not in ["NOT_PROCESSED", "PROCESSED", "CONFIRMED", "FAILED"]:
                    error = True
                    break
                else:
                    writeback_status_str += w_status + ','
            writeback_status = writeback_status_str.rstrip(',')
        elif (
            writeback_status is not None and
            (
                type(writeback_status) != str or writeback_status.upper() not in
                ["NOT_PROCESSED", "PROCESSED", "CONFIRMED", "FAILED"]
            )
        ):
            error = True

        if error:
            raise PeliqanClientException(
                f"writeback_status is not valid. "
                f"Allowed status values are "
                f"'NOT_PROCESSED', 'PROCESSED', 'CONFIRMED', 'FAILED'."
            )

        return writeback_status

    def list_changes(self, table_id=None, table_name=None, writeback_status=None, change_type=None,
                     latest_changes_first=False):
        """
        List the cdc changes in order.
        Optionally, pass writeback_status and/or change_type as a string or list of strings.

        :param table_id: unique integer identifier for a table
        :param table_name: the name or fqn of the table.
        :param writeback_status: valid string or list of string values
        :param change_type: valid string or list of string values
        :param latest_changes_first: use this to get toggle the order of changes (Asc/Desc of id). default is False.
        :return:
        """

        error = False
        # i = insert, u = update, d = delete, t = transformation, f = formula, l = link (to another table)
        # m = multiselect
        if type(change_type) is list:
            change_type_str = ''
            for c in change_type:
                c_type = c.lower()
                if c_type not in ["i", "u", "d", "f", "t", "m", "l"]:
                    error = True
                    break
                else:
                    change_type_str += c_type + ','

            change_type = change_type_str.rstrip(',')
        elif (
            change_type is not None and
            (type(change_type) is not str or change_type.lower() not in ["i", "u", "d", "f", "t", "m", "l"])
        ):
            error = True

        if error:
            raise PeliqanClientException(
                f"change_type is not valid. Allowed status values are 'i', 'u', 'd', 'f', 't', 'm', 'l'.\n"
                f"i = insert, u = update, d = delete, t = transformation, f = formula, l = link (to another table)"
                f"m = multiselect."
            )

        writeback_status = self._validate_writeback_status(writeback_status)

        table_id = self._validate_and_lookup_table(table_id, table_name)

        return self.__service_client__.get_cdclogs(table_id=table_id, writeback_status=writeback_status,
                                                   change_type=change_type, latest_changes_first=latest_changes_first)

    def update_writeback_status(self, change_id, writeback_status, table_id=None, table_name=None):
        """
        Update the writeback_status for a cdc log.

        :param change_id: unique integer identifier for a cdc log.
        :param writeback_status: valid status value.
        :param table_id: unique integer identifier for a table
        :param table_name: the name or fqn of the table.
        :return:
        """
        table_id = self._validate_and_lookup_table(table_id, table_name)
        if (
            type(writeback_status) is not str or
            writeback_status.upper() not in ["NOT_PROCESSED", "PROCESSED", "CONFIRMED", "FAILED"]
        ):
            raise PeliqanClientException(
                f"writeback_status is not valid. "
                f"Allowed status values are "
                f"'NOT_PROCESSED', 'PROCESSED', 'CONFIRMED', 'FAILED'."
            )

        try:
            change_id = int(change_id)
        except ValueError:
            raise PeliqanClientException("change_id must be a valid integer")

        return self.__service_client__.update_writeback_status(table_id, change_id, writeback_status)

    def list_connections(self):
        """
        Returns a list of servers in the account.

        :return: list of databases
        """
        return self.__service_client__.list_servers()

    def list_databases(self):
        """
        Returns a list of all databases in the account including tables and fields in tables.

        :return: list of databases
        """
        return self.__service_client__.list_databases()

    def get_schema(self, schema_id):
        """
        Returns all meta-data for a schema.

        :return: schema meta-data
        """
        return self.__service_client__.get_schema(schema_id)

    def get_table(self, table_id):
        """
        Returns all meta-data for a table including fields.

        :return: table meta-data
        """
        return self.__service_client__.get_table(table_id)

    def update_field(self, field_id, description=None, tags=None):
        """
        Updates a field (column).

        :param field_id: required, integer, id of the field to update
        :param description: optional, string, description of the field (data catalog metadata)
        :param tags: optional, array of strings, tags assigned to the field (data catalog metadata)
        :return: result of update
        """

        return self.__service_client__.update_field_metadata(field_id, description, tags)

    def update_table(
        self,
        table_id,
        name=None,
        query=None,
        primary_field_id=None,
        settings=None,
        description=None,
        tags=None,
        run_on_peliqan_trino=empty,
        materialize=empty
    ):
        """
        Updates a table.

        :param table_id: required, integer, id of the table to update
        :param name: optional, string, new name of the table
        :param query: optional, string, new SQL query for tables of type 'query'
        :param primary_field_id: optional, integer, primary key field id for this table, i.e. the field id in Peliqan.
        See, table details page in Peliqan to get the primary_field_id for a table.
        :param settings: optional, string (json), settings of the table
        :param description: optional, string, description of the table (data catalog metadata)
        :param tags: optional, array of strings, tags assigned to the table (data catalog metadata)
        :param run_on_peliqan_trino: optional, boolean, whether the query should run on the native engine or trino engine.
        :param materialize: optional, boolean,  whether the query should be materialized as a table into a database.

        :return: result of update
        """

        update_result_dict = {}
        update_metadata_result_dict = {}
        if name or query or settings or run_on_peliqan_trino != empty or materialize != empty:
            update_result_dict = self.__service_client__.update_table(
                table_id,
                name,
                query,
                settings,
                run_on_peliqan_trino,
                materialize
            )
        if description or tags or primary_field_id:
            update_metadata_result_dict = self.__service_client__.update_table_metadata(
                table_id,
                description,
                tags,
                primary_field_id
            )
        return {**update_result_dict, **update_metadata_result_dict}

    def update_schema(self, schema_id, name):
        """
        Updates a schema.

        :param schema_id: required, integer, id of the schema to update
        :param name: required, new name of the schema
        :return: result of update
        """

        return self.__service_client__.update_schema(schema_id, name)

    def update_database(self, database_id, description=None, tags=None):
        """
        Updates a database.

        :param database_id: required, integer, id of the database to update
        :param description: optional, string, description of the database (data catalog metadata)
        :param tags: optional, array of strings, tags assigned to the database (data catalog metadata)
        :return: result of update
        """

        return self.__service_client__.update_database_metadata(database_id, description, tags)

    def list_scripts(self):
        return self.__service_client__.list_interfaces()

    def get_script(self, script_id=None, script_name=None):
        if not script_id and not script_name:
            raise PeliqanClientException("'script_id' or 'script_name' must be provided")

        if not script_id and script_name:
            script_id = self.__service_client__.get_cached_results('interface', script_name, 'interface_id')

        if not script_id:
            interface_data = self.__service_client__.find_resource('interface', resource_name=script_name)
            script_id = interface_data['interface_id']

        return self.__service_client__.get_interface(script_id)

    def update_script(
        self,
        script_id,
        name=empty,
        group=empty,
        raw_script=empty,
        settings=empty,
        state=empty,
        flow=empty,
        editor=empty
    ):
        """
        A function to update a script in Peliqan.

        :param script_id: The id of the script that needs to be updated.
        :param name: A string value that represents the new name of the script.
        :param group: The new group id that the script should belong to.
        :param raw_script: The python code that should be associated with this script.
        :param settings: Update the script run schedule settings.
        :param state: Update the state of the script.
        :param flow: The json settings associated with the visual flow editor.
        :param editor: An enum value that decides which editor type must be opened in the Peliqan code editor.
        Options: [RAW_SCRIPT_EDITOR, FLOW_EDITOR]
        :return:
        """
        return self.__service_client__.update_interface(
            script_id,
            name=name,
            group=group,
            raw_script=raw_script,
            settings=settings,
            state=state,
            flow=flow,
            editor=editor
        )

    def add_script(self, group_id, name, run_mode='STREAMLIT', script_type='streamlit'):
        """

        :param group_id: The group the script will belong to.
        :param name: The name of the new script.
        :param script_type: An enum value that decides the type of script. Options: [streamlit]
        :param run_mode:  An enum value that decides whether the script will be triggered by an API or a streamlit app.
        Options: [STREAMLIT, API, SHELL]
        :return:
        """
        return self.__service_client__.create_interface(
            group_id,
            name=name,
            type=script_type,
            run_mode=run_mode
        )

    def add_query_table(
        self,
        table_name,
        query,
        database_id=None,
        schema_id=None,
        run_on_peliqan_trino=empty,
        materialize=empty,
    ):
        return self.__service_client__.create_query(
            table_name=table_name,
            query=query,
            database_id=database_id,
            schema_id=schema_id,
            run_on_peliqan_trino=run_on_peliqan_trino,
            materialize=materialize
        )

    def generate_sql_union(self, table_ids, sources=None):
        """
        Generates an SQL UNION query for the given tables.
        All columns of all tables will be added to the UNION query.
        If a column does not exist in one of the tables, it will be added with a null value.
        Optionally, a "source" column can be added to indicate from which table each row originated.

        :param table_ids: required, list of integers, list of table ids to include in UNION query
        :param sources: optional, dict, if set an extra 'source' column will be added to indicate to which table the record belongs. Keys are table ids. Values are source value to include in UNION result. Example: { 1: "Paris", 2: "London" }. This will add a column "source" to the UNION where all records from table id 1 will have value "Paris" for the source.
        :return: result of update
        """

        tables = []
        fields = []
        field_types = {}
        fields_to_cast = []
        for table_id in table_ids:
            table = self.get_table(table_id)
            tables.append(table)
            for field in table["all_fields"]:
                if field["name"] not in fields:
                    fields.append(field["name"])
                    if field["sql_data_type"]:
                        # Actual field type in source, e.g. timestamp, timestamptz...
                        # (might not be available for all sources)
                        field_types[field["name"]] = field["sql_data_type"]
                    else:
                        # Peliqan field type, e.g. "date"
                        field_types[field["name"]] = field["type"]
                elif (
                    field["sql_data_type"] and field["sql_data_type"] != field_types[field["name"]]
                ) or field["type"] != field_types[field["name"]]:
                    fields_to_cast.append(field["name"])

        table_selects = []
        for table in tables:
            table_select_fields = []
            if sources:
                source_name = ""
                for source_table_id, source_table_name in sources.items():
                    if int(source_table_id) == table['id']:
                        source_name = source_table_name
                table_select_fields.append("'%s'" % source_name + " source")
            for field in fields:
                table_has_field = False
                for table_field in table["all_fields"]:
                    if (
                        field[0] == '"' and table_field["name"] == field) or (
                        field[0] != '"' and table_field["name"].lower() == field.lower()
                    ):
                        table_has_field = True
                        break
                if table_has_field:
                    if field in fields_to_cast:
                        if table_field["sql_data_type"] and table_field["sql_data_type"] == "timestamptz":
                            # Postgres fields of type timestamptz (timestamp with timezone)
                            # cannot be cast to varchar directly by Trino
                            table_select_fields.append("CAST(CAST(%s AS TIMESTAMP) AS VARCHAR) AS %s" % (field, field))
                        else:
                            table_select_fields.append("CAST(%s AS VARCHAR) AS %s" % (field, field))
                    else:
                        table_select_fields.append(field)
                else:
                    table_select_fields.append("null " + field)
            table_select_fields_str = ", ".join(table_select_fields)

            table_select = "SELECT %s FROM %s" % (table_select_fields_str, table["name"])
            table_selects.append(table_select)

        union = " UNION ALL ".join(table_selects)
        return union

    def get_interface_state(self, interface_id):
        """
        An interface is a saved program. Get the stored state for a specific interface.

        :param interface_id: The id of the interface.
        :return: Any
        """
        return self.__service_client__.get_interface_state(interface_id)

    def set_interface_state(self, interface_id, state):
        """
        An interface is a saved program. Set the state for a specific interface in the peliqan environment.

        :param interface_id: The id of the interface.
        :param state: The data that will be stored as the state value for an interface.
        :return:
        """
        return self.__service_client__.set_interface_state(interface_id, state)

    def get_pipeline_logs(self, pipeline_run_id):
        """
        Retrieves the pipeline logs of a SaaS connection.

        :param pipeline_run_id: id of the pipeline run.

        :return: logs of the pipeline
        """
        return self.__service_client__.get_pipeline_logs(pipeline_run_id)

    def get_pipeline_runs(self, connection_name=None, connection_id=None, page=1, per_page=10):
        """
        Retrieves the pipeline logs of a SaaS connection.

        :param connection_name: string, name of the source connection.
        :param connection_id: integer, id of the source connection.
        :param page: integer, the page number to fetch.
        :param per_page: integer, the number of results per page.
        :return: list of pipeline runs
        """
        if not connection_id and connection_name:
            response = self.find_resource('connection', resource_id=connection_id, resource_name=connection_name)
            connection_id = response['connection_id']

        return self.__service_client__.get_pipeline_runs(connection_id, page, per_page)

    def get_script_runs(self, script_id=None, page=1, per_page=10):
        return self.__service_client__.get_interface_runs(script_id, page, per_page)

    def send_connection_invite(
        self,
        recipient,
        subject,
        message,
        confirmation_recipient,
        server_type
    ):

        return self.__service_client__.send_connection_invite(
            recipient,
            subject,
            message,
            confirmation_recipient,
            server_type
        )

    def get_or_create_schema(self, schema_name, database_name=None, database_id=None):
        if not database_id and not database_name:
            raise PeliqanClientException("'database_name' or 'database_id' must be provided.")

        if not database_id and database_name:
            response = self.find_resource('database', resource_name=database_name)
            database_id = response['database_id']

        try:
            url = f"{self.BACKEND_URL}/api/database/schemas/database/{database_id}/"
            response = self.__service_client__.call_backend("POST", url, json={'schema_name': schema_name})
        except PeliqanClientException as e:
            if 'ERROR_SCHEMA_ALREADY_EXISTS' not in str(e):
                raise

            response = self.__service_client__.find_schema(database_id=database_id, schema_name=schema_name)
            schema_id = response.get('schema_id')
            if schema_id:
                response = self.get_schema(schema_id)

        return response

    def upsert_query_table(
        self,
        table_name,
        query,
        schema_id=None,
        schema_name=None,
        database_id=None,
        database_name=None,
        run_on_peliqan_trino=empty,
        materialize=empty
    ):

        if not database_id and not database_name and not schema_id and not schema_name:
            schema_name = "My Queries"  # default `My Queries` schema in database
            database_id = self.DW_ID

        try:
            response = self.__service_client__.find_table_or_field(
                database_id=database_id,
                database_name=database_name,
                schema_id=schema_id,
                schema_name=schema_name,
                table_name=table_name
            )

            table_id = response.get('table_id')
            if table_id:
                response = self.update_table(
                    table_id,
                    name=table_name,
                    query=query,
                    run_on_peliqan_trino=run_on_peliqan_trino,
                    materialize=materialize
                )

        except PeliqanClientException as e:
            if 'ERROR_TABLE_DOES_NOT_EXIST' not in str(e):
                raise

            if not database_id and database_name:
                try:
                    response = self.find_resource('database', resource_name=database_name)
                    database_id = response['database_id']
                except PeliqanClientException as e:
                    if (
                        'ERROR_APPLICATION_DOES_NOT_EXIST' not in str(e) or
                        "ERROR_DATABASE_DOES_NOT_EXIST" not in str(e)
                    ):
                        raise

            if not schema_id and schema_name:
                try:
                    response = self.find_resource(
                        'schema',
                        resource_name=schema_name,
                        database_name=database_name,
                        database_id=database_id
                    )
                    schema_id = response['schema_id']

                except PeliqanClientException as e:
                    if 'ERROR_SCHEMA_DOES_NOT_EXIST' not in str(e):
                        raise

                    # if not the default schema then perform the schema retrieval
                    if schema_name != 'My Queries':
                        database_id = database_id or self.DW_ID
                        response = self.get_or_create_schema(schema_name, database_id=database_id)
                        schema_id = response['id']

            response = self.add_query_table(
                table_name,
                query,
                database_id=database_id,
                schema_id=schema_id,
                run_on_peliqan_trino=run_on_peliqan_trino,
                materialize=materialize,
            )

        return response

    def discover_object_schema(self, records):
        if not isinstance(records, (list, tuple)):
            records = [records]

        url = f"{self.BACKEND_URL}/api/database/resource/json-schema/"
        return self.__service_client__.call_backend("POST", url, json={'records': records})

