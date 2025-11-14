================================================================================
                         ImageConverter for macOS
                     Installation & Usage Instructions
================================================================================

DOWNLOAD & INSTALLATION
================================================================================

METHOD 1: Using DMG File (Recommended)
---------------------------------------
1. Download "ImageConverter-DMG.zip" from GitHub Releases
2. Unzip the file to get "ImageConverter.dmg"
3. Double-click "ImageConverter.dmg"
4. Drag "ImageConverter.app" to the Applications folder
5. Eject the DMG by right-clicking and selecting "Eject"
6. Open ImageConverter from Launchpad or Applications folder


METHOD 2: Using .app File Directly
-----------------------------------
1. Download "ImageConverter-macOS.zip" from GitHub Releases
2. Unzip the file to get "ImageConverter.app"
3. Move "ImageConverter.app" to your Applications folder
4. Open ImageConverter from Applications folder


FIRST TIME SETUP (IMPORTANT!)
================================================================================

When you open ImageConverter for the first time, macOS will show this warning:

    "ImageConverter cannot be opened because the developer 
     cannot be verified."

This is normal for apps not distributed through the Mac App Store.

SOLUTION - Option 1 (Quick):
----------------------------
1. Right-click (or Control+click) on ImageConverter.app
2. Select "Open" from the menu
3. Click "Open" again in the dialog box
4. The app will now open normally


SOLUTION - Option 2 (System Settings):
---------------------------------------
1. Try to open the app normally (it will be blocked)
2. Go to: System Settings → Privacy & Security
3. Scroll down to find: "ImageConverter was blocked from use"
4. Click "Open Anyway"
5. Enter your password if prompted
6. Click "Open" in the confirmation dialog


HOW TO USE
================================================================================

1. Click "Select Images" to choose your image files
   - Supported formats: HEIC, HEIF, PNG, JPG, BMP, TIFF, WEBP

2. Choose output format:
   - WEBP: Modern format with best compression
   - JPG: Universal compatibility

3. Adjust quality slider (1-100):
   - Higher = Better quality, larger file size
   - Lower = Smaller file size, lower quality

4. Click "Start Conversion"

5. Choose where to save your converted images

6. Done! Check the output folder for your converted images


FEATURES
================================================================================

✓ Convert HEIC/HEIF images to WEBP or JPG
✓ Batch processing (convert multiple images at once)
✓ Adjustable quality settings
✓ Modern, user-friendly interface
✓ Fast and efficient conversion


SYSTEM REQUIREMENTS
================================================================================

• macOS 10.13 (High Sierra) or later
• 100 MB free disk space
• Python runtime (included in the app)


TROUBLESHOOTING
================================================================================

Problem: App won't open at all
Solution: Make sure you followed the "First Time Setup" steps above

Problem: "App is damaged" error
Solution: 
  1. Open Terminal
  2. Type: xattr -cr /Applications/ImageConverter.app
  3. Press Enter
  4. Try opening the app again

Problem: Conversion fails
Solution: 
  • Make sure source images are valid and not corrupted
  • Check that you have write permission to the output folder
  • Try restarting the app


SUPPORT & DONATION
================================================================================

If you find this app useful, consider supporting the developer:
https://coffeete.ir/sajadp

For issues and feature requests:
Visit the GitHub repository


VERSION INFORMATION
================================================================================

Version: 1.0
Build Date: November 2025
Developer: sajadp
License: MIT


================================================================================
                    Thank you for using ImageConverter!
================================================================================
