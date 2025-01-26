import pandas as pd
import numpy as np
import pycountry
import phonenumbers

def validate_payment_status(status):
    if status in ['completed', 'due_now', 'overdue', 'pending']:
        return status
    else:
        return np.nan

def is_valid_country_code(country_code):
    try:
        pycountry.countries.get(alpha_2=country_code)
        return True
    except LookupError:
        return False


def validate_phone_number(phone_number):
    try:
        phone_number = str(phone_number)
        parsed_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.phonenumberutil.NumberParseException:
        return np.nan

def is_valid_currency_code(currency_code):
    try:
        pycountry.currencies.get(alpha_3=currency_code)
        return True
    except KeyError:
        return False

df = pd.read_csv('payment_information.csv', dtype={'payee_phone_number': str})
df['payee_first_name'] = df['payee_first_name'].str.strip().str.title()
df['payee_last_name'] = df['payee_last_name'].str.strip().str.title()
df['payee_payment_status'] = df['payee_payment_status'].apply(validate_payment_status)
df['payee_added_date_utc'] = pd.to_datetime(df['payee_added_date_utc'], utc=True)
df['payee_due_date'] = pd.to_datetime(df['payee_due_date'], format='%Y-%m-%d')
df['payee_address_line_1'] = df['payee_address_line_1'].str.strip()
df['payee_address_line_2'] = df['payee_address_line_2'].str.strip()
df['payee_city'] = df['payee_city'].str.strip().str.title()
df['payee_country'] = df['payee_country'].apply(lambda x: x.upper() if is_valid_country_code(x) else np.nan)
df['payee_province_or_state'] = df['payee_province_or_state'].str.strip().fillna('')
df['payee_postal_code'] = df['payee_postal_code'].apply(str)
df['payee_phone_number'] = df['payee_phone_number'].apply(validate_phone_number)
df['payee_email'] = df['payee_email'].str.strip().str.lower()
df['currency'] = df['currency'].apply(lambda x: x.upper() if is_valid_currency_code(x) else np.nan)
df['discount_percent'] = df['discount_percent'].apply(lambda x: round(x, 2) if pd.notnull(x) else np.nan)
df['tax_percent'] = df['tax_percent'].apply(lambda x: round(x, 2) if pd.notnull(x) else np.nan)
df['due_amount'] = df['due_amount'].apply(lambda x: round(x, 2))
# df['total_due'] = df['due_amount'] * (1 - df['discount_percent'] / 100) * (1 + df['tax_percent'] / 100)
# df['total_due'] = df['total_due'].round(2)

# print(df.head())
# print(df.to_string())
normalized_data = df.to_dict(orient='records')
