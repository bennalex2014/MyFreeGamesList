Because we are using FreeToGame as our API, there are specific permissions that are required in order for the calls to work properly, and they are ones that do not work by default in any browser.

In order to use this server, you must use a Chromium based browser with the Allow CORS: Access-Control-Allow-Origin extension.

This extension can be found at https://chromewebstore.google.com/detail/allow-cors-access-control/lhobafahddgcelffkeicbaginigeejlf

For our API, we use the FreeToGame API: https://www.freetogame.com/api-doc

To run the server, build the TypeScript files, and then use the command "flask run". To turn it off, hit CTRL-C in the terminal.