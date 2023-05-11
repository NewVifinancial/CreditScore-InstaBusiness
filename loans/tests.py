from django.test import TestCase
from . models import Transactions, Calculation, CreditScore
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status


# Create your tests here.


class TransactionsTestCase(APITestCase):

    """
    Test suite for Transactions
    """
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "transaction_date": "31-Mar-2023",
			'transaction_time':"02:09:32",
			'from_acct':"43122976",
			'from_name':"EMMANUEL LAMPTEY", 
			'from_no':"233244471083",
			'trans_type':"DEBIT", 
			'amount':"10",
			'fees':"0",
			'ba_before':"61.72", 
			'bal_after':"51:72", 
			'to_no':"0", 
			'to_name':"cis",
			'to_acct':"53169694",
			'f_id':"14730101024", 
			'ref':"Internet Bundle", 
			'ova':"cis"
		
        }
        self.url = "/transactions/"

    # def test_create_contact(self):
    #     '''
    #     test ContactViewSet create method
    #     '''
    #     data = self.data
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(Contact.objects.count(), 1)
    #     self.assertEqual(Contact.objects.get().title, "Billy Smith")

    # def test_create_contact_without_name(self):
    #     '''
    #     test ContactViewSet create method when name is not in data
    #     '''
    #     data = self.data
    #     data.pop("name")
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # def test_create_contact_when_name_equals_blank(self):
    #     '''
    #     test ContactViewSet create method when name is blank
    #     '''
    #     data = self.data
    #     data["name"] = ""
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_contact_without_message(self):
    #     '''
    #     test ContactViewSet create method when message is not in data
    #     '''
    #     data = self.data
    #     data.pop("message")
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # def test_create_contact_when_message_equals_blank(self):
    #     '''
    #     test ContactViewSet create method when message is blank
    #     '''
    #     data = self.data
    #     data["message"] = ""
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_contact_without_email(self):
    #     '''
    #     test ContactViewSet create method when email is not in data
    #     '''
    #     data = self.data
    #     data.pop("email")
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # def test_create_contact_when_email_equals_blank(self):
    #     '''
    #     test ContactViewSet create method when email is blank
    #     '''
    #     data = self.data
    #     data["email"] = ""
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_contact_when_email_equals_non_email(self):
    #     '''
    #     test ContactViewSet create method when email is not email
    #     '''
    #     data = self.data
    #     data["email"] = "test"
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)