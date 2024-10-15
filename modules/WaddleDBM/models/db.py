# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
#if request.is_local and not configuration.get('app.production'):
response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

# Define the identities table
db.define_table('identities', 
                Field('name', 'string'),
                Field('country', 'string'),
                Field('ip_address', 'string'),
                Field('browser_fingerprints', 'list:string'))

# Define the communities table
db.define_table('communities', 
                Field('community_name'),
                Field('community_description'))

# Define table for community modules
db.define_table('community_modules', 
                Field('module_id', 'integer'),
                Field('community_id', db.communities),
                Field('enabled', 'boolean', default=True),
                Field('privilages', 'list:string'))

# Define a table for roles
db.define_table('roles',
                Field('name', 'string'),
                Field('description', 'string'),
                Field('privilages', 'list:string'),
                Field('requirements', 'list:string'))

# Define a table for community members table
db.define_table('community_members', 
                Field('community_id', db.communities),
                Field('identity_id', db.identities),
                Field('role_id', db.roles))
                # Field('currency', 'integer', default=0),
                # Field('reputation', 'integer', default=0))

# Define a table to store the reputation of a user, per community
db.define_table('reputation',
                Field('community_id', db.communities),
                Field('identity_id', db.identities),
                Field('amount', 'integer', default=0))

# Define a table that stores the currency of a user, per community
db.define_table('currency',
                Field('community_id', db.communities),
                Field('identity_id', db.identities),
                Field('amount', 'integer', default=0))

# Define a table that contains different gateway server types
db.define_table('gateway_server_types',
                Field('type_name', 'string'),
                Field('description', 'string'))


# Define a table that keeps track of gateway servers
db.define_table('gateway_servers', 
                Field('name', 'string'),
                Field('server_id', 'string'),
                Field('server_nick', 'string'),
                Field('server_type', db.gateway_server_types),
                Field('protocol', 'string'))


# Define a table that maps specific gateways to a community through an ID
db.define_table('routing', 
                Field('channel', 'string'),
                Field('community_id', db.communities),
                Field('routing_gateway_ids', 'list:integer'),
                Field('aliases', 'list:string'))


# Define a table that binds an identity to a community namespace through an ID, as a context. Every identity can only be in one community namespace at a time
db.define_table('context', 
                Field('identity_id', db.identities),
                Field('community_id', db.communities))

# Define a table that stores matterbridge account types
db.define_table('account_types',
                Field('type_name', 'string'),
                Field('description', 'string'))

# Define a table that stores routing gateway types
db.define_table('gateway_types',
                Field('type_name', 'string'),
                Field('description', 'string'))

# Define a table that keeps track of routing gateways for the creation of the matterbridge configuration file
db.define_table('routing_gateways',
                Field('gateway_server', db.gateway_servers),
                Field('channel_id', 'string'),
                Field('gateway_type', db.gateway_types),
                Field('activation_key', 'string'),
                Field('is_active', 'boolean', default=False))

# Define a table that stores calendar events, per community
db.define_table('calendar',
                Field('community_id', db.communities),
                Field('event_name', 'string'),
                Field('event_description', 'string'),
                Field('event_start', 'datetime'),
                Field('event_end', 'datetime'),
                Field('not_start_sent', 'boolean', default=False),
                Field('not_end_sent', 'boolean', default=False))


# After defining the tables, create the "Global" community, if it does not exist
if db(db.communities.community_name == "Global").count() == 0:
    db.communities.insert(community_name="Global", community_description="The global community.")

# After the Global community is created, create a routing entry for the Global community, if it does not exist
global_community = db(db.communities.community_name == "Global").select().first()
if db(db.routing.community_id == global_community.id).count() == 0:
    db.routing.insert(channel="Global", community_id=global_community.id, gateways=[], aliases=[])

# Also create the "member" and "owner" roles, if they do not exist
if db(db.roles.name == "member").count() == 0:
    db.roles.insert(name="member", description="A member of a community.", privilages=["read", "write"], requirements=["reputation >= 0"])

if db(db.roles.name == "owner").count() == 0:
    db.roles.insert(name="owner", description="The owner of a community.", privilages=["read", "write", "admin"], requirements=["reputation >= 0"])