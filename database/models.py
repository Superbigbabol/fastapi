import datetime
import decimal
from pydantic import BaseModel, computed_field

class Payment(BaseModel):
    id: str
    payee_first_name: str
    payee_last_name: str
    payee_payment_status: str
    payee_added_date_utc: str
    payee_due_date: str
    payee_address_line_1: str
    payee_address_line_2: str
    payee_city: str
    payee_country: str
    payee_province_or_state: str
    payee_postal_code: str
    payee_phone_number: str
    payee_email: str
    currency: str
    discount_percent: float
    tax_percent: float
    due_amount: float
    total_due: float
    # @computed_field
    # @property
    # def total_due(self) -> float:
    #     return self.due_amount * (1 - self.discount_percent / 100) * (1 + self.tax_percent / 100)
