<p align="center">
  <a href="./README.md">
    <img src="https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/3.5.0/flags/4x3/gb.svg" alt="English" width="40">
  </a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="./README_tr.md">
    <img src="https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/3.5.0/flags/4x3/tr.svg" alt="Türkçe" width="40">
  </a>
</p>

<h1 align="center">
  Fountext Screenwriting Editor for Linux
</h1>

<p align="center">
  <strong>A blazing fast, professional screenwriting environment built with Python, PyQt6, and a custom C++ layout engine.</strong>
</p>

<p align="center">
  <a href="https://github.com/SametCirik/Fountext-Screenwriting-Editor/releases">
    <img alt="Latest Release" src="https://img.shields.io/badge/latest%20release-v1.2-blue">
  </a>
  <a href="https://github.com/SametCirik/Fountext-Screenwriting-Editor/blob/master/LICENSE">
    <img alt="License" src="https://img.shields.io/badge/license-GPLv3-green">
  </a>
  <a href="https://github.com/SametCirik/Fountext-Screenwriting-Editor">
    <img alt="Platform" src="https://img.shields.io/badge/platform-Linux-important">
  </a>
</p>

---

## About Fountext

Fountext is a modern, lightweight, and powerful screenwriting editor that fully embraces the **Fountain** syntax. Forget about formatting struggles; just write. Fountext's custom-built C++ rendering engine handles all the professional formatting for you automatically.

### Key Features

**Fountain Format Support** - Full support for the .fountain screenwriting format  
**Real-time Rendering** - Custom C++ layout engine provides millimeter-perfect positioning  
**Auto-Formatting** - Automatically formats scene headings, character names, and dialogue  
**Scene Navigation** - Floating panel for quick scene/location navigation  
**PDF Export** - Export to industry-standard, text-selectable vector PDFs  
**Smooth Scrolling** - Navigate seamlessly between scenes  
**Page Statistics** - Real-time page count and character count tracking  
**Bilingual Support** - Full support for English and Turkish  

---

## Quick Start

### Option 1: Download Pre-built Binaries (Recommended for Most Users)

1. **Go to the [Releases Page](https://github.com/SametCirik/Fountext-Screenwriting-Editor/releases)**

2. **Download the Latest Version**
   - Click on the latest release (currently **v1.2**)
   - Download the `Fountext-v1.2-Linux.tar.gz` file

3. **Extract and Run**
   ```bash
   # Extract the archive
   tar -xzf Fountext-v1.2-Linux.tar.gz
   
   # Navigate to the directory
   cd Fountext
   
   # Make the binary executable (if needed)
   chmod +x Fountext
   
   # Run the application
   ./Fountext
   ```

That's it! The pre-built binary includes all dependencies and is ready to use.

### Option 2: Build from Source

#### Prerequisites

- **Python 3.8+**
- **PyQt6**
- **CMake 3.15+**
- **C++ compiler** (GCC 7+ or Clang)
- **pybind11**

#### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/SametCirik/Fountext-Screenwriting-Editor.git
   cd Fountext-Screenwriting-Editor
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Build the C++ Layout Engine**
   ```bash
   mkdir build
   cd build
   cmake ..
   make
   cd ..
   ```

4. **Run the Application**
   ```bash
   python src/main.py
   ```

---

## Contributing & Forking

We welcome contributions! Here's how to get started:

### Fork the Repository

1. **Click the "Fork" button** at the top right of the [main repository page](https://github.com/SametCirik/Fountext-Screenwriting-Editor)
   - This creates a copy of the repository under your GitHub account

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Fountext-Screenwriting-Editor.git
   cd Fountext-Screenwriting-Editor
   ```

3. **Create a Branch for Your Changes**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

4. **Make Your Changes and Commit**
   ```bash
   git add .
   git commit -m "Clear description of your changes"
   ```

5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to the [main repository](https://github.com/SametCirik/Fountext-Screenwriting-Editor)
   - Click "Pull Requests" → "New Pull Request"
   - Select your fork and branch
   - Describe your changes and submit!

### Areas for Contribution

- **Bug Fixes** - Found an issue? Help us fix it!
- **Features** - Have an idea? Implement it!
- **Documentation** - Help improve guides and documentation
- **Translations** - Add support for new languages
- **Testing** - Report issues and test new features

---

## Usage Guide

### Basic Writing

1. **Start Writing** - Open the application and begin typing in Fountain format
2. **Automatic Formatting** - Scene headings, character names, and dialogue are formatted automatically
3. **Navigate Scenes** - Click the "SCENES" menu to jump between locations

### Exporting

- **PDF Export** - `File → Export as PDF` or press `Ctrl + E`
- Professional industry-standard formatting
- Text-selectable content
- Vector-based rendering

### Project Structure

```
Fountext-Screenwriting-Editor/
├── src/                    # Python source code
├── src_cpp/                # C++ layout engine source
├── requirements.txt        # Python dependencies
├── CMakeLists.txt         # C++ build configuration
├── guide_EN.pdf           # User guide (English)
├── guide_TR.pdf           # User guide (Turkish)
└── README.md              # This file
```

---

## System Requirements

- **OS**: Linux (Ubuntu 20.04+, Fedora 33+, Debian 11+, or similar)
- **Python**: 3.8 or higher
- **RAM**: 512 MB minimum, 2 GB recommended
- **Disk Space**: ~200 MB for installation

---

## Documentation

- **[User Guide (English)](./guide_EN.pdf)** - Complete user guide in Fountain format
- **[User Guide (Turkish)](./guide_TR.pdf)** - Türkçe kullanıcı rehberi

---

## License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](./LICENSE) file for details.

---

## Support & Community

- **Issues** - Found a bug? [Report it here](https://github.com/SametCirik/Fountext-Screenwriting-Editor/issues)
- **Discussions** - Have questions? [Start a discussion](https://github.com/SametCirik/Fountext-Screenwriting-Editor/discussions)
- **Contact** - Reach out on [GitHub](https://github.com/SametCirik)

---

## Roadmap

- [ ] Cross-platform support (Windows, macOS)
- [ ] Additional export formats (FDXM, AV Pro)
- [ ] Collaboration features
- [ ] Theme customization
- [ ] Plugin system

---

## Acknowledgments

Built with:
- **Python** - Core application logic
- **PyQt6** - User interface
- **C++17** - High-performance layout engine
- **pybind11** - Python/C++ bindings
- **Fountain Format** - Industry-standard screenplay syntax

---

## Questions?

Feel free to open an [issue](https://github.com/SametCirik/Fountext-Screenwriting-Editor/issues) or [discussion](https://github.com/SametCirik/Fountext-Screenwriting-Editor/discussions) for any questions or feedback!

**Happy writing!**
