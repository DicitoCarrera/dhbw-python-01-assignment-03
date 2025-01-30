import Data.List (find)
import Distribution.FieldGrammar (List)
import Distribution.Fields (Name)
import Language.Haskell.TH (Strict)

-- ContactDetail represents various types of contact information
data ContactDetail
  = Telephone
      { countryCode :: String,
        cityCode :: String,
        number :: String
      } -- A phone number
  | Email String -- An email address
  | SocialMedia String String -- Social media platform and handle
  deriving (Show, Eq)

-- Contact represents an individual contact with name and multiple contact details
data Contact = Contact
  { name :: String, -- Contact's name
    details :: [ContactDetail] -- List of contact details (Phone, Email, etc.)
  }
  deriving (Show, Eq)

-- A contact list is simply a list of contacts
type ContactList = [Contact]

-- Add a new contact to the contact list
addContact :: Contact -> ContactList -> ContactList
addContact newContact contacts = newContact : contacts

-- List all contacts in a user-friendly format
listContacts :: ContactList -> String
listContacts [] = "No contacts available."
listContacts contacts = unlines $ map showContact contacts
  where
    showContact :: Contact -> String
    showContact contact = name contact ++ "\n" ++ unlines (map showDetail (details contact))

    showDetail :: ContactDetail -> String
    showDetail (Telephone countryCode cityCode number) = "Phone: " ++ countryCode ++ cityCode ++ number
    showDetail (Email address) = "Email: " ++ address
    showDetail (SocialMedia platform handle) = platform ++ ": " ++ handle

-- Search for a contact by name
searchContact :: String -> ContactList -> Maybe Contact
searchContact searchName contacts =
  case filter (\c -> name c == searchName) contacts of
    [] -> Nothing
    (x : _) -> Just x

-- Edit a contact's details by name
editContact :: String -> Contact -> ContactList -> ContactList
editContact searchName newContact = map (\c -> if name c == searchName then newContact else c)

-- Delete a contact by name
deleteContact :: String -> ContactList -> ContactList
deleteContact searchName = filter (\c -> name c /= searchName)
