from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
from frappe.utils import flt,today
from frappe import _


def validate(doc, method):
    salary_structure_doc = frappe.get_doc("Salary Structure",doc.salary_structure)
    if salary_structure_doc.for_reference_purpose==1:
        data = frappe.db.sql("""select name from `tabSalary Structure Assignment` where employee = '%s' and from_date > '%s' """%(doc.employee,doc.from_date))
        if not data:
            frappe.throw("No Salary Structure Assignment currently active please add Salary Structure Assignment")

	













	
