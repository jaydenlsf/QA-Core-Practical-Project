# QA DevOps Core Practical Project

## Contents
- [Brief](#brief)

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
A detailed risk assessment can be seen below, outlining the potential risks associated with this project:

ADD IMAGE

The risk assessment for this project can be found in full [here](LINK) ADD LINK

### Project Tracking
A Kanban board (Trello) was used to document the progress of my project, which has allowed me to effectively organise and prioritise tasks in a flexible way.

![trello](https://user-images.githubusercontent.com/54101378/120698979-b2022680-c4a7-11eb-9327-243fc5d44021.png)

The link to this board can be found [here](https://trello.com/b/3ikIXUKP/qa-devops-core-practical-project).

### Testing Analysis
In order to make sure that the application works as intended, testing is an essential part of the project. Since all 4 services reliy on each other, it is crucial to test the functionality of individual routes, making sure each route is returning the desired information.

ADD TESTING ANALYSIS

## Infrastructure

### Continuous Integration Pipeline
The continuous integration approach allowed me to frequently integrate modified code, and this is achieved through the use of automated testing tools to check the code before full integration. Whenever a new commit is pushed to the `dev` branch on version control system (Github), Jenkins will automatically fetch the changes via Github webhook and run unit and integration tests:

#### 1. Test
- Unit tests are run and a coverage report is produced and can be viewed in the console log.

#### 2. Setup Docker
- Install docker (if it is not already installed) and add Jenkins to docker group

#### 3. Build docker-compose
- Build images for each service

#### 4. Push docker-compose
- Login to DockerHub by refering to the login credentials set on Jenkins' credential system, and then push the images to the repository specified

#### 5. Ansible configuration
- Install dependencies
- Setting up swarm manager and joining a swarm working to the manager node
- Reload NGINX when a change is made to nginx.conf file

#### 6. Deploy
- Jenkins copies the `docker-compose.yaml` file over to the manager node, SSH onto it, and then runs docker stack deploy to deploy the app to all nodes

![ci-pipeline](https://user-images.githubusercontent.com/54101378/120700876-1de58e80-c4aa-11eb-824c-95898e74c6cb.jpg)

### Database Structure
This application will only make use of one database as shown below:

![erd](https://user-images.githubusercontent.com/54101378/120701241-82a0e900-c4aa-11eb-8445-52ed2a3a706b.jpg)

### Interaction Diagram
The following diagram shows the layout of the virtual machines involved in this project. This demonstrates the interaction where the user connects to the NGINX machine on port 80.

![user-interaction](https://user-images.githubusercontent.com/54101378/120928976-fc211d00-c6de-11eb-93e2-fec97de877e0.png)

By using an orchestration tool (Docker Swarm), we are able to create a network of virtual machines that are able to be accessed by the user to provide the same service. NGINX serves as the load balancer, automatically directing the connection to the VM with the least connections. Apart from that, NGINX also improves the security of the application by further abstracting the application from the user.

### Docker Containers
The diagram below demonstrates the services interacting with each other.

![containers-diagram](https://user-images.githubusercontent.com/54101378/120701835-4621bd00-c4ab-11eb-81cd-2ee8a4d62496.jpg)

#### Service 1 
- Serve the front-end of the application and is responsible for communicating with the other 3 services, and finally for persisting some data in a SQL database.

#### Service 2
- Generate a random 2 character string (country Alpha-2 code) and sends a GET request to http://country.io/names.json to check if the string is valid. If it is, return the Alpha-2 code and the name of the country.

### Service 3
- Receive a POST request from Service 1, containing an Alpha-2 code, and then sends a GET request to https://restcountries.eu/rest/v2/alpha/{alpha-2-code} to get the population of the country.

### Service 4
- Receive a POST request from Service 2, containing a country name, and then sends a GET request to https://www.worldometers.info/coronavirus/country/{country-name} to get new Covid-19 cases of the country. Service 4 also receives a POST request from Service 3 to get the population of that country and then calculate the percentage of population involved in the newly reported number of Covid-19 cases.