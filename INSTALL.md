# ADA - CHATBOX
A Simple Application that exposes REST API with the below mentioned 4 operations. The API is restricted to use in-memory message store and handles request data only in *application/x-www-form-urlencoded* and *application/json* formats. Included *application/x-www-form-urlencoded*  validation in code to implement UI for the chatbox. In order to interconnect the containers in local, used *docker link* while creating the containers using docker compose.
 
The responses from the api is *application/json* and has following fields to provide information about the operations.

*status - Http status of the request made

action - The name of the API function

error - error encountered during the api execution(if any)

info - status of the operation and miscellanious information

response - The message contents(if no errors)*

### Requirements

[docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce-1)

[docker-compose](https://docs.docker.com/compose/install/)

#### 1. Allows user to post new message
Users can submit new messages to the api URL **/message** using HTTP POST method. It accepts all sort of messages from integer and string but not a blank message.


#### 2. Retrieve conversation using conversation-id
Users can retrieve specific conversation from the store by sending a GET request to the api **/conversation/*conversation-id***, where conversationID is the unique ID allotted to the set of messages while adding it to the store. A *404* message is excepted when the request conversation ID is not in the store.


### Technical Information
The API is written in python using the flask framework for the web services. A Sample output is given below:

    $ curl -X POST http://localhost:5000/message -H "Content-Type:application/json" -d '{"conversation_id":"010","sender":"ada","message":"hello, welcome to ada"}'
    {"action":"Add Message","error":null,"info":"Success","response":{"conversation_id":"010","created":"2019-09-20T05:37:18.771Z","message":"hello, welcome to ada","sender":"ada"},"status":200}
    $ curl http://localhost:5000/conversations/010
    {"action":"List messages under a conversation id","error":null,"info":"Success::","response":{"id":"010","messages":[{"created":"2019-09-20T05:37:18.771Z","message":"welcome to ada","sender":"ada"},{"created":"2019-09-20T05:37:12.207Z","message":"thank you","sender":"ram"}]},"status":200}

### Deployment
The application stack has been built with two component services *web* and *dynamodb*. These services are configured to run on docker platform.

Docker compose file *docker-compose.yml* used to deploy the infra, the build can be done via the below steps:
    
    # Clone the repo
      git clone url

    # change to the cloned repo dir
      cd dir_name

    # Build using docker-compose
      docker-compose build
    
    # Start the containers 
      docker-compose up -d
 
 ### Scope of Improvements
1. Attach a block storage to the dynamodb container to increase the level to data persistance
2. Used docker link to connect between container of web-app and dynamo, We can use remove this using orchestartion platforms.
3. Implement a web UI to make the chatbox more user friendly using flask(webix).
4. Implement more validation on user inputs tests.
5. Change the directory structure of the webapp to universal standards instead of single script file. 

## License - MIT


Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
