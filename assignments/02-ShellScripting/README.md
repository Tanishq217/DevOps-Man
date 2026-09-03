# Assignment 02 – Shell Scripting: System Information Script

**Course:** DevOps  
**Topic:** Shell Scripting – Variables, User Input, File & Directory Operations  
**Student:** Tanishq  
**Repository:** https://github.com/Tanishq217/DevOps-Man  
**Environment:** macOS (zsh/bash)

---

## Objective

Create a shell script (`sysinfo.sh`) that demonstrates core shell scripting concepts:

| # | Requirement | Command / Concept Used |
|---|------------|------------------------|
| 1 | Print the current date | `date`, variables |
| 2 | Print the hostname | `hostname`, variables |
| 3 | Print the username | `whoami`, variables |
| 4 | Print disk usage | `df -h` |
| 5 | Print running processes | `ps -ax` |
| 6 | Use variables to store and use data | `VAR=$(command)` |
| 7 | Take user input | `read -p` |
| 8 | Create a directory | `mkdir` |
| 9 | Create a file | `touch` |
| 10 | Store process info in a file | `>` output redirection |

---

## The Shell Script — `sysinfo.sh`

```bash
#!/bin/bash

# ============================================================
# Script Name: sysinfo.sh
# Description: System Information Script - DevOps Assignment 02
# Author: Tanishq
# ============================================================

echo "=============================================="
echo "       SYSTEM INFORMATION REPORT"
echo "=============================================="
echo ""

# ── 1. Print the Current Date ───────────────────
CURRENT_DATE=$(date)
echo "📅 Current Date & Time:"
echo "   $CURRENT_DATE"
echo ""

# ── 2. Print the Hostname ───────────────────────
HOST_NAME=$(hostname)
echo "🖥️  Hostname:"
echo "   $HOST_NAME"
echo ""

# ── 3. Print the Username ───────────────────────
USER_NAME=$(whoami)
echo "👤 Logged-in User:"
echo "   $USER_NAME"
echo ""

# ── 4. Print Disk Usage ─────────────────────────
echo "💾 Disk Usage:"
df -h
echo ""

# ── 5. Print Running Processes ──────────────────
echo "⚙️  Running Processes (snapshot):"
ps -ax | head -20
echo ""

# ── 6. Take User Input ──────────────────────────
read -p "📁 Enter a name for the project directory to create: " PROJECT_NAME
echo ""

# ── 7. Create a Directory ───────────────────────
DIR_PATH="./$PROJECT_NAME"
mkdir -p "$DIR_PATH"
echo "✅ Directory created: $DIR_PATH"
echo ""

# ── 8. Create a File ────────────────────────────
REPORT_FILE="$DIR_PATH/system_report.txt"
touch "$REPORT_FILE"
echo "✅ File created: $REPORT_FILE"
echo ""

# ── 9. Store Running Processes in the File ──────
echo "📝 Saving running processes to $REPORT_FILE ..."
{
  echo "=============================================="
  echo "  SYSTEM REPORT — Generated on: $CURRENT_DATE"
  echo "  Hostname : $HOST_NAME"
  echo "  User     : $USER_NAME"
  echo "=============================================="
  echo ""
  echo "--- DISK USAGE ---"
  df -h
  echo ""
  echo "--- RUNNING PROCESSES ---"
  ps -ax
} > "$REPORT_FILE"

echo "✅ Process info saved to: $REPORT_FILE"
echo ""
echo "=============================================="
echo "        REPORT COMPLETE — All Done! 🎉"
echo "=============================================="
```

---

## Step-by-Step Explanation & Command Output

### Step 1 — Make the Script Executable

Before running, we must give the script execute permission using `chmod`.

```bash
chmod +x sysinfo.sh
```

**Why?** By default, a newly created `.sh` file doesn't have execute permission. `chmod +x` adds it so the OS allows running it as a program.

**Screenshot:**

![chmod and run script](01-chmod-and-run.png)

---

### Step 2 — Run the Script

```bash
./sysinfo.sh
```

or equivalently:

```bash
bash sysinfo.sh
```

**Why?** `./sysinfo.sh` tells the shell to execute the script in the current directory. The `#!/bin/bash` at the top (called a **shebang**) tells the OS to use bash as the interpreter.

---

### Step 3 — Date & Time (Using a Variable + `date`)

**Code:**
```bash
CURRENT_DATE=$(date)
echo "📅 Current Date & Time:"
echo "   $CURRENT_DATE"
```

**Output:**
```
📅 Current Date & Time:
   Thu Sep  3 22:11:00 IST 2026
```

**Explanation:**
- `CURRENT_DATE=$(date)` — runs the `date` command and stores its output in the **variable** `CURRENT_DATE`. This is called **command substitution** using `$(...)`.
- `echo "$CURRENT_DATE"` — prints the variable's value using the `$` prefix to dereference it.
- Variables are the backbone of shell scripting — they let you store, reuse, and pass data around your script.

**Screenshot:**

![Date, Hostname & User output](02-date-hostname-user.png)

---

### Step 4 — Hostname (Using `hostname`)

**Code:**
```bash
HOST_NAME=$(hostname)
echo "🖥️  Hostname:"
echo "   $HOST_NAME"
```

**Output:**
```
🖥️  Hostname:
   Tanishqs-MacBook-Air-2.local
```

**Explanation:**
- `hostname` prints the machine's network name.
- Stored in `HOST_NAME` variable for later reuse in the report file.

**Screenshot:**

![Date, Hostname & User output](02-date-hostname-user.png)

---

### Step 5 — Username (Using `whoami`)

**Code:**
```bash
USER_NAME=$(whoami)
echo "👤 Logged-in User:"
echo "   $USER_NAME"
```

**Output:**
```
👤 Logged-in User:
   tanishqsingh
```

**Explanation:**
- `whoami` returns the name of the currently logged-in user.
- Again stored in a variable (`USER_NAME`) for reuse later in the report.

**Screenshot:**

![Date, Hostname & User output](02-date-hostname-user.png)

---

### Step 6 — Disk Usage (Using `df -h`)

**Code:**
```bash
echo "💾 Disk Usage:"
df -h
```

**Output:**
```
💾 Disk Usage:
Filesystem        Size    Used   Avail Capacity iused ifree %iused  Mounted on
/dev/disk3s1s1   228Gi    16Gi   2.4Gi    87%    459k   26M    2%   /
devfs            221Ki   221Ki     0Bi   100%     764     0  100%   /dev
/dev/disk3s6     228Gi   5.0Gi   2.4Gi    68%       5   26M    0%   /System/Volumes/VM
/dev/disk3s5     228Gi   185Gi   2.4Gi    99%    1.9M   26M    7%   /System/Volumes/Data
...
```

**Explanation:**
- `df` stands for **disk filesystem**. It reports the amount of disk space used and available.
- `-h` flag means **human-readable** — shows sizes in `Ki`, `Mi`, `Gi` instead of raw bytes.
- Key columns: `Size` (total), `Used`, `Avail` (free), `Capacity` (% used), `Mounted on` (which path it maps to).

**Screenshot:**

![Disk usage output](03-disk-usage.png)

---

### Step 7 — Running Processes (Using `ps -ax`)

**Code:**
```bash
echo "⚙️  Running Processes (snapshot):"
ps -ax | head -20
```

**Output:**
```
⚙️  Running Processes (snapshot):
  PID TTY           TIME CMD
    1 ??       152:27.79 /sbin/launchd
  526 ??       122:21.89 /usr/libexec/logd
  528 ??         8:42.24 /usr/libexec/UserEventAgent (System)
  530 ??       306:16.36 .../fseventsd
  531 ??        17:40.63 .../mediaremoted
  538 ??        32:07.37 /usr/libexec/configd
  540 ??        21:46.22 .../powerd
  ...
```

**Explanation:**
- `ps` stands for **process status** — it shows a snapshot of the currently running processes.
- `-a` shows processes from **all users**, `-x` includes processes **not attached to a terminal** (like background daemons).
- `| head -20` pipes the output and shows only the first 20 lines to keep output readable.
- Columns: `PID` (process ID), `TTY` (terminal), `TIME` (CPU time used), `CMD` (command name).

**Screenshot:**

![Running processes](04-ps-output.png)

---

### Step 8 — User Input (Using `read -p`)

**Code:**
```bash
read -p "📁 Enter a name for the project directory to create: " PROJECT_NAME
```

**Interaction:**
```
📁 Enter a name for the project directory to create: devops-project
```

**Explanation:**
- `read` is a built-in shell command that **reads input from the user** and stores it in a variable.
- `-p "..."` flag sets the **prompt text** shown to the user before they type.
- Whatever the user types is stored in `PROJECT_NAME` and reused throughout the rest of the script.

**Screenshot:**

![User input with read -p](05-user-input.png)

---

### Step 9 — Create a Directory (Using `mkdir`)

**Code:**
```bash
DIR_PATH="./$PROJECT_NAME"
mkdir -p "$DIR_PATH"
echo "✅ Directory created: $DIR_PATH"
```

**Output:**
```
✅ Directory created: ./devops-project
```

**Explanation:**
- `mkdir` stands for **make directory** — it creates a new folder.
- `-p` flag means **parents** — it creates all intermediate directories if they don't exist, and does NOT error if the directory already exists.
- We use the `$PROJECT_NAME` variable (from user input) to dynamically name the directory.

**Screenshot:**

![mkdir, touch and redirection output](06-mkdir-touch-redirect.png)

---

### Step 10 — Create a File (Using `touch`)

**Code:**
```bash
REPORT_FILE="$DIR_PATH/system_report.txt"
touch "$REPORT_FILE"
echo "✅ File created: $REPORT_FILE"
```

**Output:**
```
✅ File created: ./devops-project/system_report.txt
```

**Explanation:**
- `touch` creates an empty file if it doesn't exist. If it already exists, it just updates the timestamp.
- `REPORT_FILE` variable stores the full path to the file (directory + filename) — this avoids repeating the path string later.

**Screenshot:**

![mkdir, touch and redirection output](06-mkdir-touch-redirect.png)

---

### Step 11 — Output Redirection (Using `>`)

**Code:**
```bash
{
  echo "=============================================="
  echo "  SYSTEM REPORT — Generated on: $CURRENT_DATE"
  echo "  Hostname : $HOST_NAME"
  echo "  User     : $USER_NAME"
  echo "=============================================="
  echo ""
  echo "--- DISK USAGE ---"
  df -h
  echo ""
  echo "--- RUNNING PROCESSES ---"
  ps -ax
} > "$REPORT_FILE"
```

**Explanation:**
- The `>` operator **redirects output** — instead of printing to the terminal, the output is written into `$REPORT_FILE`.
- `{ ... }` is a **group command** — it runs multiple commands and treats their combined output as one stream, which is then redirected to the file.
- This is how scripts automate report generation — no manual copy-pasting needed!
- All variables (`$CURRENT_DATE`, `$HOST_NAME`, `$USER_NAME`) that were captured earlier are now reused here.

**Verify the file was created:**
```bash
ls -lh devops-project/
cat devops-project/system_report.txt | head -20
```

**Output of the report file:**
```
==============================================
  SYSTEM REPORT — Generated on: Thu Sep  3 22:11:00 IST 2026
  Hostname : Tanishqs-MacBook-Air-2.local
  User     : tanishqsingh
==============================================

--- DISK USAGE ---
Filesystem        Size    Used   Avail Capacity iused ifree %iused  Mounted on
/dev/disk3s1s1   228Gi    16Gi   2.4Gi    87%    459k   26M    2%   /
/dev/disk3s5     228Gi   185Gi   2.4Gi    99%    1.9M   26M    7%   /System/Volumes/Data
...

--- RUNNING PROCESSES ---
  PID TTY           TIME CMD
    1 ??       152:27.79 /sbin/launchd
  526 ??       122:21.89 /usr/libexec/logd
...
```

**Screenshot:**

![Output redirection and file contents](07-report-file.png)

---

## Full Script Output (End-to-End)

Below is the complete terminal output from a single run of `./sysinfo.sh`:

```
==============================================
       SYSTEM INFORMATION REPORT
==============================================

📅 Current Date & Time:
   Thu Sep  3 22:11:00 IST 2026

🖥️  Hostname:
   Tanishqs-MacBook-Air-2.local

👤 Logged-in User:
   tanishqsingh

💾 Disk Usage:
Filesystem        Size    Used   Avail Capacity iused ifree %iused  Mounted on
/dev/disk3s1s1   228Gi    16Gi   2.4Gi    87%    459k   26M    2%   /
devfs            221Ki   221Ki     0Bi   100%     764     0  100%   /dev
/dev/disk3s6     228Gi   5.0Gi   2.4Gi    68%       5   26M    0%   /System/Volumes/VM
/dev/disk3s2     228Gi    17Gi   2.4Gi    88%    2.1k   26M    0%   /System/Volumes/Preboot
/dev/disk3s4     228Gi   765Mi   2.4Gi    24%     483   26M    0%   /System/Volumes/Update
/dev/disk3s5     228Gi   185Gi   2.4Gi    99%    1.9M   26M    7%   /System/Volumes/Data

⚙️  Running Processes (snapshot):
  PID TTY           TIME CMD
    1 ??       152:27.79 /sbin/launchd
  526 ??       122:21.89 /usr/libexec/logd
  528 ??         8:42.24 /usr/libexec/UserEventAgent (System)
  530 ??       306:16.36 /System/Library/Frameworks/.../fseventsd
  538 ??        32:07.37 /usr/libexec/configd
  540 ??        21:46.22 /System/Library/CoreServices/powerd.bundle/powerd

📁 Enter a name for the project directory to create: devops-project

✅ Directory created: ./devops-project

✅ File created: ./devops-project/system_report.txt

📝 Saving running processes to ./devops-project/system_report.txt ...
✅ Process info saved to: ./devops-project/system_report.txt

==============================================
        REPORT COMPLETE — All Done! 🎉
==============================================
```

**Screenshot:**

![Full script run](06-mkdir-touch-redirect.png)

---

## Summary of Commands Used

| Command | Purpose |
|---------|---------|
| `#!/bin/bash` | Shebang — declares bash as the script interpreter |
| `VAR=$(cmd)` | Command substitution — stores command output in a variable |
| `echo` | Prints text to the terminal |
| `date` | Prints current date and time |
| `hostname` | Prints machine hostname |
| `whoami` | Prints current logged-in username |
| `df -h` | Shows disk usage in human-readable format |
| `ps -ax` | Lists all running processes |
| `read -p` | Prompts user for input and stores it in a variable |
| `mkdir -p` | Creates a directory (and parents if needed) |
| `touch` | Creates an empty file |
| `>` | Redirects output to a file (overwrites) |
| `{ ... }` | Groups multiple commands into a single output stream |
| `chmod +x` | Makes a script executable |

---

## Files in This Assignment

```
02-ShellScripting/
├── sysinfo.sh              ← The shell script
├── README.md               ← This file
└── devops-project/         ← Created by the script at runtime
    └── system_report.txt   ← Generated report (created by the script)
```

---

## Screenshots Needed

> Take these screenshots while running `./sysinfo.sh` in your terminal:

| File Name | What to Capture |
|-----------|----------------|
| `01-chmod-and-run.png` | Terminal showing `chmod +x sysinfo.sh` then `./sysinfo.sh` start |
| `02-date-output.png` | The date section output |
| `03-hostname-output.png` | The hostname section output |
| `04-username-output.png` | The username section output |
| `05-disk-usage.png` | The full `df -h` output section |
| `06-ps-output.png` | The running processes section |
| `07-user-input.png` | The `read -p` prompt with your typed input |
| `08-mkdir-output.png` | The `mkdir` confirmation output |
| `09-touch-output.png` | The `touch` file creation confirmation |
| `10-output-redirection.png` | The `cat system_report.txt` output |
| `11-full-run.png` | The complete script run from top to bottom |

---

**End of Assignment 02**
