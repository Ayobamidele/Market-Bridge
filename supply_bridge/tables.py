from flask_table import Table, Col

class OrderTable(Table):
    title = Col('Title')
    content = Col('Content')
    date_created = Col('Date Created')
    owner = Col("Owner")
    
