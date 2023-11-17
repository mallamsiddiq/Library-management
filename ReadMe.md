**Library Management App Documentation**

This documentation provides an overview of a library management app created for local office use. The app is designed to run locally and is built to work seamlessly with Docker without the need for complex setup. Below, you'll find instructions on how to run the app, an overview of its features, and insights into the codebase.

## Getting Started

To get your app up and running, follow these steps:

**Using Docker:**

1. Run the following command to start the app using Docker Compose:
   ```
   docker-compose up
   ```

2. After running the command, your app will be accessible on Port 8000. You can access it in your web browser.

**For Windows Users:**

If you're on Windows, you can use a batch script to start the app. Simply run:
```
watch spinup.bat
```

This script will set up your app and get it running.

**For Non-Windows Users:**

For users on macOS or Linux, you can create an executable profile with the provided batch script:

1. Make the script executable:
   ```
   chmod +x spinup.sh
   ```

2. Run the script to start your app:
   ```
   ./spinup.sh
   ```

**Manual Installation:**

If you prefer manual installation, follow these steps:

1. Create a virtual environment.

2. Install the app's dependencies from `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```

3. Run the database migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Start the development server:
   ```
   python manage.py runserver
   ```

## App Structure

This app is built using a loosely coupled architecture and consists of several apps within the library system:

1. **Library App:** This is the main app for managing the library.

2. **Students App:** This app handles student-related functionality.

3. **Auth App:** Manages educational aspects of the system.

## Data Relationships

The app manages relationships between students, books, and book issuances. Students are connected to book issuances through a many-to-many relationship in the database. The app includes methods and properties to facilitate these relationships.

## Data Relationships

#### Book Model

- The `Book` model represents books in the library.
- Each book has a many-to-many relationship with students through the `readers` field. This relationship is managed through the `BookIssuance` model, which tracks book issuances to students.
- The `total_stock` field keeps track of the total number of copies of a book available in the library.
- The `available_copies` property calculates the number of available copies of the book by subtracting the active issuances from the total stock.
- The `out_of_shelves` method checks whether the book is available for issuing, considering the available copies.

#### BookIssuance Model

- The `BookIssuance` model records book issuances to students.
- It has foreign keys to the `StudentExtra` and `Book` models, creating a link between students and the books they borrow.
- The `active` field represents the status of the issuance, indicating whether it's active or has been returned.
- The `expirydate` field stores the date when the book should be returned.
- The `due_in` property calculates the number of days remaining until the book is due.
- The `expired` property checks if the book issuance has expired based on the due date.
- The `is_qualified` method checks if the book is available for issuing and if the student has overdue books, returning an error message if the issuance is not qualified.
- The `return_book` method marks the issuance as inactive when the book is returned.

#### StudentExtra Model

- The `StudentExtra` model extends the built-in User model to include additional student-specific fields.
- Students have a many-to-many relationship with books through the `book_issuance` field.
- The `overdue_books` property filters and returns books that are overdue for a specific student.
- The `has_overdue_books` method checks if a student has any overdue books.
- The `clear_overdue_books` method allows students to return overdue books, marking them as inactive.

#### User Model

- The `User` model is used for authentication and extends the built-in `AbstractBaseUser` and `PermissionsMixin`.
- It includes fields such as `email`, `first_name`, and `last_name` for user profile information.
- The `is_active` and `is_staff` fields determine user access and administrative privileges.

These data relationships help manage book issuances, track overdue books, and provide information about students and users within the library management system.


## Features

The app includes various features, such as:

- Checking if a student has any overdue books.
- Verifying the availability of books in the library before issuance.
- Tracking the total stock of books in the library.

### Features Updates
- The latest updates to the Library Management App include:

- **Book Deadline Tracking**: Admins can easily identify due books, as they are highlighted in red on the book table.

- **User Management**: Admins can manage users, and users with overdue books are marked with a distinctive color in the all-users dashboard table.

- **Student Book Requests**: Students can now make requests for books, and admins have the ability to review and grant book issuances based on these requests.

## Testing

To ensure the reliability of the app, test cases have been written. While not an exhaustive set of tests, these cases cover critical functionality.

---

## Notes and Considerations

### Frontend Code

Please note that due to time constraints, I couldn't fully upgrade the frontend part of this app to adhere to the best coding standards and principles. While my focus was on the backend code to ensure it's designed for efficiency, reduces possible bottlenecks, and follows best practices, the frontend code still needs improvements in terms of adhering to the DRY (Don't Repeat Yourself), structuring and more.

### Running the App Locally

This app is specifically designed to run locally, and the setup has been tailored for local deployment. If you have any questions or require assistance with running the app locally, please feel free to contact the developer at `mallamsidddiq@gmail.com`.

For any inquiries, suggestions, or improvements, I welcome your feedback and look forward to hearing from you.