from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
from frappe.utils import flt,today
from frappe import _
import decimal    
import json
from datetime import datetime, timedelta
def num2words(num):
	num = decimal.Decimal(num)
	decimal_part = num - int(num)
	num = int(num)

	if decimal_part:
		return num2words(num) + " point " + (" ".join(num2words(i) for i in str(decimal_part)[2:]))

	under_20 = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
	tens = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
	above_100 = {100: 'Hundred', 1000: 'Thousand', 100000: 'Lakh', 10000000: 'Crore'}

	if num < 20:
		return under_20[num]

	if num < 100:
		return tens[num // 10 - 2] + ('' if num % 10 == 0 else ' ' + under_20[num % 10])

	# find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
	pivot = max([key for key in above_100.keys() if key <= num])

	return num2words(num // pivot) + ' ' + above_100[pivot] + ('' if num % pivot==0 else ' ' + num2words(num % pivot))





@frappe.whitelist()
def get_employee_transfer_data(doc):
	
	date  =  datetime.strptime(str(doc.transfer_date), '%Y-%m-%d')- timedelta(days=1)

	data={"designation" :[None,None],"department":[None,None]}
	data['date']=date.strftime("%d %b, %Y")
	for i in doc.transfer_details:
		if i.property == "Designation":
			data['designation'] = [i.current if i.current else 0, i.new if i.new else 0]
		if i.property == "Department":
			data['department'] = [i.current if i.current else 0, i.new if i.new else 0]
	if data['designation'][0]== None:
		frappe.throw("Current designation not found. Please add it to employee. ")
	if data['designation'][1]== None:
		frappe.throw("New designation not found. Please add it to Employee Transfer. ")
	if data['department'][0]== None:
		frappe.throw("Current department not found. Please add it to employee. ")
	if data['department'][1]== None:
		frappe.throw("New department not found. Please add it to Employee Transfer. ")

	return data

@frappe.whitelist()
def get_table_data_for_promotion(doc):
	data = frappe.db.sql("""select name,from_date,salary_structure from `tabSalary Structure Assignment` where employee = '%s' group by from_date desc """%(doc.employee))
	if not data:
		frappe.throw("Salary Structure Assignment not found for this employee.")
	send_data = {}
	total_fixed_pay_monthly =0
	total_fixed_pay_annually=0
	total_fixed_deduction_annually=0
	prev_sal_struct=0
	items = ['basic_salary','house_rent_allowance','personal_allowance','conveyance_allowance','basic_salary','provident_fund','professional_tax']
	for i in items:
		send_data[i]=[0,0]
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
		send_data['total_fixed_pay_annually_words'] = num2words(total_fixed_pay_annually)
		send_data['gross'] = send_data['total_fixed_pay_annually']-send_data['total_fixed_deduction_annually']
		doc_salary_structure_two = frappe.get_doc("Salary Structure",data[1][2])
		for i in doc_salary_structure_two.earnings:
			prev_sal_struct += i.amount
		#for i in doc_salary_structure_two.deductions:
			#prev_sal_struct -= i.amount
		send_data['prev_sal_struct']=prev_sal_struct

	else:
		frappe.throw("Please assign salary structure")
	return send_data

@frappe.whitelist()
def validate_data_for_job_offer_letter(doc):
	if not frappe.db.get_value("Employee",{'job_applicant':doc.job_applicant},"date_of_joining"):
		frappe.throw("Please enter date of joining for employee.")
	if not frappe.db.get_value("Employee",{'job_applicant':doc.job_applicant},"reports_to"):
		frappe.throw("Please add reports to field for the employee.")
	rep_to =frappe.db.get_value("Employee",{'job_applicant':doc.job_applicant},"reports_to")
	if not frappe.db.get_value("Employee",rep_to,"designation"):
		frappe.throw("Please add designation for employee %s "%(rep_to))
	if not frappe.db.get_value("Employee",{'job_applicant':doc.job_applicant},"branch"):
		frappe.throw("Please add branch for employee.")
	return 1
@frappe.whitelist()
def get_job_offer_data(doc):
	class Dict2Class(object):  
		def __init__(self, my_dict):
			for key in my_dict:
				setattr(self, key, my_dict[key])
	return get_tableA_data(Dict2Class(doc))
	


@frappe.whitelist()
def get_tableA_data(doc):
	

	#frappe.get_doc("Salary Structure Assignment")
	#data = frappe.db.sql("""select ssa.name,ssa.from_date	 from `tabSalary Structure Assignment` ssa inner join 
	#	(select name ,MAX(from_date) as from_date from `tabSalary Structure Assignment` group by name) ssa2 on ssa.name=ssa2.name and ssa.from_date=ssa2.from_date and
	#	 ssa.employee = '%s' group by"""%(doc.employee),debug=1)
	data = frappe.db.sql("""select name,from_date,salary_structure from `tabSalary Structure Assignment` where employee = '%s' group by from_date desc """%(doc.employee))
	if not data:
		frappe.throw("Salary Structure Assignment not found for this employee.")
	send_data = {}
	total_fixed_pay_monthly =0
	total_fixed_pay_annually=0
	total_fixed_deduction_annually=0
	items = ['basic_salary','house_rent_allowance','personal_allowance','conveyance_allowance','basic_salary','provident_fund','professional_tax']
	for i in items:
		send_data[i]=[0,0]
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
		send_data['total_fixed_pay_annually_words'] = num2words(total_fixed_pay_annually)
		send_data['gross'] = send_data['total_fixed_pay_annually']-send_data['total_fixed_deduction_annually']
	else:
		frappe.throw("Please assign salary structure")



	data_bahrain = frappe.db.sql("""select ssa.name,ssa.from_date,ssa.salary_structure from `tabSalary Structure Assignment` ssa inner join `tabSalary Structure` ss on ssa.salary_structure = ss.name  and ssa.employee = '%s' and ss.for_reference_purpose = 1 group by ssa.from_date desc """%(doc.employee))
	if not data_bahrain:
		frappe.throw("Salary Structure Assignment with For Reference Purpose flag checked, not found for this employee. ")
	total_earnings = 0
	total_deduction = 0
	basic_salary_bh = 0
	send_bahrain_data={}
	bahrain_items = ['basic_salary','house_rent_allowance','conveyance_allowance','client_engagement_allowance','siogosi','advance']
	for j in bahrain_items:
		send_bahrain_data[j]=0
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
	else:
		frappe.throw("Please add back dated salary structure with for reference purpose flag ticked")
	send_data['bahrain_data'] = send_bahrain_data
	return send_data



@frappe.whitelist()
def validate_data_for_confirmation_letter(doc):
	if not frappe.db.get_value("Job Offer",{'job_applicant': doc.job_applicant},["name"]):
		frappe.throw("Job Offer not found.Please create one.")
	return 1


	validate_data_for_appointment_letter
@frappe.whitelist()
def validate_data_for_appointment_letter(doc):
	if not frappe.db.get_value("Job Offer",{'job_applicant': doc.job_applicant},["name"]):
		frappe.throw("Job Offer not found.Please create one.")
	if not doc.designation:
		frappe.throw("Please add designation for the employee.")
	if not doc.date_of_joining:
		frappe.throw("Please add date of joining for the employee.")
	if not doc.branch:
		frappe.throw("Please add branch for the employee.")
	if not doc.reports_to:
		frappe.throw("Please add reports to field for the employee.")
	if not frappe.db.get_value("Employee",doc.reports_to,"designation"):
		frappe.throw("Designation not added for %s "%(doc.reports_to))
	return 1

@frappe.whitelist()
def validate_data_for_transfer_letter(doc):
	if not frappe.db.get_value("Employee",doc.employee,"date_of_joining"):
		frappe.throw("Please add date of joining field for the employee %s "%(doc.employee))
	if not frappe.db.get_value("Employee",doc.employee,"reports_to"):
		frappe.throw("Please add reports to field for the employee.")
	if not frappe.db.get_value("Employee",frappe.db.get_value("Employee",doc.employee,"reports_to"),"designation"):
		frappe.throw("Designation not added for %s "%(frappe.db.get_value("Employee",doc.employee,"reports_to")))
	return 1

