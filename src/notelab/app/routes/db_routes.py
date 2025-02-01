from flask_restx import Namespace, Resource, fields
from flask import request
from notelab.utils.app_logger import setup_logger
from notelab.utils.app_config import AppConfig
from notelab.db.db_handler import DBHandler
from flask_restx import Api

config = AppConfig()
logger = setup_logger('DBRoutes')
root = config.database_endpoints.root
endpoints = config.database_endpoints

tables_ns = Namespace('Tables', path=root, description='Operations related to tables')

schema_ns = Namespace('Table Schema', path=root, description='Schema-related operations')
row_ns = Namespace('Row', path=root, description='Operations for a single row')
rows_ns = Namespace('Rows', path=root, description='Operations for multiple rows')

db = DBHandler('database')
db_path = config.db_path

def init_routes(flask_api: Api):
    flask_api.add_namespace(tables_ns)
    flask_api.add_namespace(schema_ns)
    flask_api.add_namespace(row_ns)
    flask_api.add_namespace(rows_ns)

# POST Response model
generic_response_model = tables_ns.model('TablePostResponse', {
    "message": fields.String(description="Result of the operation", example="Success"),
    "status": fields.Integer(description="HTTP status code", example=200),
})

@tables_ns.route(endpoints.tables)
class TablesResource(Resource):
    def get(self):
        logger.info(f"Fetching tables from {request.url}")
        return db.get_tables()



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