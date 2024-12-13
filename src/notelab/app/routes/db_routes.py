from flask_restx import Namespace, Resource, fields
from flask import request
from utils.app_logger import setup_logger
from utils.app_config import Config
from notelab.db.db_handler import DBHandler
from flask_restx import Api

config = Config()

logger = setup_logger('DBRoutes')
root = config.database_endpoints.root
endpoints = config.database_endpoints

tables_ns = Namespace('Tables', path=root, description='Operations related to tables')
table_ns = Namespace('Table', path=root, description='Operations for a single table')
schema_ns = Namespace('Table Schema', path=root, description='Schema-related operations')
row_ns = Namespace('Row', path=root, description='Operations for a single row')
rows_ns = Namespace('Rows', path=root, description='Operations for multiple rows')

db = DBHandler('database')
db_path = config.db_path
db.connect(db_path)

def init_routes(flask_api: Api):
    flask_api.add_namespace(tables_ns)
    flask_api.add_namespace(table_ns)
    flask_api.add_namespace(schema_ns)
    flask_api.add_namespace(row_ns)
    flask_api.add_namespace(rows_ns)

# POST Response model
generic_response_model = tables_ns.model('TablePostResponse', {
    "message": fields.String(description="Result of the operation", example="Success"),
    "status": fields.Integer(description="HTTP status code", example=200),
})

@table_ns.route(endpoints.tables)
class TablesResource(Resource):
    def get(self):
        logger.info(f"Fetching tables from {request.url}")
        return db.get_tables()

@table_ns.route(endpoints.table)
class TableResource(Resource):

    # GET Response model
    get_response_model = tables_ns.model('TableGetResponse', {
        "tables": fields.List(fields.String, description="List of table names"),
        "status": fields.Integer(description="HTTP status code"),
    })

    @table_ns.marshal_with(get_response_model)
    def get(self, table_name):
        logger.info(f"Fetching table {table_name} from {request.url}")
        return db.get_table(table_name)

    # POST Request model
    post_request_model = tables_ns.model('TablePostRequest', {
        'columns': fields.List(
            fields.String,
            required=True,
            description='List of column definitions (e.g., id INT PRIMARY KEY)',
            example=["id INT PRIMARY KEY", "name VARCHAR(255)", "age INT"]
        ),
    })

    @table_ns.expect(post_request_model)
    @table_ns.marshal_with(generic_response_model)
    def post(self, table_name):
        logger.info(f"Creating table {table_name} from {request.url}")
        if not request.is_json:
            return {"message": "Error: Request must be JSON", "status": 400}
        data = request.get_json()
        columns = data.get('columns')
        if not columns:
            return {"message": "No columns provided.", "status": 400}
        try:
            message, status = db.create_table(table_name, columns=columns)
            return {"message": message, "status": status}
        except Exception as e:
            return {"message": e, "status": 500}

    @table_ns.marshal_with(generic_response_model)
    def delete(self, table_name):
        logger.info(f"Deleting table {table_name} from {request.url}")
        message, status = db.drop_table(table_name)
        return {"message": message, "status": status}

@schema_ns.route(endpoints.table_schema)
class TableSchemaResource(Resource):
    def get(self, table_name):
        logger.info(f"Fetching schema for table {table_name} from {request.url}")
        return db.get_table_schema(table_name)

@row_ns.route(endpoints.row)
class RowResource(Resource):
    def get(self, table_name, row_id):
        logger.info(f"Fetching row {row_id} from {request.url}")
        return db.get_row(table_name, row_id)

@rows_ns.route(endpoints.rows)
class RowsResource(Resource):
    def get(self, table_name):
        logger.info(f"Fetching rows from {request.url}")
        conditions = []
        for key, value in request.args.items():
            condition = f"{key}='{value}'"
            conditions.append(condition)
        return db.get_rows(table_name, conditions)

    def post(self, table_name):
        logger.info(f"Inserting rows into {table_name} from {request.url}")
        if not request.is_json:
            return {"error": "Request must be JSON"}, 400
        data = request.get_json()["rows"]
        return db.insert_rows(table_name, data)

    def put(self, table_name):
        logger.info(f"Updating rows in {table_name} from {request.url}")
        if not request.is_json:
            return {"error": "Request must be JSON"}, 400
        data = request.get_json()["rows"]
        return db.update_rows(table_name, data)