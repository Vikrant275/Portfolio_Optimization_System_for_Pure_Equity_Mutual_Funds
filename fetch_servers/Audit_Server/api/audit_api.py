from flask import Blueprint, jsonify
from fetch_servers.auth_user import authenticate
from fetch_servers.Audit_Server.service.audit_service import get_audit_metrics

audit_bp = Blueprint('audit',__name__)

@audit_bp.route('/audit/<stock>',methods=['GET'])
def audit(stock):
    authenticate()
    return jsonify(get_audit_metrics(stock))