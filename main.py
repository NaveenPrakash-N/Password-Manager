from tkinter import Tk,Canvas,PhotoImage,Label,Entry,Button,END,messagebox
import random 
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def random_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters= [random.choice(letters) for _ in range(nr_letters)]
    password_numbers= [random.choice(numbers) for _ in range(nr_numbers)]
    password_symbols= [random.choice(symbols) for _ in range(nr_symbols)]

    password_list = password_letters+password_symbols+password_numbers
    random.shuffle(password_list)

    generated_password = ''.join(password_list)
    pyperclip.copy(generated_password)
    password_entry.insert(0,generated_password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    user_website = webstie_entry.get()
    user_email = email_entry.get()
    user_password = password_entry.get()
    new_data = {
        user_website:{
            'email':user_email,
            'password':user_password
        }
    }
    if len(user_password) == 0 or len(user_email) == 0 or len(user_website) == 0:
        messagebox.showinfo(title='WARNING',message='Please dont leave any fields empty !')
    else:
        try:
            with open('data.json',"r") as file:
            # reading old data
                load_data = json.load(file)
        except FileNotFoundError:
            with open('data.json','w') as file:
                json.dump(new_data,file,indent=4)
        else:
            # adding old with new
            load_data.update(new_data)
            with open('data.json', "w") as file:
            # writing in json
                json.dump(load_data,file,indent=4)
        finally:
            webstie_entry.delete(0,END)
            password_entry.delete(0,END)



def find_password():
    website_value = webstie_entry.get()
    try:
        with open('data.json','r') as data:
            load_data = json.load(data)
            if webstie_entry.get() in load_data:
                user_data = load_data[website_value]
                messagebox.showinfo(
                    title=f"Details for {website_value}",
                    message=f"Username: {user_data['email']}\nPassword: {user_data['password']}"
                )
            else:
                messagebox.showinfo(title='Not Found', message='No data found on this Website')
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(pady=40,padx=40)


lock_image = PhotoImage(file='logo.png')

canvas = Canvas(width=250,height=200)
canvas.create_image(150,100,image=lock_image)
canvas.grid(row = 0,column = 1)

website = Label(text='Website :')
website.grid(row = 1,column = 0)


email = Label(text='Email/Username :')
email.grid(row = 2,column = 0)

password = Label(text='Password :')
password.grid(row = 3,column = 0)

webstie_entry = Entry()
webstie_entry.grid(row=1, column = 1, columnspan = 2, sticky='EW')
webstie_entry.focus()


email_entry = Entry()
email_entry.grid(row=2, column = 1, columnspan = 2, sticky='EW')
email_entry.insert(0,f'{email_entry.get()}')

password_entry = Entry()
password_entry.grid(row=3, column = 1, sticky='EW')

generate_button = Button(text='Generate Password',command=random_password)
generate_button.grid(row=3,column = 2,sticky='EW')

add_button = Button(text='Add',command=save)
add_button.grid(row = 4,column = 1,columnspan = 2,sticky='EW')

search_button = Button(text='Search',command=find_password)
search_button.grid(row = 1,column = 2,sticky = 'EW')




window.mainloop()
