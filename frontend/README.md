# InfinityEleNa FrontEnd

Steps to run the frontend angular server(Assuming this is a fresh ubuntu 20.04.1)

Open a new terminal window and navigate to the frontend folder


1. Install node npm package manager
```
sudo apt install npm;
```

2. Install angular cli
```
sudo npm install -g @angular/cli;
```

3. Navigate into my-maps-project directory. Install all the dependencies
```
cd my-maps-project;
npm install;
```

4. Setup the ng alias. This step varies from PC to Mac to Ubuntu Machine. The below step is for ubuntu machine. The path to ng changes.
```
alias ng=/usr/local/lib/node_modules/@angular/cli/bin/ng;
```

5. Start the angular server. Below command opens the application by default but incase it does not check in localhost: in the webbrowser of your choice
```
ng serve --open;
```
