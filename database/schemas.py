
import datetime

def calculate_total_due(discount_percent, tax_percent, due_amount):
    total_due = due_amount * (1 - discount_percent/ 100) * (1 + tax_percent/ 100)
    return round(total_due, 2)

def payee_payment_status_check(payee_payment_status, payee_due_date):
    now_obj = str(datetime.datetime.now()).split(" ")[0]
    now = datetime.datetime(int(now_obj.split("-")[0]), int(now_obj.split("-")[1]), int(now_obj.split("-")[2]))
    # print(now)
    
    due_obj = str(payee_due_date).split(" ")[0]
    due_date = datetime.datetime(int(due_obj.split("-")[0]), int(due_obj.split("-")[1]), int(due_obj.split("-")[2]))
    
    if due_date == now:
        return "due_now"
    elif due_date < now:
        return "overdue"
    else:
        return payee_payment_status

def payee_country_check(payee_country):
    if type(payee_country) != str :
        return "NA"
    else:
        return payee_country

def individual_data(payment):
    return {
        "id": str(payment["_id"]),
        "payee_first_name": payment["payee_first_name"],
        "payee_last_name": payment["payee_last_name"],
        "payee_payment_status": payee_payment_status_check(payment["payee_payment_status"], payment["payee_due_date"]),
        "payee_added_date_utc": str(payment["payee_added_date_utc"]),
        "payee_due_date": str(payment["payee_due_date"]),
        "payee_address_line_1": payment["payee_address_line_1"],
        "payee_address_line_2": payment["payee_address_line_2"],
        "payee_city": payment["payee_city"],
        "payee_country": payee_country_check(payment["payee_country"]),
        "payee_province_or_state": payment["payee_province_or_state"],
        "payee_postal_code": payment["payee_postal_code"],
        "payee_phone_number": payment["payee_phone_number"],
        "payee_email": payment["payee_email"],
        "currency": payment["currency"],
        "discount_percent": payment["discount_percent"],
        "tax_percent": payment["tax_percent"],
        "due_amount": payment["due_amount"],
        "fid": str(payment["fid"]) if "fid" in payment else "",
        "total_due": calculate_total_due(payment["discount_percent"], payment["tax_percent"], payment["due_amount"])
    }

def all_data(payments):
    return [individual_data(payment) for payment in payments]