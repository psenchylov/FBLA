import sys
from PyQt6.QtWidgets import *

#main class - main window 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() #calling QMainWindow to do all magic
        self.setWindowTitle("Alpharetta High School GPA Calculator")  
        self.setStyleSheet("background-color: lightgrey; border: 1px solid blue;")
        
        self.score_fields = list() #a list to keep entry fields pairs, a core data structure! 
        self.score_fields.append((QTextEdit(), QTextEdit())) #set an initial pair "class-score"

        self.label_calculated_gpa = QLabel("0") #set initial value to GPA 

        #it's a hack. padding-bottom moves down the buttons
        self.label_calculated_gpa.setStyleSheet("border: 0; padding-bottom: 10px; font-weight: bold;")
        
        self.resize(400, 100) #window size 
        container = self.create_central_widget() #draw the all components 
        self.setCentralWidget(container) #re-draw the window 
     
	#what to do when the button "Add class name and grade" is pressed 
    def add_class_handler(self):
        new_pair_fields = (QTextEdit(), QTextEdit()) #creating two fields as a tuple!
        self.score_fields.append(new_pair_fields) #adding these two fields to the list 
        container = self.create_central_widget() #create a central widget again (with the new fields in the list)
        self.setCentralWidget(container) #re-set the window content

    #what to do when the button "Clear All Fields" is pressed 
    def clear_all_handler(self):
        self.score_fields = [] #clean up a list of fields 
        self.score_fields.append((QTextEdit(), QTextEdit())) #adding the first empty pairs 
        container = self.create_central_widget() #create a central widget again 
        self.setCentralWidget(container) #re-set the window 
        self.resize(400, 100) #resize the window. DOES NOT WORK WHEN IT'S PRESSED FIRST! HELP IS NEEDED!
    
    #what to do when the button "Clear All Fields" is pressed 
    def calculate_gpa_handler(self):
        class_dict = {} #this is a -=dictionary=- to keep all grades from all entered fields  
        for element in self.score_fields: #reading the element from the list
            class_text_edit, score_text_edit = element #unpacking the tuple 
            class_name = class_text_edit.toPlainText() #getting a class name from the QTextEdit
            score_value = score_text_edit.toPlainText() #getting a score from the QTextEdit
            if score_value.isdigit(): #it might be text, so we need to check it first 
                score_text_edit.setStyleSheet("color: black;") #it's neccessary if it was colored red before 
                class_dict.update({class_name:int(score_value)}) # put a class score
            else:
                score_text_edit.setStyleSheet("color: red;") #higlight the wrong field 
                score_text_edit.setPlainText("Should be digital") #add a suggestion to a user
                self.label_calculated_gpa.setText("n/a") #disable a GPA value if it was calculated
                break #no further calculations make sense 
        gpa_score = calculate_gpa(class_dict)
        self.label_calculated_gpa.setText(str(gpa_score)) #put the GPA to the label 


    def create_central_widget(self):
        #create a vertical layout for the whole window 
        self.window_layout = QVBoxLayout() 
        label_class_layout = self.create_label_layout() #create two labels-headers: Class Name and The Grade    
        self.window_layout.addLayout(label_class_layout) #adding labels to the window 

        for element in self.score_fields: #adding entry fields 
            class_text_edit, score_text_edit = element
            text_entry_class_layout = self.create_entry_class_layout(class_text_edit, score_text_edit)
            self.window_layout.addLayout(text_entry_class_layout)
        
        label_gpa_layout = self.create_gpa_layout() #adding GPA result labels 
        self.window_layout.addLayout(label_gpa_layout)
        
        button_layout = self.create_button_layout() #adding buttons 
        self.window_layout.addLayout(button_layout)
        
        container = QWidget() #a container that is keeping all the components we created above 
        container.setLayout(self.window_layout) 
        return container

    #create three buttons
    def create_button_layout(self):
        button_calculate =  QPushButton("Calculate GPA")                                               
        button_clear_all = QPushButton("Clear All Fields")
        button_add_class = QPushButton("Add class name and grade")

        #adding functions-handlers to the buttons 
        button_add_class.clicked.connect(self.add_class_handler)
        button_clear_all.clicked.connect(self.clear_all_handler)
        button_calculate.clicked.connect(self.calculate_gpa_handler)

        #create a horizontal layout to order buttons
        button_layout = QHBoxLayout() 
        
        #adding buttons to the button layout
        button_layout.addWidget(button_clear_all)  
        button_layout.addWidget(button_calculate)                  
        button_layout.addWidget(button_add_class)

        #I found this is necessary, otherwise the buttons inherit the main window style
        button_add_class.setStyleSheet("padding-top: 5px;padding-right: 5px;padding-left: 5px;padding-bottom: 5px;")
        button_calculate.setStyleSheet("padding-top: 5px;padding-right: 5px;padding-left: 5px;padding-bottom: 5px;")
        button_clear_all.setStyleSheet("color: red; padding-top: 5px;padding-right: 5px;padding-left: 5px;padding-bottom: 5px;")

        return button_layout 

    #create a horizontal layout and the labels 
    def create_label_layout(self):
        label_class_layout = QHBoxLayout()
        label_class_name = QLabel("Class name") 
        label_scope_value = QLabel("The grade")
        label_class_layout.addWidget(label_class_name)
        label_class_layout.addWidget(label_scope_value)

        #no borders needed for the labels 
        label_class_name.setStyleSheet("border: 0;")
        label_scope_value.setStyleSheet("border: 0;")
        return label_class_layout
    
    #creates a horizontal layout and puts the labels: GPA and Value
    def create_gpa_layout(self):
        label_class_layout = QHBoxLayout()
        label_gpa = QLabel("Your GPA = ") 
        label_class_layout.addWidget(label_gpa)
        label_class_layout.addWidget(self.label_calculated_gpa)

        #no borders needed for the labels 
        label_gpa.setStyleSheet("border: 0; padding-bottom: 10px; font-weight: bold;")
        
        return label_class_layout
    
    #create a horizontal layout and the entry fields  
    def create_entry_class_layout(self, class_text_edit, score_text_edit):      
        text_entry_class_layout = QHBoxLayout()
        
        class_text_edit.setFixedHeight(30)
        score_text_edit.setFixedHeight(30)
        
        text_entry_class_layout.addWidget(class_text_edit)
        text_entry_class_layout.addWidget(score_text_edit)
        return text_entry_class_layout

#the main calculating function. It's out of the class to make it available for the CLI version    
def calculate_gpa(grade):
        sum = 0
        num = 0
        for i in grade:
            if 90 <= grade[i] <= 100:
                sum += 4
                num += 1
            elif 80 <= grade[i] <= 89:
                sum += 3
                num += 1
            elif 70 <= grade[i] <= 79:
                sum += 2
                num += 1
            elif grade[i] >= 69:
                sum += 1
                num += 1
        result = round(sum/num, ndigits=1)
        return result
    
if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 1: #GUI version is called by default
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec()
    if len(sys.argv) == 2 and sys.argv[1] == '--cli':
        #calling the CLI version
        class_grade = 0
        class_dict = {}
        classes = True
        print("Welcome to our Alpharetta High School GPA calcultor!\n")
        while classes:
            print("1. Add a class")
            print("2. Calculate GPA")
            print("3. Exit the program")
            class_option = input("\nEnter the number to pick your option: ")
            if class_option == "1":
                print("\nYou have chosen to add a class.\n")
                class_name = input("Enter the name of the class: ")
                class_grade = float(input("Enter the grade for the class: "))
                class_credits = input("Enter the credits for the class: ")
                class_dict.update({class_name:class_grade})
                print("\nClass added successfully!")
            elif class_option == "2":
                if class_dict == {}:
                    print("\nPlease add a class first!!")
                else:
                    print("\nYou have chosen to calculate GPA!!")
                    gpa = calculate_gpa(class_dict)
                    print(f"\nYour GPA: {gpa}\n")
            elif class_option == "3":
                classes = False
                print("\nExiting the program. Goodbye!")
            else:
                print("Invalid option. Please Try Again!!\n")


