# Video presentation of the project:

[Video presentation](https://youtu.be/JW-QwixgMnc)


## The problem:

I have noticed that me and many other people spend too much time with the fridge's door open trying to figure out what to snack or what to cook, because sometimes the fridge is really out of free space and you just can't remember even in which direction to look for something that might be interesting for you at the moment. It's also very difficult to keep track of food in the stock, especially when you have many fridge users — family members, roommates, colleagues or anybody else with whom your are sharing the kitchen. And this is one more reason why sometimes you may spend extra time with the fridge just trying to realize that the thing you’re looking for is out of the stock. 


## The solution (The Project):

This is a useful web application that can help user manage the fridge food by tracking all the items that he or his family members, roommates or colleagues have put in or out of the fridge, and this application gives an ability to build a detailed Wishlist where user can input the products that he need to buy and to use this wishlist as a regular shopping list when he is visiting supermarket. It is also possible to checkout the bought item from the wishlist and it will will automatically appear in the main list of the items that are currently in the fridge. 


## Technical information:

- Stack of used technologies:
    1. Flask — backend Python framework
    2. SQLite3 — database to store users data on the server
    3. JavaScript, html and css — front end part
    4. Figma — for layout design

- List of Implemented functions:
    1. What’s in the fridge — list on current fridge items
        - Add item to the fridge list function
        - List item selection function
        - Update selected function 
        - Remove selected function
    2. Wishlist — a “to buy” list
        - Add to wishlist function
        - Multiply items selection function
        - Remove all the selected items function
        - Done function — moving all the selected items from the wishlist to fridge list
    3. Fridge History — list of all the actions that have been taken with the fridge
        - A list of all the actions that have been taken with the fridge items of the account
            - The rows in the history table are automatically colored depending on the action (added, updated or removed from fridge list)
        - Clear history function — is extremely needed because at some point the amount of the data in the history database may be so enormous that it may lag on the user’s browser
    4. Filter function — an algorithm that comparing filter input and the items in the tables word by word to show not only the final result but all the items that starts with the same words and doing it on real time
    5. Voice input — any text or number input in the app (except of sign in and signup pages) is accompanied by the voice recognition option to make the app usage very easy and friendly
    6. Google search selected items by names
    7. User settings page:
        - Ability to upload a profile picture from computer to the account, and in case the user ever decides to change the picture — the new image will be set and the old one will be removed from the server storage directory to free space.
        - Logout function
        - Clear fridge history function that requires user’s confirmation before applied
    8. Sign in function
    9. Sign up function
    10. Fully adaptive and responsive layout — looks well on any modern browser and device
    11. Browser language detection function



