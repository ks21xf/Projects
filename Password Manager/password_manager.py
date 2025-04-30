import random
import pandas as pd 
import string
import pyautogui as auto
from time import sleep
import pyperclip

class PasswordManager:
    def __init__(self):
        self.ALLOWED_CHARACTERS = [x for x in range(33,123) if x != 92] #ascii codes of all chars besides \ since it causes problems
        self.df = pd.read_csv('passwords.csv')

    def _save(self):
        self.df.to_csv('passwords.csv', index=False,encoding='utf-8', header=True)
        print("Database has been updated. Reset program to see changes.")

    def encrypt(self,plaintext):
        """Encrypts by generating random offsets"""
        cyphertext = ""
        random.seed(9999)
        for i in range(len(plaintext)):
            offset = random.randint(0,56)
            new_char = ord(plaintext[i])+offset
            if new_char >=123:
                new_char = (new_char%123)+32
            cyphertext+=chr(new_char)
        return cyphertext

    def decrypt(self,cyphertext):
        """Decrypts taking advantage of the random seed. we can figure out the random offsets as long as we have the exact seed"""
        plaintext = ""
        random.seed(9999)
        for i in range(len(cyphertext)):
            offset = random.randint(0,56)
            new_char = ord(cyphertext[i])-offset
            if new_char -32 <=0: 
                new_char = 123 + new_char -32
            plaintext +=chr(new_char)
        return plaintext

    def generate_password(self,length):
        """generates a password with a specified length as a parameter"""
        random.seed(None)
        pswd = ""
        for i in range(length):
            char = 0
            char = random.choice(self.ALLOWED_CHARACTERS)
            pswd = pswd +chr(char)
        return pswd

    def generate_password_alphanumeric(self,length):
        """generates an alphanumeric password with specified length as a parameter. useful since some primitive websites don't allow symbols to be used in passwords"""
        random.seed(None)
        listy = list(string.ascii_letters+string.digits)
        e = random.choice([0,1,2,3,4,5,6,7,8,9])
        pswd = str(e) #guarantees 1 numeric value for smaller password
        for i in range(length-1):
            picker = random.randint(0,len(listy)-1)
            pswd += listy[picker]
        return pswd

    def test(self):
        """Debug function to test if encryption and decryption works by generating 10000 passwords and seeing if the password is intact after encrypting then decrypting"""

        for i in range(10000):
            orig = self.generate_password_alphanumeric(36)
            encr = self.encrypt(orig)
            decr = self.decrypt(encr)
            
            if decr != orig:
                failure_count += 1
                print("Test Failed!")
                print(f" Original: {orig}")
                print(f"Decrypted: {decr}")
                input("Something went wrong. Press Enter to continue...")
                return  # Stop further testing if an error is found
        print('Test Passed!')

    def return_site_index(self):
        """function that searches the database of 'passwords' and gets the index of the site the user is logging into"""
        get_site = None
        get_site_index = 0
        site_found = False
        while(True):
            get_site = input("For what site: ")
            for index,rows in self.df.iterrows():
                if rows["Website"].strip() == get_site.strip():
                    site_found = True
                    print("Information Found.")
                    break
                get_site_index+=1
            if site_found:
                break
            else:
                print(f"There is no information linked to the website '{get_site}'. Try again.")
        return get_site_index 
    
    def generate_password(self):
        while True:
            print('for your password: ')
            print("press 1 to put in your own password")
            print("press 2 to generate a new password (length 36)")
            print("press 3 to generate new password (length 24)")
            print("press 4 to generate a new password (length 36, alphanumeric only)")
            print("press 5 to generate new password (length 24, alphanumeric only)")
            print("press 6 to generate a new password (length 12)")
            print("press 7 to generate new password (length 12, alphanumeric only)")
            choice = input("enter here:")
            pswd = ""
            if choice == "1":
                while True:
                    pswd = input("enter password you want:")
                    checker = input("enter it again")
                    if pswd == checker:
                        print("passwords match")
                        break
                return pswd
            elif choice =="2":
                pswd = self.generate_password(36)
                print("New password generated. Length of 36")
            elif choice =="3":
                pswd = self.generate_password(24)
                print("New password generated. Length of 24")
            elif choice =="4":
                pswd = self.generate_password_alphanumeric(36)
                print("New password generated. Length of 36")
            elif choice =="5":
                pswd = self.generate_password_alphanumeric(24)
                print("New password generated. Length of 24")
            elif choice =="6":
                pswd = self.generate_password(12)
                print("New password generated. Length of 24")
            elif choice =="7":
                pswd = self.generate_password_alphanumeric(12)
                print("New password generated. Length of 12")
            else:
                print('enter a valid number')
                continue
            pyperclip.copy(pswd)
            print("Your password has been copied to clipboard.")
            return pswd
        
    def add_website(self):
        """adds a website to the database"""
        get_site = None
        get_site_index = 0
        site_found = False
        while(True):
            get_site_index = 0
            get_site = input("Enter name of Website")
            for index,rows in self.df.iterrows():
                if rows["Website"].strip() == get_site.strip():
                    site_found = True
                    print("Information for this site already exists. Try again.")
                    break
                get_site_index+=1
            if site_found:
                continue
            else:
                print(f"Creating new information for the website '{get_site}'")
                break
        pswd = self.generate_password()
        new_row = [get_site,self.encrypt(pswd)]
        self.df.loc[len(self.df)] = new_row
        self._save()

    def retrieve_password(self):
        index = self.return_site_index()
        pyperclip.copy(self.decrypt(self.df.iloc[index][1]))
        print("Your password has been copied to your clipboard")

    def use_encryption(self):
        response = input("Enter a message to encrypt")
        encr = self.encrypt(response)
        print("Your encrypted message will be printed below.")
        print(encr,'\n')
    
    def use_decryption(self):
        response = input("Enter a message to decrypt")
        decr = self.decrypt(response)
        print("Your decrypted message will be printed below.")
        print(decr,'\n')

    def replace_pswd(self):
        get_site_index = self.return_site_index()
        pswd = self.generate_password()
        self.df.iloc[get_site_index, 1] = self.encrypt(pswd)
        self._save()

    def delete_pswd(self):
        get_site_index = self.return_site_index()
        self.df = self.df.drop(get_site_index)
        self.df = self.df.reset_index(drop=True)
        self._save()
    def main_program(self):
        print("Password Manager\n")
        action_dict = {
            '1': self.add_website,
            '2':self.retrieve_password,
            '3': self.replace_pswd,
            '4': self.delete_pswd,
            '5':self.use_encryption,
            '6':self.use_decryption,
        }
        while True:
            print("Press 1 to store a password")
            print("Press 2 to retrieve password")
            print("Press 3 to change one of your passwords")
            print("Press 4 to delete one of your passwords")
            print("Press 5 to use encryption")
            print("Press 6 to use decryption")
            print("Press 0 to exit program")
            response = input("Enter response here:")

            if response == '0':
                break
            elif response == '1' or response == '2' or response == '3' or response =='4':
                action_dict[response]()
            else:
                print("Please enter again.")

pm = PasswordManager()
pm.main_program()

