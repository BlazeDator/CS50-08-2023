/*
    When loading dynamically the <head> element which contained the css,
    the background went from white to grey, and the transition was bad,
    so I added the background color as early as I could.
*/
document.querySelector('html').style.backgroundColor = "#ebebeb";

/* Hiding the page */
document.querySelector('html').style.visibility = "hidden";

/* Showing a centered spinner while page isn't loaded */
document.querySelector('html').innerHTML +=
'<div class="spinner-border" role="status" '+
'style="width:5vw;height:5vw;position:absolute;top:47.5vh;left:47.5vw;visibility:visible;">'+
'</div>';


document.addEventListener('DOMContentLoaded', function()
{
    /*
        I also added the head element dinamically, so I don't have to rewrite it everytime.
        But I needed, to wait for the window to load the css or it would look weird
        So I implemented a hide and show code at the start and end of this script.
    */

    document.querySelector('head').innerHTML +=
    '<title>Paulo\'s Homepage</title>' +
    '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">' +
    '<link href="styles.css" rel="stylesheet"></link>' +
    '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>';

    /*
        I wanted to know which page was loaded by looking at the navbar, Bootstrap already had this
        functionality, but I was a bit confused how it was implemented, and I wanted to implement only
        stuff that I understood.

        So I wrote my own script that reads the Document URL, and then adds to the dinamically
        generated  navbar the correct class, to make sure it styles different.
    */
    let active = ["", "", "", ""];

    let current = document.URL;

    if (current.includes("index.html"))
    {
        active[0] = "active";
    }
    else if (current.includes("games.html"))
    {
        active[1] = "active";
    }
    else if (current.includes("movies-shows.html"))
    {
        active[2] = "active";
    }
    else if (current.includes("music.html"))
    {
        active[3] = "active";
    }
    /*
        Since i didn't want to write the nav bar and footer, in every possible page, I wanted a dinamyc way
        of inserting the code in each page. I tried it iframes, embeds and a lot of stuff I found online.
        Ultimately, after looking at some solutions using jquery, I looked at the lab from this week
        and tried using the code, used to add correct and inccorrect to the questions, to add the nav bar and footer,
        in the desired locations.

        So the script after the DOM loads, adds the right html code, that I trialed before on index.html,
        to any page containing <header> and <footer>.
    */
    document.querySelector('header').innerHTML =
    '<nav class="navbar nav-justified bg-dark">' +
        '<a class="nav-link btn ' + active[0] + '" href="index.html">         <h2>Home</h2>          </a>' +
        '<a class="nav-link btn ' + active[1] + '" href="games.html">         <h2>Games</h2>         </a>' +
        '<a class="nav-link btn ' + active[2] + '" href="movies-shows.html">  <h2>Movies/Shows</h2>  </a>' +
        '<a class="nav-link btn ' + active[3] + '" href="music.html">         <h2>Music</h2>         </a>' +
    '</nav>';

    document.querySelector('footer').innerHTML = '<h6>Created by Paulo Cunha, for CS50\'s Homepage Problem set.</h6>';
});

/* Showing the page once everything is loaded in, and hiding the spinner */
window.onload = function()
{
    document.querySelector('div.spinner-border').style.display = "none";
    document.querySelector('html').style.visibility = "visible";
}
