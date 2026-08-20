# DevOps — Chapter 2: Linux Fundamentals

> **Important for MacBook users:** macOS is Unix-based, but it is **not Linux**. Many basic shell commands are similar, but Linux-specific commands, package managers, services, file locations, and administrative behavior can differ. For this course, practice Linux-specific material inside an actual Linux environment such as Ubuntu. Do not blindly run Linux commands such as `apt`, `systemctl`, or `useradd` in the macOS Terminal and expect the same behavior.

---

# 1. What is Linux?

Linux is an open-source operating-system kernel.

In everyday DevOps conversations, "Linux" often refers to a complete Linux operating system/distribution built around the Linux kernel.

Examples of Linux distributions:

- Ubuntu
- Debian
- Fedora
- Red Hat Enterprise Linux (RHEL)
- Rocky Linux
- AlmaLinux
- Amazon Linux

For learning DevOps, Ubuntu is a very useful beginner environment.

---

# 2. Linux vs macOS

Your MacBook uses macOS.

Your DevOps class may use Linux.

Both provide a Unix-like command-line environment, so commands such as these are familiar:

```bash
pwd
ls
cd
mkdir
touch
cp
mv
rm
cat
grep
head
tail
```

But they are not identical operating systems.

Examples:

| Task | macOS | Typical Ubuntu Linux |
|---|---|---|
| Package manager | Homebrew (`brew`) commonly used | `apt` |
| Service manager | `launchd` | `systemd` |
| Service command | `launchctl` | `systemctl` |
| Linux users/groups | Different system behavior | `useradd`, `usermod`, `groupadd`, etc. |
| Linux filesystem hierarchy | Not identical | Standard Linux hierarchy |

Therefore, use the Mac Terminal for general shell practice, but use Linux for Linux-specific administration practice.

---

# 3. The Linux Terminal

A terminal allows you to interact with the operating system using commands.

Example:

```bash
pwd
```

You type the command and press Enter.

A command generally follows this pattern:

```text
command + options + arguments
```

Example:

```bash
ls -la /tmp
```

Here:

- `ls` = command
- `-la` = options
- `/tmp` = argument/path

---

# 4. Linux File System

Linux uses a single hierarchical filesystem.

The top is called the **root directory**:

```text
/
```

Do not confuse:

```text
/
```

with:

```text
/root
```

`/` is the filesystem root.

`/root` is the home directory of the root user.

---

# 5. Important Linux Directories

A simplified Linux filesystem looks like:

```text
/
├── bin
├── boot
├── dev
├── etc
├── home
├── lib
├── mnt
├── opt
├── root
├── tmp
├── usr
└── var
```

## `/`

The root of the entire filesystem.

Everything begins under `/`.

---

## `/bin`

Contains essential command programs.

Modern Linux distributions may merge `/bin` with `/usr/bin`, but `/bin` remains an important concept to understand.

---

## `/boot`

Contains files required for booting the operating system.

Examples may include:

- Kernel files
- Bootloader-related files
- Initial RAM filesystem files

---

## `/dev`

Contains device files representing devices and device interfaces.

Examples include files representing:

- Disks
- Terminals
- Random-number devices

---

## `/etc`

Contains system-wide configuration files.

Examples:

```text
/etc/hosts
/etc/passwd
/etc/ssh/
```

A useful memory trick:

> `/etc` → system configuration

---

## `/home`

Contains normal users' home directories.

Example:

```text
/home/tanishq
```

A user's personal files commonly live here.

---

## `/lib`

Contains important shared libraries and other files required by essential programs.

Modern distributions may use merged directories such as `/usr/lib`.

---

## `/mnt`

Traditionally used as a mount point for temporarily mounted filesystems.

---

## `/opt`

Often used for optional/add-on application software.

---

## `/tmp`

Used for temporary files.

Important:

- Files here are temporary.
- Programs can create temporary data here.
- Do not assume files in `/tmp` are permanent.

---

## `/var`

Contains variable data that changes while the system operates.

Examples:

```text
/var/log
/var/cache
```

Logs are particularly important in DevOps.

---

## `/usr`

A very important directory that was not always emphasized in beginner summaries.

It commonly contains user-space programs, libraries, documentation, and other resources.

Examples:

```text
/usr/bin
/usr/lib
/usr/share
```

---

## `/root`

Home directory of the root user.

This is different from `/`.

---

# 6. Absolute and Relative Paths

## Absolute path

An absolute path starts from `/`.

Example:

```bash
/home/tanishq/project
```

It identifies a location independently of your current directory.

---

## Relative path

A relative path starts from your current directory.

Example:

```bash
project
```

If you are currently in `/home/tanishq`, then:

```text
project
```

refers to:

```text
/home/tanishq/project
```

---

# 7. Special Path Symbols

## `.`

Current directory.

```bash
.
```

---

## `..`

Parent directory.

Example:

```bash
cd ..
```

moves one directory upward.

---

## `~`

The current user's home directory.

Example:

```bash
cd ~
```

---

## `/`

Filesystem root.

---

# 8. `pwd`

`pwd` means **Print Working Directory**.

It tells you where you currently are.

```bash
pwd
```

Example:

```text
/home/tanishq
```

---

# 9. `ls`

`ls` lists directory contents.

```bash
ls
```

## Long format

```bash
ls -l
```

Shows information such as:

- Permissions
- Owner
- Group
- Size
- Modification time
- Name

## Hidden files

```bash
ls -a
```

Linux hidden files normally begin with `.`.

Example:

```text
.bashrc
.profile
```

## Long + hidden

```bash
ls -la
```

A common command you should become comfortable with.

---

# 10. `cd`

`cd` means **Change Directory**.

```bash
cd /tmp
```

Go to `/tmp`.

Go to parent:

```bash
cd ..
```

Go home:

```bash
cd ~
```

Go to previous directory:

```bash
cd -
```

---

# 11. `mkdir`

Creates directories.

```bash
mkdir project
```

Create multiple directories:

```bash
mkdir dir1 dir2 dir3
```

Create nested directories:

```bash
mkdir -p project/src/main
```

`-p` creates missing parent directories as required.

---

# 12. `touch`

Creates an empty file if it does not exist.

```bash
touch notes.txt
```

It can also update file timestamps when the file already exists.

Important:

> `touch` is not primarily a "write text into a file" command.

---

# 13. `cat`

Displays file contents.

```bash
cat notes.txt
```

It can also concatenate multiple files:

```bash
cat file1.txt file2.txt
```

---

# 14. `echo`

Prints text.

```bash
echo "Hello Linux"
```

It becomes especially useful with redirection.

Example:

```bash
echo "Hello" > file.txt
```

---

# 15. Output Redirection

## `>`

Redirects standard output to a file.

```bash
echo "Hello" > file.txt
```

If the file exists, its previous contents are replaced.

Therefore:

> `>` = overwrite

---

## `>>`

Appends output to the end of a file.

```bash
echo "Second line" >> file.txt
```

Therefore:

> `>>` = append

---

# 16. Pipes `|`

A pipe sends the output of one command as input to another command.

Example:

```bash
ls -l | grep ".txt"
```

Conceptually:

```text
ls -l
  ↓
output
  ↓
grep
  ↓
filtered output
```

Pipes are one of the most important shell concepts for DevOps.

---

# 17. `cp`

Copies files.

```bash
cp file.txt backup.txt
```

Copy a directory recursively:

```bash
cp -R project project-backup
```

---

# 18. `mv`

Moves or renames files/directories.

Rename:

```bash
mv old.txt new.txt
```

Move:

```bash
mv file.txt /tmp/
```

Important:

> `mv` is used for both moving and renaming.

---

# 19. `rm`

Removes files.

```bash
rm file.txt
```

Remove a directory recursively:

```bash
rm -r project
```

Force removal:

```bash
rm -f file.txt
```

Recursive + force:

```bash
rm -rf project
```

## ⚠️ Important

Be extremely careful with:

```bash
rm -rf
```

It does not normally move files to a trash/recycle bin.

Always inspect your path before executing destructive commands.

---

# 20. Wildcards

The `*` wildcard matches many possible characters.

Example:

```bash
ls *.txt
```

This can list files ending in `.txt`.

Example:

```bash
rm *.log
```

This attempts to remove matching `.log` files.

Be especially careful when combining wildcards with `rm`.

---

# 21. `head`

Displays the beginning of a file.

```bash
head file.txt
```

First 5 lines:

```bash
head -n 5 file.txt
```

---

# 22. `tail`

Displays the end of a file.

```bash
tail file.txt
```

Last 20 lines:

```bash
tail -n 20 file.txt
```

Very important DevOps use:

```bash
tail -f application.log
```

`-f` follows a growing file and is commonly used to watch logs in real time.

---

# 23. `grep`

Searches text using patterns.

Example:

```bash
grep "error" application.log
```

Case-insensitive:

```bash
grep -i "error" application.log
```

Useful with pipes:

```bash
ps aux | grep java
```

Important idea:

```text
Command output
      ↓
     grep
      ↓
Matching lines
```

---

# 24. `less`

Views text one screen at a time.

```bash
less largefile.txt
```

Useful for large logs.

Common navigation:

```text
Space → next page
b     → previous page
q     → quit
```

---

# 25. `more`

Another pager for viewing files.

```bash
more file.txt
```

`less` is generally more capable and commonly preferred.

---

# 26. File Permissions

Linux controls access to files using permissions.

A typical `ls -l` result may look like:

```text
-rwxr-xr--
```

Break it down:

```text
- rwx r-x r--
│ │   │   │
│ │   │   └── Others
│ │   └────── Group
│ └────────── Owner/User
└──────────── File type
```

There are three main permission categories:

- User/Owner (`u`)
- Group (`g`)
- Others (`o`)

Three common permissions:

- `r` = read
- `w` = write
- `x` = execute

---

# 27. Numeric Permissions

Permissions can be represented numerically.

Values:

```text
read    = 4
write   = 2
execute = 1
```

Add them together.

Examples:

```text
r-- = 4
-w- = 2
--x = 1

rw- = 6
r-x = 5
rwx = 7
```

Therefore:

```text
755
```

means:

```text
Owner  = 7 = rwx
Group  = 5 = r-x
Others = 5 = r-x
```

And:

```text
644
```

means:

```text
Owner  = 6 = rw-
Group  = 4 = r--
Others = 4 = r--
```

---

# 28. `chmod`

`chmod` changes file permissions.

Numeric example:

```bash
chmod 755 script.sh
```

Symbolic example:

```bash
chmod u+x script.sh
```

Meaning:

```text
u = user/owner
+ = add
x = execute
```

Remove group write permission:

```bash
chmod g-w file.txt
```

---

# 29. `chown`

`chown` changes file ownership.

General form:

```bash
chown user file.txt
```

User and group:

```bash
chown user:group file.txt
```

Changing ownership often requires administrative privileges.

---

# 30. Users and Groups

Linux is a multi-user operating system.

Important concepts:

- User
- Group
- Owner
- Permissions
- Root

Groups make it easier to grant permissions to multiple users.

---

# 31. Root User

`root` is the superuser on Linux.

Root has very high privileges.

Be careful when using commands through `sudo`.

Example:

```bash
sudo apt update
```

`sudo` asks the system to execute the command with elevated privileges, subject to the user's permissions/configuration.

A useful rule:

> Do not use `sudo` just because a command fails. First understand why it failed.

---

# 32. User Management

Create a user:

```bash
sudo useradd username
```

Modify a user:

```bash
sudo usermod ...
```

Create a group:

```bash
sudo groupadd developers
```

Modify a group:

```bash
sudo groupmod ...
```

These commands are Linux administration commands and should be practiced in a Linux environment.

---

# 33. Processes

A **process** is a running instance of a program.

Example:

```text
Program
   ↓
Started
   ↓
Process
```

A process has information such as:

- Process ID (PID)
- User
- CPU usage
- Memory usage
- State

---

# 34. `ps`

`ps` displays process information.

A common form is:

```bash
ps
```

Another commonly used form:

```bash
ps aux
```

This displays a broader process listing on many Linux systems.

---

# 35. `top`

`top` provides a continuously updating view of processes and system activity.

```bash
top
```

It can show:

- CPU usage
- Memory usage
- Processes
- Process IDs
- Load information

This is useful when investigating a server that is slow or overloaded.

---

# 36. `uptime`

Shows how long the system has been running and provides load information.

```bash
uptime
```

Example concept:

```text
up 2 days, 4 hours
```

---

# 37. `date`

Displays the system date/time.

```bash
date
```

---

# 38. `whoami`

Displays the current effective username.

```bash
whoami
```

Very useful when you need to know which user you are operating as.

---

# 39. Networking Basics

DevOps requires networking knowledge.

At this stage, remember:

```text
Computer
   ↓
Network Interface
   ↓
IP Address
   ↓
Network
   ↓
Other Systems
```

We will study networking deeply in a separate chapter.

---

# 40. `ping`

`ping` is commonly used to test whether a destination is reachable using ICMP echo requests.

Example:

```bash
ping 8.8.8.8
```

You can also use a hostname:

```bash
ping google.com
```

Important:

> A failed `ping` does not always prove that a server is down. Firewalls or network policies can block ICMP.

---

# 41. `ip`

Linux's `ip` command is used to inspect and manage networking information.

Examples:

```bash
ip addr
```

Shows network addresses/interfaces.

```bash
ip link
```

Shows network interfaces.

```bash
ip route
```

Shows routing information.

These commands are Linux-focused.

---

# 42. Ports

A **port** identifies a network service endpoint on a host.

A simplified model:

```text
IP address → identifies the host
Port       → identifies the service endpoint
```

Examples of commonly encountered ports:

| Port | Common protocol/service |
|---:|---|
| 22 | SSH |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |

Ports will be studied in depth in the networking chapter.

Do not memorize a huge port list yet. First understand what a port actually represents.

---

# 43. Package Management

Software is commonly installed using package managers.

For Debian/Ubuntu systems:

```bash
apt
```

Update package metadata:

```bash
sudo apt update
```

Install a package:

```bash
sudo apt install package-name
```

Important distinction:

```text
apt update
```

updates the package information available to the package manager.

It does **not** mean "update every installed application."

---

# 44. Services and `systemctl`

Many Linux servers use **systemd** as the system and service manager.

`systemctl` is used to interact with systemd.

Examples:

```bash
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
systemctl status nginx
```

Meaning:

- `start` → start service
- `stop` → stop service
- `restart` → restart service
- `status` → inspect service status

Important:

> `systemctl` is primarily a Linux/systemd concept and does not work the same way on macOS.

---

# 45. Text Editors

## nano

Beginner-friendly terminal editor.

```bash
nano file.txt
```

Common controls are displayed at the bottom of the editor.

---

## vim

A powerful terminal editor.

```bash
vim file.txt
```

Important concept:

Vim has modes.

Common modes include:

- Normal mode
- Insert mode
- Command-line mode

You do not need to master Vim immediately. Learn enough to open, edit, save, and exit files, then improve gradually.

---

# 46. Disk Usage

## `df`

Shows filesystem disk-space usage.

```bash
df -h
```

`-h` means human-readable sizes.

Example output may show:

```text
Filesystem
Size
Used
Avail
Use%
Mounted on
```

---

## `du`

Estimates space used by files/directories.

```bash
du -sh .
```

Useful for discovering which directories consume storage.

---

# 47. Command History

`history` displays previously executed commands.

```bash
history
```

This is extremely useful while learning Linux.

You can also use the keyboard:

```text
↑
```

to navigate previous commands in many shells.

---

# 48. `man`

`man` displays manual pages.

Example:

```bash
man ls
```

Think of `man` as the built-in documentation for many Unix/Linux commands.

You should learn to read command documentation instead of trying to memorize every option.

---

# 49. Environment Variables

Environment variables are named values available to processes.

Example:

```bash
NAME="Tanishq"
```

Export it:

```bash
export NAME="Tanishq"
```

Read it:

```bash
echo $NAME
```

A common environment variable:

```bash
$PATH
```

`PATH` tells the shell where to look for executable commands.

Inspect it:

```bash
echo $PATH
```

Environment variables become extremely important later for:

- API keys
- Application configuration
- Cloud credentials
- Docker
- CI/CD
- Deployment

Never commit secrets such as passwords or API keys to Git.

---

# 50. `.bashrc`

`.bashrc` is a shell startup/configuration file commonly used by Bash for interactive non-login shells.

It can contain things such as:

- Aliases
- Environment variables
- Shell functions
- Prompt configuration

Example:

```bash
alias ll='ls -la'
```

After changing `.bashrc`, the shell may need to reload it:

```bash
source ~/.bashrc
```

Important:

> macOS commonly uses Zsh rather than Bash as the default interactive shell, so macOS users may encounter `~/.zshrc` instead.

---

# 51. Shell Scripting

A shell script is a file containing shell commands that can be executed as a program.

Example:

```bash
#!/bin/bash

echo "Starting"
mkdir -p project
touch project/file.txt
echo "Finished"
```

Instead of manually entering commands one by one:

```text
mkdir
touch
echo
...
```

we can automate them in one script.

This is one of the foundations of DevOps automation.

---

# 52. Shebang

The first line:

```bash
#!/bin/bash
```

is commonly called a **shebang**.

It tells the system which interpreter should be used to run the script.

For Bash:

```bash
#!/bin/bash
```

A portable alternative sometimes used is:

```bash
#!/usr/bin/env bash
```

---

# 53. Executing a Shell Script

Suppose:

```text
script.sh
```

exists.

Run through Bash:

```bash
bash script.sh
```

Or make it executable:

```bash
chmod +x script.sh
```

Then:

```bash
./script.sh
```

The `./` means:

> Execute the file named `script.sh` from the current directory.

---

# 54. Standard Input, Output, and Error

Every Unix process commonly works with three standard streams:

```text
stdin   → 0
stdout  → 1
stderr  → 2
```

### stdin

Input to a command.

### stdout

Normal output.

### stderr

Error output.

This becomes important for pipes, redirection, logs, and CI/CD.

Examples:

```bash
command > output.txt
```

Redirect stdout.

```bash
command 2> error.txt
```

Redirect stderr.

```bash
command > output.txt 2>&1
```

Redirect stdout and stderr to the same destination in this common shell form.

---

# 55. Command Options

Options modify command behavior.

Examples:

```bash
ls -l
ls -a
ls -la
```

Many commands support both short and long options, depending on the command.

Examples:

```bash
ls --all
```

Do not assume every command uses identical option syntax.

Use:

```bash
man command
```

to verify.

---

# 56. Linux Command Cheat Sheet

| Command | Purpose |
|---|---|
| `pwd` | Show current directory |
| `ls` | List contents |
| `cd` | Change directory |
| `mkdir` | Create directory |
| `touch` | Create/update file timestamp |
| `cp` | Copy |
| `mv` | Move/rename |
| `rm` | Remove |
| `cat` | Display/concatenate files |
| `echo` | Print text |
| `head` | Show beginning |
| `tail` | Show end |
| `grep` | Search/filter text |
| `less` | Paginated file viewing |
| `chmod` | Change permissions |
| `chown` | Change ownership |
| `ps` | Show processes |
| `top` | Live process/system view |
| `ping` | Test reachability with ICMP |
| `ip` | Inspect/manage networking |
| `uptime` | Show uptime/load information |
| `date` | Show date/time |
| `whoami` | Show current user |
| `apt` | Package management on Debian/Ubuntu |
| `systemctl` | Manage systemd services |
| `useradd` | Create user |
| `usermod` | Modify user |
| `groupadd` | Create group |
| `groupmod` | Modify group |
| `df` | Filesystem disk usage |
| `du` | File/directory disk usage |
| `history` | Command history |
| `man` | Manual/documentation |

---

# 57. Commands You Should Understand First

Do not attempt to memorize every command immediately.

Master these first:

```bash
pwd
ls
ls -la
cd
mkdir
touch
cat
echo
cp
mv
rm
head
tail
grep
chmod
ps
df
du
```

Then add:

```bash
ip
apt
systemctl
useradd
usermod
groupadd
chown
```

---

# 58. Important Safety Rules

## Rule 1 — Be careful with `rm`

Especially:

```bash
rm -rf
```

---

## Rule 2 — Understand `sudo`

`sudo` gives a command elevated privileges.

Do not use it blindly.

---

## Rule 3 — Check your current directory

Before destructive commands:

```bash
pwd
ls
```

---

## Rule 4 — Never expose secrets

Do not put these into Git:

```text
passwords
API keys
private keys
cloud credentials
tokens
```

Use environment variables and secret-management mechanisms.

---

# 59. Practical Mental Model

Think of Linux as five major areas:

```text
                 Linux
                   │
      ┌────────────┼────────────┐
      ↓            ↓            ↓
   Files        Processes     Network
      │            │            │
 permissions    services       IP/ports
      │
      ↓
 Users + Groups
```

And around all of it:

```text
Shell + Commands + Automation
```

This mental model will help later with Docker, cloud, Kubernetes, and CI/CD.

---

# 60. Beginner Practice Sequence

Practice in this order:

```text
1. pwd
2. ls
3. cd
4. mkdir
5. touch
6. echo
7. cat
8. cp
9. mv
10. rm
11. head
12. tail
13. grep
14. chmod
15. ps
16. df
17. du
18. pipes
19. redirection
20. shell script
```

Do not rush.

The objective is to understand what the command does, not merely memorize its spelling.

---

# 61. Exam Questions

1. What is Linux?
2. Explain the Linux filesystem hierarchy.
3. What is the root directory?
4. Difference between `/` and `/root`.
5. What is an absolute path?
6. What is a relative path?
7. Explain `.`, `..`, and `~`.
8. What does `pwd` do?
9. Explain `ls -l`, `ls -a`, and `ls -la`.
10. Difference between `cp` and `mv`.
11. Difference between `>` and `>>`.
12. What is a pipe?
13. What is `grep`?
14. Explain Linux file permissions.
15. Explain `chmod 755`.
16. Explain `chmod 644`.
17. What is `chown`?
18. What is a process?
19. Difference between `ps` and `top`.
20. What does `ping` do?
21. What is the `ip` command used for?
22. What is a package manager?
23. Difference between `apt update` and installing a package.
24. What is `systemctl`?
25. What is `sudo`?
26. What are users and groups?
27. What is an environment variable?
28. What is `$PATH`?
29. What is `.bashrc`?
30. What is shell scripting?
31. What is a shebang?
32. Difference between `bash script.sh` and `./script.sh`.
33. What are stdin, stdout, and stderr?
34. Why are Linux skills important in DevOps?
35. Why should Linux commands be practiced separately from macOS commands?

---

# 62. Chapter 2 Final Mental Picture

```text
Linux
│
├── Filesystem
│   ├── /
│   ├── /etc
│   ├── /home
│   ├── /var
│   ├── /tmp
│   ├── /usr
│   └── /boot
│
├── Shell
│   ├── commands
│   ├── pipes
│   ├── redirection
│   └── scripts
│
├── Permissions
│   ├── user
│   ├── group
│   └── others
│
├── Processes
│   ├── ps
│   └── top
│
├── Networking
│   ├── IP
│   ├── interfaces
│   └── routes
│
├── Packages
│   └── apt
│
├── Services
│   └── systemctl
│
└── Automation
    └── shell scripting
```
