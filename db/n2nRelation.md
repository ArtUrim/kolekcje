**1\. Create the Tables**

* **Table 1 (e.g., users)**

SQL

`CREATE TABLE users (`  
    `id INT AUTO_INCREMENT PRIMARY KEY,`  
    `name VARCHAR(255) NOT NULL`  
`);`

* **Table 2 (e.g., groups)**

SQL

`CREATE TABLE groups (`  
    `id INT AUTO_INCREMENT PRIMARY KEY,`  
    `name VARCHAR(255) NOT NULL`  
`);`

* **Junction Table (e.g., user\_groups)**

SQL

`CREATE TABLE user_groups (`  
    `user_id INT,`  
    `group_id INT,`  
    `PRIMARY KEY (user_id, group_id), -- Composite primary key`  
    `FOREIGN KEY (user_id) REFERENCES users(id),`  
    `FOREIGN KEY (group_id) REFERENCES groups(id)`  
`);`

**Explanation:**

* **Junction Table:** This table connects the users and groups tables.  
  * user\_id and group\_id are foreign keys referencing the primary keys of the respective tables.  
  * The composite primary key (user\_id, group\_id) ensures that each pair of user and group can only exist once in the junction table.

**2\. Insert Sample Data**

SQL

`-- Insert users`  
`INSERT INTO users (name) VALUES`  
    `('John Doe'),`  
    `('Jane Smith'),`  
    `('David Lee');`

`-- Insert groups`  
`INSERT INTO groups (name) VALUES`  
    `('Administrators'),`  
    `('Users'),`  
    `('Guests');`

`-- Insert user-group relationships`  
`INSERT INTO user_groups (user_id, group_id) VALUES`  
    `(1, 1), -- John Doe is an Administrator`  
    `(2, 2), -- Jane Smith is a User`  
    `(3, 3), -- David Lee is a Guest`  
    `(1, 2); -- John Doe is also a User`

**3\. Query Data (Example)**

* **Get all groups for a specific user:**

SQL

`SELECT g.name`   
`FROM groups g`  
`JOIN user_groups ug ON g.id = ug.group_id`  
`JOIN users u ON ug.user_id = u.id`  
`WHERE u.id = 1; -- Replace with the user ID`

* **Get all users in a specific group:**

SQL

`SELECT u.name`  
`FROM users u`  
`JOIN user_groups ug ON u.id = ug.user_id`  
`JOIN groups g ON ug.group_id = g.id`  
`WHERE g.id = 2; -- Replace with the group ID`

**Key Considerations:**

* **Data Integrity:** The foreign key constraints in the user\_groups table ensure data integrity by preventing invalid user-group relationships.  
* **Flexibility:** This approach allows for many-to-many relationships between users and groups, meaning a user can belong to multiple groups, and a group can have multiple users.  
* **Efficiency:** For frequent lookups, consider adding indexes to the user\_id and group\_id columns in the user\_groups table.

This example demonstrates a basic n:n relationship. You can adapt and extend it based on your specific requirements and data model.