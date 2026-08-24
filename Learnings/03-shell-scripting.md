# DevOps — Chapter 3: Shell Scripting

## 1. Introduction to Shell Scripting

### What is Shell?

A shell is a program that allows us to communicate with the operating system through commands.

For example:

```bash
ls
```

asks the shell to list files.

```bash
mkdir project
```

asks the shell to create a directory.

```bash
cd project
```

asks the shell to change the current directory.

So the basic flow is:

```
You
 ↓
Shell
 ↓
Operating System
 ↓
Result
```

## 2. What is Shell Scripting?

Shell scripting means writing multiple shell commands in a file so that they can be executed automatically.

For example, instead of manually doing:

```bash
mkdir project
cd project
touch app.txt
echo "Hello" > app.txt
```

we can put everything inside:

```
setup.sh
```

and execute:

```bash
./setup.sh
```

The shell will execute the commands one after another.

## 3. Why is Shell Scripting Important in DevOps?

DevOps involves a lot of repetitive tasks.

For example:

- Creating directories
- Creating files
- Installing software
- Starting services
- Stopping services
- Checking servers
- Checking disk usage
- Checking processes
- Managing logs
- Taking backups
- Deploying applications
- Running tests
- Monitoring systems

Doing these manually every time is inefficient.

Shell scripting allows us to automate repetitive tasks.

The important idea is:

```
Manual Work
     ↓
Shell Commands
     ↓
Shell Script
     ↓
Automation
     ↓
DevOps
```

## 4. Bash

One of the most commonly used shells in Linux is Bash.

Bash stands for:

**Bourne Again SHell**

Other shells include:

- sh
- zsh
- fish
- ksh

On many Linux servers, Bash is commonly available.

## 5. Shell vs Shell Script

**Shell**

A program that interprets and executes commands.

**Shell Script**

A file containing shell commands and programming logic.

Example:

```
backup.sh
```

The shell reads this file and executes its instructions.

## 6. Shell Script File Extension

Shell scripts commonly use:

```
.sh
```

Example:

- `script.sh`
- `backup.sh`
- `deploy.sh`
- `setup.sh`

The `.sh` extension is a convention. The operating system does not require the extension, but using it makes the file's purpose clear.

## 7. Shebang

A shell script commonly starts with:

```bash
#!/bin/bash
```

This is called the **shebang**.

It tells the system which interpreter should be used to execute the script.

Example:

```bash
#!/bin/bash

echo "Hello World"
```

Another common form is:

```bash
#!/usr/bin/env bash
```

## 8. Creating a Shell Script

Create a file:

```bash
touch script.sh
```

Check it:

```bash
ls
```

Open it using an editor such as:

```bash
nano script.sh
```

Put:

```bash
#!/bin/bash

echo "Hello World"
```

Save the file.

## 9. Executing a Shell Script

There are two important ways.

### Method 1 — Execute through Bash

```bash
bash script.sh
```

Here, we explicitly tell Bash to interpret the file.

### Method 2 — Execute directly

First give execute permission:

```bash
chmod +x script.sh
```

Then:

```bash
./script.sh
```

`./` means:

Look for this file in the current directory.

## 10. Why chmod +x?

Linux has file permissions.

`x` means:

**execute**

Therefore:

```bash
chmod +x script.sh
```

adds execute permission to the script.

Then:

```bash
./script.sh
```

can execute it directly.

## 11. Comments

Comments are ignored by the shell.

A comment starts with:

```
#
```

Example:

```bash
#!/bin/bash

# This script prints a greeting

echo "Hello"
```

Comments are useful for explaining:

- What a script does
- Why something is being done
- Complex logic
- Important assumptions

## 12. Basic Linux Commands Inside Shell Scripts

Shell scripts can execute normal Linux commands.

For example:

```bash
mkdir project
```

creates a directory.

```bash
cd project
```

changes directory.

```bash
touch file.txt
```

creates a file.

```bash
echo "Hello"
```

prints text.

```bash
ls
```

lists files.

```bash
cat file.txt
```

displays file contents.

```bash
ps
```

shows processes.

```bash
df -h
```

shows disk usage.

```bash
who
```

shows logged-in users.

The important concept is:

**Shell scripting combines Linux commands with programming logic.**

## 13. Variables

Variables are used to store values.

Example:

```bash
name="John"
```

Now:

```bash
echo "$name"
```

produces:

```
John
```

## 14. Important Variable Rule

There must be **NO spaces** around `=`.

Correct:

```bash
name="John"
```

Incorrect:

```bash
name = "John"
```

Bash interprets spaces differently, so this will not create the variable as intended.

## 15. Accessing Variables

When retrieving a variable, use `$`.

```bash
name="John"

echo "$name"
```

Output:

```
John
```

You can also use braces:

```bash
echo "${name}"
```

## 16. Why Use ${}?

Suppose:

```bash
name="John"
```

and we want:

```
John123
```

We can write:

```bash
echo "${name}123"
```

Without braces, Bash may interpret the variable name differently when characters immediately follow it.

## 17. Quoting Variables

Prefer:

```bash
echo "$name"
```

rather than:

```bash
echo $name
```

Quoting is especially important when a variable may contain spaces.

For example:

```bash
name="John Smith"
```

Using:

```bash
echo "$name"
```

safely treats the value as one string.

## 18. Taking User Input

The `read` command is used to take input from the user.

Example:

```bash
read name
```

Then:

```bash
echo "Hello $name"
```

### Using `read -p`

Instead of separately printing a prompt:

```bash
echo "Enter your name:"
read name
```

we can write:

```bash
read -p "Enter your name: " name
```

Then:

```bash
echo "Hello $name"
```

Example:

```
Enter your name: Tanishq
Hello Tanishq
```

## 19. Command Substitution

Sometimes we want the output of a Linux command to become a variable.

We use:

```bash
$(command)
```

Example:

```bash
current_date=$(date)
```

Now:

```bash
echo "$current_date"
```

prints the date.

Another example:

```bash
username=$(whoami)

echo "Current user is $username"
```

Mental model:

```
Linux command
     ↓
command output
     ↓
$(command)
     ↓
stored inside variable
```

This is extremely useful in automation.

## 20. Arithmetic in Bash

Bash supports arithmetic using:

```bash
$((expression))
```

Example:

```bash
sum=$((5 + 10))

echo "$sum"
```

Output:

```
15
```

Using variables:

```bash
a=10
b=20

sum=$((a + b))

echo "$sum"
```

## 21. Arithmetic Operators

| Operator | Meaning      |
|----------|--------------|
| `+`      | Addition     |
| `-`      | Subtraction  |
| `*`      | Multiplication |
| `/`      | Division     |
| `%`      | Remainder    |

Example:

```bash
a=10
b=3

echo $((a + b))
echo $((a - b))
echo $((a * b))
echo $((a / b))
echo $((a % b))
```

## 22. Conditional Statements

Conditional statements allow a script to make decisions.

Basic structure:

```bash
if [ condition ]; then
    # commands
elif [ another_condition ]; then
    # commands
else
    # commands
fi
```

Important:

```
if
 ↓
condition
 ↓
then
 ↓
commands
 ↓
elif / else
 ↓
fi
```

`fi` marks the end of the if block.

## 23. Bash if Spacing

This is extremely important.

Correct:

```bash
if [ "$age" -gt 18 ]; then
    echo "Adult"
fi
```

Incorrect:

```bash
if["$age" -gt 18]; then
```

The spaces around `[`, condition, and `]` matter.

## 24. Numeric Comparison Operators

Bash uses special operators for integer comparisons.

| Operator | Meaning                  |
|----------|--------------------------|
| `-eq`    | Equal                    |
| `-ne`    | Not equal                |
| `-gt`    | Greater than             |
| `-lt`    | Less than                |
| `-ge`    | Greater than or equal    |
| `-le`    | Less than or equal       |

Example:

```bash
age=22

if [ "$age" -ge 18 ]; then
    echo "Adult"
else
    echo "Minor"
fi
```

## 25. if-else Example

```bash
read -p "Enter your age: " age

if [ "$age" -ge 18 ]; then
    echo "You are an adult"
else
    echo "You are a minor"
fi
```

## 26. elif

`elif` means:

**else if**

Example:

```bash
read -p "Enter marks: " marks

if [ "$marks" -ge 90 ]; then
    echo "A"
elif [ "$marks" -ge 75 ]; then
    echo "B"
elif [ "$marks" -ge 60 ]; then
    echo "C"
else
    echo "Needs improvement"
fi
```

Conditions are checked from top to bottom.

Once one condition is true, the corresponding block executes.

## 27. String Comparison

Common string operators:

- `=`
- `!=`

Example:

```bash
name="Tanishq"

if [ "$name" = "Tanishq" ]; then
    echo "Correct name"
fi
```

For string comparison, quote variables:

```bash
[ "$name" = "Tanishq" ]
```

## 28. File and Directory Tests

Shell scripts can check whether files or directories exist.

Important operators:

| Operator | Meaning              |
|----------|----------------------|
| `-f`     | Regular file exists  |
| `-d`     | Directory exists     |
| `-e`     | Path exists          |
| `-r`     | Path is readable     |
| `-w`     | Path is writable     |
| `-x`     | Path is executable   |

Example:

```bash
if [ -f "notes.txt" ]; then
    echo "File exists"
else
    echo "File does not exist"
fi
```

Directory:

```bash
if [ -d "project" ]; then
    echo "Directory exists"
fi
```

This is very useful for automation scripts.

## 29. Loops

A loop allows us to execute the same logic repeatedly.

Instead of:

```bash
echo 1
echo 2
echo 3
echo 4
echo 5
```

we can use a loop.

## 30. for Loop

Basic structure:

```bash
for variable in values; do
    commands
done
```

Example:

```bash
for i in {1..5}; do
    echo "$i"
done
```

Output:

```
1
2
3
4
5
```

## 31. Looping Through Multiple Values

```bash
for name in John Alice Bob; do
    echo "Hello $name"
done
```

Output:

```
Hello John
Hello Alice
Hello Bob
```

## 32. Looping Through Files

```bash
for file in *.txt; do
    echo "$file"
done
```

`*.txt` means:

all filenames ending with `.txt`

This is useful for processing multiple files automatically.

## 33. while Loop

A while loop continues as long as its condition is true.

Example:

```bash
count=1

while [ "$count" -le 5 ]; do
    echo "$count"
    count=$((count + 1))
done
```

Output:

```
1
2
3
4
5
```

## 34. Infinite Loops

Be careful with while loops.

If the condition never becomes false, the loop may continue forever.

Example:

```bash
while true; do
    echo "Running..."
done
```

This is an infinite loop.

In real DevOps systems, infinite loops can consume CPU/resources, so loops should be designed carefully.

## 35. C-style for Loop

Bash also supports:

```bash
for ((i=1; i<=5; i++)); do
    echo "$i"
done
```

It has:

- initialization
- condition
- update

Similar to loops you may already know from Java/C/C++.

## 36. Functions

Functions allow us to group commands into reusable blocks.

Syntax:

```bash
function_name() {
    commands
}
```

Example:

```bash
greet() {
    echo "Hello"
}
```

Call it:

```bash
greet
```

Output:

```
Hello
```

## 37. Functions with Arguments

Functions can receive arguments.

```bash
greet() {
    echo "Hello $1"
}

greet "Tanishq"
```

Output:

```
Hello Tanishq
```

Here:

```
$1
```

means the first argument passed to the function.

## 38. Script Arguments

A script can receive arguments from the command line.

Example:

```bash
#!/bin/bash

echo "First argument: $1"
echo "Second argument: $2"
```

Run:

```bash
./script.sh Hello World
```

Output:

```
First argument: Hello
Second argument: World
```

## 39. Important Special Variables

| Variable | Meaning                          |
|----------|----------------------------------|
| `$0`     | Name/path of the script          |
| `$1`     | First argument                   |
| `$2`     | Second argument                  |
| `$#`     | Number of positional arguments   |
| `$@`     | All positional arguments         |
| `$?`     | Exit status of previous command  |
| `$$`     | Process ID of current shell      |

These are extremely important for scripting.

## 40. Exit Status

Every command generally returns an exit status.

The standard convention is:

```
0       → success
non-zero → failure
```

Example:

```bash
ls /tmp
echo "$?"
```

If `ls` succeeds:

```
0
```

If a command fails, it normally returns a non-zero value.

This is extremely important in DevOps because CI/CD systems often use exit codes to determine whether a step succeeded or failed.

## 41. &&

`&&` means:

Execute the next command only if the previous command succeeds.

Example:

```bash
mkdir project && echo "Directory created"
```

If `mkdir` succeeds, the `echo` runs.

## 42. ||

`||` means:

Execute the next command if the previous command fails.

Example:

```bash
mkdir project || echo "Could not create directory"
```

## 43. Pipe |

A pipe sends the output of one command as input to another command.

Example:

```bash
ps aux | grep java
```

Concept:

```
ps aux
   ↓
output
   ↓
pipe |
   ↓
grep java
   ↓
filtered output
```

## 44. Pipe vs &&

These are completely different.

**Pipe**

```bash
command1 | command2
```

Means:

Send output of command 1 to command 2.

**&&**

```bash
command1 && command2
```

Means:

Run command 2 only if command 1 succeeds.

## 45. Output Redirection

We can send command output into a file.

### `>`

Overwrite the file:

```bash
echo "Hello" > output.txt
```

If the file already exists, its previous contents are replaced.

### `>>`

Append to the file:

```bash
echo "Another line" >> output.txt
```

The existing content remains and the new content is added at the end.

## 46. Standard Streams

Linux processes commonly use three standard streams:

```
stdin   → 0
stdout  → 1
stderr  → 2
```

**stdin**

Standard input.

**stdout**

Normal program output.

**stderr**

Error output.

Understanding these becomes important when working with servers, scripts, logs and CI/CD.

## 47. Redirecting Errors

Redirect errors:

```bash
command 2> error.log
```

Here:

```
2
```

represents stderr.

## 48. Redirecting Output and Errors

Example:

```bash
command > output.log 2>&1
```

This sends normal output to:

```
output.log
```

and redirects errors to the same destination.

## 49. Practical Script — System Information

```bash
#!/bin/bash

echo "===== SYSTEM INFORMATION ====="

echo "Date:"
date

echo "Hostname:"
hostname

echo "Current User:"
whoami

echo "Running Processes:"
ps

echo "Disk Usage:"
df -h
```

This demonstrates how ordinary Linux commands can be combined into an automated report.

## 50. Practical Script — Sum from 1 to N

Goal:

Input: `5`  
Output: `15`

Script:

```bash
#!/bin/bash

read -p "Enter a number: " n

sum=0

for ((i=1; i<=n; i++)); do
    sum=$((sum + i))
done

echo "Sum = $sum"
```

For:

```
n = 5
```

calculation:

```
0 + 1 = 1
1 + 2 = 3
3 + 3 = 6
6 + 4 = 10
10 + 5 = 15
```

## 51. Practical Script — Check a File

```bash
#!/bin/bash

read -p "Enter filename: " file

if [ -f "$file" ]; then
    echo "File exists"
else
    echo "File does not exist"
fi
```

This is a very common automation pattern.

## 52. Practical Script — Create Multiple Directories

```bash
#!/bin/bash

for directory in dev test prod; do
    mkdir -p "$directory"
done

echo "Directories created"
```

This could be useful when preparing environments.

## 53. Practical Script — Disk Usage

```bash
#!/bin/bash

echo "Disk Usage:"
df -h
```

A more advanced script could check the percentage used and generate an alert when disk usage becomes too high.

## 54. Environment Variables

Environment variables are variables made available to processes.

Example:

```bash
export APP_ENV="production"
```

Read it:

```bash
echo "$APP_ENV"
```

Common examples in DevOps:

- `APP_ENV`
- `DATABASE_URL`
- `PORT`
- `API_URL`
- `JAVA_HOME`
- `PATH`

## 55. Local Variable vs Environment Variable

**Local variable:**

```bash
name="Tanishq"
```

**Exported environment variable:**

```bash
export name="Tanishq"
```

The important difference is that an exported variable can be inherited by child processes.

Concept:

```
Parent Shell
     |
     | export
     ↓
Environment Variable
     |
     ↓
Child Process
```

Environment variables are extremely important later when we study:

- Docker
- Cloud
- CI/CD
- Applications
- Secrets/configuration

## 56. Never Hardcode Secrets

Do not put sensitive information directly into scripts that are committed to Git.

**Bad:**

```bash
PASSWORD="mySecretPassword"
API_KEY="123456"
```

Instead, secrets should normally be provided through secure mechanisms such as environment variables or secret-management systems.

This becomes especially important in DevOps.

## 57. Debugging Shell Scripts

Shell scripts can fail because of:

- Syntax errors
- Missing spaces
- Incorrect variable names
- Missing quotes
- Wrong file paths
- Permission problems
- Incorrect conditions
- Failed commands
- Unexpected input
- Infinite loops

Debugging is therefore an important DevOps skill.

## 58. bash -n

Use:

```bash
bash -n script.sh
```

This checks the script for syntax errors without executing it.

Example:

```bash
bash -n script.sh
```

If there is no output, the syntax is generally valid.

**Important:**

Passing `bash -n` does **NOT** mean the script logic is correct.

It only checks syntax.

## 59. bash -x

Use:

```bash
bash -x script.sh
```

This displays commands as Bash executes them.

It is extremely useful for debugging.

For example, if:

```bash
name="Tanishq"
echo "$name"
```

Bash can show the commands being executed.

## 60. Debugging with echo

A simple debugging technique is:

```bash
echo "DEBUG: name=$name"
```

This allows us to see the current value of a variable.

## 61. ShellCheck

ShellCheck is a static analysis/linting tool for shell scripts.

It can detect many common issues, including:

- Quoting problems
- Suspicious syntax
- Common scripting mistakes
- Potential bugs

Using tools such as ShellCheck is good professional practice.

## 62. File Permissions

Check permissions:

```bash
ls -l script.sh
```

Example:

```
-rwxr-xr-x
```

The `x` means executable permission.

Add execute permission:

```bash
chmod +x script.sh
```

Remove execute permission:

```bash
chmod -x script.sh
```

## 63. Good Shell Scripting Practices

Good scripts should be:

- Readable
- Predictable
- Reusable
- Safe
- Easy to debug
- Properly documented

Use meaningful names.

**Good:**

```bash
backup_directory="/var/backups"
```

**Bad:**

```bash
x="/var/backups"
```

## 64. Recommended Script Structure

A clean script can follow:

```bash
#!/bin/bash

# Description

# Variables

# Functions

# Main logic
```

Example:

```bash
#!/bin/bash

backup_dir="/tmp/backup"

create_backup_directory() {
    mkdir -p "$backup_dir"
}

create_backup_directory

echo "Backup directory is ready"
```

## 65. Shell Scripting in DevOps

The progression we should remember:

```
Linux Commands
      ↓
Bash
      ↓
Shell Scripts
      ↓
Programming Logic
      ↓
Automation
      ↓
DevOps
```

Shell scripts can later be used with:

- CI/CD
- Docker
- Cloud servers
- Deployment
- Monitoring
- Cron jobs
- Server administration
- Infrastructure automation

## 66. Shell Scripting and CI/CD

A CI/CD system may execute:

```bash
./build.sh
```

A build script could perform:

```
Install dependencies
        ↓
Build application
        ↓
Run tests
        ↓
Create artifact
        ↓
Deploy
```

If a command fails and returns a non-zero exit code, the pipeline can detect the failure.

This is one reason exit statuses are important.

## 67. Shell Scripting and Git/GitHub

A DevOps repository could contain:

```
devops-project/
│
├── scripts/
│   ├── setup.sh
│   ├── build.sh
│   └── deploy.sh
│
├── README.md
└── .gitignore
```

Git/GitHub can be used to:

- Store scripts
- Track changes
- Collaborate
- Review code
- Create Pull Requests
- Document assignments

Git itself will be covered separately in greater detail.

## 68. Markdown Documentation

For assignments, documentation can be stored in:

```
README.md
```

Example:

```markdown
# Shell Scripting Assignment

## Objective

Create and execute Bash scripts.

## Script

```bash
./system_info.sh
```

## Concepts Used

- Linux commands
- Variables
- Functions
- Loops
- Conditions

## Output

Paste output or add screenshots here.
```

Documentation is important because a DevOps engineer should be able to explain and reproduce their work.

## 69. Typical Git Workflow for Assignments

The general workflow will eventually look like:

```text
Create/Clone Repository
        ↓
Create or modify script
        ↓
Test locally
        ↓
Document work
        ↓
git add
        ↓
git commit
        ↓
git push
        ↓
Pull Request
```

We will learn each Git concept properly when we reach the Git chapter.

## 70. Common Bash Mistakes

### Mistake 1 — Spaces around `=`

Wrong:

```bash
name = "John"
```

Correct:

```bash
name="John"
```

### Mistake 2 — Incorrect if spacing

Wrong:

```bash
if["$age" -gt 18]; then
```

Correct:

```bash
if [ "$age" -gt 18 ]; then
```

### Mistake 3 — Forgetting `fi`

Correct:

```bash
if [ "$age" -gt 18 ]; then
    echo "Adult"
fi
```

### Mistake 4 — Forgetting `done`

Correct:

```bash
for i in {1..5}; do
    echo "$i"
done
```

### Mistake 5 — Script is not executable

If:

```bash
./script.sh
```

doesn't work because of permissions:

```bash
chmod +x script.sh
```

### Mistake 6 — Missing quotes

Prefer:

```bash
echo "$name"
```

instead of:

```bash
echo $name
```

especially when variables may contain spaces.

## 71. Chapter 3 Important Commands

| Command            | Purpose                        |
|--------------------|--------------------------------|
| `bash script.sh`   | Run script using Bash          |
| `chmod +x script.sh` | Add execute permission       |
| `./script.sh`      | Execute script directly        |
| `echo`             | Print text                     |
| `read`             | Take input                     |
| `date`             | Display date/time              |
| `hostname`         | Display system hostname        |
| `whoami`           | Display current user           |
| `ps`               | Display processes              |
| `df -h`            | Display disk usage             |
| `mkdir`            | Create directory               |
| `touch`            | Create file                    |
| `cat`              | Display file                   |
| `ls`               | List files                     |

## 72. Chapter 3 Important Syntax

**Variable**

```bash
name="Tanishq"
```

**Variable access**

```bash
echo "$name"
```

**User input**

```bash
read -p "Enter name: " name
```

**Command substitution**

```bash
date_now=$(date)
```

**Arithmetic**

```bash
sum=$((a + b))
```

**If**

```bash
if [ condition ]; then
    commands
fi
```

**For loop**

```bash
for i in {1..5}; do
    echo "$i"
done
```

**While loop**

```bash
while [ condition ]; do
    commands
done
```

**Function**

```bash
function_name() {
    commands
}
```

**Function call**

```bash
function_name
```

## 73. Chapter 3 Exam Questions

### Basic

- What is a shell?
- What is shell scripting?
- What is Bash?
- What does Bash stand for?
- What is a shell script?
- What is the purpose of `.sh`?
- What is a shebang?
- What does `#!/bin/bash` mean?
- How do you create a shell script?
- How do you execute a shell script?

### Variables

- How do you declare a variable in Bash?
- Why are spaces not allowed around `=`?
- How do you access a variable?
- What is variable expansion?
- Why are quotes important around variables?
- What is command substitution?
- How do you perform arithmetic in Bash?

### Input

- What does `read` do?
- What does `read -p` do?

### Conditions

- Explain `if`, `elif`, `else`, and `fi`.
- Explain `-eq`.
- Explain `-ne`.
- Explain `-gt`.
- Explain `-lt`.
- Explain `-ge`.
- Explain `-le`.
- How do you compare strings?
- How do you check whether a file exists?
- How do you check whether a directory exists?

### Loops

- What is a loop?
- Explain a `for` loop.
- Explain a `while` loop.
- What is an infinite loop?
- What is a C-style Bash `for` loop?

### Functions and Arguments

- What is a function?
- How do you define a function?
- How do you call a function?
- What is `$1`?
- What is `$2`?
- What is `$0`?
- What is `$#`?
- What is `$@`?
- What is `$?`?
- What is `$$`?

### Operators

- What does `&&` mean?
- What does `||` mean?
- What does `|` mean?
- Difference between `|` and `&&`.
- Difference between `>` and `>>`.

### DevOps

- Why is shell scripting important in DevOps?
- How can shell scripts automate repetitive tasks?
- How can shell scripts be used in CI/CD?
- Why are exit codes important in CI/CD?
- How can shell scripts help with monitoring?
- How can shell scripts be used with Git/GitHub?
- Why should secrets not be hardcoded?

### Debugging

- What does `bash -n script.sh` do?
- What does `bash -x script.sh` do?
- What is ShellCheck?
- What are common Bash scripting mistakes?

## 74. Chapter 3 Practical Checklist

Before considering Chapter 3 complete, you should be able to:

- Create a `.sh` file
- Understand the shebang
- Run a script using `bash script.sh`
- Make a script executable
- Run a script using `./script.sh`
- Write comments
- Create variables
- Access variables
- Take user input
- Use command substitution
- Perform arithmetic
- Write `if`/`else`
- Write `elif`
- Use numeric comparisons
- Compare strings
- Check files
- Check directories
- Write `for` loops
- Write `while` loops
- Create functions
- Pass arguments
- Understand special variables
- Understand exit status
- Use `&&`
- Use `||`
- Use pipes
- Use output redirection
- Understand stdin/stdout/stderr
- Debug using `bash -n`
- Debug using `bash -x`
- Understand environment variables
- Understand why secrets should not be hardcoded
- Document scripts using Markdown
- Understand how scripts eventually fit into CI/CD

## 75. Quick Revision Table

| Concept              | Remember                          |
|----------------------|-----------------------------------|
| Shell                | Command interpreter               |
| Bash                 | Bourne Again SHell                |
| Shell script         | File containing commands + logic  |
| Shebang              | `#!/bin/bash`                     |
| Variable             | `name="value"`                    |
| Variable access      | `$name`                           |
| User input           | `read`                            |
| Prompted input       | `read -p`                         |
| Command substitution | `$(command)`                      |
| Arithmetic           | `$((expression))`                 |
| Condition            | `if [ condition ]; then ... fi`   |
| Numeric equal        | `-eq`                             |
| Not equal            | `-ne`                             |
| Greater than         | `-gt`                             |
| Less than            | `-lt`                             |
| Greater/equal        | `-ge`                             |
| Less/equal           | `-le`                             |
| For loop             | `for ... do ... done`             |
| While loop           | `while ... do ... done`           |
| Function             | `name() { ... }`                  |
| First argument       | `$1`                              |
| Second argument      | `$2`                              |
| Script name          | `$0`                              |
| Argument count       | `$#`                              |
| All arguments        | `$@`                              |
| Exit status          | `$?`                              |
| Current shell PID    | `$$`                              |
| Success              | Exit code `0`                     |
| Failure              | Non-zero exit code                |
| AND                  | `&&`                              |
| OR                   | `\|\|`                            |
| Pipe                 | `\|`                              |
| Overwrite output     | `>`                               |
| Append output        | `>>`                              |
| Error stream         | `stderr` / `2`                    |
| Execute script       | `./script.sh`                     |
| Make executable      | `chmod +x script.sh`              |
| Syntax check         | `bash -n script.sh`               |
| Debug                | `bash -x script.sh`               |

## 76. The Big Picture

You have now moved from simply knowing Linux commands to automating Linux commands.

The progression is:

```
CHAPTER 2
Linux Commands
      ↓
      ↓
CHAPTER 3
Shell / Bash
      ↓
Variables
      ↓
User Input
      ↓
Conditions
      ↓
Loops
      ↓
Functions
      ↓
Arguments
      ↓
Exit Codes
      ↓
Debugging
      ↓
Automation
      ↓
CI/CD
      ↓
DevOps
```

**Most important idea to remember**

Shell scripting is not about memorizing hundreds of commands. It is about combining Linux commands with programming logic to automate work.

And this chapter is particularly important because later, when we get into Git, Docker, CI/CD, cloud servers, Jenkins, Kubernetes and deployment, you will repeatedly see shell commands and shell scripts being used underneath them.
