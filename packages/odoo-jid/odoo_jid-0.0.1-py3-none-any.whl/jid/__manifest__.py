{
    'name': 'JID',
    'version': '0.0.1',
    'category': 'Human Resources/XMPP',
    'license': 'Apache-2.0',
    'summary': 'Adds a JID/XMPP field to customers',
    'description': """
        Adds a Jabber ID (JID) / XMPP Address field to customers, vendors, and
        other contacts.
        """,
    'depends': [
            'base',
    ],
    'author': 'Sam Whited',
    'website': 'https://blog.samwhited.com',
    'data': [
        'views/res_partner_views.xml',
    ],
    'application': True,
    'installable': True,
    'price': 15.00,
    'currency': 'USD',
    'support': 'odoo@atlbikeshed.com',
}
