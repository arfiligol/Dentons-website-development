from flask_table import Table, Col, LinkCol



class case_detail(Table):
    Case_id = Col('Case_id')
    date_time = Col('Date_time')
    Client_name = Col('Client_name')
    cause = Col('Cause')
    inverse = Col('Inverse')
    contract_lawyer = Col('Contract_lawyer')
    over_or_not = Col('Over_or_not')
    edit = LinkCol('Edit', 'user_1.edit', url_kwargs=dict(Case_id='Case_id'))
    delete = LinkCol('Delete', 'user_1.deleting', url_kwargs=dict(Case_id='Case_id'))


class case_detail_object(object):
    def __init__(self, Case_id, date_time, Client_name, cause, inverse, contract_lawyer, over_or_not):
        self.Case_id = Case_id
        self.date_time = date_time
        self.Client_name = Client_name
        self.cause = cause
        self.inverse = inverse
        self.contract_lawyer = contract_lawyer
        self.over_or_not = over_or_not