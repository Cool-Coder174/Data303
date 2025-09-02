-- Back in the PACKT_ONLINE_SHOP. It's like we never left.
USE PACKT_ONLINE_SHOP;

-- Let's add some customers. These are totally real people. Definitely not made up.
INSERT INTO Customers
  (FirstName, MiddleName, LastName, HomeAddress, Email, Phone, Notes)
VALUES
  ('Joe',   'Greg',   'Smith',  '2356 Elm St.',           'joesmith@sfghwert.com', '(310) 555-1212', 'Always gets products home delivered'),
  ('Grace', 'Murray', 'Hopper', '123 Compilation Street', 'gmhopper@ftyuw46.com',  '(818) 555-3678', 'Compiler pioneer. Total badass.');

-- You know the drill. Add more customers here.
-- If you don't have a value for a column, just use NULL. It's the universal "I don't know".