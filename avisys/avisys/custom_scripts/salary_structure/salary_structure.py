from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
from frappe.utils import flt,today
from frappe import _


def validate(doc, method):
    print("**************************")
    salary_structure_doc = frappe.get_doc("Salary Structure",doc.salary_structure)
    if salary_structure_doc.for_reference_purpose==1:
        print("ssss",salary_structure_doc,";;;;;;;;")
        data = frappe.db.sql("""select name from `tabSalary Structure Assignment` where employee = '%s' and from_date > '%s' """%(doc.employee,doc.from_date),debug=1)
        print(";;;;;;;",data)
        if not data:
            frappe.throw("no salary structure currently active please add salary structure assignment")
        #else:
            #frappe.throw("Date should be less than current active salary structure")
    else:
        print("print nonexxxxx")
	













	
