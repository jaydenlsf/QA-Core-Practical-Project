# QA DevOps Core Practical Project

## Contents
- [Brief](#brief)
    - [Requirements](#requirements)
    - [Proposal](#proposal)
- [Architecture](#architecture)
    - [Risk Assessment](#risk-assessment)
    - [Project Tracking](#project-tracking)
- [Infracstructure](#infrastructure)
    - [Continuous Integration Pipeline](#continuous-integration-pipeline)
    - [Database Structure](#database-structure)
    - [Interaction Diagram](#interaction-diagram)
    - [Docker Containers](#docker-containers)
    - [Testing Analysis](#testing-analysis)
    - [Refactoring](#refactoring)
- [Development](#development)
    - [Front-end Design](#front-end-design)
    - [Unit Testing](#unit-testing)
- [Footer](#footer)
    - [Future Improvements](#future-improvements)
    - [Author](#author)
    - [Acknowledgements](#acknowledgements)

## Brief
To create a service-oriented architecture for the application, this application must be composed of at least 4 services that work together.

### Requirements
In addition to the brief, the tech stack required is as follows:

- A Kanban board with full expansion on tasks needed to complete the project
- Provide a record of issues and risks that you faced while creating the project
- An application fully integrated using feature branch model into a version control system which will subsequently be built through a CI server and deployed to a cloud-based virtual machine
- If a change is made to a code base, a webhook should be sent to Jenkins to recreate and redeploy the changed application
- The project must follow the service-oriented architecture
- The project must be deployed using containerisation and an orchestration tool
- Create an Ansible playbook that will provision the environment that the application needs to run on
- The project must make use of a reverse proxy to make the application accessible to the user

### Proposal
The application will generate a random Alpha-2-code(country code), and then sends POST requests to external APIs to extract the country name, its population, and new Covid-19 cases.

## Architecture

### Risk Assessment
For any project, risk assessment is required for identifying, analysing and responding to risk factors throughout the life of the project. It helps to control possible future events and is proactive rather than reactive.

A detailed risk assessment can be seen below, outlining the potential risks associated with this project:

![risk-assessment](https://user-images.githubusercontent.com/54101378/121009665-5af0a000-c78c-11eb-95cc-51ae7b0a7f4a.png)

### Project Tracking
A Kanban board (Trello) was used to document the progress of my project, which has allowed me to effectively organise and prioritise tasks in a flexible way.

![trello](https://user-images.githubusercontent.com/54101378/120698979-b2022680-c4a7-11eb-9327-243fc5d44021.png)

The link to this board with updated lists can be found [here](https://trello.com/b/3ikIXUKP/qa-devops-core-practical-project).

## Infrastructure

### Continuous Integration Pipeline
The continuous integration approach allowed me to frequently integrate modified code, and this is achieved through the use of automated testing tools to check the code before full integration. Whenever a new commit is pushed to the `dev` branch on version control system (Github), Jenkins will automatically fetch the changes via Github webhook and run unit and integration tests:

![ci-pipeline](https://user-images.githubusercontent.com/54101378/120700876-1de58e80-c4aa-11eb-824c-95898e74c6cb.jpg)

#### 1. Test
- Unit tests are run and a coverage report is produced and can be viewed in the console log.

#### 2. Build docker-compose
- Build images for each service

#### 3. Push docker-compose
- Login to DockerHub by refering to the login credentials set on Jenkins' credential system, and then push the images to the repository specified

#### 4. Ansible configuration
- Install dependencies
- Setting up swarm manager and joining a swarm worker to the manager node
- Reload NGINX when a change is made to nginx.conf file

#### 5. Deploy
- Jenkins copies the `docker-compose.yaml` file over to the manager node, SSH onto it, and then runs docker stack deploy to deploy the app to all nodes

A stage view of the Jenkins pipeline set up can be seen in the image shown below:

![pipeline](https://user-images.githubusercontent.com/54101378/120932667-9f2d6300-c6ee-11eb-9f00-e61516ab9cf5.png)

### Database Structure
This application will only make use of one database as shown below:

![erd](https://user-images.githubusercontent.com/54101378/120701241-82a0e900-c4aa-11eb-8445-52ed2a3a706b.jpg)

### Interaction Diagram
The following diagram shows the layout of the virtual machines involved in this project. This demonstrates the interaction where the user connects to the NGINX machine on port 80.

![user-interaction](https://user-images.githubusercontent.com/54101378/120928976-fc211d00-c6de-11eb-93e2-fec97de877e0.png)

By using an orchestration tool (Docker Swarm), we are able to create a network of virtual machines that are able to be accessed by the user to provide the same service. NGINX serves as the load balancer, automatically directing the connection to the VM with the least connections. Apart from that, NGINX also improves the security of the application by further abstracting the application from the user.

### Docker Containers
The diagram below demonstrates the services interacting with each other.

![services](https://user-images.githubusercontent.com/54101378/120929190-01cb3280-c6e0-11eb-809b-110981ec7b7d.png)

#### Service 1 
- Serve the front-end of the application and is responsible for communicating with the other 3 services, and finally for persisting some data in a SQL database.

#### Service 2
- Generate a random 2 character string (country Alpha-2 code) and sends a GET request to http://country.io/names.json to check if the string is valid. If it is, return the Alpha-2 code and the name of the country.

#### Service 3
- Receive a POST request from Service 1, containing an Alpha-2 code, and then sends a GET request to https://restcountries.eu/rest/v2/alpha/{alpha-2-code} to get the population of the country.

#### Service 4
- Receive a POST request from Service 2, containing a country name, and then sends a GET request to https://www.worldometers.info/coronavirus/country/{country-name} to get new Covid-19 cases of the country. Service 4 also receives a POST request from Service 3 to get the population of that country and then calculate the percentage of population involved in the newly reported number of Covid-19 cases.

### Testing Analysis
In order to make sure that the application works as intended, testing is an essential part of the project. Since all 4 services rely on each other, it is crucial to test the functionality of individual routes, making sure each route is returning the desired information.

Since the majority of the data is obtained from external APIs, I had to test each of the GET requests sent to those APIs to make sure that the appropriate data is being received by my application. While sometimes the response could contain no data (404 errors) or unwanted information, these are needed to be eliminated in order to avoid having wrong information getting rendered to the frontend or stored in the database of the application.

![test-analysis](https://user-images.githubusercontent.com/54101378/120931277-c4b76e00-c6e8-11eb-9424-ad9f999369f2.png)

### Refactoring

Initially, `service 1`(country_api) would return a string containing the country code and country name seperated by '-', which is not an ideal way of representing data. Therefore, I decided to use `jsonify` to serialise the data, wrap it in a response object in Javascript Object Notation(JSON) format.

```python
@app.route("/get_country", methods=["GET"])
def get_country():
    country_url = "http://country.io/names.json"
    response = requests.get(country_url)
    countries = json.loads(response.text)
    letters = string.ascii_uppercase
    while True:
        random_country_code = "".join(random.choice(letters) for i in range(2))
        if random_country_code not in countries: continue
        else:
            return f"{random_country_code}-{countries[random_country_code]}"
```

```python
@app.route("/get_country", methods=["GET"])
def get_country():
    country_url = "http://country.io/names.json"
    response = requests.get(country_url)
    countries = json.loads(response.text)
    letters = string.ascii_uppercase
    while True:
        random_country_code = "".join(random.choice(letters) for i in range(2))
        if random_country_code not in countries: continue
        else:
            return jsonify({'country_code': random_country_code, 'country_name': countries[random_country_code]})
```



## Development

### Front-end Design
When navigating to the NGINX IP on port 80, the request will be sent to one of the VMs running docker swarm (swarm manager or swarm worker). Other than that, the user could also navigate to the IP of any of the swarm VMs on port 5000 to view the front-end of the application. The front-end of the application is displayed using HTML (with Jinja2) for the layout, and CSS for styling. Each time the user refreshes the webpage, the application will generate data for a different country, and then save the information to the database.

![front-end](https://user-images.githubusercontent.com/54101378/120931901-79eb2580-c6eb-11eb-9e79-bb79f22d4cb5.png)

### Unit Testing
Pytest was used to unit test the application. For the front-end, `requests-mock` module was also used to return known responses from HTTP requests without making an actual call. This is extremely useful as it it allows the developer to test the rest of the code without running into issues caused by random statements. Jenkins will automatically run the testing script whenever a new commit it pushed to Github, and it will display the result of the test in stage logs and also produces a coverage report showing the portion of code that was tested.

![unit-test](https://user-images.githubusercontent.com/54101378/120933029-3810ae00-c6f0-11eb-80c4-fe407a8177c2.png)

Below is the test report shown in JUnit.xml format, which is a useful Jenkins plug-in to publish test reports in graphical visualisation for tracking failures and so on. 

![test-result-trend](https://user-images.githubusercontent.com/54101378/120933742-6643bd00-c6f3-11eb-9a44-da3362f369ec.png)

## Footer

### Future Improvements
- Implement integration testing to test the application infrastructure as a whole, rather than mocking the application to it's routes as I did in unit testing.
- Improve CSS styling of front-end
- Save country codes and country names to a database so I don't have to rely on external API, which would also speed up the loading time of the application
- Add a refresh button to front-end
- Implement Nexus repository manager

### Author
Jayden Seng Foong Lee

### Acknowledgements
- [Oliver Nochols](https://github.com/OliverNichols)
- [Harry Volker](https://github.com/htr-volker)