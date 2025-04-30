
website_names = []
usernames = []
passwords = []

website_name = input("Enter website name: ")
username = input("enter username: ")
password = input("Enter password: ")


website_names.append(website_name)
usernames.append(username)
passwords.append(password)

print(website_names)
print(usernames)
print(passwords)

search_term = input("\nWhich username to delete")



if search_term in usernames:
    index = usernames.index(search_term)
    print(f"username is element {usernames[index]}")

    website_names.pop(index)
    usernames.pop(index)
    passwords.pop(index)

    print(website_names)
    print(usernames)
    print(passwords)
