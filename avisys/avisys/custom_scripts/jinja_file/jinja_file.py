from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
from frappe.utils import flt,today
from frappe import _
import decimal    
import json
from datetime import datetime, timedelta



@frappe.whitelist()
def get_employee_transfer_data(doc):
	date  =  datetime.strptime(str(doc.transfer_date), '%Y-%m-%d')- timedelta(days=1)
	data={"designation" :[None,None],"department":[None,None]}
	data['date']=date.strftime("%d %b, %Y")
	for i in doc.transfer_details:
		if i.property == "Designation":
			data['designation'] = [i.current if i.current else "", i.new if i.new else ""]
		if i.property == "Department":
			data['department'] = [i.current if i.current else "", i.new if i.new else ""]
	return data

@frappe.whitelist()
def get_table_data_for_promotion(doc):
	data = frappe.db.sql("""select name,from_date,salary_structure from `tabSalary Structure Assignment` where employee = '%s' group by from_date desc """%(doc.employee))
	send_data = {}
	total_fixed_pay_monthly =0
	total_fixed_pay_annually=0
	total_fixed_deduction_annually=0
	prev_sal_struct=0
	items = ['basic_salary','house_rent_allowance','personal_allowance','conveyance_allowance','basic_salary','provident_fund','professional_tax']
	for i in items:
		send_data[i]=[0,0]
	send_data['total_fixed_deduction_annually'] = 0
	send_data['total_fixed_pay_monthly'] = 0
	send_data['total_fixed_pay_annually'] = 0
	send_data['gross'] = 0
	send_data['prev_sal_struct']=0

	if len(data) >= 2 :
		doc_salary_structure = frappe.get_doc("Salary Structure",data[0][2])
		for i in doc_salary_structure.earnings:
			if i.salary_component == "Basic Salary":
				send_data['basic_salary']=[i.amount,12 * i.amount]
				total_fixed_pay_monthly += i.amount
				total_fixed_pay_annually += 12 * i.amount
			if i.salary_component == "House Rent Allowance":
				send_data['house_rent_allowance']=[i.amount,12 * i.amount]
				total_fixed_pay_monthly += i.amount
				total_fixed_pay_annually += 12 * i.amount
			if i.salary_component == "Personal Allowance":
				send_data['personal_allowance']=[i.amount,12 * i.amount]
				total_fixed_pay_monthly += i.amount
				total_fixed_pay_annually += 12 * i.amount
			if i.salary_component == "Conveyance Allowance/Expenses":
				send_data['conveyance_allowance']=[i.amount,12 * i.amount]
				total_fixed_pay_monthly += i.amount
				total_fixed_pay_annually += 12 * i.amount
			
		for i in doc_salary_structure.deductions:
			if i.salary_component == "Provident Fund":
				send_data['provident_fund']=[i.amount,12 * i.amount]
				total_fixed_deduction_annually += 12 * i.amount
			if i.salary_component == "Professional Tax":
				send_data['professional_tax']=[i.amount,12 * i.amount]	
				total_fixed_deduction_annually += 12 * i.amount
		send_data['total_fixed_deduction_annually'] = total_fixed_deduction_annually
		send_data['total_fixed_pay_monthly'] = total_fixed_pay_monthly
		send_data['total_fixed_pay_annually'] = total_fixed_pay_annually
		send_data['gross'] = send_data['total_fixed_pay_annually']-send_data['total_fixed_deduction_annually']
		doc_salary_structure_two = frappe.get_doc("Salary Structure",data[1][2])
		for i in doc_salary_structure_two.earnings:
			prev_sal_struct += i.amount
			send_data['prev_sal_struct']=prev_sal_struct
		#for i in doc_salary_structure_two.deductions:
			#prev_sal_struct -= i.amount
		
	return send_data


@frappe.whitelist()
def get_job_offer_data(doc):
	class Dict2Class(object):  
		def __init__(self, my_dict):
			for key in my_dict:
				setattr(self, key, my_dict[key])
	return get_tableA_data(Dict2Class(doc))
	


@frappe.whitelist()
def get_tableA_data(doc):
	data = frappe.db.sql("""select name,from_date,salary_structure from `tabSalary Structure Assignment` where employee = '%s' group by from_date desc """%(doc.employee))
	send_data = {}
	total_fixed_pay_monthly =0
	total_fixed_pay_annually=0
	total_fixed_deduction_annually=0
	items = ['basic_salary','house_rent_allowance','personal_allowance','conveyance_allowance','basic_salary','provident_fund','professional_tax']
	for i in items:
		send_data[i]=[0,0]
	send_data['total_fixed_deduction_annually'] = 0
	send_data['total_fixed_pay_monthly'] = 0
	send_data['total_fixed_pay_annually'] = 0
	send_data['gross'] = 0
	if data:
		doc_salary_structure = frappe.get_doc("Salary Structure",data[0][2])
		for i in doc_salary_structure.earnings:
			if i.salary_component == "Basic Salary":
				send_data['basic_salary']=[i.amount,12 * i.amount]
				total_fixed_pay_monthly += i.amount
				total_fixed_pay_annually += 12 * i.amount
			if i.salary_component == "House Rent Allowance":
				send_data['house_rent_allowance']=[i.amount,12 * i.amount]
				total_fixed_pay_monthly += i.amount
				total_fixed_pay_annually += 12 * i.amount
			if i.salary_component == "Personal Allowance":
				send_data['personal_allowance']=[i.amount,12 * i.amount]
				total_fixed_pay_monthly += i.amount
				total_fixed_pay_annually += 12 * i.amount
			if i.salary_component == "Conveyance Allowance/Expenses":
				send_data['conveyance_allowance']=[i.amount,12 * i.amount]
				total_fixed_pay_monthly += i.amount
				total_fixed_pay_annually += 12 * i.amount
			
		for i in doc_salary_structure.deductions:
			if i.salary_component == "Provident Fund":
				send_data['provident_fund']=[i.amount,12 * i.amount]
				total_fixed_deduction_annually += 12 * i.amount
			if i.salary_component == "Professional Tax":
				send_data['professional_tax']=[i.amount,12 * i.amount]	
				total_fixed_deduction_annually += 12 * i.amount
		send_data['total_fixed_deduction_annually'] = total_fixed_deduction_annually
		send_data['total_fixed_pay_monthly'] = total_fixed_pay_monthly
		send_data['total_fixed_pay_annually'] = total_fixed_pay_annually
		send_data['gross'] = send_data['total_fixed_pay_annually']-send_data['total_fixed_deduction_annually']
	


	data_bahrain = frappe.db.sql("""select ssa.name,ssa.from_date,ssa.salary_structure from `tabSalary Structure Assignment` ssa inner join `tabSalary Structure` ss on ssa.salary_structure = ss.name  and ssa.employee = '%s' and ss.for_reference_purpose = 1 group by ssa.from_date desc """%(doc.employee))
	total_earnings = 0
	total_deduction = 0
	basic_salary_bh = 0
	send_bahrain_data={}
	bahrain_items = ['basic_salary','house_rent_allowance','conveyance_allowance','client_engagement_allowance','siogosi','advance']
	for j in bahrain_items:
		send_bahrain_data[j]=0
	send_bahrain_data['total_deduction']=0
	send_bahrain_data['total_earnings']=0
	send_bahrain_data['gross']=0
	if data_bahrain:
		doc_salary_structure = frappe.get_doc("Salary Structure",data_bahrain[0][2])
		for i in doc_salary_structure.earnings:
			if i.salary_component == "Basic Salary":
				basic_salary_bh = i.amount
				send_bahrain_data['basic_salary']=i.amount
				total_earnings += i.amount
			if i.salary_component == "House Rent Allowance":
				send_bahrain_data['house_rent_allowance']=i.amount
				total_earnings += i.amount
			if i.salary_component == "Client Engagement Allowance":
				send_bahrain_data['client_engagement_allowance']=i.amount
				total_earnings += i.amount
			if i.salary_component == "Conveyance Allowance/Expenses":
				send_bahrain_data['conveyance_allowance']=i.amount
				total_earnings += i.amount
			
		for i in doc_salary_structure.deductions:
			if i.salary_component == "SIO/GOSI":
				send_bahrain_data['siogosi']=i.amount	
				total_deduction += basic_salary_bh * (i.amount/100)
			if i.salary_component == "Advance":
				send_bahrain_data['advance']=i.amount	
				total_deduction += i.amount
		send_bahrain_data['total_deduction']=total_deduction
		send_bahrain_data['total_earnings']=total_earnings
		send_bahrain_data['gross']=send_bahrain_data['total_earnings']- send_bahrain_data['total_deduction']
	send_data['bahrain_data'] = send_bahrain_data
	return send_data
