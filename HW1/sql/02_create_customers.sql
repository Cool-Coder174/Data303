-- We're in the PACKT_ONLINE_SHOP database now. This is where the magic happens.
USE PACKT_ONLINE_SHOP;

-- If the Customers table exists, we're getting rid of it. Out with the old, in with the new.
DROP TABLE IF EXISTS Customers;
-- Now, let's build the Customers table. This is where we'll store all our... well, customers.
CREATE TABLE Customers (
  FirstName     VARCHAR(50), -- First name. You know, like "John" or "Jane".
  MiddleName    VARCHAR(50), -- Middle name. For all the people with more than two names.
  LastName      VARCHAR(50), -- Last name. The one that goes on the back of the jersey.
  HomeAddress   VARCHAR(250), -- Where they live. Don't be creepy.
  Email         VARCHAR(200), -- How we spam them with offers.
  Phone         VARCHAR(50),  -- How we call them when they don't answer our emails.
  Notes         VARCHAR(250)  -- Juicy gossip and other important information.
);