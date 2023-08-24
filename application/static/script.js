/* Function to generate categories for user selection based on genre selection (Fiction or Non-Fiction) */
function updateCategories() {
            /* Identify the two input filters to link up and assign the value of the genre to a variable */
            var genreSelect = document.getElementById("genre");
            var categorySelect = document.getElementById("category");
            var selectedGenre = genreSelect.value;

            /* Record the chosen genre for filtering purposes */
            document.getElementById("selected_genre").value = selectedGenre;

            /* Declare an empty string for the category dropdown menu */
            categorySelect.innerHTML = "";

            /* If statement to decide on which categories to show the user based on the selected genre */
            if (selectedGenre === "fiction") {
                var categories = [
                "Adventure",
                "Crime",
                "Dystopian",
                "Fantasy",
                "Horror",
                "LGBTQ+",
                "Literary",
                "Mystery",
                "Romance",
                "Science Fiction",
                "Thriller"
                ];
            } else if (selectedGenre === "non-fiction") {
                var categories = [
                "Business",
                "Cooking",
                "Crafts & Hobbies",
                "Gardening",
                "Music",
                "Nature",
                "Philosophy",
                "Politics",
                "Religion",
                "Travel",
                "True Crime"
                ];
            }

            /* For loop to create an option for user to choose from in the dropdown menu */
            for (var i = 0; i < categories.length; i++) {
                var option = document.createElement("option");
                option.value = categories[i];
                option.text = categories[i];
                categorySelect.appendChild(option);
            }
        }

        /* Initialize the categories based on the default genre selection */
        updateCategories();


/* Function for user to email generated reading list to themselves */
function sendEmail() {
            var emailAddress = document.getElementById('email').value; /* Get the user's input to set as the email address */
            var webpageURL = window.location.href; /* Set the link to send as the results page */
            var emailSubject = "Your ChatpterOne Reading List"; /* Set the email subject to a default string */
            var emailBody = webpageURL; /* Set the results page URL as the body of the email */
            var mailtoLink = "mailto:" + emailAddress + "?subject=" + encodeURIComponent(emailSubject) + "&body=" + encodeURIComponent(emailBody); /* Create the mailto: link using the variables declared above using the encodeURIComponent() function to make sure the link is properly encoded */

            /* Opens the user's default email client with a new message populated with the variables declared above */
            window.location.href = mailtoLink;
        }

        /* Open the user's default email client to send the selected email recipient the results page URL */
        sendEmail();