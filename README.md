# Restaurant.io
This is a web application that utilizes local restaurant information near Columbia University. The user can test all of the functions just by clicking buttons or inputing a specific into the textbox.  

## Authors
Chih-Hung(Namo) Lu (cl3519) 
Jordan Joonsang Park (jjp2181)

## Project Information
- Postgre SQL account: cl3519 
- URL of web application: (http://35.185.59.123:8111/)
- The application achieves all of the functions mentioned in Part 1, such as: 

	#1: List all the address of the restaurant (e.g. address of McDonald's)

	#2: List restaurants higher than the given rating and around me

	#3: How many and what restaurants around me opened now

	#4: List restaurants below the given cost and around me

	#5: List the restaurants nearby the subway station (e.g. 110 & Broadway)

	#6: List my favorite restaurant around me

	#7: List restaurants with certain foods around me (e.g. pizza, pasta, sushi, etc)

	#8: List restaurants available for pick-up around me

- The two most interesting functions are: 
	
	_#2: List restaurants higher than the given rating and around me_
	This function utilizes two inputs: the user id and minimum rating. The user id is chosen from the selective pool of database, since we do not have login feature. The minimum rating can be chosen as a number from 1 to 5 or an input into the textbox. These will search for corresponding restaruants given the location of the user. Currently, the query to estimate nearness is set as 0.005 difference in the langitudes and longitudes.   
    
    _#3: How many and what restaurants around me opened now_
    This function utilizes three inputs: the user id, day of the week, and timeslot (lunch or dinner). Originally, from Part 1 meeting and planning phrase, this function has been somewhat vague, due to the intermix of day of the week and timeslot (which was decided to be represented as a bit 0 or 1). However, on the front-end, there is no confusion because the user can just select the time on button.