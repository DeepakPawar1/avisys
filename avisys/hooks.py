# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "avisys"
app_title = "Avisys"
app_publisher = "Avisys"
app_description = "Avisys Hr"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "avisys@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/avisys/css/avisys.css"
# app_include_js = "/assets/avisys/js/avisys.js"

# include js, css files in header of web template
# web_include_css = "/assets/avisys/css/avisys.css"
# web_include_js = "/assets/avisys/js/avisys.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "avisys.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "avisys.install.before_install"
# after_install = "avisys.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "avisys.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"avisys.tasks.all"
# 	],
# 	"daily": [
# 		"avisys.tasks.daily"
# 	],
# 	"hourly": [
# 		"avisys.tasks.hourly"
# 	],
# 	"weekly": [
# 		"avisys.tasks.weekly"
# 	]
# 	"monthly": [
# 		"avisys.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "avisys.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "avisys.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "avisys.task.get_dashboard_data"
# }
jenv = {
 "methods": [ 
 "get_job_offer_data:avisys.avisys.custom_scripts.jinja_file.jinja_file.get_job_offer_data",
 "get_tableA_data:avisys.avisys.custom_scripts.jinja_file.jinja_file.get_tableA_data",
 "get_table_data_for_promotion:avisys.avisys.custom_scripts.jinja_file.jinja_file.get_table_data_for_promotion",
 "get_employee_transfer_data:avisys.avisys.custom_scripts.jinja_file.jinja_file.get_employee_transfer_data"] 


}
fixtures = [{'doctype':'Letter Head',
'filters': {'name': ('in', ['Avisys'])
}
},
{
        'doctype': 'Print Format',
        'filters': {'name': ('in', ['Promotion Letter','Confirmation Letter','Appointment Letter','Transfer Letter','Job Offer Letter'])}
    }
    ]
doc_events = {

        "Salary Structure Assignment":{
        "validate":"avisys.avisys.custom_scripts.salary_structure.salary_structure.validate"

        },
}