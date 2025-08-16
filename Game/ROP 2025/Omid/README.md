# Concrete Evidence
Forensics Pursuit ROP: Concrete Evidence

Check out the [itch page](https://hemmatio.itch.io/forensic-pursuits-2025)

# Server guide
The webserver will run by default on `localhost:3000`, which is also what the game is configured to write to.
The api route is `/api/submit-progress`. Further details can be found in `index.js`.
Currently, the lab scene has progress tracking implemented.
The websever saves all saved progress to `progress-log.json`.

## Starting the server
Ensure that your `cd` is `webserver`. Then, run `npm start`. This will start the server and open the API endpoint.
