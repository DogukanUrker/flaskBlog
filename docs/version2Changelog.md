# FlaskBlog v2 📜

**English** | [Türkçe](./version2Changelog_tr.md)
![app](https://github.com/DogukanUrker/flaskBlog/blob/main/images/Light.png?raw=true)

## What's Changed 🔥

- reCAPTCHA v3 verification system added: We added a new verification system to prevent spam and bots from accessing our app. reCAPTCHA v3 is a Google service that analyzes the behavior of visitors and assigns them a score based on how likely they are to be human. This way, we can protect our app without interrupting the user experience with annoying challenges or pop-ups.
- UI rebuilt with TailwindCSS: We decided to redesign our user interface using TailwindCSS, a utility-first CSS framework that allows us to create custom designs with ease. TailwindCSS provides us with a set of low-level classes that we can combine to create any style we want, without writing any custom CSS. This makes our code more readable, maintainable, and consistent across the app.
- Emojis were removed from the UI and Tabler Icons were added instead: We noticed that some of our users had issues with displaying emojis correctly on their devices, so we decided to replace them with Tabler Icons, a set of free and open-source icons that are designed to be simple and elegant. Tabler Icons are compatible with all browsers and platforms, and they look great on any screen size or resolution.
- Playwright tests added: We added automated end-to-end tests using Playwright, a cross-browser testing tool that allows us to write tests in Python that run on Chromium, Firefox, and WebKit. Playwright helps us to ensure that our app works as expected on different browsers and devices, and to catch any bugs or errors before they affect our users.
- Post categories: We added a new feature that allows users to categorize their posts into different topics, such as science, sports, games, etc. This way, users can easily find and filter posts that interest them, and discover new content from other users who share their interests.
- Add sort button for index page: We added a new button that allows users to sort the posts on the index page by different criteria, such as date, views, name, etc. This way, users can customize their view of the posts and see the ones that are most important or interesting to them.
- More detailed mail content: We improved the content of the emails that we send to our users, such as welcome emails, password reset emails, verify account emails, etc. We added more information and instructions to help users understand and use our app better, and we also added some personalization and branding elements to make our emails more friendly and professional.
- Time zone awareness for all dates and times in app: We added a new feature that automatically detects and adjusts the dates and times in our app according to the user’s time zone. This way, users can see the correct and consistent time for their location, and avoid any confusion or misunderstanding with other users who are in different time zones.
- Post banners: We added a new feature that allows users to upload an image as a banner for their posts. This way, users can make their posts more attractive and eye-catching, and express their creativity and personality through their images.
- Share via X button added to posts page: We added a new button that allows users to share their posts with X. This way, users can easily spread their posts to a wider audience and increase their engagement and visibility.
- Metacolor adaptive to theme color: We added a new feature that automatically changes the color of the meta tags in our app’s HTML head according to the theme color that the user chooses. This way, we can improve the appearance and consistency of our app on different browsers and devices, and enhance the user experience and satisfaction.
- Constants(config) file added for custom app settings: We added a new file that contains all the constants and configuration variables that we use in our app, such as the app name, the app URL, the email address, the database credentials, etc. This way, we can easily manage and update our app settings in one place, and avoid hard-coding or repeating any values in our code.
- Code comments added to all Python/JavaScript/CSS/Jinja/Docker/YAML files: We added comments to all our code files to explain the purpose and functionality of each line or block of code. This way, we can make our code more understandable and readable for ourselves and other developers who work on our project, and facilitate the debugging and maintenance of our code.
- Docker integration: We integrated Docker into our project to simplify and standardize the development and deployment of our app. Docker is a tool that allows us to create and run our app in isolated containers that contain all the dependencies and configurations that our app needs. This way, we can ensure that our app works the same way on any machine or environment, and avoid any compatibility or dependency issues.
- Pipnv integration: We integrated Pipenv into our project to manage the packages and dependencies that our app requires. Pipenv is a tool that automatically creates and manages a virtual environment for our project, and keeps track of the packages that we install and use in our app. This way, we can easily install and update the packages that our app needs, and ensure that our app works with the correct versions of the packages.
- Sample data (users,posts and comments) added to the databases: We added some sample data to our databases to populate our app with some dummy users, posts, and comments. This way, we can test and demonstrate the functionality and features of our app, and see how our app looks and behaves with real data.
- Important SQL injection security fixes: We fixed some security vulnerabilities in our app that could allow malicious users to execute SQL commands on our databases by injecting them into the input fields or the URL parameters of our app. This way, we can prevent any unauthorized access or manipulation of our data, and protect our app and our users from any potential harm or damage.
- Logging system remade and more detailed logging messages added: We remade our logging system to improve the quality and quantity of the messages that we log in our app. We added more details and information to our logging messages. We also added different levels of logging, such as danger, success, info, warning, sql, etc. This way, we can monitor and track the activity and performance of our app, and identify and resolve any issues or errors that occur in our app.
- Turkish and Russian translations for documentations: We added Turkish and Russian translations for our documentations, such as the readme file, the user guide, the developer guide, etc. This way, we can make our project more accessible and inclusive for users and developers who speak these languages, and increase the reach and popularity of our project.
- Readme file rewrited: We rewrote our readme file to make it more informative and attractive for our project. We added more sections and details to our readme file. We also added some badges and icons to our readme file to make it more appealing and professional.
- Create and edit posts in mobile: We added a new feature that allows users to create and edit their posts on their mobile devices. This way, users can use our app more conveniently and flexibly, and post their content anytime and anywhere.
- Module version updates: We updated the versions of the modules that we use in our app, such as Flask, Requests, Jinja, etc. This way, we can take advantage of the latest features and improvements of these modules, and ensure that our app works with the most recent and stable versions of these modules.
- Optimize images by @imgbot: We optimized the images that we use in our app using @imgbot, a GitHub app that automatically compresses and optimizes the images in our repository. This way, we can reduce the size and improve the quality of our images, and make our app load faster and smoother.
- Log folder checker: We now have a check function that checks the log folder existence. If the log folder does not exist then it will be created.

## New Contributors 🫂

- @fliberd made their first contribution in <https://github.com/DogukanUrker/flaskBlog/pull/44>
- @barmar made their first contribution in <https://github.com/DogukanUrker/flaskBlog/pull/42> [commit](https://github.com/DogukanUrker/flaskBlog/commit/817f407a975f583eb55429dc1f92c0ea14a3ca3c)
- @imgbot made their first contribution in <https://github.com/DogukanUrker/flaskBlog/pull/54>
- @dependabot made their first contribution in <https://github.com/DogukanUrker/flaskBlog/pull/43>

## Code 🧑🏻‍💻

| Language       | files | blank | comment | code | total |
| -------------- | ----- | ----- | ------- | ---- | ----- |
| Python         | 63    | 544   | 1514    | 4150 | 6208  |
| Jinja Template | 32    | 179   | 373     | 1911 | 2463  |
| JavaScript     | 6     | 26    | 59      | 90   | 175   |
| CSS            | 4     | 10    | 25      | 79   | 114   |
| Sum            | 105   | 759   | 1971    | 6230 | 8960  |

[**Full Changelog**](https://github.com/DogukanUrker/flaskBlog/compare/1.1.0...2.0.0)
