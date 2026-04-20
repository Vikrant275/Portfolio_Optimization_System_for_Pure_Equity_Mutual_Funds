from flask import Blueprint,jsonify,request
from datetime import datetime
from fetch_servers.auth_user import authenticate
from fetch_servers.Risk_Server.service.risk_service import Risk_Service

risk_bp = Blueprint('risk', __name__)

@risk_bp.route('/risk/<stock>', methods=['GET'])
def risk(stock):
    authenticate()

    try:
        #  GET QUERY PARAMS
        start_str = request.args.get("start")
        end_str = request.args.get("end")

        if not start_str or not end_str:
            return jsonify({
                "error": "start and end parameters required (YYYY-MM-DD)"
            }), 400

        # PARSE DATES
        start = datetime.strptime(start_str, "%Y-%m-%d")
        end = datetime.strptime(end_str, "%Y-%m-%d")

        if start >= end:
            return jsonify({"error": "start must be before end"}), 400
        #  COMPUTE RISK

        service = Risk_Service(stock, start, end)
        data = service.compute_risk()


        return jsonify(data)

    except ValueError:
        return jsonify({"error": "Invalid date format (use YYYY-MM-DD)"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

