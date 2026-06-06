

MusicXML → MIDI Converter

A professional, cross-platform desktop application designed to convert batch MusicXML, .xml, and .mxl 
files into standard MIDI files (.mid). Built with Python and music21, it features an asynchronous 
architecture that ensures a smooth, non-freezing user interface during large batch operations.

🚀 Key Features

Smart Conversion Engine (Plan A, B, & C): * Plan A: Attempts a full, standard MusicXML to MIDI conversion.

Plan B: If the file has layout conflicts, the app automatically cleans specific repeats, codas, and barlines 
to rescue the track.

Plan C: If everything else fails, it extracts a raw note-and-rest stream to guarantee a working MIDI output.

True Multithreading: The UI never freezes. You can safely stop or pause processing at any point during  
a batch run.

Native Look & Feel: Utilizes system-integrated elements and standard fonts (TkFixedFont) to look 
clean and professional across all operating systems.

Smart Config Storage: Remembers your last used folder and language preferences. Settings are stored in 
official system paths (like Application Support on macOS) to prevent workspace clutter and keep 
launch speeds blazing fast.

🌍 Supported Languages (16 Languages)

The application supports real-time language switching directly inside the GUI:

🇩🇪 Deutsch (German)

🇺🇸 English (English)

🇫🇷 Français (French)

🇪🇸 Español (Spanish)

🇮🇹 Italiano (Italian)

🇳🇱 Nederlands (Dutch)

🇵🇱 Polski (Polish)

🇨🇿 Čeština (Czech)

🇷🇺 Русский (Russian)

🇺🇦 Українська (Ukrainian)

🇹🇷 Türkçe (Turkish)

🇬🇷 Ελληνικά (Greek)

🇵🇹 Português (Portuguese)

🇸🇪 Svenska (Swedish)

🇭🇺 Magyar (Hungarian)

🇷🇴 Română (Romanian)

📦 Downloads & Installation

No installation or Python knowledge is required! Simply download the ready-to-run package 
for your operating system:

🖥️ Windows

File: Konvert.7z

Instructions: Extract the .7z archive using 7-Zip or WinRAR. Open the extracted folder 
and run Konvert.exe directly. It is completely portable and can be run from a USB drive.

🍎 macOS

File: Konvert.dmg

Instructions: Open the .dmg file and drag the application into your workspace. 
It launches instantly. Because it follows Apple's native security guidelines, your settings 
are saved invisibly in the background, keeping your workspace perfectly clean.

🐧 Linux

File: Konvert.tar.gz

Instructions: Extract the .tar.gz archive. Open the extracted folder and run the 
Konvert binary file.

Note: If the application doesn't start, right-click the binary file, go to Properties -> 
Permissions, and check "Allow executing file as program" (or run chmod +x Konvert in your terminal).

📝 How To Use 

Select Language: Choose your preferred language from the dropdown menu at the top left.

Select Folder: Click "Select Folder" to choose the directory containing your sheet music files. 
the app automatically scans all subdirectories.

Convert: Click "START / REFRESH". The real-time console will print out detailed statuses of every 
file processed.
<img width="622" height="552" alt="Screenshot 2026-06-06 220034" src="https://github.com/user-attachments/assets/2d79aaf4-c804-4762-a92a-4736c0835001" />


    Stop: If needed, hit "STOP" to immediately cancel the ongoing task safely.
