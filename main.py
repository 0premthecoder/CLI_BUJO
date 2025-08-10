import questionary
import json
import datetime

print()
DATA_FILE = f'{datetime.date.today()}-bujo.json'

help ="""
📚 BuJo CLI — Command Reference

.   Add a task  
-   Add a note  
o   Add an event 
x   For ticking a task to done
/   For marking it on doing

v   View your bullet journal  
ve  Viewing your Events Only
vt  Viewing your Tasks Only
vn  Viewing your Notes Only

q   quitting
"""

def loadData():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return data.get("tasks", {}) , data.get("notes", []) , data.get("events", [])
    except FileNotFoundError:
        return {}, [], []


tasks ,notes , events = loadData()

def save_data(tasks, notes, events):
    data = {
        "tasks": tasks,
        "notes": notes,
        "events": events
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def prinCli(todos, urNotes, urEvents):
    todo = ""
    for i in todos:
        todo += todos[i] + " " + i + "\n"
    
    if not todo:
        todo = "  (No tasks yet. Add one with '.')\n"

    note = ""
    for i in urNotes:
        note += "- " + i + "\n"
    if not note:
        note = "  (No notes yet. Add one with '-')\n"

    event = ""
    for i in urEvents:
        event += "◉ " + i + "\n"
    if not event:
        event = "  (No events yet. Add one with 'o')\n"

    print(f"""
╭───────────────────────────────╮
│        📝  BuJo CLI           │
╰───────────────────────────────╯

[Tasks]
{todo}[Notes]
{note}[Events]
{event}─────────────────────────────────
( / : Mark Doing | x : Mark Done )
( h : for help | q : Quit        )
─────────────────────────────────
""")

def changeTodoStatus(tasks, status):
    if not tasks:
        print("Nothing here..")
        return

    choices = [f"{tasks[task]} {task}" for task in tasks]
    
    selected = questionary.select(
        "📌 Select a task to update its status:",
        choices=choices
    ).ask()

    if selected:
        # Extract task text (removing the bullet prefix)
        print(selected)
        task_name = selected.split(' ', 1)[1]
        tasks[task_name] = status
        save_data(tasks, notes, events)
        print(f"\n✅ Changed Status {task_name}")
    else:
        print("❌ No selection made.")

print("📝 Welcome to BuJo CLI – Your terminal-based bullet journal.\nSimple. Fast. Focused.\nUse it to plan your day, track tasks, and reflect — without distractions.\nType `v` to get started.")


while True:
    options = input("").strip()

    match options.lower():
        case 'h':
            print(help)

        case '.':
            task = input("Whats the Work\n")
            if task in tasks:
                print("Already in")
            elif not task:
                print("type . for writting ur todo")
                continue
            else:
                tasks[task] = "●"
                save_data(tasks, notes, events)
                print("Finish it as soon as possible")  

        case '-':
            note = input("Type your note\n")
            if not note:
                print("type - for writting a note")
                continue
            notes.append(note)
            save_data(tasks, notes, events)
            print("Noted Down ✅")
    
        case '/':
            changeTodoStatus(tasks,"/")
        case 'x':
            changeTodoStatus(tasks, "⛌")

        case 'o':
            event = input("Type about Event\n")
            if not event:
                print("type o for Adding ur Events")
                continue
            events.append(event)
            save_data(tasks, notes, events)
            print("Added on Events ✅")

        case 'v':
            prinCli(tasks,notes,events)
        case 'vt':
            print("Tasks U have to Complete")
            for i in tasks:
                print(tasks[i] + i)
        case 've':
            print("Your events")
            for i in events:
                print("◉",i)
        case 'vn':
            print("Your Notes")
            for i in notes:
                print("-",i)
        case 'q':
            print("Exiting...")
            break
        case _:
            print("INVALID INSTRUCTION")
