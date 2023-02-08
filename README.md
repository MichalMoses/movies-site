# movies-site
A movie database website that was built as a final project in a Python course using Django framework
All the data in the site was scraped from TMDB.com. Scraping code included.

The website conatins three main screen as the user interface: 

1. Home screen. 
    Displays all the movies that exists in the database. 
    Contains filters for narrowing down the movie list.
    In the header of the page the user's options appear: creating account (sign up), logging in, logging out. Available only for superusers is the option to add a new        movie to the database. 
  
  ![main_page](https://user-images.githubusercontent.com/119158314/217504609-888f3133-4c22-46ec-b2e3-3239c4e767ac.png)

  
 2. Movie page. 
    A page for each movie. 
    displays the movie poster, details, overview, and rating. 
    displays the list of actors with their photo, name and character. Each actor is clickable and will lead to the actor page. 
    displays an 'add review' button and a list of all reviews. Each reivews can be ranked liked\disliked. The review list is sorted by the number of likes.
    
  ![movie_page](https://user-images.githubusercontent.com/119158314/217505096-c9dc75a8-7eeb-4433-8efc-3594d05fb459.png)

3. Actor page.
   A page for each actor. 
   displays the actor portrait and some stats
   displays the actor filmography. each film is clickable and will lead to the movie page.
   
   ![actor_page](https://user-images.githubusercontent.com/119158314/217505318-02f366ef-9c22-45d4-9379-1c42d1497cc4.png)
   
   
