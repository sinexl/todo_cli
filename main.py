import shutil

FILE_PATH = r'./tasks.txt'


class Task:
    def __init__(self, description: str):
        self.desc = description
        self.is_completed = False

    def __str__(self) -> str:
        return f"{self.desc}\t\t\t" + ("Completed" if self.is_completed else "Not Completed")


def read_tasks_from_file(path: str = FILE_PATH) -> list[Task]:
    ls = []
    with open(path, "r", encoding='utf-8') as f:
        file_content = f.readlines()
    for i in range(0, len(file_content) - 1, 2):
        task = Task(file_content[i].strip())

        match file_content[i + 1].strip():
            case "False":
                task.is_completed = False
            case "True":
                task.is_completed = True
            case _:
                raise ValueError("Can't Read From File (Unknown format)")
        ls.append(task)
    return ls


def write_tasks_to_file(task_list: list[Task], path: str = FILE_PATH) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        for i in task_list:
            f.write(f'{i.desc}\n{i.is_completed}\n')


def print_tasks(ls: list[Task], term_width: int) -> None:
    print("═" * term_width)
    if not ls:
        print("You have no tasks")
        return
    for index, task in enumerate(ls):
        print(f"{index}\t{task}")
    # print("═" * term_width)


def main():
    todo_tasks: list[Task] = read_tasks_from_file(FILE_PATH)
    action_dict = {
        "l": "Show List of TODO tasks available",
        "c": "Create TODO task",
        'm': "Mark Task as done/not done",
        "r": "Remove the task",
        "h": "Show list of available actions",
        "w": "Save current TODO list and write it to the file",
        "q": "Save to the file and quit"
    }

    actions_string = "\n".join([f'\t{keyword} - {action}' for (keyword, action) in action_dict.items()])
    action = ""
    while True:
        terminal_size = shutil.get_terminal_size()
        unicode_line = "═" * (terminal_size.columns - 1)
        action = input(unicode_line +
                       f"\nPlease enter an keyword argument. Print 'h' for list of available arguments\n>>")
        match action:
            case "l":
                print_tasks(todo_tasks, term_width=terminal_size.columns - 1)
            case "c":
                task_desc = input("Task description\n\t>> ")
                if not task_desc:
                    print("Please enter a name of the task")
                else:
                    todo_tasks.append(Task(task_desc))
            case "m":
                try:
                    index = int(input("Enter Index Of Task\n>>"))
                    todo_tasks[index].is_completed = not todo_tasks[index].is_completed
                    print(f"'{todo_tasks[index].desc}' is now " + (
                        "Completed" if todo_tasks[index].is_completed else "Not Completed")
                          )
                except (IndexError, ValueError):
                    print("Please enter a number of existing task")
            case "r":
                try:
                    index_to_remove = int(input("Enter Index Of Task to remove\n>>"))
                    temp = todo_tasks[index_to_remove]
                    del todo_tasks[index_to_remove]
                    print(f"'{temp.desc}' was removed")
                except (IndexError, ValueError):
                    print("Please enter an index of existing task")
            case "q":
                write_tasks_to_file(todo_tasks, FILE_PATH)
                print(unicode_line)
                print(f"Saved {len(todo_tasks)} tasks to the file... ")
                exit(0)
            case "w":
                write_tasks_to_file(todo_tasks, FILE_PATH)
                print(unicode_line)
                print(f"Saved {len(todo_tasks)} tasks to the file... ")

            case "h":
                print(f"Available arguments: \n{actions_string}")
            case _:
                print("Unknown keyword argument")
    else:
        print("Exit...")


if __name__ == '__main__':
    # read_tasks_from_file(FILE_PATH)
    main()
