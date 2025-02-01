from flask_restx import Namespace
from flask_restx import Resource
from flask_restx import fields
from flask import request
from utils.app_config import AppConfig
from utils.app_logger import setup_logger

config = AppConfig()
logger = setup_logger('DBRoutes')
root = config.database_endpoints.root
endpoints = config.database_endpoints

table_ns = Namespace('Table', path=root, description='Operations for a single table')

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