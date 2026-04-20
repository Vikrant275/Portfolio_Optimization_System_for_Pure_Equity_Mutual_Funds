import numpy as np

def get_audit_metrics(stock):
    return {
        'stock': stock,
        'fraud_flag' : int(np.random.choice([0,1], p=[0.9,0.1])),
        'governance_flag' : round(np.random.uniform(0,1),2)
    }

