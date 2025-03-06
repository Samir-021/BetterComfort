-


Tribhuvan University 
Faculty of Humanities and Social Sciences 
Vishwa Adarsha College

“BetterComfort”
A PROJECT REPORT
Submitted to:
Department of Computer Application
Vishwa Adarsha College
Itahari-04, Sunsari
In partial Fulfillment of the requirements for the Bachelors in Computer Application 

Submitted by:
Samir Adhikari
TU Registration No: 6-2-465-23-2022
Utkarsha Katwal
TU Registration No: 6-2-465-32-2022
Under the Supervision of
Mr. Niroj paudel
 
 
Tribhuvan University 
Faculty of Humanities and Social Sciences 
Vishwa Adarsha College 

Supervisor’s Recommendation
I hereby recommend that this project prepared under my supervision by Samir Adhikari and Utkarsha Katwal entitled “BetterComfort” in partial fulfillment for the degree of Bachelor of Computer Application is recommended for the final evaluation. 






 
Signature
Niroj paudel
Supervisor
Lecturer
Vishwa Adarsha College
ABSTRACT
The BetterComfort project is an innovative web application designed to merge the functionalities of restaurants and hotel services, offering users a seamless platform for discovering and comparing accommodations and dining options. Built using HTML, CSS, and JavaScript for the frontend and Python with Django for the backend, the system is designed to provide real-time location-based guidance, directing users to nearby hotels and restaurants.
The application features functionalities such as user and establishment location tracking, access to contact details, user reviews, and rating systems, fostering an interactive and engaging user experience. By leveraging robust technologies, BetterComfort ensures scalability and compatibility with modern web standards.
With its intuitive interface and efficient backend integration, BetterComfort is poised to empower users to make informed decisions, optimize their travel experiences, and enhance satisfaction through a user-centric approach. The platform addresses the growing demand for location-based services and contributes to the hospitality industry's digital transformation.












ACKNOWLEDGEMENTS
It is with great pleasure that I express my deepest gratitude and heartfelt appreciation to my esteemed guide, Niroj Paudel, for their invaluable guidance, encouragement, and unwavering support throughout the development of this project. Their insightful suggestions and cooperative demeanor have been instrumental in the successful completion of this work.
We would like to express our sincere gratitude to the Head of BCA Department of Vishwa Adarsha college Mr. Khagendra Basnet for giving us this opportunity to undertake this project and providing continuous support and encouragement. 
We’re also grateful to the whole BCA Department of Vishwa Adarsha College for providing technical support to carry out the project work, to let us utilize all the necessary facilities of the institute and guiding us at each step during the project. 
At the end we would like to express our sincere thanks to our friends and others who helped and supported me throughout this specific project lifecycle.  

















 Table of Contents 
ABSTRACT	iv
ACKNOWLEDGEMENTS	v
List of Figures	ix
List of Tables	xi
List of Abbreviation	xii
Chapter 1: Introduction	1
1.1	Introduction	1
1.2	Problem Statement	2
1.3	Objectives	2
1.4	Scope and Limitation	3
Scope	3
Limitation	3
1.5	Report Organization	3
Chapter 2: Background Study & Literature Review	4
2.1 Background Study	4
2.2 Literature Review	4
Chapter 3: System Analysis & Design	6
3.1 System Analysis	6
3.1.1 Requirement Analysis	7
3.1.1.1 Functional Requirement:	7
3.1.1.2	Non-Functional Requirement:	7
3.1.2	Feasibility Study	8
3.1.2.1	Operational Feasibility:	8
3.1.2.2	Technical Feasibility:	8
3.1.2.3	Economic Feasibility:	8
3.1.2.4	Cultural Feasibility:	8
3.1.2.5	Legal Feasibility:	9
3.1.2.6	Schedule Feasibility:	9
3.1.3	Data Modeling (ER Diagrams)	11
3.1.4	Process Modeling (DFD)	12
3.2	System Design	14
3.2.1 Architecture Design	14
3.2.2 Database Schema	15
3.2.3 Interface Design	16
Chapter 4: Implementation and Testing	23
4.1 Implementation	23
4.1.1 Tools used	23
4.1.2	Implementation Details of Modules	23
4.2	Testing	24
4.2.1.	Test Case for unit Testing	24
User Login Test 1.1	25
User Registration Test 1.2	26
Admin Login Test 1.3	26
4.2.2	Test Case for System Testing	27
Hetol/Restro Add Test 1.1	28
Hotel/Restro Delete Test 1.2	28
Saved Hotel/Restro Test 1.1	29
Delete Hotel/Restro Test 1.2	30
Book Hotel Test 1.3	30
Cancel Booking Test 1.4	31
Review and Rate Test 1.5	31
Chapter 5: Conclusion and Future Recommendations	33
5.1 Lesson Learnt/Outcome	33
5.2 Conclusion	33
5.3 Future Recommendation	33
References	34



 
List of Figures
Figure 1: Diagram of Iterative Waterfall Methodology……………………………......…...6
Figure 2: Gantt Chart ……………………………………………………….……………..9
Figure 3 Case diagram of BetterComfort…………………………………………...…….10
Figure 4: ER diagram of BetterComfort…………………………………………..…...….11
Figure 5: Context Diagram for BetterComfort……………………………………...…….12
Figure 6: Data Flow Diagram (Level 1) for BetterComfort……………………………….13
Figure 7: System Architecture…………………………………………….………..…….14
Figure 8: Database Schema……………………………………………….…………...….15
Figure 9.1: Login Page…………………………………………………….……..……….16
Figure 9.2: Registration Page……………………………………………….…………….17
Figure 9.3: Registration Page……………………………………………….…………….17
Figure 9.4: Admin page…………………………………………………….…………….18
Figure 9.5: User page…………………………………………………….……………….18
Figure 9.6 Query Searching……………………………………………….…..………….19
Figure 9.7: Hotel and Restaurant detail…………………………………….…………….19
Figure 9.8: Review and Rating……………………………………………………...…….20
Figure 9.9: Saved list…………………………………………………….……………….20
Figure 9.10: Booking hotels……………………………………………………....………21
Figure 9.11: Booking Complete……………………………………………….…….……21
Figure 9.12: View the booked hotels…………………………………………….……….21
Figure 9.13: About us page……………………………………………………………….22
Figure 9.14: Services page……………………………….…………………….…………22








 
List of Tables
Table 1: List of Products……………...…...........................................................................5
Table 2: Test case for User/Admin login…........................................................................ 25 
Table 3: Test case for User Registration…...….................................................................. 27
Table 4: Test Case for admin module ................................................................................ 27
Table 5: Test Case for user module …................................................................................ 29

 
CSS 	: Cascading Style Sheet 
DFD 	: Dataflow Diagram 
ERD 	: Entity-Relationship Diagram 
HTML 	: Hyper Text Markup Language 
JS 	: Java Script 
SQLite	: Structured Query Language - Lite
UI 	: User Interface 
API	: Application Programming Interface
List of Abbreviation
 
Chapter 1: Introduction
1.1	Introduction
The advent of Information Technology has revolutionized how people interact with their surroundings, making life more efficient and connected. With the rapid advancements in technology, applications now cater to a wide range of needs, integrating complex processes into seamless experiences. BetterComfort fulfill the user’s needs by directing them to their nearby hotels and restaurant. Users can book their hotels and add the hotels to their favorite list.
BetterComfort is an innovative platform designed to address the modern need for convenience in finding and managing nearby accommodations and dining options. The project integrates real-time location tracking to guide users to nearby hotels and restaurants, providing detailed information such as phone numbers, locations, reviews, and ratings. Built with a robust backend using Python and Django and an interactive frontend leveraging HTML, CSS, and JavaScript, BetterComfort offers a user-friendly interface that combines utility with elegance.
The primary objective of BetterComfort is to streamline the search for suitable accommodations and dining establishments, allowing users to save their favorite spots for future reference. By offering features such as real-time location guidance, customer reviews, and the ability to rate and save preferences, BetterComfort ensures an intuitive and engaging user experience. This project not only enhances convenience but also embraces the growing trend of location-based services to simplify decision-making for users in their daily lives.
BetterComfort serves as a testament to the potential of technology to bring efficiency, personalization, and satisfaction to users, enabling them to make informed choices with ease. It sets the foundation for future enhancements that can further enrich the user experience and establish itself as a reliable tool in the domain of location-based services.

1.2	Problem Statement
In today’s fast-paced world, finding suitable accommodations or dining options quickly and efficiently can be a challenging task. While platforms like TripAdvisor provide similar services, they often lack customization or features that cater to a user’s specific needs, such as real-time location guidance combined with personalized recommendations.
Many existing solutions rely solely on API data, which may not always reflect user preferences or include local entries, leading to a gap in information availability. Moreover, users often find it difficult to keep track of their favorite places or view accurate and updated reviews and ratings, making decision-making cumbersome.
Another challenge arises with users not having access to a platform that integrates both hotels and restaurants in a unified system, with features like saving favorites for future visits and access to detailed information such as phone numbers and locations. The absence of such a comprehensive solution leaves a gap in providing a seamless and satisfying user experience.
BetterComfort addresses these issues by combining the power of real-time location tracking, local database customization, and external API integration (via Geoapify) to guide users effectively to nearby hotels and restaurants while offering essential features like reviews, ratings, booking for hotels and favorites. This platform aims to bridge the gap between user needs and available technology, providing an intuitive, efficient, and user-friendly solution.
1.3	Objectives
The primary objective of the BetterComfort project is to develop an integrated platform that combines hotel and restaurant discovery.
•	To provide a user-friendly platform for discovering nearby hotels and restaurants using real-time location tracking.
•	To enable users to access essential information about hotels and restaurants, including phone numbers, locations, reviews, and ratings.
•	To allow user to book the hotels specifying check-in and check-out dates, number of adults, and children.
1.4	Scope and Limitation
Scope
•	Providing a platform that integrates real-time location tracking to guide users to nearby hotels and restaurants and book the hotels.
•	Allowing users to view essential details, such as phone numbers, locations, reviews, and ratings, for better decision-making.
•	Enabling users to save hotels and restaurants as favorites for quick access in the future.
Limitation
•	Reliance on the Geoapify API for data may lead to inaccuracies or incomplete information in certain regions.
•	The platform currently does not include advanced features like automated payment integration for booking.
•	The platform doesn’t provide multimedia like photos and videos of hotels and restaurants.
1.5	Report Organization
This report contains five chapters:
•	Chapter 1: Introduces the BetterComfort project, its objectives, scope, and problem statement.
•	Chapter 2: Provides the background study, related existing systems, and their merits and demerits.
•	Chapter 3: Covers system analysis, design, requirements, and feasibility analysis.
•	Chapter 4: Details the implementation, testing, and debugging processes.
•	Chapter 5: Discusses the conclusion, limitations, and future enhancements of the system.

Chapter 2: Background Study & Literature Review
2.1 Background Study
Where technology and internet access are integral to daily life, users demand quick and efficient solutions for their needs. The BetterComfort project leverages real-time location tracking and advanced APIs to simplify the process of finding nearby hotels and restaurants. The BetterComfort project addresses this gap by combining real-time geolocation services with a hybrid approach, integrating both API-fetched data and locally stored entries. This ensures users get not only personalized recommendations.
Key functionalities include:
•	Real-Time Location: Utilizing the Geoapify API to guide users to the nearest hotels and restaurants.
•	Search and Save: Allowing users to search for establishments and save them as favorites for future reference.
•	Details and Reviews: Providing users with contact details, location, ratings, and reviews to make informed decisions.
•	Booking: provide user to book the hotel and view them.
•	Local Database: Supporting locally added hotels and restaurants for comprehensive options.
2.2 Literature Review 
The BetterComfort project draws inspiration from advancements in location-based services and integrated platforms for customer convenience. Various systems and platforms have shaped the development of solutions aimed at enhancing user experience, with a focus on accessibility, interactivity, and reliability.
Location-based applications like TripAdvisor revolutionized the travel and hospitality industry by integrating features such as real-time reviews, ratings, and user preferences [1]. These systems have shown the value of combining user data and geographic APIs to deliver personalized recommendations, but they also face challenges such as limited database integration and user trust in automated suggestions [2].
Geoapify API, used in this project, is another milestone in location technology. It offers powerful tools to locate, filter, and present nearby points of interest (POI) based on user coordinates, showcasing the utility of combining geolocation with backend flexibility for customized experiences [3].
E-commerce platforms, including Shopify and Amazon, demonstrate the significance of user-friendly navigation and scalable systems [4]. Shopify, for example, evolved from a snowboarding equipment store into a versatile e-commerce platform by focusing on customer-centric design and developer-friendly tools [5]. Similarly, platforms like Zomato and OpenTable, designed for food and hospitality, highlight the importance of interactive features like restaurant booking, reviews, and user preferences [6].
The review highlights a critical gap in systems that cater to both hotels and restaurants while seamlessly integrating local databases and real-time geolocation APIs. BetterComfort addresses this gap by providing a hybrid system that balances API-fetched data with customizable local entries, creating a tailored, user-centric platform.
Table 1: List of Products 
S.N.	Product	Features
1	TripAdvisor	Real-time location, Review & rating, Favorites & Booking
2	Zomato	Real-time location, Review & rating, Hotel & Restaurant Listings
3	OpenTable	Restaurants Dinner Only, Review & rating, Favorites & Booking
4	Google Maps	Favorites & Bookmarks, Review & rating, Favorites & Booking
5	Airbnb	Hotels & Stays, Review & rating, Favorites & Booking
6	BetterComfort	Real-time location, Review & rating, Favorites & Booking and Custom local entries

BetterComfort differentiates itself by allowing both API-fetched and locally added hotels/restaurants, giving users real-time navigation, personalized interactions, and an integrated booking system.


Chapter 3: System Analysis & Design 
3.1 System Analysis
The BetterComfort project will utilize the Iterative Waterfall Model for its development process. This model combines the structured, phase-based approach of the Waterfall Model with the flexibility of iteration, allowing for refinements at each stage before progressing further. This approach ensures that the system is developed in a structured manner while still allowing modifications based on feedback and testing results.
In the analysis phase, system requirements are gathered and documented, with room for refinements as needed. The system will integrate the Geoapify API for location-based services and support local hotel and restaurant entries for customization.
The design phase is involved system diagrams, database structures, and UI prototypes, refined in iterations. The backend will use Python and Django, while the frontend will be built with HTML, CSS, and JavaScript.
During development and testing, the system is be built in increments, with each phase rigorously tested before progressing. This model ensures a structured yet flexible development process, enhancing reliability and user experience.
 
Figure 1: Diagram of Iterative Waterfall Methodology
3.1.1 Requirement Analysis
3.1.1.1 Functional Requirement: 
1.	Admin
I.	The admin is able to add, edit, delete hotel and restaurant listings.
II.	The admin is able to categorize products (hotels and restaurants) and manage categories.
III.	The admin is able to view and manage user accounts.
2.	Users
I.	The system is enabled users to securely register and log in to their accounts.
II.	The system is allowed users to browse hotel and restaurant listings, view details.
III.	The system is allowed users to view user and hotels locations.
IV.	The system is allowed saved the hotel and restaurant as favorite.
3.	External API
I.	The system is integrating with an external API (e.g., Geoapify API) to fetch real-time data for nearby hotels and restaurants based on the user's location.
II.	The external API is providing data that includes location, hotel/restaurant name, contact details, and available services for accurate display to users.
III.	The system is displaying the hotel and restaurant with 5000m and if no result found it will increase the radius with friendly error handling.
IV.	The system is periodically refreshing the data from the external API to ensure up-to-date listings.
3.1.1.2	Non-Functional Requirement:
I.	Security: Access is restricted to authorized users with valid credentials, and sensitive data (emails, phone numbers) is kept private
II.	Performance: The system should respond quickly to user inputs with minimal delay.
III.	Availability: The system is available online for user access at all times.
IV.	Reliability: The system is designed for consistent performance and minimal downtime.
3.1.2	Feasibility Study
3.1.2.1	Operational Feasibility:
The projects effectively combine hotel and restaurant services, offering features such as real-time location guidance using Geoapify API, detailed information on nearby places, and a user-friendly interface. Users can view phone numbers, addresses, reviews, and ratings for hotels and restaurants. Additionally, the system supports creating local database entries for hotels and restaurants and allows users to save favorites. Its intuitive interface, built with HTML, CSS, and JavaScript, ensures ease of use, enabling users with basic technical knowledge to navigate the platform effectively.
3.1.2.2	Technical Feasibility:
BetterComfort is technically feasible due to its reliance on accessible and efficient development tools. The backend is developed using Python and Django, ensuring robust and scalable functionality. The Geoapify API is utilized for fetching real-time location data and nearby hotel and restaurant information. The frontend leverages HTML, CSS, and JavaScript for a dynamic user experience. SQLite is employed as the database for its simplicity and integration with Django, making the system cross-platform and easily deployable.
3.1.2.3	Economic Feasibility:
This feasibility examines the cost-effectiveness of the BetterComfort system. The project is economically viable as it utilizes open-source tools like Django and SQLite, reducing software licensing costs. By streamlining hotel and restaurant discovery, review, and rating processes, the system offers significant time savings to users. Its real-time location guidance minimizes unnecessary travel costs for users. Hosting and maintaining the project require minimal expenses, making it a sustainable solution.
3.1.2.4	Cultural Feasibility:
Cultural feasibility assesses the acceptance and adaptability of the system by its users. BetterComfort is culturally viable as it addresses the modern user's need for convenient and efficient travel and dining experiences. By incorporating features such as personalized favorites, real-time guidance, and easy accessibility, the system aligns with user preferences. The visually appealing and interactive interface ensures users from diverse backgrounds can comfortably interact with the system.
3.1.2.5	Legal Feasibility:
BetterComfort adheres to legal considerations by leveraging open-source technologies like Python, Django, and SQLite, which are free from licensing issues. The use of the Geoapify API is subject to its terms and conditions, which are followed to ensure compliance. The system’s functionality aligns with privacy regulations, safeguarding user information such as location and saved preferences.
3.1.2.6	Schedule Feasibility:

 
Figure 2: Gantt Chart





Use case Diagram:
 
Figure 3: Case diagram of BetterComfort
3.1.3	Data Modeling (ER Diagrams)

 
Figure 4: ER diagram of BetterComfort
3.1.4	Process Modeling (DFD)

 

Figure 5: Context Diagram for BetterComfort










 

Figure 6: Data Flow Diagram (Level 1) for BetterComfort

3.2	System Design
The BetterComfort system follows a modular, layered architecture to ensure scalability, maintainability, and independence of components. This design enables localized changes without impacting other layers, promoting flexibility and ease of updates.
3.2.1 Architecture Design

 
Figure 7: System Architecture

  

 



3.2.2 Database Schema
 
Figure 8: Database Schema
3.2.3 Interface Design
Login
This layer has the user interface management. It incorporates login functionality that authenticates and verifies the system users. This page requires a username and password to start the application. Login is a process by which individual access to a computer system is controlled by finding and authenticating the user through the cardinalities by the user type.
 
Figure 9.1: Login Page

Registration
User can register the account by fill the information about you and click on register button.
 
Figure 9.2: Registration Page
Admin Login:
If he/she will login in the admin site then it will grant the all permission to manage, view, delete the hotel and restaurant with user data and manage the user preference.
 
Figure 9.3: Registration Page
Admin Window:
This page shows the details of registration user add/delete hotel and restaurant, view rating and review, manage saved hotel and restaurant.
 
Figure 9.4: Admin page
User Window:
This page shows the hotel and restaurant according to user query and allow to save the hotels, view the details of hotels and restaurant based on 5000m area.
 
Figure 9.5: User page

Query Searching:
Search for hotels and restaurant near your locations.
 
Figure 9.6 Query Searching
Hotel and Restaurant detail:
Details like phone number and address of the hotel/restaurant will be showed.
 
Figure 9.7: Hotel and Restaurant detail
Review and Rating:
The review and rating for hotel and restaurant can be showed and user and rate and leave the review.
 
Figure 9.8: Review and Rating
Saved/favorite list:
the hotel and restaurant that is saved for quick access will appear.
 
Figure 9.9: Saved list
Booking Process:
User can book the hotel and view the booked hotels.
 
Figure 9.10: Booking hotels
 
Figure 9.11: Booking Complete
 
Figure 9.12: View the booked hotels
About page:
This page shows the offers provided by BetterComfort project and mission of the project.
 
Figure 9.13: About us page
Services page:
This page shows the services provided by the platform.
 
Figure 9.14: Services page
Chapter 4: Implementation and Testing
4.1 Implementation
Implementation refers to the process where the planned system is developed into a working solution. This involves converting design specifications into a functional software system. Key steps in the implementation phase include coding, integration, testing, and documentation. For BetterComfort, this phase focused on providing a user-friendly interface, integrating real-time location services, and building a reliable backend system.
4.1.1 Tools used
•	Frontend:
I.	HTML
II.	CSS
III.	JS
IV.	Bootstrap (framework)
•	Backend:
I.	Python and Django
II.	SQLite Database
•	APIs and External Libraries:
I.	Geoapify API
II.	Leaflet.js
•	Development and Diagramming Tools:
I.	Draw.io
II.	PyCharm
4.1.2	Implementation Details of Modules
This project consists of two primary modules for implementation:
1.	Admin Module
The Admin Module is designed to provide administrative control over the platform. It is accessible only to authenticated admins with valid credentials. Once logged in, the admin can access the admin dashboard, where they can perform the following actions:
•	Add, update, or delete hotels and restaurants in the local database.
•	Manage user reviews and booking, including moderating inappropriate content if necessary.
•	View and analyze user ratings and feedback for continuous improvement.
2.	User Module
The User Module is accessible to all registered users. It provides functionality for users to interact with the platform seamlessly. Key features include:
•	Real-time Location Guidance: Users can find nearby hotels and restaurants using their current location.
•	Search Functionality: Users can search for hotels or restaurants based on location or name.
•	Favorites: Users can save their preferred hotels or restaurants for quick access later.
•	Reviews and Ratings: Users can leave reviews and rate hotels or restaurants to help others make informed choices.
•	Booking Platform: users can book the hotels specifying check-in and check-out dates, number of adults, and children and view the booked hotels.
4.2	Testing
The goal of testing is to ensure that the BetterComfort system meets its functional requirements and performs as expected. Testing verifies the accuracy of the program through various scenarios, identifying and resolving bugs. This process provides assurance that the system achieves its objectives effectively.
Testing involves several types, such as unit testing and system testing. The test plan identifies specific test cases within the system, which are described in detail below.
4.2.1.	Test Case for unit Testing
Unit testing is a type of software testing where individual units or components of software are tested. The purpose is to validate that each unit of the software code performs as expected. Unit testing is done during the development (coding phase) of an application by the developers. Unit Tests isolate a section of code and verify its correctness.
Table 2: Test case for User/Admin login
Cases	Test data	Expected outcome	Test
Outcome	Images
User
Login	Check Login credential for invalid username and Password	Error: Invalid username or password. Please try again.	Error: Invalid username or password. Please try again.	1.1
User
Login	Check login credential for valid username and password	Show home page	Show home page	1.2
Admin                       login	Check login credential for admin username and Password.	Show admin panel	Show admin panel	1.3

User Login Test 1.1
Test Case: User login
Test Data: Check login credential for invalid username and password
Expected Outcome: Invalid username or password. Please try again.
 
User Registration Test 1.2
Test Case: User login
Test Data: Check login credential for valid username and password
Expected Outcome: show home page
 
Admin Login Test 1.3
Test Case: Admin login
Test Data: Check login credential for valid admin username and password
Expected Outcome: show admin panel
 
Table 3: Test case for User Registration
ID	Test Case
Description	Test Data	Expected
Result	Annual
Result	Pass/Fail
1
	Users skip username	Username:
Email: admin@gmail.com
Password: admin	Display message**Please fill out this field**	As expected	pass
2
	Users enters an invalid email	Username: admin
Email: admin.gmail.com
Password: admin	Display message**Please include an @ in email**	As expected	pass
3	Users enters an existing username	Username: admin
Email: admin@gmail.com
Password: admin	Display message**Username already exists**	As expected	pass
4	Users enters valid email and password	Username: admin
Email: admin@gmail.com
Password: admin	Display message** Registration successful**	As expected	pass


4.2.2	Test Case for System Testing
Table 4: Test Case for admin module
ID	Test Case
Description	Test Data	Expected
Result	Test
Outcome	Images
1	Add Hotel/Restaurant	Add Hotel/Restro and saves to database	Show added hotel/restro	Show added hotel/restro	1.1
2	Delete hotel/restro	Delete hotel/restro from database	Successfully deleted	Successfully deleted	1.2

Hetol/Restro Add Test 1.1
Test Case: Add Hotel/Restro
Test data: Add Hotel/Restro and saves to database
Expected Result: Show added hotel/restro
 
Hotel/Restro Delete Test 1.2
Test Case: Delete hotel/restro
Test data: Delete hotel/restro from database
Expected Result: Successfully deleted
 
Table 5: Test Case for user module
ID	Test Case
Description	Test Data	Expected
Result	Test
Outcome	Images
1	Saved Hotel/Restaurant	Save Hotel/Restro to Favorites	Show favorited hotel/restro	Show favorited hotel/restro	1.1
2	Delete Hotel/Restaurant	Delete Hotel/Restro from Favorites	Successfully deleted	Successfully deleted	1.2
3	Book Hotel	Book Hotel to my booking	Show booked hotel	Show booked hotel	1.3
4	Cancel booking	Cancel booking hotel from my booking	Successfully cancelled!	Successfully cancelled!	1.4
5	Review and Rate Hotel/Restaurant	Rate and review the Hotel/Restro	Show Review and Rating	Show Review and Rating	1.5
Saved Hotel/Restro Test 1.1
Test Case: Saved Hotel/Restaurant
Test data: Save Hotel/Restro to Favorites
Expected Result: Show favorited hotel/restro
 
Delete Hotel/Restro Test 1.2
Test Case: Delete Hotel/Restaurant
Test data: Delete Hotel/Restro from Favorites
Expected Result: Successfully deleted
 
Book Hotel Test 1.3
Test Case: Book Hotel
Test data: Book Hotel to my booking
Expected Result: Show booked hotel
 
 
Cancel Booking Test 1.4
Test Case: Cancel booking
Test data: Cancel booking hotel from my booking
Expected Result: Successfully cancelled!
 
Review and Rate Test 1.5
Test Case: Review and Rate Hotel/Restaurant
Test data: Rate and review the Hotel/Restro
Expected Result Show Review and Rating

 















Chapter 5: Conclusion and Future Recommendations
5.1 Lesson Learnt/Outcome
The system was able to attain some of the goals that were set the beginning of development. Below are a few of those goals that were reached:
•	Users can search for nearby hotels and restaurants using real-time location tracking for better navigation.
•	The platform provides essential details such as phone numbers, locations, reviews, and ratings to help users make informed decisions.
•	Users can save hotels and restaurants as favorites for quick access.
•	A booking system is implemented, allowing users to reserve hotels, specify check-in and check-out dates, and select the number of adults and children.
5.2 Conclusion 
The BetterComfort project successfully integrates real-time location tracking to help users find nearby hotels and restaurants efficiently. By leveraging the Geoapify API, the platform fetches hotel and restaurant data while also allowing manual entries in a local database to ensure broader coverage. Users can access key details such as location, contact information, reviews, and ratings, making it easier to make informed decisions.
A major enhancement to the system is the hotel booking feature, which allows users to select check-in and check-out dates, specify the number of adults and children, and confirm reservations. Since the API does not provide availability data, this feature ensures that users can still book hotels seamlessly. Additionally, the favorites feature enables users to save preferred hotels and restaurants for future reference.
5.3 Future Recommendation
While BetterComfort has successfully achieved its core objectives, several enhancements can be made in the future to improve its usability, efficiency, and user engagement. This project serves as a strong foundation for a more advanced platform with additional features. Below are some recommendations for future improvements:
I.	Multimedia Enhancements – Allow hotel and restaurant owners to upload high-quality images and videos to enhance user decision-making and improve visual appeal.
II.	Integration of Payment Methods – Implementing a secure online payment system would allow users to confirm bookings directly through the platform, improving convenience and reliability.
III.	Table Reservation for Restaurants – Introduce a menu display with an option to book tables in advance for a more convenient dining experience.
IV.	Availability & Pricing API Integration – If available, integrating real-time hotel pricing and also for restaurant availability APIs would make the process more dynamic and accurate.
V.	Room Selection for Hotels – Add a feature for users to choose specific room types (e.g., deluxe, suite, standard) with images and descriptions during booking.

References
[1] Tripadvisor, Inc., “About Tripadvisor,” 2024. [Online]. Available: https://www.tripadvisor.com
[2] T. Filieri, “What makes an online consumer review trustworthy?,” Journal of Business Research, vol. 69, no. 2, pp. 758–769, 2016. DOI: 10.1016/j.jbusres.2015.07.002
[3] Geoapify, “Geoapify location-based API services,” 2024. [Online]. Available: https://www.geoapify.com
[4] Amazon.com, Inc., “Amazon’s approach to customer experience,” 2024. [Online]. Available: https://www.aboutamazon.com
[5] Shopify Inc., “Shopify’s evolution as a global e-commerce platform,” 2024. [Online]. Available: https://www.shopify.com
[6] Daraz Nepal, “Daraz: Online shopping in Nepal,” 2024. [Online]. Available: https://www.daraz.com.np



