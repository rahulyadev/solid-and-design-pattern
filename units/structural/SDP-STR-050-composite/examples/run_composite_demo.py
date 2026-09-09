from dataclasses import replace

from work_plan import Group, Task, describe, walk_tasks


def main() -> None:
    kit = Group("kit", (Task("cut", 12), Task("label", 3)))
    plan = Group("workshop", (Task("setup", 5), kit, kit))
    print(describe(kit))
    print(describe(plan))
    for occurrence in walk_tasks(plan):
        print(occurrence.path, occurrence.task.name, occurrence.task.minutes)
    revised = replace(plan, children=(*plan.children, Task("cleanup", 4)))
    print("original:", describe(plan))
    print("revised:", describe(revised))


if __name__ == "__main__":
    main()
