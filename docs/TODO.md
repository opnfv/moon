Here is a list of what must be done to have complete version of the Moon platform.

Architecture

- Add a complete logging system
- Replace moon_orchestrator with Kubernetes

Actions that must be done before the next version:

- manage a token/uuid (ie session ID) in the moon_interface component
- add a timestamps in moon_router to know if the database has been modified
- rename moon_db and moon_utilities because they are not container but just libraries
- work on moonclient because it doesn't work with the new data model
- check all input from moon_interface (check that input data are correct and safe)
- Move @enforce from moon_db to API in Moon_Manager
- Need to work on unit tests with the new data model

Bugs to fix:

- Connect the authz functionality with the enforce decorator
- When adding user or VM in GUI, there is a bug in the backend (manager ?)
- GUI: in the "Projects" tab, move the "Map" link in the "Action" button
- GUI: move tabs in this order : "Models, Policy, PDP, Projects"
- Fixing Error Handling at module "Interface" & "Wrapper" according to this link 'http://flask-restful.readthedocs.io/en/0.3.5/extending.html#custom-error-handlers'
- in case an error occurred, it would be better throwing an exception rather than sending result with error code (as the exception was already thrown in some cases ) [ Interface, Wrapper]

Other actions:

- Some cleaning in all classes
- Write Installation procedures
- Write User and administrator documentation
- Run unit tests
- Add and run integration tests
- Need to check if the Moon platform still can retrieve users and roles from Keystone
- Need to retrieve VM from Nova
