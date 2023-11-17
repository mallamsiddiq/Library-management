# def test_student_books_view(self):
#         # Log in the user
#         self.client.login(email=self.student.email, password = self.student.password)

#         # Create a test student

#         # Define the URL for the student books view
#         url = reverse('booksbystudent')  # Replace with your URL name

#         # Create a test book issuance
#         BookIssuance.objects.create(
#             student = self.student,
#             book = self.book,  # Replace with a valid book instance
#             status='active',
#         )

#         # Access the student books view
#         response = self.client.get(url)

#         # Check the response status code
#         self.assertEqual(response.status_code, 200)  # Replace with your expected status codes
#         # Check any other aspects of the response as needed

#     def test_all_students_view(self):
#         # Log in the user (an admin)
#         self.client.login(email='admin@example.com', password='admin_password')

#         # Define the URL for the all students view
#         url = reverse('all_students')  # Replace with your URL name

#         # Access the all students view
#         response = self.client.get(url)

#         # Check the response status code
#         self.assertEqual(response.status_code, 200)  # Replace with your expected status code

#         # Check any other aspects of the response as needed