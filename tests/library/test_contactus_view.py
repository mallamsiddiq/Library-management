from django.test import TestCase
from django.urls import reverse
from django.core.mail import outbox
from library.forms import ContactusForm

class ContactUsViewTest(TestCase):

    def test_contact_us_form_submission(self):
        data = {
            'Name': 'John Doe',
            'Email': 'john.doe@example.com',
            'Message': 'This is a test message.',
        }

        response = self.client.post(reverse('contactus'), data)

        # Check if the form submission is successful and the response contains the contactussuccess.html template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/success/contactussuccess.html')

        # Verify that an email has been sent
        self.assertEqual(len(outbox), 1)
        sent_email = outbox[0]
        self.assertEqual(sent_email.subject, 'John Doe || john.doe@example.com')
        self.assertEqual(sent_email.body, 'This is a test message.')

    def test_contact_us_form_invalid_submission(self):
        data = {
            'Name': 'John Doe',
            'Email': 'invalid_email',  # Invalid email address
            'Message': 'This is a test message.',
        }

        response = self.client.post(reverse('contactus'), data)

        # Check if the form submission is not successful and the response remains on the contactus.html template
        self.assertEqual(response.status_code, 200)

        # Verify that the form contains validation errors for the 'Email' field
        form = response.context['form']
        self.assertIn('Email', form.errors)
        self.assertEqual(form.errors['Email'], ['Enter a valid email address.'])

        # Verify that no email has been sent
        self.assertEqual(len(outbox), 0)

    def test_contact_us_form_empty_submission(self):
        data = {}  # Empty form data

        response = self.client.post(reverse('contactus'), data)

        # Check if the form submission is not successful and the response remains on the contactus.html template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/create/contactus.html')

        # Verify that the form contains validation errors for the required fields
        form = response.context['form']
        self.assertIn('Name', form.errors)
        self.assertEqual(form.errors['Name'], ['This field is required.'])
        self.assertIn('Email', form.errors)
        self.assertEqual(form.errors['Email'], ['This field is required.'])
        self.assertIn('Message', form.errors)
        self.assertEqual(form.errors['Message'], ['This field is required.'])

        # Verify that no email has been sent
        self.assertEqual(len(outbox), 0)
