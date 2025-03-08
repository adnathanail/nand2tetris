# Project 09: High-Level Programming

- Each available project is in a separate directory, next to this README
    - `Average`, `Fraction`, `HelloWorld`, `List`, and `Square` are demo projects provided by the course
    - `BitmapEditor` is a JS tool, not a Jack project
    - `Quintris` is my project, a Tetris clone with 5 blocks per piece instead of the usual 4

To run a project, take the following steps, with your terminal in the root of this repo

1. Compile the Jack code to VM code

```bash
./tools/JackCompiler.sh projects/09/Average/  # Replace the path with the project you want to run
```

2. Open the VM emulator

```bash
./tools/VMEmulator.sh
```

3. Load the VM code

    - Click `File > Load Program` in the VM emulator
    - Select directory of the selected project (e.g. `projects/09/Average/`)
    - Click `Load Program`

4. Set `Animate` to `No animation`

5. Click the double right arrow button