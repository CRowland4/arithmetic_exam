import random
import datetime


class MiniExam:
    def __init__(self):
        self.level_numbers = {
            1: [str(integer) for integer in range(2, 10)],
            2: [str(integer) for integer in range(11, 30)]
        }
        self.level_descriptions = {
            1: "Simple operations with numbers 2-9. Enter the answer to the given problem.",
            2: "Integer squares in the range 11-29. Enter the square of the given number."
        }
        self.task_level = ''
        self.task_operators = ['+', '-', '*']
        self.task = ''
        self.user_answer = 0
        self.correct_answers_count = 0
        self.task_count = 0
        self.user_wants_report = None
        self.user_name = ''

    def give_tasks(self):
        self._get_level_choice()
        self._validate_level_choice()
        self._set_task_count()

        for _ in range(self.task_count):
            self._generate_task()
            self._get_user_answer()
            self._validate_user_answer()
            self._check_answer()

        self._give_score()
        self._ask_about_report()

        if self.user_wants_report:
            self._create_results_file()

        print("Bye!")

        return

    def _set_task_count(self):
        """Asks the user how many problems they would like to do."""
        while True:
            task_count = input("How many problems would you like? > ")
            if task_count.isdigit():
                self.task_count = int(task_count)
                return
            else:
                print("\nPlease enter an integer!")

    def _get_level_choice(self):
        """Asks the user to choose the difficulty of the tasks."""
        message = f"""Please choose a level.
                    1 - {self.level_descriptions[1]}
                    2 - {self.level_descriptions[2]}\n
                    Selection: > """
        self.task_level = input(message)

        return

    def _validate_level_choice(self):
        """Ensures that the user enters a valid level choice."""
        while self.task_level not in ['1', '2']:
            print("\nPlease enter the number corresponding to one of the options.")
            self._get_level_choice()

        return

    def _generate_task(self):
        """Generates a task based on the user's level choice."""
        task_generator = getattr(self, "_generate_level" + self.task_level + "_task")
        return task_generator()

    def _generate_level1_task(self):
        """Generates a level 1 task and assigns it to the task attribute, then prints the task."""
        operator = random.choice(self.task_operators)
        self.task = random.choice(self.level_numbers[1]) + operator + random.choice(self.level_numbers[1])
        print(self.task)
        return

    def _generate_level2_task(self):
        """Generates a level 2 task and assigns it to the task attribute, then prints the task."""
        self.task = random.choice(self.level_numbers[2])
        print(self.task)
        return

    def _get_user_answer(self):
        """Gets and a user answer and updates the appropriate attribute."""
        self.user_answer = input('> ')
        return

    def _validate_user_answer(self):
        while True:
            try:
                self.user_answer = int(self.user_answer)
            except ValueError:
                print("Incorrect format.")
                self._get_user_answer()
            else:
                return True

    def _check_level1_answer(self):
        """Checks the user answer to a level 1 task."""
        if self.user_answer == eval(self.task):
            return True
        else:
            return False

    def _check_level2_answer(self):
        """Checks the user answer to a level 2 task."""
        if self.user_answer == int(self.task) ** 2:
            return True
        else:
            return False

    def _check_answer(self):
        """Checks whether the user answered correctly."""
        task_checker = getattr(self, "_check_level" + self.task_level + "_answer")

        if task_checker():
            print("Right!")
            self.correct_answers_count += 1
        else:
            print("Wrong:(")

        return

    def _give_score(self):
        """Stores the users score and informs the user."""
        self.user_score = f'{self.correct_answers_count}/{self.task_count}'
        print(f'Your score is {self.user_score}.')
        return

    def _ask_about_report(self):
        """Asks the user whether or not they want a result file, and caches the answer."""
        answer = input("Would you like to save your result to the file? Enter yes or no. > ")
        if answer in ['yes', 'YES', 'y', 'Yes']:
            self.user_wants_report = True
        else:
            self.user_wants_report = False

        return

    def _get_user_name(self):
        """Gets and stores the name of the user."""
        self.user_name = input("What is your name? > ")
        return

    def _create_results_file(self):
        """Creates the results file for the user."""
        self._get_user_name()
        level_description = self.level_descriptions[int(self.task_level)]
        report = f'{self.user_name}: {self.user_score} in level {self.task_level} ({level_description}).'
        file_name = input("Enter a name for your new or existing results file (without an extension) > ")

        with open(file_name + '.txt', 'a+') as results:
            results.write(report)

        print(f'{datetime.datetime.now()}The results are saved in "{file_name}.txt"')

        return


my_test = MiniExam()
my_test.give_tasks()
